import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  Box, Typography, Paper, IconButton, Button, Tabs, Tab,
  CircularProgress, Alert, Divider, Chip, Table, TableBody,
  TableCell, TableHead, TableRow, TableContainer, TextField,
  Stack, MenuItem, Select, FormControl, InputLabel, Tooltip,
  Dialog, DialogTitle, DialogContent, DialogActions,
} from '@mui/material';
import {
  ChevronLeft, ChevronRight, Today as TodayIcon,
  Edit as EditIcon, Delete as DeleteIcon, Add as AddIcon,
  Save as SaveIcon, Cancel as CancelIcon, ExpandMore, ExpandLess,
} from '@mui/icons-material';
import { summitAPI } from '../services/api';

// ── Constants ────────────────────────────────────────────────────────────────
const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const TYPE_OPTIONS = ['Comment', 'Trouble', 'Summary', 'Warning', 'Important'];
const STATUS_OPTIONS = ['Completed', 'Incompleted', 'Cancelled'];
const CREW_TABS = ['TO', 'IO', 'DC', 'WP', 'ALL', 'TO-IO'];
const CREW_ROLES = ['TO', 'IO', 'DC'];
const SUBSYSTEMS = ['None', 'Dome', 'Telescope', 'Instrument', 'AO', 'Electronics', 'Software', 'Other'];

const TYPE_COLOR = {
  Trouble: 'error', Warning: 'warning', Important: 'secondary',
  Comment: 'default', Summary: 'info',
};
const STATUS_COLOR = {
  Completed: 'success', Incompleted: 'warning', Cancelled: 'error',
};
const ROLE_COLOR = { TO: 'primary', IO: 'success', DC: 'warning' };

// ── Helpers ──────────────────────────────────────────────────────────────────
function padN(n) { return String(n).padStart(2, '0'); }
function fmtDate(y, m, d) { return `${y}-${padN(m)}-${padN(d)}`; }
function parseDate(s) { return s ? String(s).split('T')[0] : ''; }

function formatTimeHST(ts) {
  if (!ts) return '--:--';
  const d = new Date(ts);
  if (Number.isNaN(d.getTime())) return '--:--';
  return d.toLocaleTimeString('en-US', {
    hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Pacific/Honolulu',
  });
}

function formatDateHST(ts) {
  if (!ts) return '—';
  const d = new Date(ts);
  if (Number.isNaN(d.getTime())) return '—';
  return d.toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric', timeZone: 'Pacific/Honolulu',
  });
}

function nowHSThmm() {
  return new Date().toLocaleTimeString('en-US', {
    hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Pacific/Honolulu',
  });
}

function toUtcIso(logDate, hhmm) {
  if (!logDate || !hhmm || !hhmm.includes(':')) return null;
  const [y, m, d] = logDate.split('-').map(Number);
  const [hh, mm] = hhmm.split(':').map(Number);
  if ([y, m, d, hh, mm].some(Number.isNaN)) return null;
  return new Date(Date.UTC(y, m - 1, d, hh + 10, mm)).toISOString();
}

function weatherVal(raw, numeric, suffix = '') {
  if (raw && String(raw).trim()) return String(raw).trim();
  if (numeric != null && numeric !== '') return `${numeric}${suffix}`;
  return 'N/A';
}

// ── Design tokens ────────────────────────────────────────────────────────────
const SUMMIT_GRADIENT = 'linear-gradient(135deg, #004d40 0%, #00695c 60%, #00796b 100%)';
const HEADER_GRADIENT = 'linear-gradient(135deg, #1a237e 0%, #283593 100%)';

const TYPE_BORDER = {
  Trouble: '#f44336', Warning: '#ff9800', Important: '#9c27b0',
  Comment: '#90a4ae', Summary: '#2196f3',
};

// ── Reusable sub-components (module-level, not nested) ───────────────────────

function SectionCard({ title, children, action, accent }) {
  return (
    <Paper elevation={3} sx={{ mb: 2, borderRadius: 2, overflow: 'hidden' }}>
      <Box sx={{
        px: 2, py: 1.25,
        display: 'flex', alignItems: 'center',
        background: accent || 'linear-gradient(90deg, #37474f 0%, #546e7a 100%)',
        color: '#fff',
      }}>
        <Typography variant="subtitle2" fontWeight="bold" sx={{ flex: 1, letterSpacing: 0.3 }}>{title}</Typography>
        {action}
      </Box>
      <Box sx={{ p: 1.75 }}>{children}</Box>
    </Paper>
  );
}

function StatCard({ label, value, color, icon }) {
  return (
    <Paper elevation={2} sx={{
      p: 1.5, borderRadius: 2, flex: 1, minWidth: 110,
      background: `linear-gradient(135deg, ${color}18 0%, ${color}08 100%)`,
      border: `1px solid ${color}30`,
    }}>
      <Stack direction="row" alignItems="center" spacing={1}>
        <Box sx={{ fontSize: 20 }}>{icon}</Box>
        <Box>
          <Typography variant="h6" fontWeight="bold" sx={{ color, lineHeight: 1.1 }}>{value}</Typography>
          <Typography variant="caption" color="text.secondary">{label}</Typography>
        </Box>
      </Stack>
    </Paper>
  );
}

function ItemTypeChip({ type }) {
  if (!type) return null;
  return <Chip size="small" label={type} color={TYPE_COLOR[type] || 'default'} sx={{ fontSize: '0.68rem', height: 20, fontWeight: 600 }} />;
}

function StatusChip({ status }) {
  if (!status) return null;
  return <Chip size="small" label={status} color={STATUS_COLOR[status] || 'default'} variant="outlined" sx={{ fontSize: '0.68rem', height: 20 }} />;
}

function RoleChip({ role }) {
  return <Chip size="small" label={role} color={ROLE_COLOR[role] || 'default'} sx={{ fontSize: '0.68rem', height: 20, fontWeight: 700 }} />;
}

// ── Log Item Editor ──────────────────────────────────────────────────────────
function LogItemEditor({ editor, setEditor, onSave, onCancel, saving, selectedDate }) {
  return (
    <Paper elevation={4} sx={{ mb: 2, borderRadius: 2, overflow: 'hidden',
      border: '1.5px solid', borderColor: 'primary.light',
      boxShadow: '0 4px 20px rgba(25,118,210,0.15)' }}>
      <Box sx={{ px: 2, py: 1.25, background: HEADER_GRADIENT, color: '#fff' }}>
        <Typography variant="subtitle2" fontWeight="bold">
          {editor.itemId ? '✏️ Edit Log Entry' : '✚ New Log Entry'}
        </Typography>
      </Box>
      <Box sx={{ p: 2 }}>
      <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1.5 }} flexWrap="wrap" useFlexGap>
        <FormControl size="small" sx={{ minWidth: 110 }}>
          <InputLabel>Crew Tab</InputLabel>
          <Select value={editor.crewTab} label="Crew Tab"
            onChange={(e) => setEditor((p) => ({ ...p, crewTab: e.target.value }))}>
            {CREW_TABS.map((c) => <MenuItem key={c} value={c}>{c}</MenuItem>)}
          </Select>
        </FormControl>
        <TextField size="small" label="Time HST (HH:MM)" value={editor.itemTime}
          onChange={(e) => setEditor((p) => ({ ...p, itemTime: e.target.value }))}
          inputProps={{ placeholder: 'HH:MM' }} sx={{ maxWidth: 160 }} />
        <FormControl size="small" sx={{ minWidth: 140 }}>
          <InputLabel>Type</InputLabel>
          <Select value={editor.itemType} label="Type"
            onChange={(e) => setEditor((p) => ({ ...p, itemType: e.target.value }))}>
            {TYPE_OPTIONS.map((o) => <MenuItem key={o} value={o}>{o}</MenuItem>)}
          </Select>
        </FormControl>
        <FormControl size="small" sx={{ minWidth: 160 }}>
          <InputLabel>Status</InputLabel>
          <Select value={editor.status} label="Status"
            onChange={(e) => setEditor((p) => ({ ...p, status: e.target.value }))}>
            {STATUS_OPTIONS.map((o) => <MenuItem key={o} value={o}>{o}</MenuItem>)}
          </Select>
        </FormControl>
        <FormControl size="small" sx={{ minWidth: 140 }}>
          <InputLabel>Subsystem</InputLabel>
          <Select value={editor.subsystem} label="Subsystem"
            onChange={(e) => setEditor((p) => ({ ...p, subsystem: e.target.value }))}>
            {SUBSYSTEMS.map((o) => <MenuItem key={o} value={o}>{o}</MenuItem>)}
          </Select>
        </FormControl>
        <TextField size="small" label="Downtime (min)" type="number"
          value={editor.downtimeMinutes}
          onChange={(e) => setEditor((p) => ({ ...p, downtimeMinutes: e.target.value }))}
          sx={{ maxWidth: 140 }} />
        <TextField size="small" label="Created By" value={editor.createdBy}
          onChange={(e) => setEditor((p) => ({ ...p, createdBy: e.target.value }))}
          sx={{ maxWidth: 140 }} />
      </Stack>
      <TextField size="small" fullWidth label="Title" value={editor.title}
        onChange={(e) => setEditor((p) => ({ ...p, title: e.target.value }))} sx={{ mb: 1 }} />
      <TextField size="small" fullWidth multiline minRows={3} label="Body / Description"
        value={editor.body} onChange={(e) => setEditor((p) => ({ ...p, body: e.target.value }))} />
      <Stack direction="row" spacing={1} sx={{ mt: 1.5 }}>
        <Button variant="contained" size="small" startIcon={<SaveIcon />}
          onClick={onSave} disabled={saving}
          sx={{ borderRadius: 2, fontWeight: 600 }}>
          {saving ? 'Saving…' : editor.itemId ? 'Update' : 'Create'}
        </Button>
        <Button variant="outlined" size="small" startIcon={<CancelIcon />} onClick={onCancel}
          sx={{ borderRadius: 2 }}>
          Cancel
        </Button>
      </Stack>
      </Box>
    </Paper>
  );
}

// ── Log Item Row ─────────────────────────────────────────────────────────────
function LogItemRow({ item, onEdit, onDelete }) {
  const [expanded, setExpanded] = useState(false);
  const borderColor = TYPE_BORDER[item.item_type] || '#90a4ae';
  return (
    <Paper elevation={1} sx={{
      mb: 1, borderRadius: 1.5, overflow: 'hidden',
      borderLeft: `4px solid ${borderColor}`,
      transition: 'box-shadow 0.2s, transform 0.1s',
      '&:hover': { boxShadow: 3, transform: 'translateY(-1px)' },
    }}>
      <Box sx={{ px: 1.5, py: 1 }}>
        <Stack direction="row" spacing={1} alignItems="flex-start">
          <Box sx={{ minWidth: 46, textAlign: 'center', pt: 0.25 }}>
            <Typography variant="caption" sx={{ color: 'text.secondary', fontWeight: 600, fontSize: '0.72rem', display: 'block' }}>
              {formatTimeHST(item.item_time)}
            </Typography>
          </Box>
          <Box sx={{ flex: 1 }}>
            <Stack direction="row" spacing={0.5} alignItems="center" flexWrap="wrap" useFlexGap>
              <RoleChip role={item.crew_tab} />
              {item.item_type && <ItemTypeChip type={item.item_type} />}
              {item.status && <StatusChip status={item.status} />}
              {item.downtime_minutes > 0 && (
                <Chip size="small" label={`⬇ ${item.downtime_minutes}min`} color="error" variant="outlined"
                  sx={{ fontSize: '0.67rem', height: 20, fontWeight: 700 }} />
              )}
              {item.created_by && (
                <Typography variant="caption" color="text.secondary" sx={{ ml: 0.5 }}>— {item.created_by}</Typography>
              )}
            </Stack>
            {item.title && (
              <Typography variant="subtitle2" sx={{ mt: 0.3, fontWeight: 600 }}>{item.title}</Typography>
            )}
            {item.body && (
              <Typography variant="body2" color="text.secondary"
                sx={{ whiteSpace: 'pre-wrap', mt: 0.25, display: expanded ? 'block' : '-webkit-box',
                  WebkitLineClamp: expanded ? 'unset' : 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                {item.body}
              </Typography>
            )}
            {item.body && item.body.length > 200 && (
              <Button size="small" sx={{ p: 0, minWidth: 0, fontSize: '0.7rem', mt: 0.25 }}
                endIcon={expanded ? <ExpandLess fontSize="small" /> : <ExpandMore fontSize="small" />}
                onClick={() => setExpanded((v) => !v)}>
                {expanded ? 'Show less' : 'Show more'}
              </Button>
            )}
          </Box>
          <Stack direction="row" spacing={0.25} flexShrink={0}>
            <Tooltip title="Edit">
              <IconButton size="small" onClick={() => onEdit(item)}
                sx={{ '&:hover': { color: 'primary.main', bgcolor: 'primary.50' } }}>
                <EditIcon fontSize="small" />
              </IconButton>
            </Tooltip>
            <Tooltip title="Delete">
              <IconButton size="small" color="error" onClick={() => onDelete(item.id)}>
                <DeleteIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          </Stack>
        </Stack>
      </Box>
    </Paper>
  );
}

// ── Program Form Dialog ──────────────────────────────────────────────────────
function ProgramDialog({ open, onClose, onSave, saving, initial = {} }) {
  const blank = {
    instr: '', alloc: '', pi: '', ao1: '', ao2: '',
    gid: '', propid: '', slotStart: '', slotEnd: '',
    obs1: '', obs1loc: '', obs2: '', obs2loc: '',
    obs3: '', obs3loc: '', obs4: '', obs4loc: '',
    ss: '', ssloc: '', ss2: '', ss2loc: '',
    others1: '', others1loc: '', others2: '', others2loc: '',
    notes: '', comment_text: '',
  };
  const [form, setForm] = useState({ ...blank, ...initial });
  useEffect(() => { setForm({ ...blank, ...initial }); }, [open]); // eslint-disable-line react-hooks/exhaustive-deps
  const f = (key) => ({ size: 'small', value: form[key], onChange: (e) => setForm((p) => ({ ...p, [key]: e.target.value })) });
  const row = (fields) => (
    <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }} flexWrap="wrap" useFlexGap>
      {fields}
    </Stack>
  );
  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>{initial.id ? 'Edit Observation Program' : 'Add Observation Program'}</DialogTitle>
      <DialogContent dividers>
        {row([
          <TextField {...f('instr')} label="Instrument" sx={{ maxWidth: 120 }} />,
          <TextField {...f('alloc')} label="Alloc" sx={{ maxWidth: 100 }} />,
          <TextField {...f('pi')} label="PI" sx={{ flex: 1, minWidth: 140 }} />,
          <TextField {...f('gid')} label="GID" sx={{ maxWidth: 100 }} />,
          <TextField {...f('propid')} label="PropID" sx={{ maxWidth: 130 }} />,
        ])}
        {row([
          <TextField {...f('ao1')} label="AO1" sx={{ maxWidth: 100 }} />,
          <TextField {...f('ao2')} label="AO2" sx={{ maxWidth: 100 }} />,
          <TextField {...f('slotStart')} label="Slot Start HST (HH:MM)" sx={{ maxWidth: 180 }} />,
          <TextField {...f('slotEnd')} label="Slot End HST (HH:MM)" sx={{ maxWidth: 180 }} />,
        ])}
        <Divider sx={{ my: 1 }} />
        {row([
          <TextField {...f('obs1')} label="Observer 1" sx={{ flex: 1, minWidth: 140 }} />,
          <TextField {...f('obs1loc')} label="Loc" sx={{ maxWidth: 80 }} />,
          <TextField {...f('obs2')} label="Observer 2" sx={{ flex: 1, minWidth: 140 }} />,
          <TextField {...f('obs2loc')} label="Loc" sx={{ maxWidth: 80 }} />,
        ])}
        {row([
          <TextField {...f('obs3')} label="Observer 3" sx={{ flex: 1, minWidth: 140 }} />,
          <TextField {...f('obs3loc')} label="Loc" sx={{ maxWidth: 80 }} />,
          <TextField {...f('obs4')} label="Observer 4" sx={{ flex: 1, minWidth: 140 }} />,
          <TextField {...f('obs4loc')} label="Loc" sx={{ maxWidth: 80 }} />,
        ])}
        {row([
          <TextField {...f('ss')} label="SA 1" sx={{ flex: 1, minWidth: 140 }} />,
          <TextField {...f('ssloc')} label="Loc" sx={{ maxWidth: 80 }} />,
          <TextField {...f('ss2')} label="SA 2" sx={{ flex: 1, minWidth: 140 }} />,
          <TextField {...f('ss2loc')} label="Loc" sx={{ maxWidth: 80 }} />,
        ])}
        {row([
          <TextField {...f('others1')} label="Others 1" sx={{ flex: 1, minWidth: 140 }} />,
          <TextField {...f('others1loc')} label="Loc" sx={{ maxWidth: 80 }} />,
          <TextField {...f('others2')} label="Others 2" sx={{ flex: 1, minWidth: 140 }} />,
          <TextField {...f('others2loc')} label="Loc" sx={{ maxWidth: 80 }} />,
        ])}
        <TextField {...f('notes')} label="Notes" multiline minRows={2} fullWidth sx={{ mb: 1 }} />
        <TextField {...f('comment_text')} label="Comment" fullWidth />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} startIcon={<CancelIcon />}>Cancel</Button>
        <Button variant="contained" onClick={() => onSave(form)} disabled={saving} startIcon={<SaveIcon />}>
          {saving ? 'Saving…' : 'Save'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

// ── Work Plan Form Dialog ────────────────────────────────────────────────────
function WorkPlanDialog({ open, onClose, onSave, saving, initial = {} }) {
  const blank = {
    comptitle: '', comptext: '', nite_effect: '', day_effect: '',
    location: '', location2: '', location3: '',
    assigned1: '', assigned2: '', dcassist: '', notify: '',
    contact1: '', contact2: '', others: '', otherreq: '',
    requirements: '', notes: '', windowStart: '', windowEnd: '',
  };
  const [form, setForm] = useState({ ...blank, ...initial });
  useEffect(() => { setForm({ ...blank, ...initial }); }, [open]); // eslint-disable-line react-hooks/exhaustive-deps
  const f = (key) => ({ size: 'small', value: form[key] || '', onChange: (e) => setForm((p) => ({ ...p, [key]: e.target.value })) });
  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>{initial.id ? 'Edit Work Plan' : 'New Work Plan'}</DialogTitle>
      <DialogContent dividers>
        <TextField {...f('comptitle')} label="Title" fullWidth sx={{ mb: 1 }} />
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }}>
          <TextField {...f('windowStart')} label="Start HST (HH:MM)" sx={{ flex: 1 }} />
          <TextField {...f('windowEnd')} label="End HST (HH:MM)" sx={{ flex: 1 }} />
        </Stack>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }}>
          <TextField {...f('nite_effect')} label="Night Effect" sx={{ flex: 1 }} />
          <TextField {...f('day_effect')} label="Day Effect" sx={{ flex: 1 }} />
        </Stack>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }}>
          <TextField {...f('location')} label="Location 1" sx={{ flex: 1 }} />
          <TextField {...f('location2')} label="Location 2" sx={{ flex: 1 }} />
          <TextField {...f('location3')} label="Location 3" sx={{ flex: 1 }} />
        </Stack>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }}>
          <TextField {...f('assigned1')} label="Assigned 1" sx={{ flex: 1 }} />
          <TextField {...f('assigned2')} label="Assigned 2" sx={{ flex: 1 }} />
          <TextField {...f('dcassist')} label="DC Assist" sx={{ flex: 1 }} />
        </Stack>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }}>
          <TextField {...f('notify')} label="Notify" sx={{ flex: 1 }} />
          <TextField {...f('contact1')} label="Contact 1" sx={{ flex: 1 }} />
          <TextField {...f('contact2')} label="Contact 2" sx={{ flex: 1 }} />
        </Stack>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }}>
          <TextField {...f('others')} label="Others" sx={{ flex: 1 }} />
          <TextField {...f('otherreq')} label="Other Req." sx={{ flex: 1 }} />
        </Stack>
        <TextField {...f('comptext')} label="Completion Notes" multiline minRows={2} fullWidth sx={{ mb: 1 }} />
        <TextField {...f('requirements')} label="Requirements" multiline minRows={2} fullWidth sx={{ mb: 1 }} />
        <TextField {...f('notes')} label="Notes" multiline minRows={2} fullWidth />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} startIcon={<CancelIcon />}>Cancel</Button>
        <Button variant="contained" onClick={() => onSave(form)} disabled={saving} startIcon={<SaveIcon />}>
          {saving ? 'Saving…' : 'Save'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

// ── Main Component ────────────────────────────────────────────────────────────
export default function SummitLog({ onError }) {
  const now = new Date();
  const [year, setYear] = useState(now.getFullYear());
  const [month, setMonth] = useState(now.getMonth() + 1);
  const [monthPayload, setMonthPayload] = useState(null);
  const [monthlyLoading, setMonthlyLoading] = useState(false);
  const [monthlyError, setMonthlyError] = useState(null);

  const [selectedDate, setSelectedDate] = useState(null);
  const [dayData, setDayData] = useState(null);
  const [dayLoading, setDayLoading] = useState(false);
  const [dayError, setDayError] = useState(null);

  const [viewTab, setViewTab] = useState('summary');

  // Editor state
  const EMPTY_EDITOR = { itemId: null, crewTab: 'TO', title: '', body: '', itemType: 'Comment',
    status: 'Completed', subsystem: 'None', itemTime: '', downtimeMinutes: '', createdBy: '' };
  const [editor, setEditor] = useState(EMPTY_EDITOR);
  const [editorOpen, setEditorOpen] = useState(false);
  const [editorSaving, setEditorSaving] = useState(false);

  // Day header edit
  const [editingHeader, setEditingHeader] = useState(false);
  const [headerForm, setHeaderForm] = useState({ day_label: '', history_text: '' });
  const [headerSaving, setHeaderSaving] = useState(false);

  // Create day dialog
  const [createDayOpen, setCreateDayOpen] = useState(false);
  const [newDayDate, setNewDayDate] = useState('');
  const [createDaySaving, setCreateDaySaving] = useState(false);

  // Crew edit
  const [crewDialogOpen, setCrewDialogOpen] = useState(false);
  const [crewForm, setCrewForm] = useState({ id: null, role: 'TO', member_name: '', location: '', time_in: '', time_out: '' });
  const [crewSaving, setCrewSaving] = useState(false);

  // Weather edit
  const [weatherEditOpen, setWeatherEditOpen] = useState(false);
  const [weatherForm, setWeatherForm] = useState({ sky: '', seeing: '', temp_raw: '', wind: '', humidity_raw: '', comment_text: '' });
  const [weatherSaving, setWeatherSaving] = useState(false);

  // Program dialog
  const [programDialogOpen, setProgramDialogOpen] = useState(false);
  const [programEditing, setProgramEditing] = useState(null);
  const [programSaving, setProgramSaving] = useState(false);

  // Work plan dialog
  const [wpDialogOpen, setWpDialogOpen] = useState(false);
  const [wpEditing, setWpEditing] = useState(null);
  const [wpSaving, setWpSaving] = useState(false);

  // Search
  const [searchQ, setSearchQ] = useState('');
  const [searchFromDate, setSearchFromDate] = useState('');
  const [searchToDate, setSearchToDate] = useState('');
  const [searchCrew, setSearchCrew] = useState('');
  const [searchResult, setSearchResult] = useState(null);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState(null);
  const [searchOffset, setSearchOffset] = useState(0);
  const SEARCH_LIMIT = 30;

  const notify = useCallback((msg, severity = 'error') => {
    if (onError) onError(msg, severity);
  }, [onError]);

  // ── Data loading ─────────────────────────────────────────────────────────
  const loadMonthly = useCallback(async () => {
    setMonthlyLoading(true); setMonthlyError(null);
    try {
      setMonthPayload(await summitAPI.getMonthly(year, month));
    } catch (e) {
      const msg = e.response?.data?.detail || e.message || 'Failed to load month';
      setMonthlyError(msg); notify(msg);
    } finally { setMonthlyLoading(false); }
  }, [year, month, notify]);

  useEffect(() => { loadMonthly(); }, [loadMonthly]);

  const daysWithLog = useMemo(() => {
    const s = new Set();
    (monthPayload?.days || []).forEach((d) => s.add(parseDate(d.log_date)));
    return s;
  }, [monthPayload]);

  const dayStatsMap = useMemo(() => {
    const m = {};
    (monthPayload?.days || []).forEach((d) => {
      m[parseDate(d.log_date)] = { entry_count: d.entry_count || 0, total_downtime: d.total_downtime || 0 };
    });
    return m;
  }, [monthPayload]);

  useEffect(() => {
    const days = monthPayload?.days || [];
    if (!days.length) return;
    const last = parseDate(days[days.length - 1].log_date);
    if (!selectedDate || !daysWithLog.has(selectedDate)) loadDay(last);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [monthPayload]);

  const loadDay = useCallback(async (logDate) => {
    setSelectedDate(logDate);
    setDayLoading(true); setDayError(null); setDayData(null);
    setEditorOpen(false); setEditor(EMPTY_EDITOR); setEditingHeader(false);
    setProgramEditing(null); setWpEditing(null);
    try {
      setDayData(await summitAPI.getDay(logDate));
    } catch (e) {
      if (e.response?.status === 404) setDayError(`No summit log for ${logDate}`);
      else { const msg = e.response?.data?.detail || e.message; setDayError(msg); notify(msg); }
    } finally { setDayLoading(false); }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ── Calendar navigation ───────────────────────────────────────────────────
  const goPrev = () => { if (month === 1) { setYear(y => y - 1); setMonth(12); } else setMonth(m => m - 1); };
  const goNext = () => { if (month === 12) { setYear(y => y + 1); setMonth(1); } else setMonth(m => m + 1); };
  const goToday = () => {
    const t = new Date();
    setYear(t.getFullYear()); setMonth(t.getMonth() + 1);
    loadDay(fmtDate(t.getFullYear(), t.getMonth() + 1, t.getDate()));
  };

  const daysInMonth = new Date(year, month, 0).getDate();
  const firstWd = new Date(year, month - 1, 1).getDay();
  const calCells = [];
  for (let i = 0; i < firstWd; i++) calCells.push({ key: `p${i}`, empty: true });
  for (let d = 1; d <= daysInMonth; d++) calCells.push({ key: `d${d}`, day: d });

  // ── Day header edit ───────────────────────────────────────────────────────
  const startEditHeader = () => {
    setHeaderForm({ day_label: dayData?.day_label || '', history_text: dayData?.history_text || '' });
    setEditingHeader(true);
  };
  const saveHeader = async () => {
    setHeaderSaving(true);
    try {
      await summitAPI.patchDay(selectedDate, headerForm);
      notify('Day header updated', 'success');
      await loadDay(selectedDate);
      setEditingHeader(false);
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to update'); }
    finally { setHeaderSaving(false); }
  };

  // ── Create new day ────────────────────────────────────────────────────────
  const createDay = async () => {
    if (!newDayDate) return;
    setCreateDaySaving(true);
    try {
      await summitAPI.createDay({ log_date: newDayDate });
      notify('Summit day created', 'success');
      setCreateDayOpen(false); setNewDayDate('');
      await loadMonthly();
      loadDay(newDayDate);
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to create day'); }
    finally { setCreateDaySaving(false); }
  };

  // ── Log item CRUD ────────────────────────────────────────────────────────
  const beginCreate = (crewTab = 'TO') => {
    setEditor({ ...EMPTY_EDITOR, crewTab, itemTime: nowHSThmm() });
    setEditorOpen(true);
  };
  const beginEdit = (item) => {
    setEditor({
      itemId: item.id, crewTab: item.crew_tab || 'ALL',
      title: item.title || '', body: item.body || '',
      itemType: item.item_type || 'Comment', status: item.status || 'Completed',
      subsystem: item.subsystem || 'None',
      itemTime: item.item_time ? formatTimeHST(item.item_time) : '',
      downtimeMinutes: item.downtime_minutes != null ? String(item.downtime_minutes) : '',
      createdBy: item.created_by || '',
    });
    setEditorOpen(true);
  };
  const saveEditor = async () => {
    if (!selectedDate) return;
    if (!editor.title?.trim() && !editor.body?.trim()) { notify('Add a title or body before saving', 'warning'); return; }
    setEditorSaving(true);
    try {
      const payload = {
        crew_tab: editor.crewTab,
        title: editor.title || null,
        body: editor.body || null,
        item_type: editor.itemType || null,
        status: editor.status || null,
        subsystem: editor.subsystem === 'None' ? null : (editor.subsystem || null),
        downtime_minutes: editor.downtimeMinutes ? Number(editor.downtimeMinutes) : null,
        created_by: editor.createdBy || null,
      };
      if (editor.itemTime) {
        const iso = toUtcIso(selectedDate, editor.itemTime);
        if (iso) payload.item_time = iso;
      }
      if (editor.itemId) {
        await summitAPI.updateLogItem(editor.itemId, payload);
        notify('Log item updated', 'success');
      } else {
        await summitAPI.createLogItem(selectedDate, payload);
        notify('Log item created', 'success');
      }
      await loadDay(selectedDate);
      setEditorOpen(false); setEditor(EMPTY_EDITOR);
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to save'); }
    finally { setEditorSaving(false); }
  };
  const deleteItem = async (itemId) => {
    if (!window.confirm('Delete this log entry?')) return;
    try {
      await summitAPI.deleteLogItem(itemId);
      notify('Deleted', 'success');
      await loadDay(selectedDate);
      if (editor.itemId === itemId) { setEditorOpen(false); setEditor(EMPTY_EDITOR); }
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to delete'); }
  };

  // ── Crew CRUD ────────────────────────────────────────────────────────────
  const openAddCrew = () => {
    setCrewForm({ id: null, role: 'TO', member_name: '', location: '', time_in: '', time_out: '' });
    setCrewDialogOpen(true);
  };
  const openEditCrew = (c) => {
    setCrewForm({ id: c.id, role: c.role, member_name: c.member_name || '', location: c.location || '',
      time_in: c.time_in ? formatTimeHST(c.time_in) : '', time_out: c.time_out ? formatTimeHST(c.time_out) : '' });
    setCrewDialogOpen(true);
  };
  const saveCrew = async () => {
    setCrewSaving(true);
    try {
      const payload = {
        role: crewForm.role, member_name: crewForm.member_name || null, location: crewForm.location || null,
        time_in: crewForm.time_in ? toUtcIso(selectedDate, crewForm.time_in) : null,
        time_out: crewForm.time_out ? toUtcIso(selectedDate, crewForm.time_out) : null,
      };
      if (crewForm.id) { await summitAPI.updateCrew(crewForm.id, payload); notify('Crew updated', 'success'); }
      else { await summitAPI.createCrew(selectedDate, payload); notify('Crew added', 'success'); }
      setCrewDialogOpen(false);
      await loadDay(selectedDate);
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to save crew'); }
    finally { setCrewSaving(false); }
  };
  const deleteCrew = async (id) => {
    if (!window.confirm('Remove this crew member?')) return;
    try { await summitAPI.deleteCrew(id); notify('Crew removed', 'success'); await loadDay(selectedDate); }
    catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to delete crew'); }
  };

  // ── Weather CRUD ─────────────────────────────────────────────────────────
  const openWeatherEdit = () => {
    const w = dayData?.weather || {};
    setWeatherForm({ sky: w.sky || '', seeing: w.seeing || '', temp_raw: w.temp_raw || '',
      wind: w.wind || '', humidity_raw: w.humidity_raw || '', comment_text: w.comment_text || '' });
    setWeatherEditOpen(true);
  };
  const saveWeather = async () => {
    setWeatherSaving(true);
    try {
      const payload = {};
      Object.entries(weatherForm).forEach(([k, v]) => { if (v !== '') payload[k] = v || null; });
      await summitAPI.upsertWeather(selectedDate, payload);
      notify('Weather updated', 'success');
      setWeatherEditOpen(false);
      await loadDay(selectedDate);
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to save weather'); }
    finally { setWeatherSaving(false); }
  };

  // ── Program CRUD ──────────────────────────────────────────────────────────
  const openAddProgram = () => { setProgramEditing(null); setProgramDialogOpen(true); };
  const openEditProgram = (p) => {
    setProgramEditing({
      id: p.id, instr: p.instr || '', alloc: p.alloc || '', pi: p.pi || '',
      ao1: p.ao1 || '', ao2: p.ao2 || '', gid: p.gid || '', propid: p.propid || '',
      slotStart: p.slot_start ? formatTimeHST(p.slot_start) : '',
      slotEnd: p.slot_end ? formatTimeHST(p.slot_end) : '',
      obs1: p.obs1 || '', obs1loc: p.obs1loc || '', obs2: p.obs2 || '', obs2loc: p.obs2loc || '',
      obs3: p.obs3 || '', obs3loc: p.obs3loc || '', obs4: p.obs4 || '', obs4loc: p.obs4loc || '',
      ss: p.ss || '', ssloc: p.ssloc || '', ss2: p.ss2 || '', ss2loc: p.ss2loc || '',
      others1: p.others1 || '', others1loc: p.others1loc || '', others2: p.others2 || '', others2loc: p.others2loc || '',
      notes: p.notes || '', comment_text: p.comment_text || '',
    });
    setProgramDialogOpen(true);
  };
  const saveProgram = async (form) => {
    setProgramSaving(true);
    try {
      const nullify = (v) => v || null;
      const payload = {
        instr: nullify(form.instr), alloc: nullify(form.alloc), pi: nullify(form.pi),
        ao1: nullify(form.ao1), ao2: nullify(form.ao2),
        gid: nullify(form.gid), propid: nullify(form.propid),
        slot_start: form.slotStart ? toUtcIso(selectedDate, form.slotStart) : null,
        slot_end: form.slotEnd ? toUtcIso(selectedDate, form.slotEnd) : null,
        obs1: nullify(form.obs1), obs1loc: nullify(form.obs1loc),
        obs2: nullify(form.obs2), obs2loc: nullify(form.obs2loc),
        obs3: nullify(form.obs3), obs3loc: nullify(form.obs3loc),
        obs4: nullify(form.obs4), obs4loc: nullify(form.obs4loc),
        ss: nullify(form.ss), ssloc: nullify(form.ssloc),
        ss2: nullify(form.ss2), ss2loc: nullify(form.ss2loc),
        others1: nullify(form.others1), others1loc: nullify(form.others1loc),
        others2: nullify(form.others2), others2loc: nullify(form.others2loc),
        notes: nullify(form.notes), comment_text: nullify(form.comment_text),
      };
      if (programEditing?.id) { await summitAPI.updateProgram(programEditing.id, payload); notify('Program updated', 'success'); }
      else { await summitAPI.createProgram(selectedDate, payload); notify('Program added', 'success'); }
      setProgramDialogOpen(false); setProgramEditing(null);
      await loadDay(selectedDate);
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to save program'); }
    finally { setProgramSaving(false); }
  };
  const deleteProgram = async (id) => {
    if (!window.confirm('Remove this observation program?')) return;
    try { await summitAPI.deleteProgram(id); notify('Program removed', 'success'); await loadDay(selectedDate); }
    catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to remove program'); }
  };

  // ── Work Plan CRUD ────────────────────────────────────────────────────────
  const openAddWP = () => { setWpEditing(null); setWpDialogOpen(true); };
  const openEditWP = (wp) => {
    setWpEditing({
      id: wp.id, comptitle: wp.comptitle || '', comptext: wp.comptext || '',
      nite_effect: wp.nite_effect || '', day_effect: wp.day_effect || '',
      location: wp.location || '', location2: wp.location2 || '', location3: wp.location3 || '',
      assigned1: wp.assigned1 || '', assigned2: wp.assigned2 || '', dcassist: wp.dcassist || '',
      notify: wp.notify || '', contact1: wp.contact1 || '', contact2: wp.contact2 || '',
      others: wp.others || '', otherreq: wp.otherreq || '',
      requirements: wp.requirements || '', notes: wp.notes || '',
      windowStart: wp.window_start ? formatTimeHST(wp.window_start) : '',
      windowEnd: wp.window_end ? formatTimeHST(wp.window_end) : '',
    });
    setWpDialogOpen(true);
  };
  const saveWP = async (form) => {
    setWpSaving(true);
    try {
      const n = (v) => v || null;
      const payload = {
        comptitle: n(form.comptitle), comptext: n(form.comptext),
        nite_effect: n(form.nite_effect), day_effect: n(form.day_effect),
        location: n(form.location), location2: n(form.location2), location3: n(form.location3),
        assigned1: n(form.assigned1), assigned2: n(form.assigned2), dcassist: n(form.dcassist),
        notify: n(form.notify), contact1: n(form.contact1), contact2: n(form.contact2),
        others: n(form.others), otherreq: n(form.otherreq),
        requirements: n(form.requirements), notes: n(form.notes),
        window_start: form.windowStart ? toUtcIso(selectedDate, form.windowStart) : null,
        window_end: form.windowEnd ? toUtcIso(selectedDate, form.windowEnd) : null,
      };
      if (wpEditing?.id) { await summitAPI.updateWorkPlan(wpEditing.id, payload); notify('Work plan updated', 'success'); }
      else { await summitAPI.createWorkPlan(selectedDate, payload); notify('Work plan created', 'success'); }
      setWpDialogOpen(false); setWpEditing(null);
      await loadDay(selectedDate);
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to save work plan'); }
    finally { setWpSaving(false); }
  };
  const deleteWP = async (id) => {
    if (!window.confirm('Delete this work plan?')) return;
    try { await summitAPI.deleteWorkPlan(id); notify('Work plan deleted', 'success'); await loadDay(selectedDate); }
    catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to delete work plan'); }
  };

  // ── Search ────────────────────────────────────────────────────────────────
  const runSearch = async (offsetOverride = 0) => {
    const q = searchQ.trim();
    if (!q) return;
    setSearchLoading(true); setSearchError(null);
    const off = offsetOverride;
    setSearchOffset(off);
    try {
      const params = { q, limit: SEARCH_LIMIT, offset: off };
      if (searchFromDate) params.from_date = searchFromDate;
      if (searchToDate) params.to_date = searchToDate;
      if (searchCrew) params.crew_tab = searchCrew;
      const data = await summitAPI.search(params);
      setSearchResult(off === 0 ? data : (prev) => ({ total: data.total, items: [...(prev?.items || []), ...data.items] }));
    } catch (e) { const msg = e.response?.data?.detail || e.message || 'Search failed'; setSearchError(msg); notify(msg); }
    finally { setSearchLoading(false); }
  };

  // ── Derived filtered lists ────────────────────────────────────────────────
  const toRows = useMemo(() => (dayData?.log_items || []).filter(i => i.crew_tab === 'TO'), [dayData]);
  const ioRows = useMemo(() => (dayData?.log_items || []).filter(i => i.crew_tab === 'IO'), [dayData]);
  const dcRows = useMemo(() => (dayData?.log_items || []).filter(i => i.crew_tab === 'DC'), [dayData]);
  const wpRows = useMemo(() => (dayData?.log_items || []).filter(i => i.crew_tab === 'WP'), [dayData]);
  const troubleRows = useMemo(() => (dayData?.log_items || []).filter(i => (i.item_type || '').toLowerCase() === 'trouble'), [dayData]);
  const totalDowntime = useMemo(() => (dayData?.log_items || []).reduce((s, i) => s + (i.downtime_minutes || 0), 0), [dayData]);

  // ── Render helpers ────────────────────────────────────────────────────────
  const renderLogList = (rows, defaultCrew) => (
    <>
      {editorOpen && (
        <LogItemEditor editor={editor} setEditor={setEditor} onSave={saveEditor}
          onCancel={() => { setEditorOpen(false); setEditor(EMPTY_EDITOR); }}
          saving={editorSaving} selectedDate={selectedDate} />
      )}
      {!editorOpen && (
        <Button variant="contained" size="small" startIcon={<AddIcon />} sx={{ mb: 1.5, borderRadius: 2, fontWeight: 600 }}
          onClick={() => beginCreate(defaultCrew)}>
          New {defaultCrew} Entry
        </Button>
      )}
      {rows.length === 0 ? (
        <Typography variant="body2" color="text.secondary">No {defaultCrew} entries for this day.</Typography>
      ) : (
        rows.map((item) => (
          <LogItemRow key={item.id} item={item} onEdit={beginEdit} onDelete={deleteItem} />
        ))
      )}
    </>
  );

  // ── JSX ───────────────────────────────────────────────────────────────────
  return (
    <Box>
      {/* ── Hero Header ── */}
      <Paper elevation={4} sx={{
        mb: 2.5, borderRadius: 3, overflow: 'hidden',
        background: SUMMIT_GRADIENT,
      }}>
        <Box sx={{ px: 3, py: 2.5, color: '#fff' }}>
          <Stack direction="row" alignItems="center" justifyContent="space-between">
            <Box>
              <Typography variant="h5" fontWeight={700} sx={{ letterSpacing: 0.5 }}>
                🌙 Summit Log
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8, mt: 0.25 }}>
                Subaru Telescope — Operations Record
              </Typography>
            </Box>
            <Button variant="contained" size="small" startIcon={<AddIcon />}
              onClick={() => setCreateDayOpen(true)}
              sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: '#fff', borderRadius: 2, fontWeight: 600,
                backdropFilter: 'blur(6px)', border: '1px solid rgba(255,255,255,0.3)',
                '&:hover': { bgcolor: 'rgba(255,255,255,0.3)' } }}>
              New Day
            </Button>
          </Stack>
        </Box>
      </Paper>

      {/* ── Calendar ── */}
      <Paper elevation={3} sx={{ mb: 2.5, borderRadius: 2.5, overflow: 'hidden' }}>
        <Box sx={{ px: 2, py: 1.5, background: HEADER_GRADIENT, color: '#fff' }}>
          <Stack direction="row" alignItems="center" spacing={1}>
            <IconButton size="small" onClick={goPrev} sx={{ color: '#fff' }}><ChevronLeft /></IconButton>
            <TextField
              size="small" type="number" value={year}
              onChange={(e) => setYear(Number(e.target.value))}
              sx={{ width: 80, '& .MuiInputBase-root': { color: '#fff', bgcolor: 'rgba(255,255,255,0.15)', borderRadius: 1 },
                '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255,255,255,0.3)' } }}
              inputProps={{ min: 1990, max: 2099 }} />
            <Typography variant="h6" fontWeight={700} sx={{ minWidth: 120, textAlign: 'center' }}>
              {new Date(year, month - 1, 1).toLocaleString(undefined, { month: 'long' })}
            </Typography>
            <IconButton size="small" onClick={goNext} sx={{ color: '#fff' }}><ChevronRight /></IconButton>
            <Button size="small" startIcon={<TodayIcon />} onClick={goToday}
              sx={{ color: '#fff', borderColor: 'rgba(255,255,255,0.5)', border: '1px solid',
                borderRadius: 1.5, fontWeight: 600, ml: 1 }}>
              Today
            </Button>
          </Stack>
        </Box>

        <Box sx={{ p: 1.5 }}>
          {monthlyLoading && <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}><CircularProgress size={26} /></Box>}
          {monthlyError && <Alert severity="error" sx={{ mb: 1 }}>{monthlyError}</Alert>}

          {!monthlyLoading && !monthlyError && (
            <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: 0.5 }}>
              {WEEKDAYS.map((w) => (
                <Box key={w} sx={{ textAlign: 'center', py: 0.75 }}>
                  <Typography variant="caption" sx={{ color: 'text.secondary', fontWeight: 700, fontSize: '0.72rem', letterSpacing: 1 }}>{w}</Typography>
                </Box>
              ))}
              {calCells.map((cell) => {
                if (cell.empty) return <Box key={cell.key} />;
                const logDate = fmtDate(year, month, cell.day);
                const has = daysWithLog.has(logDate);
                const stats = dayStatsMap[logDate];
                const isSel = selectedDate === logDate;
                const hasDowntime = has && stats?.total_downtime > 0;
                return (
                  <Tooltip key={cell.key}
                    title={has ? `${stats?.entry_count || 0} entries · ${stats?.total_downtime || 0} min downtime` : 'No log'}
                    placement="top" arrow>
                    <Box sx={{ textAlign: 'center' }}>
                      <Button fullWidth size="small"
                        onClick={() => loadDay(logDate)}
                        sx={{
                          minWidth: 0, py: 0.5, flexDirection: 'column', lineHeight: 1.1, fontSize: '0.8rem',
                          borderRadius: 1.5, fontWeight: isSel ? 700 : has ? 600 : 400,
                          background: isSel
                            ? 'linear-gradient(135deg, #00695c, #00897b)'
                            : has ? 'rgba(0,105,92,0.08)' : 'transparent',
                          color: isSel ? '#fff' : has ? '#00695c' : 'text.secondary',
                          border: has && !isSel ? '1px solid #00897b55' : isSel ? 'none' : '1px solid transparent',
                          transition: 'all 0.15s',
                          '&:hover': { background: isSel ? 'linear-gradient(135deg,#00796b,#00897b)' : 'rgba(0,105,92,0.14)', transform: 'scale(1.06)' },
                        }}>
                        {cell.day}
                        {hasDowntime && (
                          <Typography component="span" sx={{ fontSize: '0.56rem', color: isSel ? 'rgba(255,255,255,0.85)' : '#e53935', lineHeight: 1, fontWeight: 700 }}>
                            ↓{stats.total_downtime}m
                          </Typography>
                        )}
                      </Button>
                    </Box>
                  </Tooltip>
                );
              })}
            </Box>
          )}
          {!monthlyLoading && !monthlyError && (monthPayload?.days || []).length === 0 && (
            <Alert severity="info" sx={{ mt: 1 }}>No summit logs this month. Navigate or create a new day.</Alert>
          )}
        </Box>
      </Paper>

      {/* ── Day Detail ── */}
      {selectedDate && (
        <Paper elevation={3} sx={{ mb: 2.5, borderRadius: 2.5, overflow: 'hidden' }}>
          {/* Day Hero */}
          <Box sx={{ background: SUMMIT_GRADIENT, color: '#fff', px: 3, py: 2 }}>
            {editingHeader ? (
              <Stack spacing={1.5}>
                <Stack direction="row" spacing={1}>
                  <TextField size="small" label="Day Label" value={headerForm.day_label}
                    onChange={(e) => setHeaderForm(p => ({ ...p, day_label: e.target.value }))}
                    sx={{ maxWidth: 140,
                      '& .MuiInputBase-root': { color: '#fff', bgcolor: 'rgba(255,255,255,0.15)' },
                      '& .MuiInputLabel-root': { color: 'rgba(255,255,255,0.8)' },
                      '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255,255,255,0.4)' } }} />
                  <TextField size="small" fullWidth label="History / Notes" value={headerForm.history_text}
                    onChange={(e) => setHeaderForm(p => ({ ...p, history_text: e.target.value }))}
                    sx={{ '& .MuiInputBase-root': { color: '#fff', bgcolor: 'rgba(255,255,255,0.15)' },
                      '& .MuiInputLabel-root': { color: 'rgba(255,255,255,0.8)' },
                      '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255,255,255,0.4)' } }} />
                </Stack>
                <Stack direction="row" spacing={1}>
                  <Button size="small" variant="contained" startIcon={<SaveIcon />} onClick={saveHeader} disabled={headerSaving}
                    sx={{ bgcolor: 'rgba(255,255,255,0.25)', '&:hover': { bgcolor: 'rgba(255,255,255,0.35)' } }}>
                    {headerSaving ? 'Saving…' : 'Save'}
                  </Button>
                  <Button size="small" variant="outlined" startIcon={<CancelIcon />} onClick={() => setEditingHeader(false)}
                    sx={{ color: '#fff', borderColor: 'rgba(255,255,255,0.5)' }}>Cancel</Button>
                </Stack>
              </Stack>
            ) : (
              <Stack direction="row" alignItems="center" spacing={1.5}>
                <Box sx={{ flex: 1 }}>
                  <Stack direction="row" alignItems="center" spacing={1} flexWrap="wrap">
                    <Typography variant="h6" fontWeight={700}>{selectedDate}</Typography>
                    {dayData?.day_label && (
                      <Chip size="small" label={dayData.day_label}
                        sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: '#fff', fontWeight: 700 }} />
                    )}
                  </Stack>
                  {dayData?.history_text && (
                    <Typography variant="body2" sx={{ opacity: 0.85, mt: 0.25 }}>{dayData.history_text}</Typography>
                  )}
                  {dayData && (
                    <Stack direction="row" spacing={1} sx={{ mt: 1 }} flexWrap="wrap" useFlexGap>
                      <StatCard label="Entries" value={dayData.entry_count ?? (dayData.log_items?.length ?? 0)} color="#4caf50" icon="📋" />
                      {totalDowntime > 0 && <StatCard label="Downtime" value={`${totalDowntime}m`} color="#ef5350" icon="⬇" />}
                      <StatCard label="Crew" value={(dayData.crew_assignments || []).length} color="#42a5f5" icon="👥" />
                      {(dayData.programs || []).length > 0 && <StatCard label="Programs" value={(dayData.programs || []).length} color="#ab47bc" icon="🔭" />}
                    </Stack>
                  )}
                </Box>
                {dayData && !dayLoading && (
                  <Tooltip title="Edit day header">
                    <IconButton size="small" onClick={startEditHeader}
                      sx={{ color: 'rgba(255,255,255,0.85)', bgcolor: 'rgba(255,255,255,0.15)',
                        '&:hover': { bgcolor: 'rgba(255,255,255,0.25)' } }}>
                      <EditIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                )}
              </Stack>
            )}
          </Box>

          {/* Loading / error */}
          {dayLoading && <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}><CircularProgress size={28} /></Box>}
          {dayError && !dayLoading && <Alert severity="warning" sx={{ m: 2 }}>{dayError}</Alert>}

          {!dayLoading && dayData && (
            <Box sx={{ px: 0 }}>
              <Tabs value={viewTab} onChange={(_, v) => setViewTab(v)} variant="scrollable" scrollButtons="auto"
                sx={{ borderBottom: '1px solid', borderColor: 'divider', px: 1,
                  '& .MuiTab-root': { fontWeight: 600, fontSize: '0.82rem', minHeight: 44, textTransform: 'none' },
                  '& .Mui-selected': { color: '#00695c' },
                  '& .MuiTabs-indicator': { backgroundColor: '#00695c', height: 3, borderRadius: '3px 3px 0 0' } }}>
                <Tab value="summary" label="Summary" />
                <Tab value="toio" label="TO / IO" />
                <Tab value="daycrew" label="Day Crew" />
                <Tab value="workplan" label="Work Plan" />
                <Tab value="crew" label="Crew & Weather" />
                <Tab value="programs" label="Programs" />
                <Tab value="trouble" label="Trouble" />
              </Tabs>
              <Box sx={{ p: 2 }}>

              {/* ── Summary Tab ── */}
              {viewTab === 'summary' && (
                <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '3fr 2fr' }, gap: 2 }}>
                  <Box>
                    {editorOpen && (
                      <LogItemEditor editor={editor} setEditor={setEditor} onSave={saveEditor}
                        onCancel={() => { setEditorOpen(false); setEditor(EMPTY_EDITOR); }}
                        saving={editorSaving} selectedDate={selectedDate} />
                    )}
                    {!editorOpen && (
                      <Button variant="contained" size="small" startIcon={<AddIcon />} sx={{ mb: 1.5, borderRadius: 2, fontWeight: 600 }}
                        onClick={() => beginCreate('TO')}>New Entry</Button>
                    )}
                    <SectionCard title={`All Log Entries (${dayData.log_items.length})`} accent={SUMMIT_GRADIENT}>
                      {dayData.log_items.length === 0
                        ? <Typography variant="body2" color="text.secondary">No entries yet.</Typography>
                        : dayData.log_items.map((item) => <LogItemRow key={item.id} item={item} onEdit={beginEdit} onDelete={deleteItem} />)
                      }
                    </SectionCard>
                  </Box>
                  <Stack spacing={2}>
                    {/* Crew summary */}
                    <SectionCard title="👥 Crew" accent="linear-gradient(90deg,#1565c0,#1976d2)">
                      <TableContainer><Table size="small">
                        <TableHead>
                          <TableRow>
                            <TableCell>Role</TableCell><TableCell>Name</TableCell>
                            <TableCell>Location</TableCell><TableCell>In/Out</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {(dayData.crew_assignments || []).map((c) => (
                            <TableRow key={c.id}>
                              <TableCell><RoleChip role={c.role} /></TableCell>
                              <TableCell>{c.member_name || '—'}</TableCell>
                              <TableCell>{c.location || '—'}</TableCell>
                              <TableCell sx={{ fontSize: '0.75rem', whiteSpace: 'nowrap' }}>
                                {formatTimeHST(c.time_in)} – {formatTimeHST(c.time_out)}
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table></TableContainer>
                    </SectionCard>
                    {/* Weather summary */}
                    <SectionCard title="🌤 Weather" accent="linear-gradient(90deg,#00838f,#0097a7)">
                      {dayData.weather ? (
                        <Stack direction="row" flexWrap="wrap" gap={0.75}>
                          {[
                            ['☁ Sky', dayData.weather.sky],
                            ['👁 Seeing', dayData.weather.seeing],
                            ['🌡 Temp', weatherVal(dayData.weather.temp_raw, dayData.weather.temp_c, '°C')],
                            ['💨 Wind', dayData.weather.wind],
                            ['💧 Humid', weatherVal(dayData.weather.humidity_raw, dayData.weather.humidity_pct, '%')],
                          ].map(([label, val]) => (
                            <Chip key={label} size="small" label={`${label}: ${val || 'N/A'}`}
                              sx={{ bgcolor: '#e0f7fa', color: '#006064', fontWeight: 600, fontSize: '0.72rem' }} />
                          ))}
                          {dayData.weather.comment_text && (
                            <Typography variant="caption" color="text.secondary" sx={{ width: '100%', mt: 0.5 }}>
                              {dayData.weather.comment_text}
                            </Typography>
                          )}
                        </Stack>
                      ) : <Typography variant="body2" color="text.secondary">No weather data.</Typography>}
                    </SectionCard>
                    {/* Email status */}
                    {dayData.email_delivery && (
                      <SectionCard title="✉ Email Status" accent="linear-gradient(90deg,#4527a0,#5e35b1)">
                        <Stack spacing={0.5}>
                          {[
                            ['Night', dayData.email_delivery.mailed, dayData.email_delivery.mailtime],
                            ['Smoka', dayData.email_delivery.mailsmoka, dayData.email_delivery.smokatime],
                            ['Day', dayData.email_delivery.mailday, dayData.email_delivery.maildtime],
                          ].map(([label, flag, ts]) => (
                            <Stack key={label} direction="row" spacing={1} alignItems="center">
                              <Typography variant="caption" sx={{ minWidth: 40 }}>{label}</Typography>
                              <Chip size="small" label={flag === 'Y' ? 'Sent' : 'Not Sent'}
                                color={flag === 'Y' ? 'success' : 'default'} variant="outlined" />
                              {flag === 'Y' && ts && (
                                <Typography variant="caption" color="text.secondary">{formatDateHST(ts)}</Typography>
                              )}
                            </Stack>
                          ))}
                        </Stack>
                      </SectionCard>
                    )}
                  </Stack>
                </Box>
              )}

              {/* ── TO / IO Tab ── */}
              {viewTab === 'toio' && (
                <Box>
                  {editorOpen && (
                    <LogItemEditor editor={editor} setEditor={setEditor} onSave={saveEditor}
                      onCancel={() => { setEditorOpen(false); setEditor(EMPTY_EDITOR); }}
                      saving={editorSaving} selectedDate={selectedDate} />
                  )}
                  <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 2 }}>
                    <SectionCard title="🔭 Telescope Operator (TO)" accent="linear-gradient(90deg,#1565c0,#1976d2)" action={
                      !editorOpen && <Button size="small" startIcon={<AddIcon />} onClick={() => beginCreate('TO')} sx={{ color: '#fff' }}>Add TO</Button>
                    }>{renderLogList(toRows, 'TO')}</SectionCard>
                    <SectionCard title="🎯 Instrument Operator (IO)" accent="linear-gradient(90deg,#2e7d32,#388e3c)" action={
                      !editorOpen && <Button size="small" startIcon={<AddIcon />} onClick={() => beginCreate('IO')} sx={{ color: '#fff' }}>Add IO</Button>
                    }>{renderLogList(ioRows, 'IO')}</SectionCard>
                  </Box>
                </Box>
              )}

              {/* ── Day Crew Tab ── */}
              {viewTab === 'daycrew' && (
                <SectionCard title="🧑‍🔬 Day Crew (DC)" accent="linear-gradient(90deg,#e65100,#f57c00)" action={
                  !editorOpen && <Button size="small" startIcon={<AddIcon />} onClick={() => beginCreate('DC')} sx={{ color: '#fff' }}>Add DC</Button>
                }>{renderLogList(dcRows, 'DC')}</SectionCard>
              )}

              {/* ── Work Plan Tab ── */}
              {viewTab === 'workplan' && (
                <Box>
                  <SectionCard title="📋 Work Plans" accent="linear-gradient(90deg,#6a1b9a,#7b1fa2)" action={
                    <Button size="small" startIcon={<AddIcon />} onClick={openAddWP} sx={{ color: '#fff' }}>New Work Plan</Button>
                  }>
                    {(dayData.work_plans || []).length === 0
                      ? <Typography variant="body2" color="text.secondary">No work plans for this day.</Typography>
                      : (dayData.work_plans || []).map((wp) => (
                          <Paper key={wp.id} elevation={2} sx={{ p: 1.5, mb: 1.5, borderRadius: 1.5, borderLeft: '4px solid #7b1fa2', transition: 'box-shadow 0.2s', '&:hover': { boxShadow: 4 } }}>
                            <Stack direction="row" alignItems="flex-start">
                              <Box sx={{ flex: 1 }}>
                                <Typography variant="subtitle2" fontWeight="bold">{wp.comptitle || '(Untitled work plan)'}</Typography>
                                {(wp.window_start || wp.window_end) && (
                                  <Typography variant="caption" color="text.secondary">
                                    {formatTimeHST(wp.window_start)} – {formatTimeHST(wp.window_end)} HST
                                  </Typography>
                                )}
                                {wp.nite_effect && <Typography variant="body2">Night effect: {wp.nite_effect}</Typography>}
                                {wp.day_effect && <Typography variant="body2">Day effect: {wp.day_effect}</Typography>}
                                {wp.assigned1 && <Typography variant="body2">Assigned: {[wp.assigned1, wp.assigned2].filter(Boolean).join(', ')}</Typography>}
                                {wp.location && <Typography variant="body2">Location: {[wp.location, wp.location2, wp.location3].filter(Boolean).join(' / ')}</Typography>}
                                {wp.comptext && <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', mt: 0.5 }}>{wp.comptext}</Typography>}
                                {wp.notes && <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', mt: 0.5 }}>{wp.notes}</Typography>}
                              </Box>
                              <Stack direction="row" spacing={0.5}>
                                <IconButton size="small" onClick={() => openEditWP(wp)}><EditIcon fontSize="small" /></IconButton>
                                <IconButton size="small" color="error" onClick={() => deleteWP(wp.id)}><DeleteIcon fontSize="small" /></IconButton>
                              </Stack>
                            </Stack>
                          </Paper>
                        ))
                    }
                  </SectionCard>
                  <SectionCard title="📝 WP Log Entries" accent="linear-gradient(90deg,#4527a0,#512da8)" action={
                    !editorOpen && <Button size="small" startIcon={<AddIcon />} onClick={() => beginCreate('WP')} sx={{ color: '#fff' }}>Add WP Entry</Button>
                  }>{renderLogList(wpRows, 'WP')}</SectionCard>
                </Box>
              )}

              {/* ── Crew & Weather Tab ── */}
              {viewTab === 'crew' && (
                <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 2 }}>
                  <SectionCard title="👥 Crew Assignments" accent="linear-gradient(90deg,#1565c0,#1976d2)" action={
                    <Button size="small" startIcon={<AddIcon />} onClick={openAddCrew} sx={{ color: '#fff' }}>Add Crew</Button>
                  }>
                    <TableContainer><Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Role</TableCell><TableCell>Name</TableCell>
                          <TableCell>Location</TableCell><TableCell>Time In</TableCell>
                          <TableCell>Time Out</TableCell><TableCell />
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {(dayData.crew_assignments || []).map((c) => (
                          <TableRow key={c.id}>
                            <TableCell><RoleChip role={c.role} /></TableCell>
                            <TableCell>{c.member_name || '—'}</TableCell>
                            <TableCell>{c.location || '—'}</TableCell>
                            <TableCell>{formatTimeHST(c.time_in)}</TableCell>
                            <TableCell>{formatTimeHST(c.time_out)}</TableCell>
                            <TableCell>
                              <Stack direction="row">
                                <IconButton size="small" onClick={() => openEditCrew(c)}><EditIcon fontSize="small" /></IconButton>
                                <IconButton size="small" color="error" onClick={() => deleteCrew(c.id)}><DeleteIcon fontSize="small" /></IconButton>
                              </Stack>
                            </TableCell>
                          </TableRow>
                        ))}
                        {(dayData.crew_assignments || []).length === 0 && (
                          <TableRow><TableCell colSpan={6}><Typography variant="body2" color="text.secondary">No crew assigned.</Typography></TableCell></TableRow>
                        )}
                      </TableBody>
                    </Table></TableContainer>
                  </SectionCard>

                  <SectionCard title="🌤 Weather Conditions" accent="linear-gradient(90deg,#00838f,#0097a7)" action={
                    <Button size="small" startIcon={<EditIcon />} onClick={openWeatherEdit} sx={{ color: '#fff' }}>
                      {dayData.weather ? 'Edit' : 'Add'} Weather
                    </Button>
                  }>
                    {dayData.weather ? (
                      <Stack spacing={0.75}>
                        {[
                          ['Sky', dayData.weather.sky],
                          ['Seeing', dayData.weather.seeing],
                          ['Temp', weatherVal(dayData.weather.temp_raw, dayData.weather.temp_c, '°C')],
                          ['Wind', dayData.weather.wind],
                          ['Humidity', weatherVal(dayData.weather.humidity_raw, dayData.weather.humidity_pct, '%')],
                        ].map(([label, val]) => (
                          <Stack key={label} direction="row" spacing={1}>
                            <Typography variant="body2" fontWeight="bold" sx={{ minWidth: 70 }}>{label}:</Typography>
                            <Typography variant="body2">{val || 'N/A'}</Typography>
                          </Stack>
                        ))}
                        {dayData.weather.comment_text && (
                          <Typography variant="body2" color="text.secondary">Comment: {dayData.weather.comment_text}</Typography>
                        )}
                      </Stack>
                    ) : <Typography variant="body2" color="text.secondary">No weather recorded.</Typography>}
                  </SectionCard>
                </Box>
              )}

              {/* ── Programs Tab ── */}
              {viewTab === 'programs' && (
                <SectionCard title="🔭 Observation Programs" accent="linear-gradient(90deg,#00695c,#00897b)" action={
                  <Button size="small" startIcon={<AddIcon />} onClick={openAddProgram} sx={{ color: '#fff' }}>Add Program</Button>
                }>
                  {(dayData.programs || []).length === 0
                    ? <Typography variant="body2" color="text.secondary">No programs scheduled.</Typography>
                      : (dayData.programs || []).map((p) => (
                        <Paper key={p.id} elevation={2} sx={{ p: 1.5, mb: 1.5, borderRadius: 1.5, borderLeft: '4px solid #00897b', transition: 'box-shadow 0.2s', '&:hover': { boxShadow: 4 } }}>
                          <Stack direction="row" alignItems="flex-start">
                            <Box sx={{ flex: 1 }}>
                              <Stack direction="row" spacing={1} alignItems="center" flexWrap="wrap" useFlexGap>
                                {p.instr && <Chip size="small" label={p.instr} color="primary" />}
                                {p.pi && <Typography variant="subtitle2">PI: {p.pi}</Typography>}
                                {p.gid && <Chip size="small" label={`GID: ${p.gid}`} variant="outlined" />}
                                {p.propid && <Chip size="small" label={`PropID: ${p.propid}`} variant="outlined" />}
                              </Stack>
                              {(p.slot_start || p.slot_end) && (
                                <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                                  {formatTimeHST(p.slot_start)} – {formatTimeHST(p.slot_end)} HST
                                </Typography>
                              )}
                              {(p.obs1 || p.obs2 || p.obs3 || p.obs4) && (
                                <Typography variant="body2">
                                  Observers: {[p.obs1, p.obs2, p.obs3, p.obs4].filter(Boolean).map((o, i) => {
                                    const loc = [p.obs1loc, p.obs2loc, p.obs3loc, p.obs4loc][i];
                                    return loc ? `${o} (${loc})` : o;
                                  }).join(', ')}
                                </Typography>
                              )}
                              {(p.ss || p.ss2) && (
                                <Typography variant="body2">
                                  SA: {[p.ss, p.ss2].filter(Boolean).map((s, i) => {
                                    const loc = [p.ssloc, p.ss2loc][i];
                                    return loc ? `${s} (${loc})` : s;
                                  }).join(', ')}
                                </Typography>
                              )}
                              {(p.ao1 || p.ao2) && <Typography variant="body2">AO: {[p.ao1, p.ao2].filter(Boolean).join(', ')}</Typography>}
                              {(p.others1 || p.others2) && <Typography variant="body2">Others: {[p.others1, p.others2].filter(Boolean).join(', ')}</Typography>}
                              {p.alloc && <Typography variant="body2">Alloc: {p.alloc}</Typography>}
                              {p.notes && <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', mt: 0.5 }}>{p.notes}</Typography>}
                              {p.comment_text && <Typography variant="body2" color="text.secondary">Comment: {p.comment_text}</Typography>}
                            </Box>
                            <Stack direction="row" spacing={0.5}>
                              <IconButton size="small" onClick={() => openEditProgram(p)}><EditIcon fontSize="small" /></IconButton>
                              <IconButton size="small" color="error" onClick={() => deleteProgram(p.id)}><DeleteIcon fontSize="small" /></IconButton>
                            </Stack>
                          </Stack>
                        </Paper>
                      ))
                  }
                </SectionCard>
              )}

              {/* ── Trouble Tab ── */}
              {viewTab === 'trouble' && (
                <SectionCard
                  title={`⚠ Trouble${troubleRows.length ? ` — ${troubleRows.length} entries · ${troubleRows.reduce((s, i) => s + (i.downtime_minutes || 0), 0)} min downtime` : ''}`}
                  accent="linear-gradient(90deg,#b71c1c,#c62828)">
                  {troubleRows.length === 0
                    ? <Typography variant="body2" color="text.secondary">No trouble entries for this day.</Typography>
                    : troubleRows.map((item) => (
                        <Box key={item.id} sx={{ mb: 1.5 }}>
                          <Stack direction="row" spacing={1} alignItems="flex-start">
                            <Typography variant="caption" color="text.secondary" sx={{ minWidth: 44, pt: 0.3 }}>
                              {formatTimeHST(item.item_time)}
                            </Typography>
                            <Box sx={{ flex: 1 }}>
                              <Stack direction="row" spacing={0.5} alignItems="center" flexWrap="wrap" useFlexGap>
                                <ItemTypeChip type={item.item_type} />
                                {item.status && <StatusChip status={item.status} />}
                                {item.subsystem && item.subsystem !== 'None' && (
                                  <Chip size="small" label={item.subsystem} variant="outlined" />
                                )}
                                {item.downtime_minutes > 0 && (
                                  <Chip size="small" label={`${item.downtime_minutes} min`} color="error" variant="outlined" />
                                )}
                              </Stack>
                              {item.title && <Typography variant="subtitle2">{item.title}</Typography>}
                              {item.body && <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'pre-wrap' }}>{item.body}</Typography>}
                            </Box>
                            <Stack direction="row">
                              <IconButton size="small" onClick={() => beginEdit(item)}><EditIcon fontSize="small" /></IconButton>
                              <IconButton size="small" color="error" onClick={() => deleteItem(item.id)}><DeleteIcon fontSize="small" /></IconButton>
                            </Stack>
                          </Stack>
                          <Divider sx={{ mt: 1 }} />
                        </Box>
                      ))
                  }
                </SectionCard>
              )}
              </Box>
            </Box>
          )}
        </Paper>
      )}

      {/* ── Search Panel ── */}
      <Paper elevation={3} sx={{ borderRadius: 2.5, overflow: 'hidden' }}>
        <Box sx={{ px: 2.5, py: 1.75, background: 'linear-gradient(90deg, #004d40 0%, #00695c 100%)', color: '#fff' }}>
          <Typography variant="subtitle1" fontWeight={700} sx={{ letterSpacing: 0.3 }}>🔍 Search Log Entries</Typography>
        </Box>
        <Box sx={{ p: 2.5 }}>
        <Stack spacing={1.5}>
          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} alignItems={{ sm: 'center' }}>
            <TextField size="small" fullWidth label="Keywords" value={searchQ}
              onChange={(e) => setSearchQ(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && runSearch(0)} />
            <Button variant="contained" onClick={() => runSearch(0)}
              disabled={searchLoading || !searchQ.trim()} sx={{ minWidth: 90 }}>
              {searchLoading ? <CircularProgress size={20} color="inherit" /> : 'Search'}
            </Button>
          </Stack>
          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1}>
            <TextField size="small" type="date" label="From Date" InputLabelProps={{ shrink: true }}
              value={searchFromDate} onChange={(e) => setSearchFromDate(e.target.value)} sx={{ flex: 1 }} />
            <TextField size="small" type="date" label="To Date" InputLabelProps={{ shrink: true }}
              value={searchToDate} onChange={(e) => setSearchToDate(e.target.value)} sx={{ flex: 1 }} />
            <FormControl size="small" sx={{ flex: 1, minWidth: 120 }}>
              <InputLabel>Crew Tab</InputLabel>
              <Select value={searchCrew} label="Crew Tab" onChange={(e) => setSearchCrew(e.target.value)}>
                <MenuItem value="">All</MenuItem>
                {CREW_TABS.map((c) => <MenuItem key={c} value={c}>{c}</MenuItem>)}
              </Select>
            </FormControl>
          </Stack>
        </Stack>

        {searchError && <Alert severity="error" sx={{ mt: 1 }}>{searchError}</Alert>}

        {searchResult && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {searchResult.total} match(es) · showing {searchResult.items?.length || 0}
            </Typography>
            <Divider sx={{ mb: 1 }} />
            {(searchResult.items || []).map((item) => (
              <Paper key={item.id} elevation={1} sx={{
                p: 1.5, mb: 1, borderRadius: 1.5,
                borderLeft: `4px solid ${TYPE_BORDER[item.item_type] || '#90a4ae'}`,
                transition: 'box-shadow 0.2s',
                '&:hover': { boxShadow: 3 },
              }}>
                <Stack direction="row" alignItems="flex-start" spacing={1}>
                  <Box sx={{ flex: 1 }}>
                    <Stack direction="row" spacing={0.75} alignItems="center" flexWrap="wrap" useFlexGap>
                      {item.log_date && (
                        <Button size="small"
                          sx={{ p: 0, minWidth: 0, fontWeight: 700, fontSize: '0.78rem', color: '#00695c' }}
                          onClick={() => {
                            const ld = typeof item.log_date === 'string' ? item.log_date.split('T')[0] : String(item.log_date);
                            const [y, m] = ld.split('-').map(Number);
                            setYear(y); setMonth(m); loadDay(ld);
                          }}>
                          📅 {item.log_date}
                        </Button>
                      )}
                      <RoleChip role={item.crew_tab} />
                      {item.item_type && <ItemTypeChip type={item.item_type} />}
                      {item.status && <StatusChip status={item.status} />}
                      <Typography variant="caption" color="text.secondary">{formatTimeHST(item.item_time)}</Typography>
                    </Stack>
                    {item.title && <Typography variant="subtitle2" sx={{ mt: 0.25, fontWeight: 600 }}>{item.title}</Typography>}
                    {item.body && (
                      <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'pre-wrap', mt: 0.25 }}>
                        {item.body.slice(0, 300)}{item.body.length > 300 ? '…' : ''}
                      </Typography>
                    )}
                  </Box>
                </Stack>
              </Paper>
            ))}
            {(searchResult.items?.length || 0) < searchResult.total && (
              <Button variant="outlined" size="small" onClick={() => runSearch(searchOffset + SEARCH_LIMIT)}
                disabled={searchLoading} sx={{ mt: 1 }}>
                Load More ({searchResult.total - (searchResult.items?.length || 0)} remaining)
              </Button>
            )}
          </Box>
        )}
        </Box>{/* close p:2.5 */}
      </Paper>

      {/* ── Dialogs ── */}

      {/* Create new day */}
      <Dialog open={createDayOpen} onClose={() => setCreateDayOpen(false)} maxWidth="xs" fullWidth>
        <DialogTitle>Create New Summit Day</DialogTitle>
        <DialogContent>
          <TextField type="date" fullWidth label="Date" InputLabelProps={{ shrink: true }}
            value={newDayDate} onChange={(e) => setNewDayDate(e.target.value)} sx={{ mt: 1 }} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDayOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={createDay} disabled={!newDayDate || createDaySaving}>
            {createDaySaving ? 'Creating…' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Crew dialog */}
      <Dialog open={crewDialogOpen} onClose={() => setCrewDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{crewForm.id ? 'Edit Crew Member' : 'Add Crew Member'}</DialogTitle>
        <DialogContent>
          <Stack spacing={1.5} sx={{ mt: 1 }}>
            <FormControl fullWidth size="small">
              <InputLabel>Role</InputLabel>
              <Select value={crewForm.role} label="Role"
                onChange={(e) => setCrewForm(p => ({ ...p, role: e.target.value }))}>
                {CREW_ROLES.map((r) => <MenuItem key={r} value={r}>{r}</MenuItem>)}
              </Select>
            </FormControl>
            <TextField size="small" fullWidth label="Name" value={crewForm.member_name}
              onChange={(e) => setCrewForm(p => ({ ...p, member_name: e.target.value }))} />
            <TextField size="small" fullWidth label="Location (e.g. summit, base)"
              value={crewForm.location}
              onChange={(e) => setCrewForm(p => ({ ...p, location: e.target.value }))} />
            <Stack direction="row" spacing={1}>
              <TextField size="small" fullWidth label="Time In HST (HH:MM)" value={crewForm.time_in}
                onChange={(e) => setCrewForm(p => ({ ...p, time_in: e.target.value }))} />
              <TextField size="small" fullWidth label="Time Out HST (HH:MM)" value={crewForm.time_out}
                onChange={(e) => setCrewForm(p => ({ ...p, time_out: e.target.value }))} />
            </Stack>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCrewDialogOpen(false)} startIcon={<CancelIcon />}>Cancel</Button>
          <Button variant="contained" onClick={saveCrew} disabled={crewSaving} startIcon={<SaveIcon />}>
            {crewSaving ? 'Saving…' : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Weather dialog */}
      <Dialog open={weatherEditOpen} onClose={() => setWeatherEditOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{dayData?.weather ? 'Edit Weather' : 'Add Weather'}</DialogTitle>
        <DialogContent>
          <Stack spacing={1.5} sx={{ mt: 1 }}>
            <Stack direction="row" spacing={1}>
              <TextField size="small" fullWidth label="Sky" value={weatherForm.sky}
                onChange={(e) => setWeatherForm(p => ({ ...p, sky: e.target.value }))} />
              <TextField size="small" fullWidth label="Seeing (arcsec)" value={weatherForm.seeing}
                onChange={(e) => setWeatherForm(p => ({ ...p, seeing: e.target.value }))} />
            </Stack>
            <Stack direction="row" spacing={1}>
              <TextField size="small" fullWidth label="Temp (°C or range)" value={weatherForm.temp_raw}
                onChange={(e) => setWeatherForm(p => ({ ...p, temp_raw: e.target.value }))} />
              <TextField size="small" fullWidth label="Wind" value={weatherForm.wind}
                onChange={(e) => setWeatherForm(p => ({ ...p, wind: e.target.value }))} />
            </Stack>
            <TextField size="small" fullWidth label="Humidity (% or range)" value={weatherForm.humidity_raw}
              onChange={(e) => setWeatherForm(p => ({ ...p, humidity_raw: e.target.value }))} />
            <TextField size="small" fullWidth label="Comment" value={weatherForm.comment_text}
              onChange={(e) => setWeatherForm(p => ({ ...p, comment_text: e.target.value }))} />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setWeatherEditOpen(false)} startIcon={<CancelIcon />}>Cancel</Button>
          <Button variant="contained" onClick={saveWeather} disabled={weatherSaving} startIcon={<SaveIcon />}>
            {weatherSaving ? 'Saving…' : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Program dialog */}
      <ProgramDialog
        open={programDialogOpen}
        onClose={() => { setProgramDialogOpen(false); setProgramEditing(null); }}
        onSave={saveProgram}
        saving={programSaving}
        initial={programEditing || {}}
      />

      {/* Work Plan dialog */}
      <WorkPlanDialog
        open={wpDialogOpen}
        onClose={() => { setWpDialogOpen(false); setWpEditing(null); }}
        onSave={saveWP}
        saving={wpSaving}
        initial={wpEditing || {}}
      />
    </Box>
  );
}
