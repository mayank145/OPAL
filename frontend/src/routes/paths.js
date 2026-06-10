/**
 * OPAL browser URL paths (React Router).
 * API calls remain under /api/v1/...
 */

export const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

export function pad2(n) {
  return String(n).padStart(2, '0');
}

/** Today's date in HST as YYYY-MM-DD */
export function todayHST() {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Pacific/Honolulu',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(new Date());
  const y = parts.find((p) => p.type === 'year')?.value;
  const m = parts.find((p) => p.type === 'month')?.value;
  const d = parts.find((p) => p.type === 'day')?.value;
  return `${y}-${m}-${d}`;
}

export function isValidLogDate(s) {
  if (!s || !DATE_RE.test(s)) return false;
  const [y, m, d] = s.split('-').map(Number);
  const dt = new Date(y, m - 1, d);
  return dt.getFullYear() === y && dt.getMonth() === m - 1 && dt.getDate() === d;
}

export const paths = {
  login: '/login',
  home: '/fats',
  fats: '/fats',
  fatsNew: '/fats/new',
  fatsDetail: (idno) => `/fats/${idno}`,
  fatsEdit: (idno) => `/fats/${idno}/edit`,
  fatsFaultLink: (idno) => `/fats/${idno}`,
  summit: '/summit',
  summitToday: () => `/summit/${todayHST()}`,
  summitDay: (date) => `/summit/${date}`,
  summitSearch: '/summit/search',
  summitCalendar: (year, month) => `/summit/calendar/${year}/${month}`,
  summitYear: (year) => `/summit/years/${year}`,
};

/** Parse legacy hash #fault-123 → fault id or null */
export function parseLegacyFaultHash(hash) {
  if (!hash || !hash.startsWith('#fault-')) return null;
  const n = parseInt(hash.replace('#fault-', ''), 10);
  return Number.isNaN(n) ? null : n;
}

/** Infer main nav section from pathname */
export function mainSectionFromPath(pathname) {
  if (pathname.startsWith('/summit/calendar')) return 'wpcalendar';
  if (pathname.startsWith('/summit')) return 'summit';
  if (pathname.startsWith('/fats')) return 'fats';
  return 'fats';
}
