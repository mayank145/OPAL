/**
 * Parse a datetime string from the backend and format it for HST display
 * The backend stores timestamps in HST (UTC-10)
 * 
 * Since the database stores times in HST format, we need to:
 * 1. Parse the datetime string as if it's HST (by treating it as UTC+10)
 * 2. Display it as HST
 * 
 * @param {string} dateString - ISO datetime string from backend (e.g., "2026-02-04T16:27:17")
 * @returns {string} - Formatted datetime string with HST label
 */
export const formatHSTTimestamp = (dateString) => {
  if (!dateString) return 'N/A';
  
  try {
    // The backend sends timestamps in HST format as bare ISO strings (e.g., "2026-02-04T16:27:17")
    // This represents 4:27 PM HST on Feb 4, 2026
    
    // Strategy to convert HST string to display:
    // 1. Parse as UTC by appending 'Z': creates Date for 4:27 PM UTC
    // 2. Add 10 hours: converts to 2:27 AM UTC (next day), which is the correct UTC equivalent of 4:27 PM HST
    // 3. Format with Pacific/Honolulu timezone: displays as 4:27 PM HST
    
    // Parse the string as UTC
    const utcDate = new Date(dateString + 'Z');
    
    // Add 10 hours to convert from HST representation to correct UTC time
    const correctUTC = new Date(utcDate.getTime() + (10 * 60 * 60 * 1000));
    
    // Format in HST timezone
    return correctUTC.toLocaleString('en-US', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true,
      timeZone: 'Pacific/Honolulu'
    }) + ' HST';
  } catch (e) {
    console.error('Error formatting HST timestamp:', e);
    return dateString;
  }
};

/**
 * Format a date for HST display (for dates without time)
 * @param {string} dateString - Date string from backend
 * @returns {string} - Formatted date string
 */
export const formatHSTDate = (dateString) => {
  if (!dateString) return 'N/A';
  
  try {
    const date = new Date(dateString + 'Z');
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      timeZone: 'Pacific/Honolulu'
    });
  } catch (e) {
    console.error('Error formatting HST date:', e);
    return dateString;
  }
};
