"""
Survicate S3 Cache Service

Manages caching of Survicate API responses in S3
"""

import json
import csv
import io
import os
import boto3
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, timezone
from pathlib import Path
from ..utils.config import Config
from ..utils.logging import get_logger
from ..models.survey import SurveyResponse

logger = get_logger('survicate_s3_cache_service')


class SurvicateS3CacheService:
    """Service for managing Survicate API cache in S3"""
    
    def __init__(self):
        """Initialize S3 cache service (with local file fallback)"""
        self.bucket_name = Config.S3_BUCKET_NAME
        self.cache_key = Config.SURVICATE_S3_CACHE_KEY
        self.augmented_cache_key = Config.SURVICATE_S3_AUGMENTED_CACHE_KEY  # Legacy single file key
        self.augmented_prefix = Config.SURVICATE_S3_AUGMENTED_PREFIX  # Prefix for timestamped files
        self.metadata_key = Config.SURVICATE_S3_METADATA_KEY
        self.augmented_metadata_key = Config.SURVICATE_S3_AUGMENTED_METADATA_KEY
        self.max_age_hours = Config.SURVICATE_CACHE_MAX_AGE_HOURS
        
        # Local file storage configuration
        self.use_local_storage = not self.bucket_name or os.getenv('SURVICATE_USE_LOCAL_STORAGE', '').lower() == 'true'
        if self.use_local_storage:
            # Use data/survicate-cache/ directory for local storage
            project_root = Path(__file__).parent.parent.parent
            self.local_cache_dir = project_root / 'data' / 'survicate-cache'
            self.local_cache_dir.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Using local file storage: {self.local_cache_dir}")
            self.s3_client = None
        else:
            self.local_cache_dir = None
            if not self.bucket_name:
                logger.warning("S3_BUCKET_NAME not configured, S3 cache will not be available")
                self.s3_client = None
            else:
                try:
                    self.s3_client = boto3.client('s3', region_name=Config.S3_REGION)
                except Exception as e:
                    logger.warning(f"Could not initialize S3 client: {e}. Falling back to local storage.")
                    # Fallback to local storage if S3 fails
                    project_root = Path(__file__).parent.parent.parent
                    self.local_cache_dir = project_root / 'data' / 'survicate-cache'
                    self.local_cache_dir.mkdir(parents=True, exist_ok=True)
                    self.use_local_storage = True
                    self.s3_client = None
    
    def is_cache_fresh(self, max_age_hours: Optional[int] = None) -> bool:
        """Check if cache is fresh (less than max_age_hours old)"""
        if self.use_local_storage and not self.local_cache_dir:
            return False
        if not self.use_local_storage and not self.s3_client:
            return False
        
        max_age = max_age_hours or self.max_age_hours
        last_modified = self.get_last_modified()
        
        if not last_modified:
            return False
        
        age = datetime.now(timezone.utc) - last_modified
        return age.total_seconds() < (max_age * 3600)
    
    def get_cache_age(self) -> Optional[timedelta]:
        """Get age of cache as timedelta"""
        if self.use_local_storage and not self.local_cache_dir:
            return None
        if not self.use_local_storage and not self.s3_client:
            return None
        
        last_modified = self.get_last_modified()
        if not last_modified:
            return None
        
        return datetime.now(timezone.utc) - last_modified
    
    def get_last_modified(self) -> Optional[datetime]:
        """Get LastModified time from S3 object metadata or local file"""
        if self.use_local_storage:
            cache_file = self.local_cache_dir / self.cache_key.split('/')[-1]
            if cache_file.exists():
                mtime = cache_file.stat().st_mtime
                return datetime.fromtimestamp(mtime, tz=timezone.utc)
            return None
        
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
        """Load survey responses from S3 cache or local file"""
        if self.use_local_storage:
            cache_file = self.local_cache_dir / self.cache_key.split('/')[-1]
            if not cache_file.exists():
                logger.info(f"Cache file not found locally: {cache_file}")
                return []
            
            logger.info(f"Loading cache from local file: {cache_file}")
            content = cache_file.read_text(encoding='utf-8')
        else:
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
        
        try:
            
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
                    
        except Exception as e:
            logger.error(f"Failed to parse CSV content: {e}")
            raise
    
    def save_to_s3(self, responses: List[SurveyResponse], questions_map: Optional[Dict[int, str]] = None):
        """Save survey responses to S3 cache as CSV (or local file if S3 not available)
        
        Args:
            responses: List of SurveyResponse objects
            questions_map: Optional dict mapping question_id (int) -> question_text (str)
        """
        if not responses:
            logger.warning("No responses to save")
            return
        
        try:
            logger.info(f"Saving {len(responses)} responses to {'local storage' if self.use_local_storage else 'S3 cache'}")
            
            # Convert to CSV format (matching manual export format)
            csv_content = self._responses_to_csv(responses, questions_map)
            
            if self.use_local_storage:
                # Save to local file
                # Preserve directory structure from cache_key (e.g., surveys/{survey_id}/raw_{timestamp}.csv)
                cache_key_parts = self.cache_key.split('/')
                if len(cache_key_parts) > 1:
                    # Create subdirectories to match S3 structure
                    subdir = self.local_cache_dir / '/'.join(cache_key_parts[:-1])
                    subdir.mkdir(parents=True, exist_ok=True)
                    cache_file = subdir / cache_key_parts[-1]
                else:
                    cache_file = self.local_cache_dir / cache_key_parts[-1]
                
                # Safety check: Never overwrite the manual CSV file
                manual_csv_path = Path(Config.SURVICATE_CSV_PATH)
                if cache_file.resolve() == manual_csv_path.resolve():
                    raise ValueError(
                        f"Cannot save API data to manual CSV file location: {manual_csv_path}. "
                        f"API downloads must use a separate location (survicate-cache/)."
                    )
                
                cache_file.write_text(csv_content, encoding='utf-8')
                logger.info(f"Saved to local file: {cache_file}")
            else:
                # Upload to S3
                if not self.s3_client:
                    raise ValueError("S3 client not available")
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
        Save augmented CSV content to S3 with timestamped filename (or local file if S3 not available)
        
        Args:
            csv_content: CSV content to save
            response_count: Number of responses in the CSV
            
        Returns:
            File key/path of the saved file
        """
        if not csv_content:
            logger.warning("No augmented CSV content to save")
            return None
        
        try:
            # Create timestamped filename
            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
            timestamped_key = f"{self.augmented_prefix}augmented_{timestamp}.csv"
            
            if self.use_local_storage:
                # Save to local file
                augmented_dir = self.local_cache_dir / 'augmented'
                augmented_dir.mkdir(parents=True, exist_ok=True)
                filename = f"augmented_{timestamp}.csv"
                file_path = augmented_dir / filename
                file_path.write_text(csv_content, encoding='utf-8')
                logger.info(f"Saved augmented CSV to local file: {file_path}")
                
                # Also save to legacy location (but check it's not the manual CSV)
                legacy_file = self.local_cache_dir / self.augmented_cache_key.split('/')[-1]
                manual_csv_path = Path(Config.SURVICATE_CSV_PATH)
                if legacy_file.resolve() != manual_csv_path.resolve():
                    legacy_file.write_text(csv_content, encoding='utf-8')
                else:
                    logger.warning(f"Skipping legacy location - would overwrite manual CSV: {manual_csv_path}")
                
                # Update metadata
                self._update_augmented_files_metadata(timestamped_key, response_count)
                return timestamped_key
            else:
                if not self.s3_client:
                    raise ValueError("S3 client not available")
                
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
            logger.error(f"Failed to save augmented CSV: {e}")
            raise
    
    def _update_augmented_files_metadata(self, new_file_key: str, response_count: int):
        """Update metadata file with list of all augmented files"""
        try:
            if self.use_local_storage:
                # Update local metadata file
                metadata_file = self.local_cache_dir / self.augmented_metadata_key.split('/')[-1]
                
                # Load existing metadata
                existing_files = []
                if metadata_file.exists():
                    try:
                        metadata_content = metadata_file.read_text(encoding='utf-8')
                        existing_files = json.loads(metadata_content).get('files', [])
                    except Exception as e:
                        logger.warning(f"Failed to load existing metadata: {e}")
                
                # Get file info from local file
                try:
                    filename = new_file_key.split('/')[-1]
                    file_path = self.local_cache_dir / 'augmented' / filename
                    if file_path.exists():
                        file_size = file_path.stat().st_size
                        mtime = file_path.stat().st_mtime
                        last_modified = datetime.fromtimestamp(mtime, tz=timezone.utc)
                    else:
                        file_size = 0
                        last_modified = datetime.now(timezone.utc)
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
                    'last_modified': last_modified.isoformat()
                }
                
                # Remove duplicate if exists
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
                
                metadata_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
                logger.info(f"Updated augmented files metadata: {len(existing_files)} files")
                return
            
            # S3 mode
            if not self.s3_client:
                logger.warning("S3 client not available, skipping metadata update")
                return
            
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
        Load augmented CSV content from S3 or local file
        
        Args:
            file_key: Specific file key to load. If None, loads the most recent file.
        
        Returns:
            CSV content as string, or None if not found
        """
        if self.use_local_storage:
            # Load from local file
            if not file_key or file_key == 'latest':
                # Get most recent augmented file
                augmented_dir = self.local_cache_dir / 'augmented'
                if not augmented_dir.exists():
                    return None
                
                augmented_files = list(augmented_dir.glob('augmented_*.csv'))
                if not augmented_files:
                    # Fallback to legacy location
                    legacy_file = self.local_cache_dir / self.augmented_cache_key.split('/')[-1]
                    if legacy_file.exists():
                        logger.info(f"Loading augmented CSV from local file: {legacy_file}")
                        return legacy_file.read_text(encoding='utf-8')
                    return None
                
                # Get most recent file
                latest_file = max(augmented_files, key=lambda p: p.stat().st_mtime)
                logger.info(f"Loading augmented CSV from local file: {latest_file}")
                return latest_file.read_text(encoding='utf-8')
            else:
                # Load specific file
                filename = file_key.split('/')[-1]
                file_path = self.local_cache_dir / 'augmented' / filename
                if file_path.exists():
                    logger.info(f"Loading augmented CSV from local file: {file_path}")
                    return file_path.read_text(encoding='utf-8')
                return None
        
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
        if self.use_local_storage:
            # Load metadata from local file
            try:
                metadata_file = self.local_cache_dir / self.augmented_metadata_key.split('/')[-1]
                if not metadata_file.exists():
                    # Try to build metadata from existing augmented files
                    return self._build_metadata_from_local_files()
                metadata_content = metadata_file.read_text(encoding='utf-8')
                return json.loads(metadata_content)
            except Exception as e:
                logger.warning(f"Failed to load augmented files metadata from local storage: {e}")
                # Try to build metadata from existing files
                return self._build_metadata_from_local_files()
        
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
            # Metadata file doesn't exist - try to build from existing S3 files
            logger.debug("Augmented metadata file not found, building from existing S3 files")
            return self._build_metadata_from_s3_files()
        except Exception as e:
            logger.warning(f"Failed to load augmented files metadata: {e}")
            # Try to build from existing files as fallback
            return self._build_metadata_from_s3_files()
    
    def _build_metadata_from_local_files(self) -> Optional[Dict]:
        """Build metadata from existing augmented files in local storage"""
        try:
            augmented_dir = self.local_cache_dir / 'augmented'
            if not augmented_dir.exists():
                return None
            
            files = []
            for csv_file in augmented_dir.glob('augmented_*.csv'):
                try:
                    # Count rows
                    content = csv_file.read_text(encoding='utf-8')
                    lines = content.strip().split('\n')
                    response_count = max(0, len(lines) - 1)
                    
                    # Get modification time
                    mtime = csv_file.stat().st_mtime
                    last_modified = datetime.fromtimestamp(mtime, tz=timezone.utc)
                    
                    files.append({
                        'key': csv_file.name,
                        'timestamp': last_modified.isoformat(),
                        'response_count': response_count,
                        'file_size': csv_file.stat().st_size,
                        'last_modified': last_modified.isoformat()
                    })
                except Exception as e:
                    logger.warning(f"Failed to process augmented file {csv_file}: {e}")
            
            # Sort by timestamp (newest first)
            files.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return {'files': files} if files else None
        except Exception as e:
            logger.warning(f"Failed to build metadata from local files: {e}")
            return None
    
    def _build_metadata_from_s3_files(self) -> Optional[Dict]:
        """Build metadata from existing augmented files in S3"""
        if not self.s3_client:
            return None
        
        try:
            # List objects with the augmented prefix
            prefix = self.augmented_prefix
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    key = obj['Key']
                    # Only include CSV files that match augmented pattern
                    if key.endswith('.csv') and 'augmented' in key:
                        try:
                            # Get file info
                            last_modified = obj.get('LastModified')
                            if not last_modified:
                                continue
                            
                            # Try to count rows (read first chunk)
                            try:
                                get_response = self.s3_client.get_object(
                                    Bucket=self.bucket_name,
                                    Key=key,
                                    Range='bytes=0-100000'  # Read first 100KB to count rows
                                )
                                content_preview = get_response['Body'].read().decode('utf-8')
                                lines = content_preview.strip().split('\n')
                                response_count = max(0, len(lines) - 1)
                            except:
                                response_count = 0
                            
                            last_modified_str = last_modified.isoformat() if hasattr(last_modified, 'isoformat') else str(last_modified)
                            
                            files.append({
                                'key': key,
                                'timestamp': last_modified_str,
                                'response_count': response_count,
                                'file_size': obj.get('Size', 0),
                                'last_modified': last_modified_str
                            })
                        except Exception as e:
                            logger.warning(f"Failed to process augmented file {key}: {e}")
            
            # Also check legacy augmented key
            try:
                response = self.s3_client.head_object(
                    Bucket=self.bucket_name,
                    Key=self.augmented_cache_key
                )
                last_modified = response.get('LastModified')
                if last_modified:
                    # Try to count rows
                    try:
                        get_response = self.s3_client.get_object(
                            Bucket=self.bucket_name,
                            Key=self.augmented_cache_key,
                            Range='bytes=0-100000'
                        )
                        content_preview = get_response['Body'].read().decode('utf-8')
                        lines = content_preview.strip().split('\n')
                        response_count = max(0, len(lines) - 1)
                    except:
                        response_count = 0
                    
                    last_modified_str = last_modified.isoformat() if hasattr(last_modified, 'isoformat') else str(last_modified)
                    files.append({
                        'key': self.augmented_cache_key,
                        'timestamp': last_modified_str,
                        'response_count': response_count,
                        'file_size': response.get('ContentLength', 0),
                        'last_modified': last_modified_str
                    })
            except self.s3_client.exceptions.NoSuchKey:
                pass  # Legacy key doesn't exist, that's fine
            except Exception as e:
                logger.debug(f"Failed to check legacy augmented key: {e}")
            
            # Sort by timestamp (newest first)
            files.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return {'files': files} if files else None
        except Exception as e:
            logger.warning(f"Failed to build metadata from S3 files: {e}")
            return None
    
    def list_raw_files(self) -> List[Dict]:
        """List all raw CSV files in S3 cache or local storage"""
        raw_files = []
        augmented_keys = set()
        
        # Get list of augmented file keys for comparison
        augmented_metadata = self.get_augmented_files_metadata()
        if augmented_metadata and augmented_metadata.get('files'):
            augmented_keys = {f['key'] for f in augmented_metadata['files']}
        
        if self.use_local_storage:
            # List files from local storage
            try:
                if not self.local_cache_dir or not self.local_cache_dir.exists():
                    return []
                
                # Find all CSV files in cache directory (excluding augmented subdirectory)
                for csv_file in self.local_cache_dir.glob('*.csv'):
                    # Skip augmented files and metadata
                    if 'augmented' in csv_file.name or csv_file.name.endswith('_meta.json'):
                        continue
                    
                    try:
                        # Count rows (read file)
                        content = csv_file.read_text(encoding='utf-8')
                        lines = content.strip().split('\n')
                        line_count = max(0, len(lines) - 1)
                        
                        # Get file modification time
                        mtime = csv_file.stat().st_mtime
                        last_modified = datetime.fromtimestamp(mtime, tz=timezone.utc)
                        
                        raw_files.append({
                            'key': csv_file.name,
                            'display_name': csv_file.name,
                            'file_size': csv_file.stat().st_size,
                            'last_modified': last_modified.isoformat(),
                            'response_count': line_count,
                            'has_augmentation': len(augmented_keys) > 0
                        })
                    except Exception as e:
                        logger.warning(f"Failed to get info for {csv_file}: {e}")
                
                # Sort by last modified (newest first)
                raw_files.sort(key=lambda x: x['last_modified'], reverse=True)
                return raw_files
                
            except Exception as e:
                logger.error(f"Failed to list raw files from local storage: {e}")
                return []
        
        # S3 mode
        if not self.s3_client:
            return []
        
        try:
            # List objects with the cache key prefix (survicate-cache/)
            prefix = 'survicate-cache/'
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
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
    
    def _responses_to_csv(self, responses: List[SurveyResponse], questions_map: Optional[Dict[int, str]] = None) -> str:
        """Convert SurveyResponse objects to CSV format matching manual export
        
        Args:
            responses: List of SurveyResponse objects
            questions_map: Optional dict mapping question_id (int) -> question_text (str)
        """
        output = io.StringIO()
        
        # Get all unique question IDs from responses
        all_question_ids = set()
        responses_with_answers = 0
        for response in responses:
            if response.answers:
                responses_with_answers += 1
                for q_key in response.answers.keys():
                    # Extract question ID from key (Q#2780078 -> 2780078)
                    q_id_str = q_key.replace('Q#', '').replace('Q', '')
                    try:
                        q_id = int(q_id_str)
                        all_question_ids.add(q_id)
                    except ValueError:
                        pass
        
        # Map question_id to sequential number (Q#1, Q#2, etc.) based on questions_map order
        # The questions_map is ordered by the API response, which reflects survey question order
        question_id_to_seq = {}  # Maps question_id -> sequential number (1, 2, 3...)
        if questions_map:
            # Use questions_map order (API returns questions in survey order)
            # Note: questions_map is a dict, but in Python 3.7+ dicts maintain insertion order
            # The API returns questions in order, so we preserve that order
            sorted_question_ids = list(questions_map.keys())
            for seq_num, q_id in enumerate(sorted_question_ids, start=1):
                question_id_to_seq[q_id] = seq_num
            logger.info(f"Mapped {len(question_id_to_seq)} questions to sequential numbers (Q#1-Q#{len(question_id_to_seq)})")
        else:
            # Fallback: sort by question_id (not ideal, but better than nothing)
            logger.warning("No questions_map provided - using question_id order (may not match survey order)")
            sorted_question_ids = sorted(all_question_ids)
            for seq_num, q_id in enumerate(sorted_question_ids, start=1):
                question_id_to_seq[q_id] = seq_num
        
        # Create mapping from original question_key (Q#2780078) to sequential key (Q#1)
        question_key_mapping = {}  # Maps Q#2780078 -> Q#1
        for q_id in all_question_ids:
            original_key = f"Q#{q_id}"
            seq_num = question_id_to_seq.get(q_id, q_id)  # Fallback to question_id if not in map
            sequential_key = f"Q#{seq_num}"
            question_key_mapping[original_key] = sequential_key
        
        # Get sorted question keys (by sequential number)
        question_keys = sorted(all_question_ids, key=lambda q_id: question_id_to_seq.get(q_id, 999))
        
        # Log warning if no questions found
        if not question_keys:
            logger.warning(f"No question columns found in {len(responses)} responses. Only {responses_with_answers} responses have answers.")
            logger.warning("This CSV cannot be augmented - it needs Q1 Answer columns. Check if API responses contain question/answer data.")
        
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
        # Format: Q#1: <question_text> (Answer) to match manual export format
        for q_id in question_keys:
            # Get sequential number for this question_id
            seq_num = question_id_to_seq.get(q_id, q_id)
            
            # Get question text from map if available
            question_text = questions_map.get(q_id, '') if questions_map else ''
            
            # Format header: Q#1: What was the main reason... (Answer)
            if question_text:
                header_base = f'Q#{seq_num}: {question_text}'
            else:
                # Fallback to just Q#1 if no question text
                header_base = f'Q#{seq_num}'
            
            headers.append(f'{header_base} (Answer)')
            headers.append(f'{header_base} (Comment)')
        
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
            for q_id in question_keys:
                # Get sequential number for this question_id
                seq_num = question_id_to_seq.get(q_id, q_id)
                
                # Get question text from map if available
                question_text = questions_map.get(q_id, '') if questions_map else ''
                
                # Format header key to match header format (Q#1: ...)
                if question_text:
                    header_base = f'Q#{seq_num}: {question_text}'
                else:
                    header_base = f'Q#{seq_num}'
                
                # Get answer data using original question_key (Q#2780078)
                original_key = f'Q#{q_id}'
                answer_data = response.answers.get(original_key, {})
                
                if isinstance(answer_data, dict):
                    row[f'{header_base} (Answer)'] = answer_data.get('Answer', '') or ''
                    row[f'{header_base} (Comment)'] = answer_data.get('Comment', '') or ''
                else:
                    row[f'{header_base} (Answer)'] = str(answer_data) if answer_data else ''
                    row[f'{header_base} (Comment)'] = ''
            
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

