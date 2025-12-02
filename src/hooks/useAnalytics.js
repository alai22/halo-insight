import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

/**
 * React hook for tracking pageviews
 * Automatically tracks route changes and sends events to analytics API
 */
export const useAnalytics = () => {
  const location = useLocation();
  const lastPathRef = useRef(null);
  const timeoutRef = useRef(null);

  useEffect(() => {
    // Debounce to avoid duplicate events on rapid navigation
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Skip if same path (e.g., hash changes)
    const currentPath = location.pathname + location.search;
    if (currentPath === lastPathRef.current) {
      return;
    }

    timeoutRef.current = setTimeout(() => {
      trackPageview(currentPath, document.referrer);
      lastPathRef.current = currentPath;
    }, 100); // 100ms debounce

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [location.pathname, location.search]);
};

/**
 * Track a pageview event
 * @param {string} pagePath - Current page path
 * @param {string} referrer - Referrer URL
 */
const trackPageview = async (pagePath, referrer) => {
  try {
    // Extract query parameters from URL
    const urlParams = new URLSearchParams(window.location.search);
    const queryParams = {};
    urlParams.forEach((value, key) => {
      queryParams[key] = value;
    });

    // Send tracking event to backend
    await axios.post('/api/analytics/track', {
      page_path: pagePath,
      query_params: queryParams,
      referrer: referrer || ''
    }, {
      withCredentials: true
    });
  } catch (error) {
    // Silently fail - don't break the app if analytics fails
    console.debug('Analytics tracking error:', error);
  }
};

export default useAnalytics;

