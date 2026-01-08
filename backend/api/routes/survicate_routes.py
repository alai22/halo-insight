"""
API routes for Survicate survey analysis
"""

from flask import Blueprint, request, jsonify, g
from datetime import datetime, timezone
import json
from ...utils.logging import get_logger
from ...utils.config import Config
from ...core.exceptions import ValidationError, ServiceUnavailableError
from ...utils.error_helpers import validate_required_fields, validate_message_format, validate_list_items
from ...api.middleware.auth import require_admin_auth

logger = get_logger('survicate_routes')

# Create blueprint
survicate_bp = Blueprint('survicate', __name__, url_prefix='/api/survicate')


@survicate_bp.route('/ask', methods=['POST'])
def survicate_ask():
    """Ask Claude about survey data with detailed RAG process information"""
    # Get services from container (injected via Flask's g)
    service_container = getattr(g, 'service_container', None)
    if not service_container:
        logger.error("Service container not available in request context")
        raise ServiceUnavailableError(
            "Service container not initialized",
            details={'suggestion': 'Check application initialization'}
        )
    
    claude_service = service_container.get_claude_service()
    survicate_rag_service = service_container.get_survicate_rag_service()
    
    data = request.get_json() or {}
    question = data.get('question')
    # Default to configured model (falls back to working model via fallback system if needed)
    model = data.get('model', Config.CLAUDE_MODEL)
    max_tokens = data.get('max_tokens', 2000)
    data_source = data.get('data_source', 'file')  # Get data source
    conversation_history = data.get('conversation_history')  # Optional conversation history
    
    # Validate required fields
    if not question:
        raise ValidationError(
            "Question is required",
            details={'field': 'question', 'suggestion': 'Provide a question in the request body'}
        )
    
    # Validate conversation_history format if provided
    if conversation_history is not None:
        validate_list_items(conversation_history, validate_message_format, 'conversation_history')
    
    logger.info(f"Survicate RAG query request: question={question[:100]}, model={model}, max_tokens={max_tokens}, data_source={data_source}, has_history={bool(conversation_history)}")
    
    # Reload surveys with specified data source before processing query
    survey_service = service_container.get_survey_service()
    survey_service.load_surveys(data_source=data_source)
    
    # Check if Claude service is initialized
    if claude_service is None or survicate_rag_service is None:
        error_msg = "Claude API service is not initialized. Please check ANTHROPIC_API_KEY configuration."
        logger.error(error_msg)
        raise ServiceUnavailableError(
            error_msg,
            details={
                'service': 'Claude API',
                'suggestion': 'ANTHROPIC_API_KEY environment variable is not set or invalid. Please configure it in your .env file or environment.'
            }
        )
    
    result = survicate_rag_service.process_query(question, model, max_tokens, conversation_history)
    result['data_source'] = data_source  # Include data source in response
    
    return jsonify(result)


@survicate_bp.route('/refresh', methods=['POST'])
@require_admin_auth
def refresh_surveys():
    """Refresh survey data from specified source (file or api)"""
    service_container = getattr(g, 'service_container', None)
    if not service_container:
        logger.error("Service container not available in request context")
        raise ServiceUnavailableError(
            "Service container not initialized",
            details={'suggestion': 'Check application initialization'}
        )
    
    data = request.get_json() or {}
    data_source = data.get('data_source', 'file')  # Default to 'file' for backward compatibility
    
    survey_service = service_container.get_survey_service()
    survey_service.refresh_surveys(data_source=data_source)
    
    summary = survey_service.get_summary()
    
    return jsonify({
        'success': True,
        'message': f'Surveys refreshed from {data_source}: {len(survey_service.surveys)} responses loaded',
        'data_source': data_source,
        'summary': {
            'total_responses': summary.total_responses,
            'date_range': summary.date_range
        }
    })


@survicate_bp.route('/summary', methods=['GET'])
def get_survey_summary():
    """Get survey statistics"""
    service_container = getattr(g, 'service_container', None)
    if not service_container:
        logger.error("Service container not available in request context")
        raise ServiceUnavailableError(
            "Service container not initialized",
            details={'suggestion': 'Check application initialization'}
        )
    
    # Get data source from query parameter
    data_source = request.args.get('data_source', 'file')
    
    # Reload surveys with specified data source
    survey_service = service_container.get_survey_service()
    survey_service.load_surveys(data_source=data_source)
    
    summary = survey_service.get_summary()
    
    return jsonify({
        'success': True,
        'data_source': data_source,
        'summary': {
            'total_responses': summary.total_responses,
            'date_range': summary.date_range,
            'question_stats': summary.question_stats,
            'response_rate_by_question': summary.response_rate_by_question
        }
    })


@survicate_bp.route('/search', methods=['POST'])
def search_surveys():
    """Search survey responses"""
    service_container = getattr(g, 'service_container', None)
    if not service_container:
        logger.error("Service container not available in request context")
        raise ServiceUnavailableError(
            "Service container not initialized",
            details={'suggestion': 'Check application initialization'}
        )
    
    survey_service = service_container.get_survey_service()
    
    data = request.get_json() or {}
    query = data.get('query')
    limit = data.get('limit', 10)
    
    if not query:
        raise ValidationError(
            "Query is required",
            details={'field': 'query', 'suggestion': 'Provide a search query in the request body'}
        )
    
    results = survey_service.semantic_search_surveys(query, limit=limit)
    
    return jsonify({
        'success': True,
        'results': results,
        'count': len(results)
    })


@survicate_bp.route('/raw-files/download', methods=['GET'])
@require_admin_auth
def download_raw_file():
    """Download a raw CSV file from S3"""
    try:
        from ...services.survicate_s3_cache_service import SurvicateS3CacheService
        from flask import Response
        import urllib.parse
        
        # Get file_key from query parameter
        file_key = request.args.get('file_key')
        if not file_key:
            return jsonify({
                'success': False,
                'error': 'file_key parameter required'
            }), 400
        
        cache_service = SurvicateS3CacheService()
        
        if not cache_service.s3_client:
            return jsonify({
                'success': False,
                'error': 'S3 not available',
                'details': 'S3 client not configured.'
            }), 503
        
        # Decode the file key (it's URL encoded)
        file_key = urllib.parse.unquote(file_key)
        
        try:
            if cache_service.use_local_storage:
                # Load from local file
                filename = file_key.split('/')[-1] if '/' in file_key else file_key
                file_path = cache_service.local_cache_dir / filename
                
                # Check if it's in augmented subdirectory
                if not file_path.exists():
                    file_path = cache_service.local_cache_dir / 'augmented' / filename
                
                if not file_path.exists():
                    return jsonify({
                        'success': False,
                        'error': 'File not found',
                        'details': f'File {file_key} does not exist locally.'
                    }), 404
                
                file_content = file_path.read_bytes()
                
                return Response(
                    file_content,
                    mimetype='text/csv',
                    headers={
                        'Content-Disposition': f'attachment; filename="{filename}"',
                        'Content-Type': 'text/csv; charset=utf-8'
                    }
                )
            else:
                # Get the file from S3
                if not cache_service.s3_client:
                    return jsonify({
                        'success': False,
                        'error': 'S3 not available',
                        'details': 'S3 client not configured.'
                    }), 503
                
                response = cache_service.s3_client.get_object(
                    Bucket=cache_service.bucket_name,
                    Key=file_key
                )
                
                # Get file content
                file_content = response['Body'].read()
                
                # Get filename from key
                filename = file_key.split('/')[-1] if '/' in file_key else file_key
                
                # Return as downloadable file
                return Response(
                    file_content,
                    mimetype='text/csv',
                    headers={
                        'Content-Disposition': f'attachment; filename="{filename}"',
                        'Content-Type': 'text/csv; charset=utf-8'
                    }
                )
            
        except cache_service.s3_client.exceptions.NoSuchKey if cache_service.s3_client else Exception:
            return jsonify({
                'success': False,
                'error': 'File not found',
                'details': f'File {file_key} does not exist in S3.'
            }), 404
        except Exception as e:
            logger.error(f"Failed to download file: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to download file',
                'details': str(e)
            }), 500
    
    except Exception as e:
        logger.error(f"Failed to download raw file: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': 'Failed to download file'
        }), 500


@survicate_bp.route('/raw-files', methods=['GET'])
@require_admin_auth
def list_raw_files():
    """List all raw CSV files in S3 or local storage"""
    try:
        from ...services.survicate_s3_cache_service import SurvicateS3CacheService
        cache_service = SurvicateS3CacheService()
        
        if not cache_service.use_local_storage and not cache_service.s3_client:
            return jsonify({
                'success': False,
                'error': 'S3 not available',
                'details': 'S3 client not configured and local storage not enabled.'
            }), 503
        
        raw_files = cache_service.list_raw_files()
        
        # Check augmentation status for each file
        augmented_metadata = cache_service.get_augmented_files_metadata()
        augmented_keys = set()
        if augmented_metadata and augmented_metadata.get('files'):
            augmented_keys = {f['key'] for f in augmented_metadata['files']}
        
        # Add augmentation status
        for file_info in raw_files:
            # Check if this raw file has been augmented
            # For now, we'll mark it as augmented if any augmented file exists
            # In the future, we could add better matching logic
            file_info['has_augmentation'] = len(augmented_keys) > 0
        
        return jsonify({
            'success': True,
            'files': raw_files
        })
    
    except Exception as e:
        logger.error(f"Failed to list raw files: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': 'Failed to list raw files'
        }), 500


@survicate_bp.route('/augmented-files', methods=['GET'])
@require_admin_auth
def list_augmented_files():
    """List all available augmented CSV files in S3 or local storage"""
    try:
        from ...services.survicate_s3_cache_service import SurvicateS3CacheService
        cache_service = SurvicateS3CacheService()
        
        if not cache_service.use_local_storage and not cache_service.s3_client:
            return jsonify({
                'success': False,
                'error': 'S3 not available',
                'details': 'S3 client not configured and local storage not enabled.'
            }), 503
        
        metadata = cache_service.get_augmented_files_metadata()
        if not metadata or not metadata.get('files'):
            return jsonify({
                'success': True,
                'files': []
            })
        
        # Format file info for frontend
        files = []
        for file_info in metadata['files']:
            files.append({
                'key': file_info['key'],
                'timestamp': file_info.get('timestamp', ''),
                'response_count': file_info.get('response_count', 0),
                'file_size': file_info.get('file_size', 0),
                'last_modified': file_info.get('last_modified', ''),
                'display_name': file_info['key'].split('/')[-1] if '/' in file_info['key'] else file_info['key']
            })
        
        return jsonify({
            'success': True,
            'files': files
        })
    
    except Exception as e:
        logger.error(f"Failed to list augmented files: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': 'Failed to list augmented files'
        }), 500


@survicate_bp.route('/augmented-files/download', methods=['GET'])
@require_admin_auth
def download_augmented_file():
    """Download an augmented CSV file"""
    try:
        from flask import send_file
        from ...services.survicate_s3_cache_service import SurvicateS3CacheService
        import os
        
        file_key = request.args.get('file_key')
        if not file_key:
            return jsonify({
                'success': False,
                'error': 'file_key parameter is required'
            }), 400
        
        cache_service = SurvicateS3CacheService()
        
        if cache_service.use_local_storage:
            # Load from local file
            file_path = cache_service.local_cache_dir / file_key
            if not file_path.exists():
                return jsonify({
                    'success': False,
                    'error': 'File not found',
                    'details': f'File {file_key} does not exist in local cache.'
                }), 404
            
            return send_file(
                str(file_path),
                mimetype='text/csv',
                as_attachment=True,
                download_name=file_key.split('/')[-1]
            )
        else:
            # Load from S3
            if not cache_service.s3_client:
                return jsonify({
                    'success': False,
                    'error': 'S3 not available',
                    'details': 'S3 client not configured.'
                }), 503
            
            try:
                response = cache_service.s3_client.get_object(
                    Bucket=cache_service.bucket_name,
                    Key=file_key
                )
                
                # Create temporary file
                import tempfile
                with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as temp_file:
                    temp_file.write(response['Body'].read())
                    temp_path = temp_file.name
                
                return send_file(
                    temp_path,
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name=file_key.split('/')[-1]
                )
            except cache_service.s3_client.exceptions.NoSuchKey:
                return jsonify({
                    'success': False,
                    'error': 'File not found',
                    'details': f'File {file_key} does not exist in S3.'
                }), 404
    
    except Exception as e:
        logger.error(f"Failed to download augmented file: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': 'Failed to download augmented file'
        }), 500


@survicate_bp.route('/augment', methods=['POST'])
@require_admin_auth
def trigger_augmentation():
    """Manually trigger augmentation of raw CSV file"""
    try:
        service_container = getattr(g, 'service_container', None)
        if not service_container:
            logger.error("Service container not available in request context")
            return jsonify({'error': 'Service container not initialized'}), 500
        
        data = request.get_json() or {}
        raw_file_key = data.get('raw_file_key')  # Optional: specific raw file to augment
        
        survey_service = service_container.get_survey_service()
        
        # Check if augmentation is already running
        from ...services.survey_service import api_refresh_state
        if api_refresh_state.get('is_running', False):
            return jsonify({
                'success': False,
                'error': 'Augmentation already in progress',
                'details': 'Please wait for the current augmentation to complete.'
            }), 409
        
        # Import cache service
        from ...services.survicate_s3_cache_service import SurvicateS3CacheService
        cache_service = SurvicateS3CacheService()
        
        if not cache_service.use_local_storage and not cache_service.s3_client:
            return jsonify({
                'success': False,
                'error': 'Storage not available',
                'details': 'S3 client not configured and local storage not enabled.'
            }), 503
        
        # Check if raw file exists
        if raw_file_key:
            # Check if file exists in local storage or S3
            if cache_service.use_local_storage:
                file_path = cache_service.local_cache_dir / raw_file_key.split('/')[-1]
                if not file_path.exists():
                    return jsonify({
                        'success': False,
                        'error': 'Raw file not found',
                        'details': f'File {raw_file_key} does not exist in local storage.'
                    }), 404
            else:
                try:
                    cache_service.s3_client.head_object(
                        Bucket=cache_service.bucket_name,
                        Key=raw_file_key
                    )
                except cache_service.s3_client.exceptions.NoSuchKey:
                    return jsonify({
                        'success': False,
                        'error': 'Raw file not found',
                        'details': f'File {raw_file_key} does not exist in S3.'
                    }), 404
        else:
            # Use default cache key
            raw_file_key = cache_service.cache_key
            if cache_service.use_local_storage:
                file_path = cache_service.local_cache_dir / raw_file_key.split('/')[-1]
                if not file_path.exists():
                    return jsonify({
                        'success': False,
                        'error': 'No raw file found',
                        'details': 'Please download data from API first using the "Download from API" button.'
                    }), 404
            else:
                try:
                    cache_service.s3_client.head_object(
                        Bucket=cache_service.bucket_name,
                        Key=raw_file_key
                    )
                except cache_service.s3_client.exceptions.NoSuchKey:
                    return jsonify({
                        'success': False,
                        'error': 'No raw file found',
                        'details': 'Please download data from API first using the "Download from API" button.'
                    }), 404
        
        # Trigger augmentation in background
        # We'll use a thread to run augmentation without blocking
        import threading
        
        def run_augmentation():
            try:
                # Temporarily set cache key to the specified file
                original_key = cache_service.cache_key
                cache_service.cache_key = raw_file_key
                
                # Load raw CSV content from local storage or S3
                try:
                    if cache_service.use_local_storage:
                        file_path = cache_service.local_cache_dir / raw_file_key.split('/')[-1]
                        raw_csv_content = file_path.read_text(encoding='utf-8')
                        logger.info(f"Loaded raw CSV from local file: {file_path}")
                    else:
                        response = cache_service.s3_client.get_object(
                            Bucket=cache_service.bucket_name,
                            Key=raw_file_key
                        )
                        raw_csv_content = response['Body'].read().decode('utf-8')
                        logger.info(f"Loaded raw CSV from S3: {raw_file_key}")
                    
                    # Count responses (approximate - number of lines minus header)
                    response_count = max(0, len(raw_csv_content.strip().split('\n')) - 1)
                except Exception as e:
                    logger.error(f"Failed to read raw file: {e}")
                    response_count = 0
                    raw_csv_content = None
                
                if not raw_csv_content:
                    logger.error("No raw CSV content to augment")
                    return
                
                # Run augmentation using the survey service method
                survey_service._augment_raw_csv_and_save_to_s3(cache_service, raw_csv_content, raw_file_key)
                
                # Restore original key
                cache_service.cache_key = original_key
                
            except Exception as e:
                logger.error(f"Background augmentation failed: {e}", exc_info=True)
        
        # Start augmentation in background thread
        thread = threading.Thread(target=run_augmentation, daemon=True)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Augmentation started in background',
            'raw_file_key': raw_file_key
        })
    
    except Exception as e:
        logger.error(f"Failed to trigger augmentation: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': 'Failed to trigger augmentation'
        }), 500


@survicate_bp.route('/churn-trends', methods=['GET'])
def get_churn_trends():
    """Get churn reason trends by month for visualization"""
    try:
        import pandas as pd
        import os
        import io
        
        # Check if we should use API mode (S3 cache) or file mode
        data_source = request.args.get('data_source', 'file')
        file_key = request.args.get('file_key')  # Optional: specific file to use
        
        if data_source == 'api':
            # Load from cache (S3 or local storage)
            try:
                from ...services.survicate_s3_cache_service import SurvicateS3CacheService
                cache_service = SurvicateS3CacheService()
                
                # Check if S3 is available or if local storage is being used
                if not cache_service.use_local_storage and not cache_service.s3_client:
                    return jsonify({
                        'success': False,
                        'error': 'Storage not available',
                        'details': 'S3 client not configured and local storage not enabled. Set S3_BUCKET_NAME or SURVICATE_USE_LOCAL_STORAGE=true.'
                    }), 503
                
                augmented_csv_content = cache_service.load_augmented_csv_from_s3(file_key=file_key)
                if not augmented_csv_content:
                    storage_type = 'local storage' if cache_service.use_local_storage else 'S3'
                    return jsonify({
                        'success': False,
                        'error': 'Augmented CSV not found',
                        'details': f'Please download and augment data from API first using the "Download from API" button. (Checked {storage_type})'
                    }), 404
                
                # Read CSV from string content
                df = pd.read_csv(io.StringIO(augmented_csv_content))
                storage_type = 'local storage' if cache_service.use_local_storage else 'S3'
                logger.info(f"Loaded {len(df)} rows from {storage_type} augmented cache (file: {file_key or 'latest'})")
                
            except Exception as e:
                logger.error(f"Failed to load augmented CSV: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to load augmented CSV',
                    'details': str(e)
                }), 500
        else:
            # Load from local file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(current_dir, '..', '..', '..', 'data', 
                                    'survicate_cancelled_subscriptions_augmented.csv')
            
            if not os.path.exists(csv_path):
                logger.error(f"CSV file not found at {csv_path}")
                return jsonify({
                    'error': 'Data file not found',
                    'details': f'Expected file at: {csv_path}'
                }), 404
            
            # Read the CSV
            df = pd.read_csv(csv_path)
        
        # Filter out rows with missing data
        df = df[df['augmented_churn_reason'].notna() & df['year_month'].notna()]
        
        # Filter out excluded months (configurable via SURVICATE_EXCLUDE_MONTHS env var)
        exclude_months = Config.SURVICATE_EXCLUDE_MONTHS.split(',') if Config.SURVICATE_EXCLUDE_MONTHS else []
        exclude_months = [m.strip() for m in exclude_months if m.strip()]
        if exclude_months:
            df = df[~df['year_month'].isin(exclude_months)]
            logger.info(f"Excluded months: {exclude_months}")
        
        if len(df) == 0:
            return jsonify({
                'error': 'No valid data found',
                'details': 'No rows with valid augmented_churn_reason and year_month'
            }), 400
        
        # Group by year_month and augmented_churn_reason
        grouped = df.groupby(['year_month', 'augmented_churn_reason']).size().reset_index(name='count')
        
        # Calculate percentages for each month
        monthly_totals = df.groupby('year_month').size()
        grouped['percentage'] = grouped.apply(
            lambda row: (row['count'] / monthly_totals[row['year_month']]) * 100, 
            axis=1
        )
        
        # Get unique months and reasons
        months = sorted(grouped['year_month'].unique())
        reasons = sorted(grouped['augmented_churn_reason'].unique())
        
        # Format data for frontend - create array of objects with month and all reason percentages and counts
        data = []
        for month in months:
            month_data = {'month': month}
            month_total = int(monthly_totals[month])
            month_data['_total'] = month_total  # Store total for the month
            month_df = grouped[grouped['year_month'] == month]
            for reason in reasons:
                reason_data = month_df[month_df['augmented_churn_reason'] == reason]
                count_key = f'{reason}_count'
                if len(reason_data) > 0:
                    month_data[reason] = round(reason_data['percentage'].values[0], 2)
                    month_data[count_key] = int(reason_data['count'].values[0])
                else:
                    month_data[reason] = 0
                    month_data[count_key] = 0
            data.append(month_data)
        
        # Calculate total counts for each reason (for sorting/legend)
        reason_totals = {}
        for reason in reasons:
            reason_totals[reason] = int(grouped[grouped['augmented_churn_reason'] == reason]['count'].sum())
        
        # Sort reasons by total count (descending) for consistent ordering
        sorted_reasons = sorted(reasons, key=lambda x: reason_totals[x], reverse=True)
        
        # Keep only top 11 reasons, aggregate the rest into "Other"
        top_n = 11
        top_reasons = sorted_reasons[:top_n]
        other_reasons = sorted_reasons[top_n:] if len(sorted_reasons) > top_n else []
        
        # Aggregate data: combine non-top reasons into "Other"
        aggregated_data = []
        for month in months:
            month_data = {'month': month}
            month_total = int(monthly_totals[month])
            month_data['_total'] = month_total
            
            # Get data for this month
            month_df = grouped[grouped['year_month'] == month]
            
            # Add top reasons
            for reason in top_reasons:
                reason_data = month_df[month_df['augmented_churn_reason'] == reason]
                count_key = f'{reason}_count'
                if len(reason_data) > 0:
                    month_data[reason] = round(reason_data['percentage'].values[0], 2)
                    month_data[count_key] = int(reason_data['count'].values[0])
                else:
                    month_data[reason] = 0
                    month_data[count_key] = 0
            
            # Aggregate "Other" reasons
            other_count = 0
            other_percentage = 0
            for reason in other_reasons:
                reason_data = month_df[month_df['augmented_churn_reason'] == reason]
                if len(reason_data) > 0:
                    other_count += int(reason_data['count'].values[0])
                    other_percentage += reason_data['percentage'].values[0]
            
            # Add "Other" category
            if len(other_reasons) > 0:
                month_data['Other'] = round(other_percentage, 2)
                month_data['Other_count'] = other_count
            
            aggregated_data.append(month_data)
        
        # Create final reasons list with "Other" if needed
        final_reasons = top_reasons.copy()
        if len(other_reasons) > 0:
            final_reasons.append('Other')
            reason_totals['Other'] = sum(reason_totals[r] for r in other_reasons)
        
        return jsonify({
            'success': True,
            'data': aggregated_data,
            'reasons': final_reasons,
            'months': months,
            'reason_totals': {r: reason_totals[r] for r in final_reasons},
            'total_responses': int(len(df)),
            'other_reasons_count': len(other_reasons)
        })
    
    except Exception as e:
        import traceback
        logger.error(f"Failed to get churn trends: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'details': 'Failed to process churn trends data'
        }), 500


@survicate_bp.route('/churn-trends-weekly', methods=['GET'])
def get_churn_trends_weekly():
    """Get churn reason trends by week for visualization"""
    try:
        import pandas as pd
        import os
        import io
        from datetime import datetime
        
        # Check if we should use API mode (S3 cache) or file mode
        data_source = request.args.get('data_source', 'file')
        file_key = request.args.get('file_key')  # Optional: specific file to use
        
        if data_source == 'api':
            # Load from cache (S3 or local storage)
            try:
                from ...services.survicate_s3_cache_service import SurvicateS3CacheService
                cache_service = SurvicateS3CacheService()
                
                # Check if S3 is available or if local storage is being used
                if not cache_service.use_local_storage and not cache_service.s3_client:
                    return jsonify({
                        'success': False,
                        'error': 'Storage not available',
                        'details': 'S3 client not configured and local storage not enabled. Set S3_BUCKET_NAME or SURVICATE_USE_LOCAL_STORAGE=true.'
                    }), 503
                
                augmented_csv_content = cache_service.load_augmented_csv_from_s3(file_key=file_key)
                if not augmented_csv_content:
                    storage_type = 'local storage' if cache_service.use_local_storage else 'S3'
                    return jsonify({
                        'success': False,
                        'error': 'Augmented CSV not found',
                        'details': f'Please download and augment data from API first using the "Download from API" button. (Checked {storage_type})'
                    }), 404
                
                # Read CSV from string content
                df = pd.read_csv(io.StringIO(augmented_csv_content))
                storage_type = 'local storage' if cache_service.use_local_storage else 'S3'
                logger.info(f"Loaded {len(df)} rows from {storage_type} augmented cache (file: {file_key or 'latest'})")
                
            except Exception as e:
                logger.error(f"Failed to load augmented CSV: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to load augmented CSV',
                    'details': str(e)
                }), 500
        else:
            # Load from local file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(current_dir, '..', '..', '..', 'data', 
                                    'survicate_cancelled_subscriptions_augmented.csv')
            
            if not os.path.exists(csv_path):
                logger.error(f"CSV file not found at {csv_path}")
                return jsonify({
                    'success': False,
                    'error': 'Data file not found',
                    'details': f'Expected file at: {csv_path}'
                }), 404
            
            # Read the CSV
            df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(df)} rows from local file")
        
        # Filter out rows with missing data
        df = df[df['augmented_churn_reason'].notna() & df['Date & Time (UTC)'].notna()]
        
        # Parse date column and create week identifier
        df['date'] = pd.to_datetime(df['Date & Time (UTC)'], errors='coerce')
        df = df[df['date'].notna()]  # Remove rows with invalid dates
        
        # Create year-week identifier using ISO week format
        # Get ISO year and week number
        df['iso_year'] = df['date'].dt.isocalendar().year
        df['iso_week'] = df['date'].dt.isocalendar().week
        df['year_week'] = df['iso_year'].astype(str) + '-W' + df['iso_week'].astype(str).str.zfill(2)
        
        # Also create a more readable format: "YYYY-MM-DD to YYYY-MM-DD"
        def get_week_range(date_series):
            """Get start and end dates of the week for a date (Monday to Sunday)"""
            week_ranges = []
            for date in date_series:
                # Get Monday of the week (ISO week starts on Monday)
                days_since_monday = date.weekday()  # Monday is 0
                week_start = date - pd.Timedelta(days=days_since_monday)
                week_end = week_start + pd.Timedelta(days=6)
                week_ranges.append(f"{week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}")
            return week_ranges
        
        df['week_label'] = get_week_range(df['date'])
        
        # Filter out excluded months (configurable via SURVICATE_EXCLUDE_MONTHS env var)
        exclude_months = Config.SURVICATE_EXCLUDE_MONTHS.split(',') if Config.SURVICATE_EXCLUDE_MONTHS else []
        exclude_months = [m.strip() for m in exclude_months if m.strip()]
        if exclude_months:
            # Convert exclude_months to year-month format and filter
            df['year_month'] = df['date'].dt.strftime('%Y-%m')
            df = df[~df['year_month'].isin(exclude_months)]
            logger.info(f"Excluded months: {exclude_months}")
        
        if len(df) == 0:
            return jsonify({
                'success': False,
                'error': 'No valid data found',
                'details': 'No rows with valid augmented_churn_reason and date'
            }), 400
        
        # Group by year_week and augmented_churn_reason
        grouped = df.groupby(['year_week', 'week_label', 'augmented_churn_reason']).size().reset_index(name='count')
        
        # Calculate percentages for each week
        weekly_totals = df.groupby('year_week').size()
        grouped['percentage'] = grouped.apply(
            lambda row: (row['count'] / weekly_totals[row['year_week']]) * 100, 
            axis=1
        )
        
        # Get unique weeks and reasons
        # Sort by year_week but use week_label for display
        weeks_df = grouped[['year_week', 'week_label']].drop_duplicates().sort_values('year_week')
        weeks = weeks_df['week_label'].tolist()
        reasons = sorted(grouped['augmented_churn_reason'].unique())
        
        # Format data for frontend - create array of objects with week and all reason percentages and counts
        data = []
        for week_label in weeks:
            week_data = {'week': week_label}
            year_week = weeks_df[weeks_df['week_label'] == week_label]['year_week'].iloc[0]
            week_total = int(weekly_totals[year_week])
            week_data['_total'] = week_total  # Store total for the week
            week_df = grouped[grouped['year_week'] == year_week]
            for reason in reasons:
                reason_data = week_df[week_df['augmented_churn_reason'] == reason]
                count_key = f'{reason}_count'
                if len(reason_data) > 0:
                    week_data[reason] = round(reason_data['percentage'].values[0], 2)
                    week_data[count_key] = int(reason_data['count'].values[0])
                else:
                    week_data[reason] = 0
                    week_data[count_key] = 0
            data.append(week_data)
        
        # Calculate total counts for each reason (for sorting/legend)
        reason_totals = {}
        for reason in reasons:
            reason_totals[reason] = int(grouped[grouped['augmented_churn_reason'] == reason]['count'].sum())
        
        # Sort reasons by total count (descending) for consistent ordering
        sorted_reasons = sorted(reasons, key=lambda x: reason_totals[x], reverse=True)
        
        # Keep only top 11 reasons, aggregate the rest into "Other"
        top_n = 11
        top_reasons = sorted_reasons[:top_n]
        other_reasons = sorted_reasons[top_n:] if len(sorted_reasons) > top_n else []
        
        # Aggregate data: combine non-top reasons into "Other"
        aggregated_data = []
        for week_label in weeks:
            year_week = weeks_df[weeks_df['week_label'] == week_label]['year_week'].iloc[0]
            week_data = {'week': week_label}
            week_total = int(weekly_totals[year_week])
            week_data['_total'] = week_total
            
            # Get data for this week
            week_df = grouped[grouped['year_week'] == year_week]
            
            # Add top reasons
            for reason in top_reasons:
                reason_data = week_df[week_df['augmented_churn_reason'] == reason]
                count_key = f'{reason}_count'
                if len(reason_data) > 0:
                    week_data[reason] = round(reason_data['percentage'].values[0], 2)
                    week_data[count_key] = int(reason_data['count'].values[0])
                else:
                    week_data[reason] = 0
                    week_data[count_key] = 0
            
            # Aggregate "Other" reasons
            other_count = 0
            other_percentage = 0
            for reason in other_reasons:
                reason_data = week_df[week_df['augmented_churn_reason'] == reason]
                if len(reason_data) > 0:
                    other_count += int(reason_data['count'].values[0])
                    other_percentage += reason_data['percentage'].values[0]
            
            # Add "Other" category
            if len(other_reasons) > 0:
                week_data['Other'] = round(other_percentage, 2)
                week_data['Other_count'] = other_count
            
            aggregated_data.append(week_data)
        
        # Create final reasons list with "Other" if needed
        final_reasons = top_reasons.copy()
        if len(other_reasons) > 0:
            final_reasons.append('Other')
            reason_totals['Other'] = sum(reason_totals[r] for r in other_reasons)
        
        return jsonify({
            'success': True,
            'data': aggregated_data,
            'reasons': final_reasons,
            'weeks': weeks,
            'reason_totals': {r: reason_totals[r] for r in final_reasons},
            'total_responses': int(len(df)),
            'other_reasons_count': len(other_reasons)
        })
    
    except Exception as e:
        import traceback
        logger.error(f"Failed to get churn trends weekly: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': 'Failed to process churn trends weekly data'
        }), 500


@survicate_bp.route('/generate-pdf-report', methods=['POST'])
def generate_pdf_report():
    """Generate and return a PDF report of churn trends"""
    try:
        import sys
        import os
        
        # Get the path to the script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, '..', '..', '..', 'generate_churn_report.py')
        
        if not os.path.exists(script_path):
            return jsonify({
                'error': 'PDF generation script not found',
                'details': f'Expected script at: {script_path}'
            }), 404
        
        # Import and run the PDF generation
        sys.path.insert(0, os.path.dirname(script_path))
        from generate_churn_report import generate_churn_report
        
        # Get CSV path
        csv_path = os.path.join(current_dir, '..', '..', '..', 'data', 
                                'survicate_cancelled_subscriptions_augmented.csv')
        
        # Generate PDF in a temporary location
        import tempfile
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, 'churn_reasons_report.pdf')
        
        result = generate_churn_report(csv_path=csv_path, output_path=output_path)
        
        if result and os.path.exists(result):
            from flask import send_file
            return send_file(
                result,
                mimetype='application/pdf',
                as_attachment=True,
                download_name='churn_reasons_report.pdf'
            )
        else:
            return jsonify({
                'error': 'Failed to generate PDF',
                'details': 'PDF generation completed but file not found'
            }), 500
    
    except ImportError as e:
        logger.error(f"Failed to import PDF generation script: {str(e)}")
        return jsonify({
            'error': 'PDF generation dependencies not available',
            'details': 'Please ensure matplotlib and pandas are installed. You can also run generate_churn_report.py directly.'
        }), 500
    except Exception as e:
        import traceback
        logger.error(f"Failed to generate PDF: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'details': 'Failed to generate PDF report'
        }), 500


@survicate_bp.route('/generate-slides-report', methods=['POST'])
def generate_slides_report():
    """Generate and return a PowerPoint presentation of churn trends"""
    try:
        import sys
        import os
        
        # Get the path to the script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, '..', '..', '..', 'generate_churn_slides.py')
        
        if not os.path.exists(script_path):
            return jsonify({
                'error': 'Slides generation script not found',
                'details': f'Expected script at: {script_path}'
            }), 404
        
        # Import and run the slides generation
        sys.path.insert(0, os.path.dirname(script_path))
        from generate_churn_slides import generate_churn_slides
        
        # Get CSV path
        csv_path = os.path.join(current_dir, '..', '..', '..', 'data', 
                                'survicate_cancelled_subscriptions_augmented.csv')
        
        # Generate PowerPoint in a temporary location
        import tempfile
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, 'churn_trends_slides.pptx')
        
        result = generate_churn_slides(csv_path=csv_path, output_path=output_path)
        
        if result and os.path.exists(result):
            from flask import send_file
            return send_file(
                result,
                mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
                as_attachment=True,
                download_name='churn_trends_slides.pptx'
            )
        else:
            return jsonify({
                'error': 'Failed to generate PowerPoint',
                'details': 'PowerPoint generation completed but file not found'
            }), 500
    
    except ImportError as e:
        logger.error(f"Failed to import slides generation script: {str(e)}")
        return jsonify({
            'error': 'Slides generation dependencies not available',
            'details': 'Please ensure python-pptx, matplotlib, and pandas are installed.'
        }), 500
    except Exception as e:
        import traceback
        logger.error(f"Failed to generate PowerPoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'details': 'Failed to generate PowerPoint presentation'
        }), 500


@survicate_bp.route('/available-questions', methods=['GET'])
def get_available_questions():
    """Get list of all available questions from the data"""
    try:
        import pandas as pd
        import os
        import io
        import re
        
        # Check if we should use API mode (S3 cache) or file mode
        data_source = request.args.get('data_source', 'file')
        file_key = request.args.get('file_key')  # Optional: specific file to use
        
        if data_source == 'api':
            # Load from cache (S3 or local storage)
            try:
                from ...services.survicate_s3_cache_service import SurvicateS3CacheService
                cache_service = SurvicateS3CacheService()
                
                if not cache_service.use_local_storage and not cache_service.s3_client:
                    return jsonify({
                        'success': False,
                        'error': 'Storage not available',
                        'details': 'S3 client not configured and local storage not enabled.'
                    }), 503
                
                augmented_csv_content = cache_service.load_augmented_csv_from_s3(file_key=file_key)
                if not augmented_csv_content:
                    storage_type = 'local storage' if cache_service.use_local_storage else 'S3'
                    return jsonify({
                        'success': False,
                        'error': 'Augmented CSV not found',
                        'details': f'Please download and augment data from API first. (Checked {storage_type})'
                    }), 404
                
                df = pd.read_csv(io.StringIO(augmented_csv_content))
            except Exception as e:
                logger.error(f"Failed to load from cache: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to load augmented CSV',
                    'details': str(e)
                }), 500
        else:
            # Load from local file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            csv_path = os.path.join(project_root, Config.SURVICATE_CSV_PATH)
            
            if not os.path.exists(csv_path):
                return jsonify({
                    'success': False,
                    'error': 'CSV file not found',
                    'details': f'File not found: {csv_path}'
                }), 404
            
            df = pd.read_csv(csv_path)
        
        # Extract question columns (format: Q#N: Question text (Answer) or Q#N: Question text (Comment))
        # Only include questions that have actual data (non-empty responses)
        questions = []
        seen_questions = set()
        
        for col in df.columns:
            # Match pattern: Q#N: Question text (Answer/Comment)
            match = re.match(r'Q#(\d+):\s*(.+?)\s*\((Answer|Comment)\)', str(col))
            if match:
                q_num = match.group(1)
                q_text = match.group(2).strip()
                q_type = match.group(3)
                
                # Only add Answer columns (skip Comment duplicates)
                if q_type == 'Answer' and q_num not in seen_questions:
                    # Check if this question has any actual data (non-null, non-empty values)
                    col_data = df[col]
                    has_data = col_data.notna().any() and (col_data.astype(str).str.strip() != '').any()
                    
                    if has_data:
                        seen_questions.add(q_num)
                        questions.append({
                            'id': f'Q{q_num}',
                            'number': int(q_num),
                            'text': f'Q#{q_num}: {q_text}',
                            'question_text': q_text
                        })
        
        # Sort by question number
        questions.sort(key=lambda x: x['number'])
        
        return jsonify({
            'success': True,
            'questions': questions,
            'total': len(questions)
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting available questions: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to get available questions',
            'details': str(e)
        }), 500


@survicate_bp.route('/question-trends', methods=['GET'])
def get_question_trends():
    """Get trends for specific survey questions by month (COUNTA of non-empty values)"""
    try:
        import pandas as pd
        import os
        import io
        
        # Check if we should use API mode (S3 cache) or file mode
        data_source = request.args.get('data_source', 'file')
        file_key = request.args.get('file_key')  # Optional: specific file to use
        
        if data_source == 'api':
            # Load from cache (S3 or local storage)
            try:
                from ...services.survicate_s3_cache_service import SurvicateS3CacheService
                cache_service = SurvicateS3CacheService()
                
                # Check if S3 is available or if local storage is being used
                if not cache_service.use_local_storage and not cache_service.s3_client:
                    return jsonify({
                        'success': False,
                        'error': 'Storage not available',
                        'details': 'S3 client not configured and local storage not enabled. Set S3_BUCKET_NAME or SURVICATE_USE_LOCAL_STORAGE=true.'
                    }), 503
                
                augmented_csv_content = cache_service.load_augmented_csv_from_s3(file_key=file_key)
                if not augmented_csv_content:
                    storage_type = 'local storage' if cache_service.use_local_storage else 'S3'
                    return jsonify({
                        'success': False,
                        'error': 'Augmented CSV not found',
                        'details': f'Please download and augment data from API first using the "Download from API" button. (Checked {storage_type})'
                    }), 404
                
                # Read CSV from string content
                df = pd.read_csv(io.StringIO(augmented_csv_content))
                storage_type = 'local storage' if cache_service.use_local_storage else 'S3'
                logger.info(f"Loaded {len(df)} rows from {storage_type} augmented cache (file: {file_key or 'latest'})")
                
            except Exception as e:
                logger.error(f"Failed to load from cache: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to load augmented CSV',
                    'details': str(e)
                }), 500
        else:
            # Load from local file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(current_dir, '..', '..', '..', 'data', 
                                    'survicate_cancelled_subscriptions_augmented.csv')
            
            if not os.path.exists(csv_path):
                logger.error(f"CSV file not found at {csv_path}")
                return jsonify({
                    'success': False,
                    'error': 'Data file not found',
                    'details': f'Expected file at: {csv_path}'
                }), 404
            
            # Read the CSV
            df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(df)} rows from local file")
        
        # Get question parameter
        question = request.args.get('question')
        if not question:
            return jsonify({
                'success': False,
                'error': 'Question parameter required',
                'details': 'Specify question as Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, or Q12'
            }), 400
        
        # Map question codes to search patterns (flexible matching by TEXT CONTENT)
        # Uses centralized question configuration for resilience to renumbering
        from ...utils.survicate_question_config import get_question_patterns, get_question_by_legacy_number
        
        # Get patterns from centralized config (supports both logical IDs and legacy Q# numbers)
        question_patterns = get_question_patterns()
        
        # Also support logical question IDs (e.g., 'learn_engagement' instead of 'Q9')
        # Check if question is a logical ID first
        question_config = None
        if question.startswith('Q'):
            # Legacy Q# format - get config by number
            question_config = get_question_by_legacy_number(question)
        else:
            # Logical ID format - get config directly
            from ...utils.survicate_question_config import get_question_by_logical_id
            question_config = get_question_by_logical_id(question)
        
        # If we have a config, use its patterns; otherwise fall back to legacy patterns
        if question_config:
            pattern = question_config['patterns']
            prefer_answer = question_config.get('prefer_answer', False)
        elif question in question_patterns:
            pattern = question_patterns[question]
            prefer_answer = question in ['Q4', 'Q6', 'Q10', 'Q12']  # Legacy hardcoded list
        else:
            # Question not found
            from ...utils.survicate_question_config import get_all_question_ids
            all_logical_ids = get_all_question_ids()
            return jsonify({
                'success': False,
                'error': 'Invalid question',
                'details': f'Question "{question}" not found. Valid questions: {", ".join(sorted(question_patterns.keys()))} or logical IDs: {", ".join(all_logical_ids)}'
            }), 400
        
        # Find the column that matches the pattern by TEXT CONTENT ONLY
        # This approach is resilient to question number shifts
        column_name = None
        
        # First, try to match by text content (ignoring Q# number)
        # This is the primary matching strategy - it works even if question numbers shift
        exclude_patterns = question_config.get('exclude_patterns', []) if question_config else []
        
        for col in df.columns:
            col_lower = str(col).lower()
            
            # Skip columns that match exclude patterns (to avoid matching wrong questions)
            if exclude_patterns and any(exclude_word.lower() in col_lower for exclude_word in exclude_patterns):
                continue
            
            # Check if all pattern words are in the column name
            if all(word.lower() in col_lower for word in pattern):
                # Prefer (Answer) version if configured
                if prefer_answer:
                    if '(Answer)' in col:
                        column_name = col
                        break
                else:
                    # For other questions, take first match (Answer or Comment)
                    if '(Answer)' in col or '(Comment)' in col:
                        column_name = col
                        break
        
        # Fallback: if text matching didn't work, try sequential number match
        # This helps with edge cases or if question text changed significantly
        if not column_name:
            # Get legacy Q# number for fallback matching
            legacy_q = question
            if question_config:
                legacy_q = question_config.get('legacy_q_number', question)
            
            if legacy_q.startswith('Q'):
                q_num = legacy_q[1:]  # Extract number part
                for col in df.columns:
                    col_str = str(col)
                    if col_str.startswith(f'Q#{q_num}:') or col_str.startswith(f'Q{q_num}:'):
                        # Prefer (Answer) version if configured
                        if prefer_answer:
                            if '(Answer)' in col_str:
                                column_name = col
                                break
                        else:
                            column_name = col
                            break
        
        if not column_name:
            logger.error(f"Could not find column for question {question}. Available columns: {[c for c in df.columns if question[1:] in str(c)]}")
            return jsonify({
                'success': False,
                'error': 'Column not found',
                'details': f'Could not find matching column for question {question}'
            }), 404
        
        # Filter out rows with missing year_month
        df = df[df['year_month'].notna()]
        
        # Filter out excluded months (configurable via SURVICATE_EXCLUDE_MONTHS env var)
        exclude_months = Config.SURVICATE_EXCLUDE_MONTHS.split(',') if Config.SURVICATE_EXCLUDE_MONTHS else []
        exclude_months = [m.strip() for m in exclude_months if m.strip()]
        if exclude_months:
            df = df[~df['year_month'].isin(exclude_months)]
            logger.info(f"Excluded months: {exclude_months}")
        
        if len(df) == 0:
            return jsonify({
                'success': False,
                'error': 'No valid data found',
                'details': 'No rows with valid year_month'
            }), 400
        
        # Filter to only rows with responses to this question
        df_with_responses = df[df[column_name].notna() & (df[column_name].astype(str).str.strip() != '')].copy()
        
        if len(df_with_responses) == 0:
            return jsonify({
                'success': False,
                'error': 'No responses found',
                'details': f'No responses found for question {question}'
            }), 400
        
        # Get unique answers
        df_with_responses['answer'] = df_with_responses[column_name].astype(str).str.strip()
        unique_answers = df_with_responses['answer'].unique().tolist()
        
        # Group by month and answer to get counts
        grouped = df_with_responses.groupby(['year_month', 'answer']).size().reset_index(name='count')
        
        # Get total responses per month (for this question only)
        monthly_totals = df_with_responses.groupby('year_month').size()
        
        # Get unique months
        months = sorted(df_with_responses['year_month'].unique())
        
        # Calculate total counts for each answer (for sorting)
        answer_totals = {}
        for answer in unique_answers:
            answer_totals[answer] = int(grouped[grouped['answer'] == answer]['count'].sum())
        
        # Sort answers by total count (descending) for consistent ordering
        sorted_answers = sorted(unique_answers, key=lambda x: answer_totals[x], reverse=True)
        
        # Format data for frontend - create array with month and all answer counts
        data = []
        for month in months:
            month_data = {'month': month}
            month_total = int(monthly_totals[month])
            month_df = grouped[grouped['year_month'] == month]
            
            for answer in sorted_answers:
                answer_data = month_df[month_df['answer'] == answer]
                if len(answer_data) > 0:
                    count = int(answer_data['count'].values[0])
                    month_data[answer] = count
                    month_data[f'{answer}_percentage'] = round((count / month_total) * 100, 2)
                else:
                    month_data[answer] = 0
                    month_data[f'{answer}_percentage'] = 0
            
            month_data['_total'] = month_total
            data.append(month_data)
        
        return jsonify({
            'success': True,
            'question': question,
            'question_text': column_name,
            'data': data,
            'answers': sorted_answers,
            'months': months,
            'total_responses': int(len(df_with_responses))
        })
    
    except Exception as e:
        import traceback
        logger.error(f"Failed to get question trends: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'details': 'Failed to process question trends data'
        }), 500


@survicate_bp.route('/cache-status', methods=['GET'])
@require_admin_auth
def get_cache_status():
    """Get S3 cache status for API mode"""
    try:
        from ...services.survicate_s3_cache_service import SurvicateS3CacheService
        from ...services.survey_service import api_refresh_state
        
        cache_service = SurvicateS3CacheService()
        cache_status = cache_service.get_cache_status()
        
        # Add refresh state
        cache_status['refresh_in_progress'] = api_refresh_state.get('is_running', False)
        cache_status['refresh_error'] = api_refresh_state.get('error')
        cache_status['refresh_last_fetch'] = api_refresh_state.get('last_fetch')
        cache_status['refresh_diagnostics'] = api_refresh_state.get('diagnostics')
        
        return jsonify({
            'success': True,
            'cache_status': cache_status
        })
    
    except Exception as e:
        logger.error(f"Failed to get cache status: {str(e)}")
        return jsonify({
            'error': str(e),
            'details': 'Failed to get cache status'
        }), 500


@survicate_bp.route('/refresh-api', methods=['POST'])
@require_admin_auth
def refresh_api_cache():
    """Manually trigger API cache refresh"""
    try:
        from ...services.survey_service import api_refresh_state, SurveyService
        
        # Check if already running
        if api_refresh_state.get('is_running', False):
            return jsonify({
                'success': False,
                'message': 'API refresh already in progress',
                'refresh_in_progress': True
            }), 409
        
        # Trigger refresh
        service_container = getattr(g, 'service_container', None)
        if not service_container:
            logger.error("Service container not available in request context")
            return jsonify({'error': 'Service container not initialized'}), 500
        
        survey_service = service_container.get_survey_service()
        survey_service._trigger_background_refresh()
        
        return jsonify({
            'success': True,
            'message': 'API cache refresh started in background',
            'refresh_in_progress': True
        })
    
    except Exception as e:
        logger.error(f"Failed to start API refresh: {str(e)}")
        return jsonify({
            'error': str(e),
            'details': 'Failed to start API cache refresh'
        }), 500


@survicate_bp.route('/env-check', methods=['GET'])
@require_admin_auth
def check_env_vars():
    """Check if Survicate environment variables are available in the container"""
    import os
    return jsonify({
        'success': True,
        'env_vars': {
            'SURVICATE_API_KEY': {
                'in_env': bool(os.getenv('SURVICATE_API_KEY')),
                'in_config': bool(Config.SURVICATE_API_KEY),
                'env_length': len(os.getenv('SURVICATE_API_KEY', '')) if os.getenv('SURVICATE_API_KEY') else 0,
                'config_length': len(Config.SURVICATE_API_KEY) if Config.SURVICATE_API_KEY else 0,
                'env_prefix': os.getenv('SURVICATE_API_KEY', '')[:10] + '...' if os.getenv('SURVICATE_API_KEY') else None,
                'config_prefix': Config.SURVICATE_API_KEY[:10] + '...' if Config.SURVICATE_API_KEY else None
            },
            'SURVICATE_WORKSPACE_KEY': {
                'in_env': bool(os.getenv('SURVICATE_WORKSPACE_KEY')),
                'in_config': bool(Config.SURVICATE_WORKSPACE_KEY),
                'env_length': len(os.getenv('SURVICATE_WORKSPACE_KEY', '')) if os.getenv('SURVICATE_WORKSPACE_KEY') else 0,
                'config_length': len(Config.SURVICATE_WORKSPACE_KEY) if Config.SURVICATE_WORKSPACE_KEY else 0
            },
            'SURVICATE_SURVEY_ID': os.getenv('SURVICATE_SURVEY_ID', Config.SURVICATE_SURVEY_ID),
            'SURVICATE_API_BASE_URL': os.getenv('SURVICATE_API_BASE_URL', Config.SURVICATE_API_BASE_URL)
        }
    })


@survicate_bp.route('/test-api-raw', methods=['GET'])
@require_admin_auth
def test_api_raw():
    """Test Survicate API with raw request to see exact error response"""
    try:
        import requests
        import os
        import base64
        
        api_key = Config.SURVICATE_API_KEY
        workspace_key = Config.SURVICATE_WORKSPACE_KEY
        base_url = Config.SURVICATE_API_BASE_URL
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'SURVICATE_API_KEY not configured'
            }), 500
        
        # Test different authentication methods and endpoints
        results = {}
        
        # Test endpoints to try
        test_endpoints = [
            '/surveys',
            '/surveys/',
            f'/surveys/{Config.SURVICATE_SURVEY_ID}/responses',
        ]
        
        # Method 1: Basic auth with API key only (standard format)
        credentials_basic = f"{api_key}:"
        encoded_basic = base64.b64encode(credentials_basic.encode()).decode()
        
        # Method 2: Basic auth with API key as username, empty password (alternative)
        # Some APIs use apiKey:password format where password is empty
        
        # Method 3: Direct API key in Basic (non-standard but some APIs use this)
        
        for endpoint in test_endpoints:
            endpoint_key = endpoint.replace('/', '_').strip('_')
            
            # Standard Basic auth: base64(apiKey:)
            headers1 = {
                'Authorization': f'Basic {encoded_basic}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            try:
                response1 = requests.get(f"{base_url}{endpoint}", headers=headers1, timeout=10)
                results[f'{endpoint_key}_basic_standard'] = {
                    'status_code': response1.status_code,
                    'response_preview': response1.text[:1000],
                    'content_type': response1.headers.get('Content-Type', ''),
                    'is_json': 'application/json' in response1.headers.get('Content-Type', ''),
                    'is_html': 'text/html' in response1.headers.get('Content-Type', ''),
                    'headers': {k: v for k, v in response1.headers.items() if k.lower().startswith(('x-', 'cdn-', 'server'))}
                }
            except Exception as e:
                results[f'{endpoint_key}_basic_standard'] = {'error': str(e)}
        
        # Also test with X-API-Key header (some APIs use this)
        headers_x_api_key = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        try:
            response_x = requests.get(f"{base_url}/surveys", headers=headers_x_api_key, timeout=10)
            results['surveys_x_api_key_header'] = {
                'status_code': response_x.status_code,
                'response_preview': response_x.text[:1000],
                'content_type': response_x.headers.get('Content-Type', ''),
                'is_json': 'application/json' in response_x.headers.get('Content-Type', ''),
            }
        except Exception as e:
            results['surveys_x_api_key_header'] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'base_url': base_url,
            'api_key_length': len(api_key) if api_key else 0,
            'api_key_prefix': api_key[:10] + '...' if api_key and len(api_key) > 10 else api_key,
            'workspace_key_length': len(workspace_key) if workspace_key else 0,
            'survey_id': Config.SURVICATE_SURVEY_ID,
            'note': 'All methods returned 403 with S3 error - likely API key permissions or subscription plan issue',
            'test_results': results
        })
    
    except Exception as e:
        logger.error(f"Failed to test API raw: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@survicate_bp.route('/inspect-response', methods=['GET'])
@require_admin_auth
def inspect_response():
    """Inspect a sample API response to see its structure"""
    try:
        from ...services.survicate_api_client import SurvicateAPIClient
        
        api_client = SurvicateAPIClient()
        
        # Fetch just one page of responses to inspect
        result = api_client.get_responses(
            survey_id=Config.SURVICATE_SURVEY_ID,
            items_per_page=1  # Just get one response
        )
        
        responses = result.get('data', [])
        if not responses:
            return jsonify({
                'success': False,
                'error': 'No responses found',
                'note': 'The API returned an empty data array. Check if the survey has any responses.'
            }), 404
        
        sample_response = responses[0]
        
        # Analyze the response structure
        response_keys = list(sample_response.keys())
        has_questions = 'questions' in sample_response
        has_answers = 'answers' in sample_response
        
        questions_info = None
        answers_info = None
        
        if has_questions:
            questions = sample_response.get('questions', [])
            questions_info = {
                'count': len(questions),
                'sample': questions[0] if questions else None,
                'sample_keys': list(questions[0].keys()) if questions and questions[0] else None
            }
        
        if has_answers:
            answers = sample_response.get('answers', [])
            answers_info = {
                'count': len(answers),
                'sample': answers[0] if answers else None,
                'sample_keys': list(answers[0].keys()) if answers and answers[0] else None
            }
        
        return jsonify({
            'success': True,
            'survey_id': Config.SURVICATE_SURVEY_ID,
            'response_structure': {
                'all_keys': response_keys,
                'has_questions': has_questions,
                'has_answers': has_answers,
                'questions_info': questions_info,
                'answers_info': answers_info
            },
            'sample_response': sample_response,  # Full response for inspection
            'note': 'This shows the structure of a single API response. Check if questions/answers are present.'
        })
    
    except Exception as e:
        import traceback
        logger.error(f"Failed to inspect response: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@survicate_bp.route('/api-status', methods=['GET'])
@require_admin_auth
def get_api_status():
    """Test Survicate API connection"""
    try:
        from ...services.survicate_api_client import SurvicateAPIClient
        
        # Log environment variable status for debugging
        import os
        api_key_env = os.getenv('SURVICATE_API_KEY')
        workspace_key_env = os.getenv('SURVICATE_WORKSPACE_KEY')
        api_key_set = bool(api_key_env)
        workspace_key_set = bool(workspace_key_env)
        
        logger.info(f"API status check - Env vars: SURVICATE_API_KEY set={api_key_set}, SURVICATE_WORKSPACE_KEY set={workspace_key_set}")
        logger.info(f"Config values: SURVICATE_API_KEY set={bool(Config.SURVICATE_API_KEY)}, SURVICATE_WORKSPACE_KEY set={bool(Config.SURVICATE_WORKSPACE_KEY)}")
        logger.info(f"Survey ID: {Config.SURVICATE_SURVEY_ID}, Base URL: {Config.SURVICATE_API_BASE_URL}")
        
        try:
            api_client = SurvicateAPIClient()
            logger.info("SurvicateAPIClient created successfully")
        except Exception as e:
            logger.error(f"Failed to create SurvicateAPIClient: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': f'Failed to initialize API client: {str(e)}',
                'env_check': {
                    'api_key_in_env': api_key_set,
                    'workspace_key_in_env': workspace_key_set,
                    'api_key_in_config': bool(Config.SURVICATE_API_KEY),
                    'workspace_key_in_config': bool(Config.SURVICATE_WORKSPACE_KEY)
                }
            }), 500
        
        logger.info("Testing API connection...")
        status = api_client.test_connection()
        logger.info(f"API connection test result: connected={status.get('connected')}, error={status.get('error')}")
        
        # Add environment variable status to response for debugging
        status['env_check'] = {
            'api_key_in_env': api_key_set,
            'workspace_key_in_env': workspace_key_set,
            'api_key_in_config': bool(Config.SURVICATE_API_KEY),
            'workspace_key_in_config': bool(Config.SURVICATE_WORKSPACE_KEY)
        }
        
        return jsonify({
            'success': True,
            'api_status': status
        })
    
    except Exception as e:
        logger.error(f"Failed to test API connection: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': 'Failed to test API connection. Check SURVICATE_API_KEY configuration.'
        }), 500


@survicate_bp.route('/surveys', methods=['GET'])
def list_surveys():
    """List all surveys in the Survicate account"""
    try:
        from ...services.survicate_api_client import SurvicateAPIClient
        
        api_client = SurvicateAPIClient()
        surveys = api_client.list_surveys()
        
        logger.info(f"Received {len(surveys)} surveys from Survicate API")
        if surveys and len(surveys) > 0:
            logger.debug(f"Sample survey keys: {list(surveys[0].keys()) if isinstance(surveys[0], dict) else 'Not a dict'}")
        
        # Format survey data for frontend (matching Survicate API response structure)
        formatted_surveys = []
        for survey in surveys:
            # Map API fields to frontend format
            # API has: id, type, name, created_at, enabled, responses, launch
            formatted_surveys.append({
                'id': survey.get('id'),
                'name': survey.get('name', 'Unnamed Survey'),
                'type': survey.get('type', ''),
                'description': '',  # Not in API response
                'status': 'active' if survey.get('enabled', False) else 'inactive',
                'enabled': survey.get('enabled', False),
                'created_at': survey.get('created_at'),
                'updated_at': survey.get('last_response_at'),  # Use last_response_at as updated_at
                'questions_count': 0,  # Would need separate API call to get this
                'responses_count': survey.get('responses', 0),
                'launch': survey.get('launch', {})
            })
        
        return jsonify({
            'success': True,
            'surveys': formatted_surveys,
            'total': len(formatted_surveys)
        })
    
    except Exception as e:
        logger.error(f"Failed to list surveys: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': 'Failed to list surveys. Check SURVICATE_API_KEY configuration.'
        }), 500


@survicate_bp.route('/surveys/<survey_id>/responses', methods=['GET'])
def get_survey_responses(survey_id):
    """Get responses from a specific survey (for multi-survey management)"""
    try:
        from ...services.survicate_api_client import SurvicateAPIClient
        from datetime import datetime
        
        api_client = SurvicateAPIClient()
        
        # Get optional query parameters
        start = request.args.get('start')
        end = request.args.get('end')
        items_per_page = int(request.args.get('items_per_page', 100))
        page = int(request.args.get('page', 1))
        
        # Fetch responses with pagination
        result = api_client.get_responses(
            survey_id=survey_id,
            start=start,
            end=end,
            items_per_page=min(max(items_per_page, 1), 100)
        )
        
        responses = result.get('data', [])
        pagination = result.get('pagination_data', {})
        
        # Format responses for frontend display (extract readable values from complex objects)
        formatted_responses = []
        for response in responses:
            formatted_response = {
                'id': response.get('uuid') or response.get('id', 'N/A'),
                'created_at': response.get('collected_at') or response.get('created_at'),
                'answers': []
            }
            
            # Extract answers from the response
            answers_array = response.get('answers', []) or []
            for answer_item in answers_array:
                if not isinstance(answer_item, dict):
                    continue
                
                question_id = answer_item.get('question_id')
                answer_data = answer_item.get('answer')
                
                # Extract readable answer text
                answer_text = 'N/A'
                if isinstance(answer_data, str):
                    answer_text = answer_data
                elif isinstance(answer_data, dict):
                    # Try common fields
                    answer_text = answer_data.get('content') or answer_data.get('text') or answer_data.get('answer', '')
                    # If still empty, try to stringify the object
                    if not answer_text:
                        answer_text = json.dumps(answer_data)
                elif answer_data is not None:
                    answer_text = str(answer_data)
                
                formatted_response['answers'].append({
                    'question_id': question_id,
                    'answer': answer_text,
                    'question_type': answer_item.get('question_type', '')
                })
            
            formatted_responses.append(formatted_response)
        
        return jsonify({
            'success': True,
            'survey_id': survey_id,
            'responses': formatted_responses,
            'pagination': {
                'has_more': pagination.get('has_more', False),
                'next_url': pagination.get('next_url'),
                'current_page': page,
                'items_per_page': items_per_page,
                'total_items': len(responses) + (len(responses) if pagination.get('has_more') else 0)
            }
        })
    
    except Exception as e:
        logger.error(f"Failed to get survey responses: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': f'Failed to get responses for survey {survey_id}'
        }), 500


@survicate_bp.route('/surveys/<survey_id>/download', methods=['POST'])
@require_admin_auth
def download_survey_responses(survey_id):
    """Download all responses from a specific survey and save to S3/local storage"""
    try:
        from ...services.survicate_api_client import SurvicateAPIClient
        from ...services.survicate_api_parser import SurvicateAPIParser
        from ...services.survicate_s3_cache_service import SurvicateS3CacheService
        import threading
        
        # Handle request data - allow missing Content-Type header
        try:
            data = request.get_json() or {}
        except Exception:
            # If JSON parsing fails (e.g., missing Content-Type), use empty dict
            data = {}
        start = data.get('start')
        end = data.get('end')
        
        # Check if download is already in progress for this survey
        from ...services.survey_service import api_refresh_state
        if api_refresh_state.get('is_running', False):
            return jsonify({
                'success': False,
                'error': 'Download already in progress',
                'details': 'Please wait for the current download to complete.'
            }), 409
        
        # Initialize services with error handling
        try:
            api_client = SurvicateAPIClient()
        except Exception as e:
            logger.error(f"Failed to initialize SurvicateAPIClient: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': f'Failed to initialize API client: {str(e)}',
                'details': 'Check SURVICATE_API_KEY configuration.'
            }), 500
        
        try:
            parser = SurvicateAPIParser()
        except Exception as e:
            logger.error(f"Failed to initialize SurvicateAPIParser: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': f'Failed to initialize parser: {str(e)}',
                'details': 'Internal error initializing parser.'
            }), 500
        
        try:
            cache_service = SurvicateS3CacheService()
        except Exception as e:
            logger.error(f"Failed to initialize SurvicateS3CacheService: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': f'Failed to initialize cache service: {str(e)}',
                'details': 'Check S3 configuration or enable local storage.'
            }), 500
        
        # Check if storage is available
        if cache_service.use_local_storage:
            logger.info(f"Using local storage for survey {survey_id}")
        elif not cache_service.s3_client:
            return jsonify({
                'success': False,
                'error': 'Storage not available',
                'details': 'S3 client not configured and local storage not enabled.'
            }), 503
        
        # Mark as running
        api_refresh_state['is_running'] = True
        api_refresh_state['error'] = None
        api_refresh_state['last_fetch'] = datetime.now().isoformat()
        
        def download_survey():
            try:
                logger.info(f"Starting download for survey {survey_id}")
                
                # Fetch survey questions
                questions_map = {}
                try:
                    questions_map = api_client.get_survey_questions(survey_id)
                    parser.questions_map = questions_map
                    logger.info(f"Fetched {len(questions_map)} questions for survey {survey_id}")
                except Exception as e:
                    logger.warning(f"Failed to fetch survey questions: {e}")
                    parser.questions_map = {}
                
                # Fetch all responses
                logger.info(f"Fetching responses from Survicate API for survey {survey_id}...")
                api_responses = api_client.get_all_responses(
                    survey_id=survey_id,
                    start=start,
                    end=end
                )
                logger.info(f"Successfully fetched {len(api_responses)} responses from API")
                
                if not api_responses:
                    api_refresh_state['error'] = f'No responses found for survey {survey_id}'
                    api_refresh_state['is_running'] = False
                    return
                
                # Parse responses to SurveyResponse objects
                logger.info(f"Parsing {len(api_responses)} responses...")
                survey_responses = parser.parse_responses(api_responses)
                
                if not survey_responses:
                    api_refresh_state['error'] = f'No responses were parsed for survey {survey_id}'
                    api_refresh_state['is_running'] = False
                    return
                
                # Temporarily set cache key for this survey
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                original_key = cache_service.cache_key
                cache_service.cache_key = f'surveys/{survey_id}/raw_{timestamp}.csv'
                
                try:
                    # Save to S3 or local storage using existing method
                    cache_service.save_to_s3(survey_responses, questions_map=questions_map)
                    logger.info(f"Saved {len(survey_responses)} responses for survey {survey_id}")
                finally:
                    # Restore original cache key
                    cache_service.cache_key = original_key
                
                api_refresh_state['is_running'] = False
                api_refresh_state['last_fetch'] = datetime.now().isoformat()
                api_refresh_state['error'] = None
                
            except Exception as e:
                logger.error(f"Error downloading survey {survey_id}: {e}", exc_info=True)
                api_refresh_state['error'] = str(e)
                api_refresh_state['is_running'] = False
        
        # Start download in background thread
        thread = threading.Thread(target=download_survey, daemon=True)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Download started for survey {survey_id}',
            'survey_id': survey_id
        })
    
    except Exception as e:
        logger.error(f"Failed to start survey download: {str(e)}", exc_info=True)
        from ...services.survey_service import api_refresh_state
        api_refresh_state['is_running'] = False
        api_refresh_state['error'] = str(e)
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Full traceback: {error_details}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': f'Failed to start download for survey {survey_id}. Check server logs for details.'
        }), 500


@survicate_bp.route('/surveys/<survey_id>/files', methods=['GET'])
def list_survey_files(survey_id):
    """List all downloaded files for a specific survey"""
    try:
        from ...services.survicate_s3_cache_service import SurvicateS3CacheService
        import boto3
        from pathlib import Path
        
        cache_service = SurvicateS3CacheService()
        files = []
        
        if cache_service.use_local_storage:
            # List files from local storage
            if cache_service.local_cache_dir and cache_service.local_cache_dir.exists():
                # Look for files in survey-specific subdirectory
                survey_dir = cache_service.local_cache_dir / f'surveys/{survey_id}'
                if survey_dir.exists():
                    for csv_file in survey_dir.glob('raw_*.csv'):
                        try:
                            content = csv_file.read_text(encoding='utf-8')
                            lines = content.strip().split('\n')
                            line_count = max(0, len(lines) - 1)
                            mtime = csv_file.stat().st_mtime
                            last_modified = datetime.fromtimestamp(mtime, tz=timezone.utc)
                            
                            # Store with full path for download
                            file_key = f'surveys/{survey_id}/{csv_file.name}'
                            
                            files.append({
                                'key': file_key,
                                'display_name': csv_file.name,
                                'file_size': csv_file.stat().st_size,
                                'last_modified': last_modified.isoformat(),
                                'response_count': line_count
                            })
                        except Exception as e:
                            logger.warning(f"Failed to get info for {csv_file}: {e}")
        else:
            # List files from S3
            if cache_service.s3_client:
                try:
                    prefix = f'surveys/{survey_id}/'
                    response = cache_service.s3_client.list_objects_v2(
                        Bucket=cache_service.bucket_name,
                        Prefix=prefix
                    )
                    
                    if 'Contents' in response:
                        for obj in response['Contents']:
                            key = obj['Key']
                            if key.endswith('.csv'):
                                files.append({
                                    'key': key,
                                    'display_name': key.split('/')[-1],
                                    'file_size': obj.get('Size', 0),
                                    'last_modified': obj.get('LastModified', datetime.now(timezone.utc)).isoformat(),
                                    'response_count': 0  # Would need to read file to count
                                })
                except Exception as e:
                    logger.error(f"Failed to list files from S3: {e}")
        
        # Sort by last modified (newest first)
        files.sort(key=lambda x: x['last_modified'], reverse=True)
        
        return jsonify({
            'success': True,
            'survey_id': survey_id,
            'files': files,
            'total': len(files)
        })
    
    except Exception as e:
        logger.error(f"Failed to list survey files: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': f'Failed to list files for survey {survey_id}'
        }), 500


@survicate_bp.route('/surveys/<survey_id>/files/download', methods=['GET'])
def download_survey_file(survey_id):
    """Download a specific survey file"""
    try:
        from ...services.survicate_s3_cache_service import SurvicateS3CacheService
        from flask import Response
        import urllib.parse
        
        file_key = request.args.get('file_key')
        if not file_key:
            return jsonify({
                'success': False,
                'error': 'file_key parameter required'
            }), 400
        
        cache_service = SurvicateS3CacheService()
        file_key = urllib.parse.unquote(file_key)
        
        if cache_service.use_local_storage:
            # Load from local file
            # file_key format: surveys/{survey_id}/raw_{timestamp}.csv
            # Extract just the filename for local storage
            filename = file_key.split('/')[-1] if '/' in file_key else file_key
            file_path = cache_service.local_cache_dir / filename
            if not file_path.exists():
                return jsonify({
                    'success': False,
                    'error': 'File not found',
                    'details': f'File {filename} does not exist locally.'
                }), 404
            
            file_content = file_path.read_bytes()
            filename = file_key.split('/')[-1] if '/' in file_key else file_key
            
            return Response(
                file_content,
                mimetype='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                    'Content-Type': 'text/csv; charset=utf-8'
                }
            )
        else:
            # Get from S3
            if not cache_service.s3_client:
                return jsonify({
                    'success': False,
                    'error': 'S3 not available',
                    'details': 'S3 client not configured.'
                }), 503
            
            try:
                response = cache_service.s3_client.get_object(
                    Bucket=cache_service.bucket_name,
                    Key=file_key
                )
                file_content = response['Body'].read()
                filename = file_key.split('/')[-1] if '/' in file_key else file_key
                
                return Response(
                    file_content,
                    mimetype='text/csv',
                    headers={
                        'Content-Disposition': f'attachment; filename="{filename}"',
                        'Content-Type': 'text/csv; charset=utf-8'
                    }
                )
            except cache_service.s3_client.exceptions.NoSuchKey:
                return jsonify({
                    'success': False,
                    'error': 'File not found',
                    'details': f'File {file_key} does not exist in S3.'
                }), 404
    
    except Exception as e:
        logger.error(f"Failed to download survey file: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': 'Failed to download file'
        }), 500


@survicate_bp.route('/surveys/<survey_id>/summary', methods=['GET'])
def get_survey_aggregated_summary(survey_id):
    """Get aggregated summary statistics for a survey from downloaded files"""
    try:
        import pandas as pd
        import io
        import re
        from ...services.survicate_s3_cache_service import SurvicateS3CacheService
        
        # Get file_key from query parameter (optional - defaults to most recent)
        file_key = request.args.get('file_key')
        
        cache_service = SurvicateS3CacheService()
        
        # Load the CSV file
        csv_content = None
        if cache_service.use_local_storage:
            if file_key:
                filename = file_key.split('/')[-1]
                file_path = cache_service.local_cache_dir / f'surveys/{survey_id}' / filename
                if file_path.exists():
                    csv_content = file_path.read_text(encoding='utf-8')
            else:
                # Get most recent file
                survey_dir = cache_service.local_cache_dir / f'surveys/{survey_id}'
                if survey_dir.exists():
                    csv_files = list(survey_dir.glob('raw_*.csv'))
                    if csv_files:
                        latest_file = max(csv_files, key=lambda p: p.stat().st_mtime)
                        csv_content = latest_file.read_text(encoding='utf-8')
        else:
            # Load from S3
            if not cache_service.s3_client:
                return jsonify({
                    'success': False,
                    'error': 'S3 not available',
                    'details': 'S3 client not configured.'
                }), 503
            
            if file_key:
                try:
                    response = cache_service.s3_client.get_object(
                        Bucket=cache_service.bucket_name,
                        Key=file_key
                    )
                    csv_content = response['Body'].read().decode('utf-8')
                except cache_service.s3_client.exceptions.NoSuchKey:
                    return jsonify({
                        'success': False,
                        'error': 'File not found',
                        'details': f'File {file_key} does not exist in S3.'
                    }), 404
            else:
                # Get most recent file
                prefix = f'surveys/{survey_id}/'
                response = cache_service.s3_client.list_objects_v2(
                    Bucket=cache_service.bucket_name,
                    Prefix=prefix
                )
                if 'Contents' in response and response['Contents']:
                    # Sort by LastModified, get most recent
                    latest_obj = max(response['Contents'], key=lambda x: x['LastModified'])
                    file_response = cache_service.s3_client.get_object(
                        Bucket=cache_service.bucket_name,
                        Key=latest_obj['Key']
                    )
                    csv_content = file_response['Body'].read().decode('utf-8')
        
        if not csv_content:
            return jsonify({
                'success': False,
                'error': 'No data found',
                'details': f'No downloaded files found for survey {survey_id}. Please download responses first.'
            }), 404
        
        # Parse CSV
        df = pd.read_csv(io.StringIO(csv_content))
        
        # Basic statistics
        total_responses = len(df)
        
        # Date range
        date_col = 'Date & Time (UTC)'
        date_range = None
        if date_col in df.columns:
            df['_parsed_date'] = pd.to_datetime(df[date_col], errors='coerce')
            valid_dates = df['_parsed_date'].dropna()
            if len(valid_dates) > 0:
                date_range = {
                    'start': valid_dates.min().isoformat(),
                    'end': valid_dates.max().isoformat()
                }
        
        # Extract question columns and aggregate answers
        question_stats = {}
        question_pattern = re.compile(r'Q#(\d+):\s*(.+?)\s*\((Answer|Comment)\)')
        
        # Helper function to convert numpy/pandas types to native Python types
        def _convert_to_native_types(obj):
            """Recursively convert numpy/pandas types to native Python types for JSON serialization"""
            import numpy as np
            if isinstance(obj, dict):
                return {k: _convert_to_native_types(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [_convert_to_native_types(item) for item in obj]
            elif isinstance(obj, (np.integer, np.floating)):
                return obj.item()
            elif isinstance(obj, np.bool_):
                return bool(obj)
            elif isinstance(obj, (bool, int, float, str)) or obj is None:
                return obj
            else:
                # Fallback: convert to string
                return str(obj)
        
        # Helper function to analyze text responses with LLM
        def analyze_text_responses_with_llm(question_text, text_responses, claude_service):
            """Use Claude to analyze free-form text responses and extract insights"""
            if not claude_service or len(text_responses) == 0:
                return None
            
            try:
                # Limit to first 100 responses to avoid token limits
                sample_responses = text_responses[:100]
                responses_text = "\n".join([f"- {resp}" for resp in sample_responses])
                
                system_prompt = f"""You are analyzing free-form text responses to a survey question. Your task is to extract quantified insights from these responses.

Question: "{question_text}"

Analyze the following {len(sample_responses)} responses and provide:
1. Common themes/topics (list 5-10 most common themes with approximate frequency)
2. Sentiment distribution (positive, neutral, negative with approximate percentages)
3. Key phrases or keywords that appear frequently
4. Categorized feedback (group similar feedback into categories with counts)

Format your response as JSON with this structure:
{{
  "themes": [
    {{"theme": "theme name", "frequency": "high/medium/low", "examples": ["example 1", "example 2"]}}
  ],
  "sentiment": {{
    "positive": 35,
    "neutral": 45,
    "negative": 20
  }},
  "key_phrases": ["phrase 1", "phrase 2", "phrase 3"],
  "categories": [
    {{"category": "category name", "count": 15, "percentage": 25.5, "examples": ["example 1"]}}
  ],
  "summary": "Brief 2-3 sentence summary of the main insights"
}}

Be concise but specific. Focus on actionable insights."""

                message = f"Analyze these survey responses:\n\n{responses_text}"
                
                response = claude_service.send_message(
                    message=message,
                    model=None,  # Use default model
                    max_tokens=2000,
                    system_prompt=system_prompt
                )
                
                # Parse JSON from response
                response_text = response.content.strip()
                
                # Try to extract JSON from response (might have markdown code blocks)
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    try:
                        insights = json.loads(json_match.group(0))
                        # Convert any numpy/pandas types to native Python types for JSON serialization
                        insights = _convert_to_native_types(insights)
                        return insights
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse LLM response as JSON: {e}")
                        # Fallback: return as text summary
                        return {
                            'summary': response_text,
                            'raw_analysis': True
                        }
                else:
                    # Fallback: return as text summary
                    return {
                        'summary': response_text,
                        'raw_analysis': True
                    }
            except Exception as e:
                logger.warning(f"Failed to analyze text responses with LLM: {e}")
                return None
        
        # Get Claude service for text analysis (optional)
        claude_service = None
        try:
            service_container = getattr(g, 'service_container', None)
            if service_container:
                claude_service = service_container.get_claude_service()
        except Exception as e:
            logger.debug(f"Claude service not available for text analysis: {e}")
        
        for col in df.columns:
            match = question_pattern.match(str(col))
            if match and match.group(3) == 'Answer':  # Only process Answer columns
                q_num = match.group(1)
                q_text = match.group(2).strip()
                
                # Get non-null answers
                answers = df[col].dropna()
                answers = answers[answers.astype(str).str.strip() != '']
                
                if len(answers) > 0:
                    # Count answer frequencies
                    answer_counts = answers.value_counts().to_dict()
                    total_answers = len(answers)
                    
                    # Calculate percentages
                    answer_distribution = {}
                    for answer, count in answer_counts.items():
                        answer_distribution[str(answer)] = {
                            'count': int(count),
                            'percentage': round((count / total_answers) * 100, 2)
                        }
                    
                    # Sort by count (descending)
                    sorted_answers = sorted(answer_distribution.items(), key=lambda x: x[1]['count'], reverse=True)
                    
                    # Detect if this is a free-form text question
                    # Criteria: high unique answer ratio (>50%) or average answer length > 50 chars
                    unique_ratio = len(answer_distribution) / total_answers if total_answers > 0 else 0
                    avg_length = answers.astype(str).str.len().mean() if len(answers) > 0 else 0
                    is_text_question = unique_ratio > 0.5 or avg_length > 50
                    
                    question_data = {
                        'question_number': int(q_num),
                        'question_text': q_text,
                        'total_responses': int(total_answers),
                        'response_rate': round((total_answers / total_responses) * 100, 2) if total_responses > 0 else 0,
                        'top_answers': dict(sorted_answers[:10]),  # Top 10 answers
                        'unique_answers_count': len(answer_distribution),
                        'is_text_question': bool(is_text_question),  # Ensure native Python bool
                        'average_answer_length': float(round(avg_length, 1)) if avg_length else 0.0  # Ensure native Python float
                    }
                    
                    # If it's a text question, analyze with LLM
                    if is_text_question and claude_service:
                        text_responses_list = answers.astype(str).tolist()
                        llm_insights = analyze_text_responses_with_llm(q_text, text_responses_list, claude_service)
                        if llm_insights:
                            question_data['llm_insights'] = llm_insights
                    
                    question_stats[f'Q{q_num}'] = question_data
        
        # Sort questions by question number
        sorted_questions = sorted(question_stats.items(), key=lambda x: x[1]['question_number'])
        
        # Convert all data to native Python types for JSON serialization
        summary_data = {
            'total_responses': int(total_responses),
            'date_range': date_range,
            'questions': dict(sorted_questions),
            'total_questions': int(len(question_stats))
        }
        
        # Recursively convert any numpy/pandas types
        summary_data = _convert_to_native_types(summary_data)
        
        return jsonify({
            'success': True,
            'survey_id': survey_id,
            'summary': summary_data
        })
    
    except Exception as e:
        import traceback
        logger.error(f"Failed to get survey summary: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': f'Failed to analyze survey data for survey {survey_id}'
        }), 500


@survicate_bp.route('/surveys/<survey_id>/questions', methods=['GET'])
def get_survey_questions_endpoint(survey_id):
    """Get questions for a specific survey"""
    try:
        from ...services.survicate_api_client import SurvicateAPIClient
        
        api_client = SurvicateAPIClient()
        questions_map = api_client.get_survey_questions(survey_id)
        
        # Format questions for frontend
        questions = []
        for q_id, q_text in questions_map.items():
            questions.append({
                'id': q_id,
                'text': q_text
            })
        
        return jsonify({
            'success': True,
            'survey_id': survey_id,
            'questions': questions,
            'total': len(questions)
        })
    
    except Exception as e:
        logger.error(f"Failed to get survey questions: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'details': f'Failed to get questions for survey {survey_id}'
        }), 500