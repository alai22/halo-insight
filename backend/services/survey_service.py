"""
Survey data service
"""

import threading
from datetime import datetime
from typing import List, Dict, Optional, Any
from ..utils.config import Config
from ..utils.logging import get_logger
from ..models.survey import SurveyResponse, SurveySummary
from .survey_parser_service import SurveyParserService

logger = get_logger('survey_service')

# Global API refresh state
api_refresh_state = {
    'is_running': False,
    'last_fetch': None,
    'error': None
}


class SurveyService:
    """Service for managing survey data"""
    
    def __init__(self, csv_path: Optional[str] = None):
        """Initialize survey service"""
        self.csv_path = csv_path or Config.SURVICATE_CSV_PATH
        self.surveys: List[SurveyResponse] = []
        self.load_surveys()
    
    def load_surveys(self, data_source: Optional[str] = None):
        """
        Load surveys from specified source
        
        Args:
            data_source: 'file' (CSV file) or 'api' (S3 cached API data)
        """
        source = data_source or 'file'
        
        if source == 'api':
            self.load_from_api()
        else:
            self.load_from_file()
    
    def load_from_file(self, csv_path: Optional[str] = None):
        """Load surveys from CSV file"""
        path = csv_path or self.csv_path
        try:
            parser = SurveyParserService(path)
            self.surveys = parser.parse_csv()
            logger.info(f"Surveys loaded from file: {len(self.surveys)}")
        except Exception as e:
            logger.error(f"Failed to load surveys from file: {str(e)}")
            self.surveys = []
    
    def load_from_api(self):
        """Load surveys from S3 cache (API mode)"""
        try:
            from .survicate_s3_cache_service import SurvicateS3CacheService
            
            cache_service = SurvicateS3CacheService()
            
            # Check if S3 is available
            if not cache_service.s3_client:
                logger.warning("S3 client not available, falling back to file mode")
                self.load_from_file()
                return
            
            # Check if cache is fresh
            if cache_service.is_cache_fresh():
                logger.info("Cache is fresh, loading from S3")
                try:
                    self.surveys = cache_service.load_from_s3()
                    logger.info(f"Surveys loaded from S3 cache: {len(self.surveys)}")
                except ValueError as e:
                    # S3 credential error - fallback to file
                    logger.warning(f"S3 access error: {e}. Falling back to file mode.")
                    self.load_from_file()
            else:
                # Cache is stale or missing
                logger.info("Cache is stale or missing")
                
                # Try to load from cache anyway (might be stale but usable)
                try:
                    self.surveys = cache_service.load_from_s3()
                    logger.info(f"Loaded stale cache: {len(self.surveys)} responses")
                except ValueError as e:
                    # S3 credential error - fallback to file
                    logger.warning(f"Could not load stale cache (S3 access error): {e}. Falling back to file mode.")
                    self.load_from_file()
                except Exception as e:
                    logger.warning(f"Could not load stale cache: {e}. Falling back to file mode.")
                    self.load_from_file()
                
                # Trigger background refresh (non-blocking) if S3 is available
                if cache_service.s3_client:
                    self._trigger_background_refresh()
        except Exception as e:
            logger.error(f"Failed to load from API cache: {e}")
            # Fallback to file
            self.load_from_file()
    
    def _trigger_background_refresh(self):
        """Trigger background refresh of API cache"""
        global api_refresh_state
        
        # Don't start if already running
        if api_refresh_state['is_running']:
            logger.info("API refresh already in progress")
            return
        
        try:
            # Start background thread
            refresh_thread = threading.Thread(
                target=self._refresh_api_cache,
                daemon=True
            )
            refresh_thread.start()
            logger.info("Started background API cache refresh")
        except Exception as e:
            logger.error(f"Failed to start background refresh: {e}")
    
    def _refresh_api_cache(self):
        """Background thread to fetch from API and save to S3"""
        global api_refresh_state
        
        api_refresh_state['is_running'] = True
        api_refresh_state['error'] = None
        
        try:
            from .survicate_api_client import SurvicateAPIClient
            from .survicate_api_parser import SurvicateAPIParser
            from .survicate_s3_cache_service import SurvicateS3CacheService
            
            logger.info("Starting API cache refresh")
            
            # Check if API key is configured
            if not Config.SURVICATE_API_KEY:
                error_msg = "SURVICATE_API_KEY not configured"
                logger.error(error_msg)
                api_refresh_state['error'] = error_msg
                return
            
            # Log configuration for debugging
            import os
            logger.info(f"API refresh - API key set: {bool(Config.SURVICATE_API_KEY)}, Workspace key set: {bool(Config.SURVICATE_WORKSPACE_KEY)}")
            logger.info(f"API refresh - Survey ID: {Config.SURVICATE_SURVEY_ID}, Base URL: {Config.SURVICATE_API_BASE_URL}")
            
            # Initialize services
            logger.info("Initializing SurvicateAPIClient...")
            api_client = SurvicateAPIClient()
            logger.info("SurvicateAPIClient initialized successfully")
            parser = SurvicateAPIParser()
            cache_service = SurvicateS3CacheService()
            
            # Check if S3 is available
            if not cache_service.s3_client:
                error_msg = "S3 client not available. Check AWS credentials and S3_BUCKET_NAME configuration."
                logger.error(error_msg)
                api_refresh_state['error'] = error_msg
                return
            
            # Fetch all responses from API
            logger.info(f"Fetching responses from Survicate API for survey {Config.SURVICATE_SURVEY_ID}...")
            api_responses = api_client.get_all_responses(
                survey_id=Config.SURVICATE_SURVEY_ID
            )
            logger.info(f"Successfully fetched {len(api_responses)} responses from API")
            
            # Parse responses
            survey_responses = parser.parse_responses(api_responses)
            
            # Save raw CSV to S3
            try:
                cache_service.save_to_s3(survey_responses)
                logger.info(f"Raw CSV saved to S3: {len(survey_responses)} responses")
            except Exception as s3_error:
                error_msg = f"Failed to save raw CSV to S3: {s3_error}"
                logger.error(error_msg)
                api_refresh_state['error'] = error_msg
                return
            
            # Augment the data and save augmented CSV to S3
            try:
                logger.info("Starting augmentation process...")
                self._augment_and_save_to_s3(cache_service, survey_responses)
                logger.info("Augmentation completed successfully")
            except Exception as aug_error:
                error_msg = f"Failed to augment data: {aug_error}"
                logger.error(error_msg, exc_info=True)
                # Don't fail the whole refresh if augmentation fails - raw data is still saved
                api_refresh_state['error'] = error_msg
            
            api_refresh_state['last_fetch'] = datetime.now().isoformat()
            logger.info(f"API cache refresh completed: {len(survey_responses)} responses")
            
        except ValueError as e:
            # API authentication/authorization error
            error_msg = str(e)
            
            # Add diagnostic info
            import os
            api_key_env = bool(os.getenv('SURVICATE_API_KEY'))
            workspace_key_env = bool(os.getenv('SURVICATE_WORKSPACE_KEY'))
            api_key_config = bool(Config.SURVICATE_API_KEY)
            workspace_key_config = bool(Config.SURVICATE_WORKSPACE_KEY)
            
            diagnostic_info = f" (API key in env: {api_key_env}, in config: {api_key_config}, Workspace key in env: {workspace_key_env}, in config: {workspace_key_config})"
            error_msg_with_diagnostics = error_msg + diagnostic_info
            
            logger.error(f"API cache refresh failed: {error_msg_with_diagnostics}")
            api_refresh_state['error'] = error_msg_with_diagnostics
            api_refresh_state['diagnostics'] = {
                'api_key_in_env': api_key_env,
                'workspace_key_in_env': workspace_key_env,
                'api_key_in_config': api_key_config,
                'workspace_key_in_config': workspace_key_config
            }
        except Exception as e:
            logger.error(f"API cache refresh failed: {e}", exc_info=True)
            
            # Add diagnostic info for any error
            import os
            api_key_env = bool(os.getenv('SURVICATE_API_KEY'))
            workspace_key_env = bool(os.getenv('SURVICATE_WORKSPACE_KEY'))
            api_key_config = bool(Config.SURVICATE_API_KEY)
            workspace_key_config = bool(Config.SURVICATE_WORKSPACE_KEY)
            
            error_msg = str(e)
            diagnostic_info = f" (API key in env: {api_key_env}, in config: {api_key_config}, Workspace key in env: {workspace_key_env}, in config: {workspace_key_config})"
            
            api_refresh_state['error'] = error_msg + diagnostic_info
            api_refresh_state['diagnostics'] = {
                'api_key_in_env': api_key_env,
                'workspace_key_in_env': workspace_key_env,
                'api_key_in_config': api_key_config,
                'workspace_key_in_config': workspace_key_config
            }
        finally:
            api_refresh_state['is_running'] = False
    
    def _augment_and_save_to_s3(self, cache_service, survey_responses: List):
        """Augment survey data and save augmented CSV to S3"""
        import tempfile
        import os
        import sys
        
        # Import augmentation function
        # Add project root to path to import augment_churn_reasons
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        try:
            from augment_churn_reasons import augment_csv
            
            # Download raw CSV from S3 to temp file
            logger.info("Downloading raw CSV from S3 for augmentation...")
            raw_csv_content = None
            try:
                response = cache_service.s3_client.get_object(
                    Bucket=cache_service.bucket_name,
                    Key=cache_service.cache_key
                )
                raw_csv_content = response['Body'].read().decode('utf-8')
            except Exception as e:
                logger.error(f"Failed to download raw CSV from S3: {e}")
                raise
            
            # Write to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_input:
                temp_input.write(raw_csv_content)
                temp_input_path = temp_input.name
            
            # Create temp output file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_output:
                temp_output_path = temp_output.name
            
            try:
                # Run augmentation with LLM (does keyword matching first, then LLM for remaining)
                logger.info("Running augmentation with LLM (keyword matching first, then LLM for remaining)...")
                augment_csv(
                    input_path=temp_input_path,
                    output_path=temp_output_path,
                    use_claude=True  # Use LLM for better categorization
                )
                
                # Read augmented CSV
                with open(temp_output_path, 'r', encoding='utf-8') as f:
                    augmented_csv_content = f.read()
                
                # Count responses (number of non-header lines)
                response_count = len(augmented_csv_content.strip().split('\n')) - 1
                
                # Save augmented CSV to S3 with timestamp
                logger.info("Saving augmented CSV to S3 with timestamp...")
                saved_key = cache_service.save_augmented_csv_to_s3(augmented_csv_content, response_count=response_count)
                logger.info(f"Augmented CSV saved to S3 successfully: {saved_key}")
                
            finally:
                # Clean up temp files
                for temp_path in [temp_input_path, temp_output_path]:
                    if os.path.exists(temp_path):
                        try:
                            os.unlink(temp_path)
                        except Exception as e:
                            logger.warning(f"Failed to delete temp file {temp_path}: {e}")
                            
        except ImportError as e:
            logger.error(f"Failed to import augment_churn_reasons: {e}")
            raise ValueError(f"Augmentation script not available: {e}")
        except Exception as e:
            logger.error(f"Augmentation failed: {e}", exc_info=True)
            raise
    
    def _augment_raw_csv_and_save_to_s3(self, cache_service, raw_csv_content: str, source_file_key: str = None):
        """Augment raw CSV content and save augmented CSV to S3 (can be called independently)"""
        import tempfile
        import os
        import sys
        
        # Import augmentation function
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        try:
            from augment_churn_reasons import augment_csv
            
            # Write to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_input:
                temp_input.write(raw_csv_content)
                temp_input_path = temp_input.name
            
            # Create temp output file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_output:
                temp_output_path = temp_output.name
            
            try:
                # Run augmentation with LLM
                logger.info("Running augmentation with LLM (keyword matching first, then LLM for remaining)...")
                augment_csv(
                    input_path=temp_input_path,
                    output_path=temp_output_path,
                    use_claude=True
                )
                
                # Read augmented CSV
                with open(temp_output_path, 'r', encoding='utf-8') as f:
                    augmented_csv_content = f.read()
                
                # Count responses (number of non-header lines)
                response_count = max(0, len(augmented_csv_content.strip().split('\n')) - 1)
                
                # Save augmented CSV to S3 with timestamp
                logger.info("Saving augmented CSV to S3 with timestamp...")
                saved_key = cache_service.save_augmented_csv_to_s3(augmented_csv_content, response_count=response_count)
                logger.info(f"Augmented CSV saved to S3 successfully: {saved_key}")
                
            finally:
                # Clean up temp files
                for temp_path in [temp_input_path, temp_output_path]:
                    if os.path.exists(temp_path):
                        try:
                            os.unlink(temp_path)
                        except Exception as e:
                            logger.warning(f"Failed to delete temp file {temp_path}: {e}")
                            
        except ImportError as e:
            logger.error(f"Failed to import augment_churn_reasons: {e}")
            raise ValueError(f"Augmentation script not available: {e}")
        except Exception as e:
            logger.error(f"Augmentation failed: {e}", exc_info=True)
            raise
    
    def get_summary(self) -> SurveySummary:
        """Get survey data summary"""
        if not self.surveys:
            return SurveySummary(
                total_responses=0,
                date_range={'start': 'Unknown', 'end': 'Unknown'},
                question_stats={},
                response_rate_by_question={}
            )
        
        # Calculate date range
        dates = [s.date_time for s in self.surveys if s.date_time]
        dates.sort()
        date_range = {
            'start': dates[0] if dates else 'Unknown',
            'end': dates[-1] if dates else 'Unknown'
        }
        
        # Calculate question statistics
        question_stats = {}
        question_response_counts = {}
        
        for survey in self.surveys:
            for question_key, answer_data in survey.answers.items():
                if question_key not in question_stats:
                    question_stats[question_key] = {}
                    question_response_counts[question_key] = 0
                
                # Extract answer value
                if isinstance(answer_data, dict):
                    answer_value = answer_data.get('Answer') or answer_data.get('answer') or ''
                    comment_value = answer_data.get('Comment') or answer_data.get('comment') or ''
                    # Use answer if available, otherwise use comment
                    answer_text = answer_value if answer_value else comment_value
                else:
                    answer_text = str(answer_data) if answer_data else ''
                
                if answer_text:
                    question_response_counts[question_key] += 1
                    answer_text = answer_text.strip()
                    if answer_text:
                        question_stats[question_key][answer_text] = question_stats[question_key].get(answer_text, 0) + 1
        
        # Calculate response rates
        total_surveys = len(self.surveys)
        response_rate_by_question = {}
        for question_key, count in question_response_counts.items():
            response_rate_by_question[question_key] = (count / total_surveys * 100) if total_surveys > 0 else 0
        
        return SurveySummary(
            total_responses=total_surveys,
            date_range=date_range,
            question_stats=question_stats,
            response_rate_by_question=response_rate_by_question
        )
    
    def search_surveys(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search surveys for specific content"""
        if not self.surveys:
            return []
        
        query_lower = query.lower()
        results = []
        
        for survey in self.surveys:
            if query_lower in survey.searchable_text:
                results.append(survey.to_dict())
                if len(results) >= limit:
                    break
        
        logger.info(f"Search completed: query={query}, results_count={len(results)}")
        return results
    
    def semantic_search_surveys(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Enhanced semantic search with concept mappings"""
        if not self.surveys:
            logger.warning(f"Semantic search called but no surveys available (total: {len(self.surveys)})")
            return []
        
        query_lower = query.lower()
        scored_results = []
        
        # Define concept mappings for survey-specific terms
        concept_mappings = {
            'cancel': ['cancel', 'cancelled', 'cancellation', 'canceled', 'stopped', 'ended'],
            'reason': ['reason', 'why', 'because', 'due to', 'caused by'],
            'gps': ['gps', 'location', 'pin', 'coordinates', 'position', 'map', 'tracking', 'accuracy'],
            'battery': ['battery', 'charge', 'charging', 'power', 'dead', 'low', 'drain', 'life'],
            'expensive': ['expensive', 'cost', 'price', 'pricing', 'afford', 'value', 'worth'],
            'dog': ['dog', 'pet', 'animal', 'puppy', 'canine'],
            'response': ['response', 'respond', 'feedback', 'reaction', 'react'],
            'training': ['training', 'train', 'learn', 'curriculum', 'teach'],
            'customer_service': ['customer service', 'support', 'help', 'service', 'contact'],
            'containment': ['containment', 'fence', 'boundary', 'correction', 'feedback'],
            'feedback': ['feedback', 'correction', 'static', 'vibration', 'sound'],
        }
        
        # Find related concepts
        related_terms = set()
        for concept, terms in concept_mappings.items():
            if any(term in query_lower for term in terms):
                related_terms.update(terms)
        
        # Add original query terms
        related_terms.update(word.lower() for word in query.split())
        
        query_words = query_lower.split()
        for word in query_words:
            related_terms.add(word)
            if len(word) > 4:
                related_terms.add(word[:4])
        
        items_checked = 0
        items_with_searchable_text = 0
        
        for survey in self.surveys:
            items_checked += 1
            score = 0
            
            searchable = survey.searchable_text
            if searchable:
                items_with_searchable_text += 1
            
            # Calculate relevance score
            for term in related_terms:
                term_lower = term.lower()
                if term_lower and searchable and term_lower in searchable:
                    if term_lower == query_lower:
                        score += 10
                    elif term_lower in concept_mappings.get(query_lower, []):
                        score += 5
                    elif any(term_lower in mapped_term for mapped_term in concept_mappings.values()):
                        score += 2
                    else:
                        score += 1
            
            if score > 0:
                scored_results.append((survey.to_dict(), score))
        
        # Sort by relevance score
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = [item for item, score in scored_results[:limit]]
        
        logger.info(f"Semantic search: query='{query}', checked={items_checked} surveys, "
                   f"with_searchable_text={items_with_searchable_text}, scored={len(scored_results)}, "
                   f"returning={len(results)} results")
        
        return results
    
    def get_surveys_by_date_range(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get surveys within a date range"""
        if not self.surveys:
            return []
        
        from datetime import datetime
        
        results = []
        for survey in self.surveys:
            if not survey.date_time:
                continue
            
            try:
                survey_date = datetime.strptime(survey.date_time, '%Y-%m-%d %H:%M:%S')
                
                if start_date:
                    start = datetime.strptime(start_date, '%Y-%m-%d')
                    if survey_date < start:
                        continue
                
                if end_date:
                    end = datetime.strptime(end_date, '%Y-%m-%d')
                    # Set end to end of day
                    from datetime import timedelta
                    end = end + timedelta(days=1) - timedelta(seconds=1)
                    if survey_date > end:
                        continue
                
                results.append(survey.to_dict())
            except:
                # Skip surveys with invalid dates
                continue
        
        logger.info(f"Retrieved {len(results)} surveys for date range: {start_date} to {end_date}")
        return results
    
    def refresh_surveys(self, data_source: Optional[str] = None):
        """
        Refresh surveys from specified source
        
        Args:
            data_source: 'file' (CSV file) or 'api' (S3 cached API data)
        """
        source = data_source or 'file'
        logger.info(f"Refreshing surveys from {source}")
        self.load_surveys(data_source=source)
        logger.info(f"Surveys refreshed: {len(self.surveys)}")
    
    def is_available(self) -> bool:
        """Check if survey service is available"""
        return len(self.surveys) > 0

