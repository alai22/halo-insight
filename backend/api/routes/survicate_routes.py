"""
API routes for Survicate survey analysis
"""

from flask import Blueprint, request, jsonify, g
from ...utils.logging import get_logger
from ...utils.config import Config

logger = get_logger('survicate_routes')

# Create blueprint
survicate_bp = Blueprint('survicate', __name__, url_prefix='/api/survicate')


@survicate_bp.route('/ask', methods=['POST'])
def survicate_ask():
    """Ask Claude about survey data with detailed RAG process information"""
    try:
        # Get services from container (injected via Flask's g)
        service_container = getattr(g, 'service_container', None)
        if not service_container:
            logger.error("Service container not available in request context")
            return jsonify({'error': 'Service container not initialized'}), 500
        
        claude_service = service_container.get_claude_service()
        survicate_rag_service = service_container.get_survicate_rag_service()
        
        data = request.get_json()
        question = data.get('question')
        # Default to configured model (falls back to working model via fallback system if needed)
        model = data.get('model', Config.CLAUDE_MODEL)
        max_tokens = data.get('max_tokens', 2000)
        data_source = data.get('data_source', 'file')  # Get data source
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        logger.info(f"Survicate RAG query request: question={question[:100]}, model={model}, max_tokens={max_tokens}, data_source={data_source}")
        
        # Reload surveys with specified data source before processing query
        survey_service = service_container.get_survey_service()
        survey_service.load_surveys(data_source=data_source)
        
        # Check if Claude service is initialized
        if claude_service is None or survicate_rag_service is None:
            error_msg = "Claude API service is not initialized. Please check ANTHROPIC_API_KEY configuration."
            logger.error(error_msg)
            return jsonify({
                'error': error_msg, 
                'details': 'ANTHROPIC_API_KEY environment variable is not set or invalid. Please configure it in your .env file or environment.'
            }), 503
        
        result = survicate_rag_service.process_query(question, model, max_tokens)
        result['data_source'] = data_source  # Include data source in response
        
        return jsonify(result)
    
    except TimeoutError as e:
        error_msg = str(e) if str(e) else "Request to Claude API timed out. The query may be too complex."
        logger.error(f"Survicate RAG query timeout: {error_msg}")
        return jsonify({
            'error': 'Request timeout',
            'details': error_msg,
            'type': 'TimeoutError',
            'suggestion': 'Try simplifying your query or increasing CLAUDE_API_TIMEOUT if needed.'
        }), 504
    
    except ValueError as e:
        error_msg = f"Configuration error: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg, 'details': 'Please check your API configuration (ANTHROPIC_API_KEY)'}), 500
    except Exception as e:
        import traceback
        logger.error(f"Survicate RAG query error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        error_details = str(e)
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            error_details = f"{str(e)} - Response: {e.response.text}"
        
        return jsonify({
            'error': str(e),
            'details': error_details,
            'type': type(e).__name__
        }), 500


@survicate_bp.route('/refresh', methods=['POST'])
def refresh_surveys():
    """Refresh survey data from specified source (file or api)"""
    try:
        service_container = getattr(g, 'service_container', None)
        if not service_container:
            logger.error("Service container not available in request context")
            return jsonify({'error': 'Service container not initialized'}), 500
        
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
    
    except Exception as e:
        logger.error(f"Failed to refresh surveys: {str(e)}")
        return jsonify({
            'error': str(e),
            'details': 'Failed to refresh survey data'
        }), 500


@survicate_bp.route('/summary', methods=['GET'])
def get_survey_summary():
    """Get survey statistics"""
    try:
        service_container = getattr(g, 'service_container', None)
        if not service_container:
            logger.error("Service container not available in request context")
            return jsonify({'error': 'Service container not initialized'}), 500
        
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
    
    except Exception as e:
        logger.error(f"Failed to get survey summary: {str(e)}")
        return jsonify({
            'error': str(e),
            'details': 'Failed to get survey summary'
        }), 500


@survicate_bp.route('/search', methods=['POST'])
def search_surveys():
    """Search survey responses"""
    try:
        service_container = getattr(g, 'service_container', None)
        if not service_container:
            logger.error("Service container not available in request context")
            return jsonify({'error': 'Service container not initialized'}), 500
        
        survey_service = service_container.get_survey_service()
        
        data = request.get_json()
        query = data.get('query')
        limit = data.get('limit', 10)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        results = survey_service.semantic_search_surveys(query, limit=limit)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    
    except Exception as e:
        logger.error(f"Failed to search surveys: {str(e)}")
        return jsonify({
            'error': str(e),
            'details': 'Failed to search survey data'
        }), 500


@survicate_bp.route('/raw-files/download', methods=['GET'])
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
                'details': 'Specify question as Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, or Q11'
            }), 400
        
        # Map question codes to search patterns (flexible matching)
        question_patterns = {
            'Q2': ['location pin', 'not match', 'dog'],
            'Q3': ['pet location pin', 'grayed out', 'inaccurate'],
            'Q4': ['collar', 'not sending feedback', 'dog not responding'],
            'Q5': ['screw in', 'contact tips', 'static feedback'],
            'Q6': ['battery life', 'charging', 'power issues'],
            'Q7': ['containment solution', 'purchase'],
            'Q8': ['engage', 'Learn training curriculum'],
            'Q9': ['main reason', 'didn\'t complete', 'Learn curriculum'],
            'Q10': ['contact', 'Customer Service', 'Dog Park'],
            'Q11': ['free session', 'trainer', 'collar effectively']
        }
        
        if question not in question_patterns:
            return jsonify({
                'success': False,
                'error': 'Invalid question',
                'details': f'Valid questions: {", ".join(sorted(question_patterns.keys()))}'
            }), 400
        
        # Find the column that matches the pattern
        pattern = question_patterns[question]
        column_name = None
        
        # First try pattern matching
        for col in df.columns:
            col_lower = str(col).lower()
            # Check if all pattern words are in the column name
            if all(word.lower() in col_lower for word in pattern):
                # Also check if it starts with the question number
                if f'q#{question[1:]}' in col_lower or f'q{question[1:]}' in col_lower:
                    column_name = col
                    break
        
        # If pattern matching didn't work, try exact match
        if not column_name:
            # Look for columns that start with the question number
            for col in df.columns:
                col_str = str(col)
                if col_str.startswith(f'Q#{question[1:]}:') or col_str.startswith(f'Q{question[1:]}:'):
                    # For Q4, Q6, Q9, prefer the (Answer) version
                    if question in ['Q4', 'Q6', 'Q9']:
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