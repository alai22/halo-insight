"""
Survicate S3 Cache Service

Manages caching of Survicate API responses in S3
"""

import json
import csv
import io
import boto3
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, timezone
from ..utils.config import Config
from ..utils.logging import get_logger
from ..models.survey import SurveyResponse

logger = get_logger('survicate_s3_cache_service')


class SurvicateS3CacheService:
    """Service for managing Survicate API cache in S3"""
    
    def __init__(self):
        """Initialize S3 cache service"""
        self.bucket_name = Config.S3_BUCKET_NAME
        self.cache_key = Config.SURVICATE_S3_CACHE_KEY
        self.augmented_cache_key = Config.SURVICATE_S3_AUGMENTED_CACHE_KEY  # Legacy single file key
        self.augmented_prefix = Config.SURVICATE_S3_AUGMENTED_PREFIX  # Prefix for timestamped files
        self.metadata_key = Config.SURVICATE_S3_METADATA_KEY
        self.augmented_metadata_key = Config.SURVICATE_S3_AUGMENTED_METADATA_KEY
        self.max_age_hours = Config.SURVICATE_CACHE_MAX_AGE_HOURS
        
        if not self.bucket_name:
            logger.warning("S3_BUCKET_NAME not configured, S3 cache will not be available")
            self.s3_client = None
        else:
            try:
                self.s3_client = boto3.client('s3', region_name=Config.S3_REGION)
            except Exception as e:
                logger.warning(f"Could not initialize S3 client: {e}")
                self.s3_client = None
    
    def is_cache_fresh(self, max_age_hours: Optional[int] = None) -> bool:
        """Check if cache is fresh (less than max_age_hours old)"""
        if not self.s3_client:
            return False
        
        max_age = max_age_hours or self.max_age_hours
        last_modified = self.get_last_modified()
        
        if not last_modified:
            return False
        
        age = datetime.now(timezone.utc) - last_modified
        return age.total_seconds() < (max_age * 3600)
    
    def get_cache_age(self) -> Optional[timedelta]:
        """Get age of cache as timedelta"""
        if not self.s3_client:
            return None
        
        last_modified = self.get_last_modified()
        if not last_modified:
            return None
        
        return datetime.now(timezone.utc) - last_modified
    
    def get_last_modified(self) -> Optional[datetime]:
        """Get LastModified time from S3 object metadata"""
        if not self.s3_client:
            return None
        
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=self.cache_key
            )
            # S3 returns LastModified in UTC
            return response['LastModified']
        except self.s3_client.exceptions.NoSuchKey:
            logger.debug(f"Cache file not found in S3: {self.cache_key}")
            return None
        except self.s3_client.exceptions.ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code in ('403', 'Forbidden', 'InvalidAccessKeyId', 'SignatureDoesNotMatch'):
                logger.warning(f"S3 access denied - check AWS credentials: {error_code}")
            else:
                logger.warning(f"Failed to check S3 cache metadata: {e}")
            return None
        except Exception as e:
            logger.warning(f"Failed to check S3 cache metadata: {e}")
            return None
    
    def load_from_s3(self) -> List[SurveyResponse]:
        """Load survey responses from S3 cache"""
        if not self.s3_client:
            raise ValueError("S3 client not available. Check S3_BUCKET_NAME configuration.")
        
        try:
            logger.info(f"Loading cache from S3: s3://{self.bucket_name}/{self.cache_key}")
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=self.cache_key
            )
            
            # Read CSV content
            content = response['Body'].read().decode('utf-8')
            
            # Parse CSV using existing parser
            from .survey_parser_service import SurveyParserService
            import tempfile
            import os
            
            # Create temporary file for parser
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                f.write(content)
                temp_path = f.name
            
            try:
                parser = SurveyParserService(temp_path)
                responses = parser.parse_csv()
                logger.info(f"Loaded {len(responses)} responses from S3 cache")
                return responses
            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except self.s3_client.exceptions.NoSuchKey:
            logger.info(f"Cache file not found in S3: {self.cache_key}")
            return []
        except self.s3_client.exceptions.ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            error_msg = e.response.get('Error', {}).get('Message', str(e))
            if error_code in ('403', 'Forbidden', 'InvalidAccessKeyId', 'SignatureDoesNotMatch'):
                raise ValueError(f"S3 access denied - check AWS credentials. Error: {error_code} - {error_msg}")
            else:
                logger.error(f"Failed to load cache from S3: {error_code} - {error_msg}")
                raise
        except Exception as e:
            logger.error(f"Failed to load cache from S3: {e}")
            raise
    
    def save_to_s3(self, responses: List[SurveyResponse]):
        """Save survey responses to S3 cache as CSV"""
        if not self.s3_client:
            raise ValueError("S3 client not available")
        
        if not responses:
            logger.warning("No responses to save")
            return
        
        try:
            logger.info(f"Saving {len(responses)} responses to S3 cache")
            
            # Convert to CSV format (matching manual export format)
            csv_content = self._responses_to_csv(responses)
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=self.cache_key,
                Body=csv_content.encode('utf-8'),
                ContentType='text/csv'
            )
            
            logger.info(f"Successfully saved cache to S3: s3://{self.bucket_name}/{self.cache_key}")
            
            # Update metadata
            self.update_metadata(datetime.now(timezone.utc), 'success')
            
        except Exception as e:
            logger.error(f"Failed to save cache to S3: {e}")
            # Update metadata with error
            self.update_metadata(datetime.now(timezone.utc), f'error: {str(e)}')
            raise
    
    def save_augmented_csv_to_s3(self, csv_content: str, response_count: int = 0) -> str:
        """
        Save augmented CSV content to S3 with timestamped filename
        
        Args:
            csv_content: CSV content to save
            response_count: Number of responses in the CSV
            
        Returns:
            S3 key of the saved file
        """
        if not self.s3_client:
            raise ValueError("S3 client not available")
        
        if not csv_content:
            logger.warning("No augmented CSV content to save")
            return None
        
        try:
            # Create timestamped filename
            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
            timestamped_key = f"{self.augmented_prefix}augmented_{timestamp}.csv"
            
            logger.info(f"Saving augmented CSV to S3: s3://{self.bucket_name}/{timestamped_key}")
            
            # Upload timestamped file to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=timestamped_key,
                Body=csv_content.encode('utf-8'),
                ContentType='text/csv'
            )
            
            logger.info(f"Successfully saved augmented CSV to S3: s3://{self.bucket_name}/{timestamped_key}")
            
            # Also save to legacy key for backward compatibility
            try:
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=self.augmented_cache_key,
                    Body=csv_content.encode('utf-8'),
                    ContentType='text/csv'
                )
                logger.info(f"Also saved to legacy key: {self.augmented_cache_key}")
            except Exception as e:
                logger.warning(f"Failed to save to legacy key: {e}")
            
            # Update metadata file listing all augmented files
            self._update_augmented_files_metadata(timestamped_key, response_count)
            
            return timestamped_key
            
        except Exception as e:
            logger.error(f"Failed to save augmented CSV to S3: {e}")
            raise
    
    def _update_augmented_files_metadata(self, new_file_key: str, response_count: int):
        """Update metadata file with list of all augmented files"""
        try:
            # Load existing metadata
            existing_files = []
            try:
                response = self.s3_client.get_object(
                    Bucket=self.bucket_name,
                    Key=self.augmented_metadata_key
                )
                metadata_content = response['Body'].read().decode('utf-8')
                existing_files = json.loads(metadata_content).get('files', [])
            except self.s3_client.exceptions.NoSuchKey:
                pass  # No existing metadata, start fresh
            except Exception as e:
                logger.warning(f"Failed to load existing metadata: {e}")
            
            # Get file info from S3
            try:
                response = self.s3_client.head_object(
                    Bucket=self.bucket_name,
                    Key=new_file_key
                )
                file_size = response.get('ContentLength', 0)
                last_modified = response.get('LastModified')
            except Exception as e:
                logger.warning(f"Failed to get file info: {e}")
                file_size = 0
                last_modified = datetime.now(timezone.utc)
            
            # Add new file entry
            new_entry = {
                'key': new_file_key,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'response_count': response_count,
                'file_size': file_size,
                'last_modified': last_modified.isoformat() if hasattr(last_modified, 'isoformat') else str(last_modified)
            }
            
            # Remove duplicate if exists (shouldn't happen, but just in case)
            existing_files = [f for f in existing_files if f['key'] != new_file_key]
            
            # Add new entry at the beginning (most recent first)
            existing_files.insert(0, new_entry)
            
            # Keep only last 50 files to avoid metadata bloat
            existing_files = existing_files[:50]
            
            # Save updated metadata
            metadata = {
                'files': existing_files,
                'last_updated': datetime.now(timezone.utc).isoformat()
            }
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=self.augmented_metadata_key,
                Body=json.dumps(metadata, indent=2).encode('utf-8'),
                ContentType='application/json'
            )
            
            logger.info(f"Updated augmented files metadata: {len(existing_files)} files")
            
        except Exception as e:
            logger.warning(f"Failed to update augmented files metadata: {e}")
            # Don't fail the whole operation if metadata update fails
    
    def load_augmented_csv_from_s3(self, file_key: Optional[str] = None) -> Optional[str]:
        """
        Load augmented CSV content from S3
        
        Args:
            file_key: Specific S3 key to load. If None, loads the most recent file.
        
        Returns:
            CSV content as string, or None if not found
        """
        if not self.s3_client:
            raise ValueError("S3 client not available. Check S3_BUCKET_NAME configuration.")
        
        # If no specific key provided, get the most recent file
        if not file_key:
            file_key = self.get_latest_augmented_file_key()
            if not file_key:
                # Fallback to legacy key
                file_key = self.augmented_cache_key
        
        try:
            logger.info(f"Loading augmented CSV from S3: s3://{self.bucket_name}/{file_key}")
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            
            # Read CSV content
            content = response['Body'].read().decode('utf-8')
            logger.info(f"Loaded augmented CSV from S3 ({len(content)} bytes)")
            return content
                    
        except self.s3_client.exceptions.NoSuchKey:
            logger.info(f"Augmented CSV not found in S3: {file_key}")
            return None
        except self.s3_client.exceptions.ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            error_msg = e.response.get('Error', {}).get('Message', str(e))
            if error_code in ('403', 'Forbidden', 'InvalidAccessKeyId', 'SignatureDoesNotMatch'):
                raise ValueError(f"S3 access denied - check AWS credentials. Error: {error_code} - {error_msg}")
            else:
                logger.error(f"Failed to load augmented CSV from S3: {error_code} - {error_msg}")
                raise
        except Exception as e:
            logger.error(f"Failed to load augmented CSV from S3: {e}")
            raise
    
    def get_latest_augmented_file_key(self) -> Optional[str]:
        """Get the S3 key of the most recent augmented file"""
        try:
            metadata = self.get_augmented_files_metadata()
            if metadata and metadata.get('files'):
                return metadata['files'][0]['key']  # Files are sorted newest first
        except Exception as e:
            logger.warning(f"Failed to get latest file key: {e}")
        return None
    
    def get_augmented_files_metadata(self) -> Optional[Dict]:
        """Get metadata about all available augmented files"""
        if not self.s3_client:
            return None
        
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=self.augmented_metadata_key
            )
            metadata_content = response['Body'].read().decode('utf-8')
            return json.loads(metadata_content)
        except self.s3_client.exceptions.NoSuchKey:
            return None
        except Exception as e:
            logger.warning(f"Failed to load augmented files metadata: {e}")
            return None
    
    def list_raw_files(self) -> List[Dict]:
        """List all raw CSV files in S3 cache"""
        if not self.s3_client:
            return []
        
        try:
            # List objects with the cache key prefix (survicate-cache/)
            prefix = 'survicate-cache/'
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            raw_files = []
            augmented_keys = set()
            
            # Get list of augmented file keys for comparison
            augmented_metadata = self.get_augmented_files_metadata()
            if augmented_metadata and augmented_metadata.get('files'):
                augmented_keys = {f['key'] for f in augmented_metadata['files']}
            
            if 'Contents' in response:
                for obj in response['Contents']:
                    key = obj['Key']
                    # Only include CSV files that are raw (not augmented, not metadata)
                    if (key.endswith('.csv') and 
                        'augmented' not in key and 
                        key != self.augmented_cache_key and  # Exclude legacy augmented key
                        not key.endswith('_meta.json')):
                        
                        # Get file info
                        try:
                            # Count rows (approximate - read first chunk)
                            try:
                                get_response = self.s3_client.get_object(
                                    Bucket=self.bucket_name,
                                    Key=key,
                                    Range='bytes=0-50000'  # Read first 50KB to count headers and some rows
                                )
                                content_preview = get_response['Body'].read().decode('utf-8')
                                # Count lines (subtract 1 for header)
                                lines = content_preview.strip().split('\n')
                                line_count = max(0, len(lines) - 1)
                            except:
                                line_count = 0
                            
                            last_modified = obj.get('LastModified')
                            if hasattr(last_modified, 'isoformat'):
                                last_modified_str = last_modified.isoformat()
                            else:
                                last_modified_str = str(last_modified) if last_modified else datetime.now(timezone.utc).isoformat()
                            
                            raw_files.append({
                                'key': key,
                                'display_name': key.split('/')[-1],
                                'file_size': obj.get('Size', 0),
                                'last_modified': last_modified_str,
                                'response_count': line_count,
                                'has_augmentation': len(augmented_keys) > 0  # For now, just check if any augmented files exist
                            })
                        except Exception as e:
                            logger.warning(f"Failed to get info for {key}: {e}")
            
            # Sort by last modified (newest first)
            raw_files.sort(key=lambda x: x['last_modified'], reverse=True)
            return raw_files
            
        except Exception as e:
            logger.error(f"Failed to list raw files: {e}")
            return []
    
    def check_if_raw_file_has_augmentation(self, raw_file_key: str) -> Optional[str]:
        """Check if a raw file has a corresponding augmented file"""
        if not self.s3_client:
            return None
        
        try:
            # Get augmented files metadata
            metadata = self.get_augmented_files_metadata()
            if not metadata or not metadata.get('files'):
                return None
            
            # Check if any augmented file corresponds to this raw file
            # We'll match by timestamp (raw file timestamp should match augmented file timestamp)
            # For now, just return the most recent augmented file if it exists
            # In the future, we could add a mapping in metadata
            augmented_files = metadata['files']
            if augmented_files:
                # Return the most recent augmented file key
                return augmented_files[0]['key']
            
            return None
        except Exception as e:
            logger.warning(f"Failed to check augmentation status: {e}")
            return None
    
    def _responses_to_csv(self, responses: List[SurveyResponse]) -> str:
        """Convert SurveyResponse objects to CSV format matching manual export"""
        output = io.StringIO()
        
        # Get all unique question keys
        all_question_keys = set()
        for response in responses:
            all_question_keys.update(response.answers.keys())
        
        question_keys = sorted(all_question_keys, key=lambda k: int(k[1:]) if k[1:].isdigit() else 999)
        
        # Build CSV headers
        headers = [
            'Date & Time (UTC)',
            'Response uuid',
            'Respondent uuid',
            'Device',
            'Platform',
            'Page',
            'email',
            'first_name',
            'last_name',
            'user_id',
            'braze_id',
            'sso_id'
        ]
        
        # Add question columns (Answer and Comment for each)
        for q_key in question_keys:
            headers.append(f'{q_key} (Answer)')
            headers.append(f'{q_key} (Comment)')
        
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        
        # Write rows
        for response in responses:
            row = {
                'Date & Time (UTC)': response.date_time,
                'Response uuid': response.response_uuid,
                'Respondent uuid': response.respondent_uuid,
                'Device': response.metadata.get('device', ''),
                'Platform': response.metadata.get('platform', ''),
                'Page': response.metadata.get('page', ''),
                'email': response.email or '',
                'first_name': response.first_name or '',
                'last_name': response.last_name or '',
                'user_id': response.user_id or '',
                'braze_id': response.metadata.get('braze_id', ''),
                'sso_id': response.metadata.get('sso_id', ''),
            }
            
            # Add question answers
            for q_key in question_keys:
                answer_data = response.answers.get(q_key, {})
                if isinstance(answer_data, dict):
                    row[f'{q_key} (Answer)'] = answer_data.get('Answer', '') or ''
                    row[f'{q_key} (Comment)'] = answer_data.get('Comment', '') or ''
                else:
                    row[f'{q_key} (Answer)'] = str(answer_data) if answer_data else ''
                    row[f'{q_key} (Comment)'] = ''
            
            writer.writerow(row)
        
        return output.getvalue()
    
    def update_metadata(self, fetch_time: datetime, status: str):
        """Update cache metadata in S3"""
        if not self.s3_client:
            return
        
        try:
            metadata = {
                'last_fetch': fetch_time.isoformat(),
                'status': status,
                'fetch_time_utc': fetch_time.strftime('%Y-%m-%d %H:%M:%S UTC')
            }
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=self.metadata_key,
                Body=json.dumps(metadata, indent=2).encode('utf-8'),
                ContentType='application/json'
            )
            
            logger.debug(f"Updated cache metadata: {status}")
        except Exception as e:
            logger.warning(f"Failed to update cache metadata: {e}")
    
    def get_metadata(self) -> Optional[Dict[str, Any]]:
        """Get cache metadata from S3"""
        if not self.s3_client:
            return None
        
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=self.metadata_key
            )
            content = response['Body'].read().decode('utf-8')
            return json.loads(content)
        except self.s3_client.exceptions.NoSuchKey:
            return None
        except Exception as e:
            logger.warning(f"Failed to load cache metadata: {e}")
            return None
    
    def get_cache_status(self) -> Dict[str, Any]:
        """Get comprehensive cache status"""
        if not self.s3_client:
            return {
                'cache_exists': False,
                's3_available': False,
                'error': 'S3 client not available'
            }
        
        last_modified = self.get_last_modified()
        cache_age = self.get_cache_age()
        metadata = self.get_metadata()
        
        cache_age_hours = cache_age.total_seconds() / 3600 if cache_age else None
        
        return {
            'cache_exists': last_modified is not None,
            's3_available': True,
            'is_fresh': self.is_cache_fresh() if last_modified else False,
            'last_modified': last_modified.isoformat() if last_modified else None,
            'cache_age_hours': round(cache_age_hours, 2) if cache_age_hours else None,
            'max_age_hours': self.max_age_hours,
            'metadata': metadata,
            'cache_key': self.cache_key
        }

