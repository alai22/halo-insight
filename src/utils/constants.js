/**
 * Application-wide constants
 * 
 * NOTE: If you change DEFAULT_SURVICATE_DATA_SOURCE, also update:
 * - backend/utils/config.py: SURVICATE_DEFAULT_DATA_SOURCE
 * These should always match to ensure consistent behavior.
 */

// Default data source for Survicate/Churn analysis
// Options: 'api' (live API data) or 'file' (CSV file)
export const DEFAULT_SURVICATE_DATA_SOURCE = 'api';

/**
 * Get the data source from localStorage or return the default
 * @returns {string} The data source ('api' or 'file')
 */
export const getSurvicateDataSource = () => {
  return localStorage.getItem('survicate_data_source') || DEFAULT_SURVICATE_DATA_SOURCE;
};

