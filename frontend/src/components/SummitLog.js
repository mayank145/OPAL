import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  Box, Typography, Paper, IconButton, Button, Tabs, Tab,
  CircularProgress, Alert, Divider, Chip, Table, TableBody,
  TableCell, TableHead, TableRow, TableContainer, TextField,
  Stack, MenuItem, Select, FormControl, InputLabel, Tooltip,
  Dialog, DialogTitle, DialogContent, DialogActions,
  Collapse, Link, List, ListItem, ListItemButton, ListItemText,
  Autocomplete,
} from '@mui/material';
import {
  ChevronLeft, ChevronRight, Today as TodayIcon,
  Edit as EditIcon, Delete as DeleteIcon, Add as AddIcon,
  Save as SaveIcon, Cancel as CancelIcon, ExpandMore, ExpandLess,
  PostAdd as PostAddIcon, ContentCopy as ContentCopyIcon,
  Email as EmailIcon, AccessTime as AccessTimeIcon,
  Visibility as VisibilityIcon,
} from '@mui/icons-material';
import { useNavigate, useSearchParams, useLocation } from 'react-router-dom';
import { summitAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { paths, isValidLogDate, todayHST } from '../routes/paths';

// ── Constants ────────────────────────────────────────────────────────────────
const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const TYPE_OPTIONS = ['Comment', 'Trouble', 'Summary', 'Warning', 'Important'];
const CREW_TABS = ['TO', 'IO', 'DC', 'WP', 'ALL', 'TO-IO'];
const CREW_ROLES = ['TO', 'IO', 'DC'];
const SUBSYSTEMS = ['', 'Tel', 'Inst', 'SOSS', 'Weather', 'Operations', 'Others'];
const INTERVENE_OPTIONS = ['Choose', 'No', 'Yes'];

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

// Store times as naive HST strings. The backend tags all naive datetimes as
// HST (-10:00) on read, so they display correctly in any browser timezone.
function toUtcIso(logDate, hhmm) {
  if (!logDate || !hhmm || !hhmm.includes(':')) return null;
  const [y, m, d] = logDate.split('-').map(Number);
  const [hh, mm] = hhmm.split(':').map(Number);
  if ([y, m, d, hh, mm].some(Number.isNaN)) return null;
  const p = (n) => String(n).padStart(2, '0');
  return `${String(y).padStart(4, '0')}-${p(m)}-${p(d)}T${p(hh)}:${p(mm)}:00`;
}

function weatherVal(raw, numeric, suffix = '') {
  if (raw && String(raw).trim()) return String(raw).trim();
  if (numeric != null && numeric !== '') return `${numeric}${suffix}`;
  return 'N/A';
}

function formatApiError(detail) {
  if (!detail) return 'Request failed';
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) {
    return detail.map((e) => e.msg || e.message || JSON.stringify(e)).join('; ');
  }
  return String(detail);
}

function pickDefaultLogDate(days) {
  if (!days?.length) return null;
  const withEntries = [...days].reverse().find((d) => (d.entry_count || 0) > 0);
  const pick = withEntries || days[days.length - 1];
  return parseDate(pick.log_date);
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
function LogItemEditor({ editor, setEditor, onSave, onCancel, saving, selectedDate, workPlans = [], showDowntime = true }) {
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
        <FormControl size="small" sx={{ minWidth: 140 }}>
          <InputLabel>Subsystem</InputLabel>
          <Select value={editor.subsystem} label="Subsystem"
            onChange={(e) => setEditor((p) => ({ ...p, subsystem: e.target.value }))}>
            {SUBSYSTEMS.map((o) => <MenuItem key={o} value={o}>{o || '— none —'}</MenuItem>)}
          </Select>
        </FormControl>
        {showDowntime && (
          <TextField size="small" label="Downtime (min)" type="number"
            value={editor.downtimeMinutes}
            onChange={(e) => setEditor((p) => ({ ...p, downtimeMinutes: e.target.value }))}
            sx={{ maxWidth: 140 }} />
        )}
        <TextField size="small" label="Created By" value={editor.createdBy}
          onChange={(e) => setEditor((p) => ({ ...p, createdBy: e.target.value }))}
          sx={{ maxWidth: 140 }} />
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>Summit Access</InputLabel>
          <Select value={editor.summitAccess || 'Choose'} label="Summit Access"
            onChange={(e) => setEditor((p) => ({ ...p, summitAccess: e.target.value }))}>
            {INTERVENE_OPTIONS.map((o) => <MenuItem key={o} value={o}>{o}</MenuItem>)}
          </Select>
        </FormControl>
      </Stack>
      <TextField size="small" fullWidth label="Title" value={editor.title}
        onChange={(e) => setEditor((p) => ({ ...p, title: e.target.value }))} sx={{ mb: 1 }} />
      <TextField size="small" fullWidth multiline minRows={3} label="Body / Description"
        value={editor.body} onChange={(e) => setEditor((p) => ({ ...p, body: e.target.value }))}
        sx={{ mb: 1 }} />
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
function LogItemRow({ item, onEdit, onDelete, onCreateFatsFromSummit, logDate, highlighted = false }) {
  const [expanded, setExpanded] = useState(false);
  const borderColor = TYPE_BORDER[item.item_type] || '#90a4ae';
  return (
    <Paper id={`log-item-${item.id}`} elevation={highlighted ? 4 : 1} sx={{
      mb: 1, borderRadius: 1.5, overflow: 'hidden',
      borderLeft: `4px solid ${borderColor}`,
      transition: 'box-shadow 0.2s, transform 0.1s, background-color 0.4s',
      backgroundColor: highlighted ? '#fff9c4' : undefined,
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
              {item.summit_access === 'Yes' && (
                <Chip size="small" label="⛰ Access" color="warning" sx={{ fontSize: '0.67rem', height: 20, fontWeight: 700 }} />
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
            {onCreateFatsFromSummit && logDate && (
              <Tooltip title="Start FATS from this entry">
                <IconButton size="small" onClick={() => onCreateFatsFromSummit(item, logDate)}
                  sx={{ color: '#1565c0', '&:hover': { bgcolor: 'rgba(21,101,192,0.08)' } }}>
                  <PostAddIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            )}
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

// ── Program dialog constants — sourced from sumlogs.refer table ──────────────
// INSTR options (sumlogs.refer WHERE code='INSTR', ordered by seq)
const PROG_INSTR_OPTIONS = [
  'Choose', 'CHARIS', 'CIAO', 'CISCO', 'COMICS', 'FMOS', 'FOCAS',
  'HDS', 'HICIAO', 'HIPWAC', 'HSC', 'IRCS', 'IRCS/AO', 'IRD',
  'K3D', 'MIMIZUKU', 'MIRTOS', 'MOIRCS', 'None', 'OHS',
  'PFS', 'SWIMS', 'SupCam',
];
// ALLOC options (sumlogs.refer WHERE code='ALLOC', ordered by seq)
const PROG_ALLOC_OPTIONS = [
  'Choose', 'OpenUse', 'InstrEng', 'TelEng', 'UHObs',
  'ServiceObs', 'StaffObs', 'DiscTime', 'GuarTime',
];
const PROG_AO_OPTIONS = ['', 'AO188', 'SCExAO', 'RAVEN', 'No'];
const PROG_LOC_OPTIONS = ['', 'Summit', 'Base', 'HP', 'GERS', 'Mitaka', 'Zoom', 'Other'];

// ── Program Form Dialog ──────────────────────────────────────────────────────
function ProgramDialog({ open, onClose, onSave, saving, initial = {} }) {
  const blank = {
    instr: 'Choose', alloc: 'Choose', pi: '', ao1: '', ao2: '',
    gid: '', propid: '', slotStart: '', slotEnd: '',
    obs1: '', obs1loc: '', obs2: '', obs2loc: '',
    obs3: '', obs3loc: '', obs4: '', obs4loc: '',
    ss: '', ssloc: '', ss2: '', ss2loc: '',
    others1: '', others1loc: '', others2: '', others2loc: '',
    notes: '', comment_text: '',
  };
  const [form, setForm] = useState({ ...blank, ...initial });
  useEffect(() => { setForm({ ...blank, ...initial }); }, [open]); // eslint-disable-line react-hooks/exhaustive-deps

  const f = (key) => ({
    size: 'small', value: form[key],
    onChange: (e) => setForm((p) => ({ ...p, [key]: e.target.value })),
  });
  const sel = (key, options) => (
    <FormControl size="small" sx={{ minWidth: 120 }}>
      <Select value={form[key]} displayEmpty
        onChange={(e) => setForm((p) => ({ ...p, [key]: e.target.value }))}>
        {options.map((o) => <MenuItem key={o} value={o}>{o || '— —'}</MenuItem>)}
      </Select>
    </FormControl>
  );
  const row = (fields) => (
    <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }} flexWrap="wrap" useFlexGap>
      {fields}
    </Stack>
  );

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle sx={{ background: 'linear-gradient(90deg,#00695c,#00897b)', color: '#fff', py: 1.5 }}>
        {initial.id ? '✏️ Edit Observation Program' : '🔭 Add Observation Program'}
      </DialogTitle>
      <DialogContent dividers>
        {row([
          <Box key="instr">
            <Typography variant="caption" color="text.secondary">Instrument</Typography>
            {sel('instr', PROG_INSTR_OPTIONS)}
          </Box>,
          <Box key="alloc">
            <Typography variant="caption" color="text.secondary">Alloc</Typography>
            {sel('alloc', PROG_ALLOC_OPTIONS)}
          </Box>,
          <TextField key="pi" {...f('pi')} label="PI" sx={{ flex: 1, minWidth: 140 }} />,
          <TextField key="gid" {...f('gid')} label="GID" sx={{ maxWidth: 110 }} />,
          <TextField key="propid" {...f('propid')} label="PropID" sx={{ maxWidth: 130 }} />,
        ])}
        {row([
          <Box key="ao1">
            <Typography variant="caption" color="text.secondary">AO1</Typography>
            {sel('ao1', PROG_AO_OPTIONS)}
          </Box>,
          <Box key="ao2">
            <Typography variant="caption" color="text.secondary">AO2</Typography>
            {sel('ao2', PROG_AO_OPTIONS)}
          </Box>,
          <TextField key="slotStart" {...f('slotStart')} label="Slot Start HST (HH:MM)" sx={{ maxWidth: 180 }} />,
          <TextField key="slotEnd" {...f('slotEnd')} label="Slot End HST (HH:MM)" sx={{ maxWidth: 180 }} />,
        ])}
        <Divider sx={{ my: 1 }} />
        {[
          ['obs1','obs1loc','Observer 1'],['obs2','obs2loc','Observer 2'],
          ['obs3','obs3loc','Observer 3'],['obs4','obs4loc','Observer 4'],
          ['ss','ssloc','SA 1'],['ss2','ss2loc','SA 2'],
          ['others1','others1loc','Others 1'],['others2','others2loc','Others 2'],
        ].reduce((rows, item, i) => {
          if (i % 2 === 0) rows.push([item]);
          else rows[rows.length - 1].push(item);
          return rows;
        }, []).map((pair, ri) => (
          row(pair.flatMap(([nameKey, locKey, label]) => [
            <TextField key={nameKey} {...f(nameKey)} label={label} sx={{ flex: 1, minWidth: 140 }} />,
            <Box key={locKey}>
              <Typography variant="caption" color="text.secondary">Loc</Typography>
              {sel(locKey, PROG_LOC_OPTIONS)}
            </Box>,
          ]))
        ))}
        <TextField {...f('notes')} label="Notes" multiline minRows={2} fullWidth sx={{ mb: 1, mt: 0.5 }} />
        <TextField {...f('comment_text')} label="Comment" fullWidth />
      </DialogContent>
      <DialogActions sx={{ px: 2, py: 1.5 }}>
        <Button onClick={onClose} startIcon={<CancelIcon />} sx={{ borderRadius: 2 }}>Cancel</Button>
        <Button variant="contained" onClick={() => onSave(form)} disabled={saving} startIcon={<SaveIcon />}
          sx={{ borderRadius: 2, background: 'linear-gradient(90deg,#00695c,#00897b)', fontWeight: 600 }}>
          {saving ? 'Saving…' : 'Save'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

// ── Work Plan Form Dialog ────────────────────────────────────────────────────
// Values sourced directly from legacy refer table (sumlogs DB)
const WP_STATUS_OPTIONS    = ['Planned', 'Started', 'Completed', 'NotComplete', 'Cancelled'];
const WP_TYPE_OPTIONS      = ['Comment', 'Trouble', 'Summary', 'Warning', 'Observation', 'Important'];
const WP_SUBSYSTEM_OPTIONS = ['-none-', 'Tel', 'Inst', 'SOSS', 'Weather', 'Operations', 'Others'];
const WP_DCASSIST_OPTIONS  = ['.none', 'DC1', 'DC2', 'DC-Any', 'DC-All'];
const WP_LOCATION_OPTIONS  = [
  '.none','CB-1-Floor','CB-2-Floor','CB-3-Floor','ESB','ESB-Exterior','ESB-Catwalk',
  'Elevators','Vent-Floor','Obs-Floor','Obs-Floor-Opt','Obs-Floor-IR',
  'Nas-Floor','Nas-Floor-Opt','Nas-Floor-IR',
  'Tertiary-Floor','Tertiary-Floor-Opt','Tertiary-Floor-IR',
  'TUE-Floor','TUE-Floor-Opt','TUE-Floor-IR',
  'High-Roof','Low-Roof','Summit-Safety',
  'MainShutter-IR','MainShutter-Opt','Penthouse','Coude','Crane Floor',
];
const WP_TIME_OPTIONS = [
  '', '00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30',
  '04:00','04:30','05:00','05:30','06:00','06:30','07:00','07:30',
  '08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30',
  '12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30',
  '16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30',
  '20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30',
];
// Window Start / End — 08:00 – 18:00 HST (30-min slots)
const WP_WINDOW_TIME_OPTIONS = [
  '', '08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30',
  '12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30',
  '16:00','16:30','17:00','17:30','18:00',
];
// Real Start / End — 08:00 – 17:00 HST (30-min slots)
const WP_DAY_TIME_OPTIONS = [
  '', '08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30',
  '12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30',
  '16:00','16:30','17:00',
];
const REQUIRED_FLAGS = [
  'Move-Tel','Move-EL','Move-AZ','80t-Crane','NsIR-Crane','SmallDoor-Crane',
  'BSIT','TUE-Opt-Crane','TUE-Opt-US','Gen2-Allocation','MirrorHatch','CherryPicker',
  'ForkLift','Hazardous-Materials','MainShutter','Others',
];
const LOCKOUT_FLAGS = [
  'No-Tel-Move','No-AZ-Move','No-EL-Move','NoLights-Dome',
  'No-TopScreen-Move','No-MirrorCover-Move','No-MainShutter','No-UnitSelector-Move',
];

export function WorkPlanDialog({ open, onClose, onSave, saving, initial = {}, currentUsername = '' }) {
  // orgUsers: [{ username, display }] from clients.users where privy='subaru'
  const [orgUsers, setOrgUsers] = useState([{ username: '.none', display: '— none —' }]);
  const [staffLoading, setStaffLoading] = useState(false);
  useEffect(() => {
    if (open) {
      setStaffLoading(true);
      import('../services/api').then(({ referenceAPI }) =>
        referenceAPI.getOrgUsers()
          .then(list => setOrgUsers(list.length > 1 ? list : [{ username: '.none', display: '— none —' }]))
          .catch(() => {})
          .finally(() => setStaffLoading(false))
      );
    }
  }, [open]);

  const blank = {
    comptitle: '', plan_text: '',
    // Pre-fill requestor with the logged-in user for new work plans
    requestor: initial.id ? (initial.requestor || '') : (currentUsername || ''),
    contact2: '', others: '',
    wp_status: 'Planned', wp_type: 'Comment', wp_subsystem: '-none-',
    windowStart: '08:00', windowEnd: '17:00',
    day_warning: '', nite_warning: '',
    nite_effect: '', day_effect: '',
    location: '.none', location2: '.none', location3: '.none',
    assigned1: '.none', assigned2: '',
    dcassist: '.none', notify: '.none',
    teampass: '', otherreq: '',
    realstart: '', realend: '',
    completion_title: '', comptext: '',
    req_flags: '', lockout_flags: '',
    notes: '',
  };
  const [form, setForm] = useState({ ...blank, ...initial });
  useEffect(() => {
    setForm({
      ...blank,
      ...initial,
      // Always keep requestor as current user for new WPs
      requestor: initial.id ? (initial.requestor || '') : (currentUsername || initial.requestor || ''),
    });
  }, [open]); // eslint-disable-line react-hooks/exhaustive-deps

  const f = (key) => ({ size: 'small', value: form[key] || '', onChange: (e) => setForm((p) => ({ ...p, [key]: e.target.value })) });
  const sel = (key, opts, label, minW = 110) => (
    <FormControl size="small" sx={{ flex: 1, minWidth: minW }}>
      <InputLabel>{label}</InputLabel>
      <Select value={form[key] || opts[0]} label={label}
        onChange={(e) => setForm(p => ({ ...p, [key]: e.target.value }))}>
        {opts.map(o => <MenuItem key={o} value={o}>{o || '— none —'}</MenuItem>)}
      </Select>
    </FormControl>
  );
  const timeSel = (key, label, opts = WP_TIME_OPTIONS) => (
    <FormControl size="small" sx={{ flex: 1, minWidth: 110 }}>
      <InputLabel>{label}</InputLabel>
      <Select value={form[key] || ''} label={label}
        onChange={(e) => setForm(p => ({ ...p, [key]: e.target.value }))}>
        {opts.map(t => <MenuItem key={t} value={t}>{t || '— none —'}</MenuItem>)}
      </Select>
    </FormControl>
  );

  // Checkbox flag helpers (stored as comma-separated string)
  const flagSet = (raw) => new Set((raw || '').split(',').map(s => s.trim()).filter(Boolean));
  const toggleFlag = (field, flag) => setForm(p => {
    const s = flagSet(p[field]);
    s.has(flag) ? s.delete(flag) : s.add(flag);
    return { ...p, [field]: [...s].join(',') };
  });

  const reqSet  = flagSet(form.req_flags);
  const lockSet = flagSet(form.lockout_flags);
  const othersChecked = reqSet.has('Others');

  const SectionHeader = ({ label }) => (
    <Typography variant="caption" fontWeight={700} sx={{
      display: 'block', mb: 0.75, mt: 1.5, px: 0.5, py: 0.25,
      color: '#6a1b9a', textTransform: 'uppercase', letterSpacing: 0.8,
      borderBottom: '1.5px solid #ce93d8',
    }}>{label}</Typography>
  );

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle sx={{ background: 'linear-gradient(90deg,#6a1b9a,#7b1fa2)', color: '#fff', py: 1.5 }}>
        {initial.id ? '✏️ Edit Work Plan' : '📋 New Work Plan'}
      </DialogTitle>
      <DialogContent dividers sx={{ pt: 1.5 }}>

        {/* ── Requested section ── */}
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }} flexWrap="wrap" useFlexGap>
          <TextField
            {...f('requestor')}
            label="Requestor"
            sx={{ flex: 1, minWidth: 140 }}
            InputProps={{
              readOnly: !initial.id,
              sx: !initial.id ? { bgcolor: '#f5f5f5', color: 'text.secondary' } : {},
            }}
            helperText={!initial.id ? 'Auto-filled from your account' : undefined}
          />
          <TextField {...f('contact2')} label="DayCrew2" sx={{ flex: 1, minWidth: 120 }} />
          <TextField {...f('others')} label="Others" sx={{ flex: 1, minWidth: 120 }} />
        </Stack>

        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }} flexWrap="wrap" useFlexGap>
          {sel('wp_status', WP_STATUS_OPTIONS, 'Status')}
          {sel('wp_type', WP_TYPE_OPTIONS, 'Type')}
          {sel('wp_subsystem', WP_SUBSYSTEM_OPTIONS, 'Subsystem')}
        </Stack>

        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }}>
          {timeSel('windowStart', 'Start HST (08:00–18:00)', WP_WINDOW_TIME_OPTIONS)}
          {timeSel('windowEnd',   'End HST (08:00–18:00)',   WP_WINDOW_TIME_OPTIONS)}
        </Stack>

        <TextField {...f('comptitle')} label="Plan Title" fullWidth sx={{ mb: 1 }} />
        <TextField {...f('plan_text')} label="Plan Text" multiline minRows={2} fullWidth sx={{ mb: 1 }} />

        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }}>
          {sel('location',  WP_LOCATION_OPTIONS, 'Location 1')}
          {sel('location2', WP_LOCATION_OPTIONS, 'Location 2')}
          {sel('location3', WP_LOCATION_OPTIONS, 'Location 3')}
        </Stack>

        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }}>
          <TextField {...f('day_warning')} label="Day Warning" sx={{ flex: 1 }} />
          <TextField {...f('nite_warning')} label="Night Warning" sx={{ flex: 1 }} />
        </Stack>

        {/* ── Assigned section ── */}
        <SectionHeader label="Assigned" />
        {staffLoading && (
          <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }}>
            <CircularProgress size={14} />
            <Typography variant="caption" color="text.secondary">Loading Subaru Telescope staff list…</Typography>
          </Stack>
        )}
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }}>
          {/* Assigned 1 — searchable org user list */}
          <Autocomplete
            size="small"
            sx={{ flex: 1, minWidth: 220 }}
            options={orgUsers}
            getOptionLabel={(o) => (typeof o === 'string' ? o : o.display)}
            isOptionEqualToValue={(o, v) =>
              (typeof o === 'string' ? o : o.username) === (typeof v === 'string' ? v : v.username)
            }
            value={orgUsers.find(u => u.username === (form.assigned1 || '.none')) || null}
            onChange={(_, newVal) =>
              setForm(p => ({ ...p, assigned1: newVal ? newVal.username : '.none' }))
            }
            renderInput={(params) => (
              <TextField {...params} label="Assigned 1" placeholder="Type to search…" />
            )}
            filterOptions={(options, { inputValue }) => {
              const q = inputValue.toLowerCase();
              return options.filter(o => o.display.toLowerCase().includes(q));
            }}
            noOptionsText="No matching staff found"
          />
          <TextField {...f('assigned2')} label="Assigned 2" sx={{ flex: 1 }} />
        </Stack>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }} alignItems="center">
          {sel('dcassist', WP_DCASSIST_OPTIONS, 'DC Assist')}
          {/* Notify — searchable org user list */}
          <Autocomplete
            size="small"
            sx={{ flex: 1, minWidth: 220 }}
            options={orgUsers}
            getOptionLabel={(o) => (typeof o === 'string' ? o : o.display)}
            isOptionEqualToValue={(o, v) =>
              (typeof o === 'string' ? o : o.username) === (typeof v === 'string' ? v : v.username)
            }
            value={orgUsers.find(u => u.username === (form.notify || '.none')) || null}
            onChange={(_, newVal) =>
              setForm(p => ({ ...p, notify: newVal ? newVal.username : '.none' }))
            }
            renderInput={(params) => (
              <TextField {...params} label="Notify" placeholder="Type to search…" />
            )}
            filterOptions={(options, { inputValue }) => {
              const q = inputValue.toLowerCase();
              return options.filter(o => o.display.toLowerCase().includes(q));
            }}
            noOptionsText="No matching staff found"
          />
          <TextField {...f('teampass')} label="Team Pass" sx={{ flex: 1 }} />
        </Stack>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }}>
          {timeSel('realstart', 'Real Start HST (08:00–17:00)', WP_DAY_TIME_OPTIONS)}
          {timeSel('realend',   'Real End HST (08:00–17:00)',   WP_DAY_TIME_OPTIONS)}
        </Stack>
        <TextField {...f('completion_title')} label="Completion Title" fullWidth sx={{ mb: 1 }} />
        <TextField {...f('comptext')} label="Completion Text" multiline minRows={2} fullWidth sx={{ mb: 1 }} />

        {/* ── Effects & Location ── */}
        <SectionHeader label="Effects" />
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} sx={{ mb: 1 }}>
          <TextField {...f('nite_effect')} label="Night Effect" sx={{ flex: 1 }} />
          <TextField {...f('day_effect')} label="Day Effect" sx={{ flex: 1 }} />
        </Stack>

        {/* ── Required + LockOuts side-by-side (matches legacy layout) ── */}
        <SectionHeader label="Required & LockOuts" />
        <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2, mt: 0.5 }}>
          {/* Required column */}
          <Box>
            <Typography variant="caption" fontWeight={700} sx={{ mb: 0.5, display: 'block' }}>Required:</Typography>
            {REQUIRED_FLAGS.map(flag => (
              <Box key={flag} sx={{ display: 'flex', alignItems: 'center', mb: 0.25 }}>
                <input type="checkbox" checked={reqSet.has(flag)}
                  onChange={() => toggleFlag('req_flags', flag)}
                  style={{ marginRight: 6, cursor: 'pointer', accentColor: '#1565c0' }} />
                <Typography variant="body2"
                  sx={{ fontWeight: reqSet.has(flag) ? 700 : 400,
                        color: reqSet.has(flag) ? '#1565c0' : 'inherit' }}>
                  {flag}
                </Typography>
              </Box>
            ))}
            {othersChecked && (
              <TextField {...f('otherreq')} label="Others Req." size="small" sx={{ mt: 0.5, width: '90%' }} />
            )}
          </Box>

          {/* LockOuts column */}
          <Box>
            <Typography variant="caption" fontWeight={700} sx={{ mb: 0.5, display: 'block' }}>LockOuts:</Typography>
            {LOCKOUT_FLAGS.map(flag => (
              <Box key={flag} sx={{
                display: 'flex', alignItems: 'center', mb: 0.25,
                bgcolor: lockSet.has(flag) ? '#ffcdd2' : undefined,
                borderRadius: 0.5, px: lockSet.has(flag) ? 0.5 : 0,
              }}>
                <input type="checkbox" checked={lockSet.has(flag)}
                  onChange={() => toggleFlag('lockout_flags', flag)}
                  style={{ marginRight: 6, cursor: 'pointer', accentColor: '#c62828' }} />
                <Typography variant="body2"
                  sx={{ fontWeight: lockSet.has(flag) ? 700 : 400,
                        color: lockSet.has(flag) ? '#c62828' : 'inherit' }}>
                  {flag}
                </Typography>
              </Box>
            ))}
          </Box>
        </Box>

        {/* ── Notes ── */}
        <SectionHeader label="Notes" />
        <TextField {...f('notes')} label="Notes" multiline minRows={2} fullWidth />
      </DialogContent>
      <DialogActions sx={{ px: 2, py: 1.5 }}>
        <Button onClick={onClose} startIcon={<CancelIcon />} sx={{ borderRadius: 2 }}>Cancel</Button>
        <Button variant="contained" onClick={() => onSave(form)} disabled={saving} startIcon={<SaveIcon />}
          sx={{ borderRadius: 2, background: 'linear-gradient(90deg,#6a1b9a,#7b1fa2)', fontWeight: 600 }}>
          {saving ? 'Saving…' : 'Save'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

// ── Main Component ────────────────────────────────────────────────────────────
const SUMMIT_VIEW_TABS = ['summary', 'toio', 'daycrew', 'workplan', 'crew', 'programs', 'trouble'];

export default function SummitLog({ onError, onCreateFatsFromSummit, routeDate, routePanel }) {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const location = useLocation();
  const isSearchRoute = routePanel === 'search' || location.pathname === paths.summitSearch;
  const searchSectionRef = React.useRef(null);

  const now = new Date();
  const [year, setYear] = useState(now.getFullYear());
  const [month, setMonth] = useState(now.getMonth() + 1);
  const [monthPayload, setMonthPayload] = useState(null);
  const [monthlyLoading, setMonthlyLoading] = useState(false);
  const [monthlyError, setMonthlyError] = useState(null);

  const [yearOverviewOpen, setYearOverviewOpen] = useState(false);
  const [yearPayload, setYearPayload] = useState(null);
  const [yearLoading, setYearLoading] = useState(false);
  const [yearError, setYearError] = useState(null);

  const [selectedDate, setSelectedDate] = useState(null);
  const [dayData, setDayData] = useState(null);
  const [dayLoading, setDayLoading] = useState(false);
  const [dayError, setDayError] = useState(null);

  const [viewTab, setViewTab] = useState('summary');

  // Editor state — createdBy is injected at open-time (see beginCreate)
  const EMPTY_EDITOR = { itemId: null, crewTab: 'TO', title: '', body: '', itemType: 'Comment',
    status: 'Completed', subsystem: '', itemTime: '', downtimeMinutes: '', createdBy: '',
    summitAccess: 'Choose', historyText: '', commentText: '', workPlanId: '' };
  const [editor, setEditor] = useState(EMPTY_EDITOR);
  const [editorOpen, setEditorOpen] = useState(false);
  const [editorCard, setEditorCard] = useState(null); // which card the editor belongs to
  const [editorSaving, setEditorSaving] = useState(false);

  // Day header edit
  const [editingHeader, setEditingHeader] = useState(false);
  const [headerForm, setHeaderForm] = useState({
    day_label: '', history_text: '',
    zoom_meeting_id: '', zoom_password: '', zoom_join_url: '',
  });
  const [headerSaving, setHeaderSaving] = useState(false);

  // Create day dialog
  const [createDayOpen, setCreateDayOpen] = useState(false);
  const [newDayDate, setNewDayDate] = useState('');
  const [newDayLabel, setNewDayLabel] = useState('');
  const [newDayHistory, setNewDayHistory] = useState('');
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
  const [highlightItemId, setHighlightItemId] = useState(null);

  // Copy Work Plan
  const [recentWPs, setRecentWPs] = useState([]);
  const [recentWPsLoading, setRecentWPsLoading] = useState(false);
  const [copyWPOpen, setCopyWPOpen] = useState(false);

  // Email sending
  const [emailSending, setEmailSending] = useState(null); // 'to'|'dc'|'smoka'|null
  const [emailPreview, setEmailPreview] = useState(null); // { type, body } | null
  const [emailPreviewLoading, setEmailPreviewLoading] = useState(false);
  const [opalPrograms, setOpalPrograms] = useState([]);
  const [opalProgramsLoading, setOpalProgramsLoading] = useState(false);

  const { user } = useAuth();

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

  const loadYearOverview = useCallback(async () => {
    setYearLoading(true);
    setYearError(null);
    try {
      setYearPayload(await summitAPI.getYear(year));
    } catch (e) {
      const msg = e.response?.data?.detail || e.message || 'Failed to load year';
      setYearError(msg);
      notify(msg);
    } finally {
      setYearLoading(false);
    }
  }, [year, notify]);

  useEffect(() => {
    if (yearOverviewOpen) loadYearOverview();
  }, [yearOverviewOpen, year, loadYearOverview]);

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
    if (routeDate) return;
    const days = monthPayload?.days || [];
    if (!days.length) return;
    const target = pickDefaultLogDate(days);
    if (!target) return;
    if (!selectedDate || !daysWithLog.has(selectedDate)) loadDay(target);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [monthPayload, routeDate]);

  // When URL is "today" but the night log is still empty, open the latest day that has entries.
  useEffect(() => {
    if (!routeDate || routeDate !== todayHST() || !monthPayload?.days?.length) return;
    const todayRow = monthPayload.days.find((d) => parseDate(d.log_date) === routeDate);
    if ((todayRow?.entry_count || 0) > 0) return;
    const fallback = pickDefaultLogDate(monthPayload.days);
    if (fallback && fallback !== routeDate) loadDay(fallback);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [monthPayload, routeDate]);

  const fetchDay = useCallback(async (logDate) => {
    setSelectedDate(logDate);
    setDayLoading(true); setDayError(null); setDayData(null);
    setEditorOpen(false); setEditorCard(null); setEditor(EMPTY_EDITOR); setEditingHeader(false);
    setProgramEditing(null); setWpEditing(null);
    setOpalPrograms([]);
    try {
      const payload = await summitAPI.getDay(logDate);
      setDayData({
        ...payload,
        crew_assignments: payload.crew_assignments || [],
        programs: payload.programs || [],
        work_plans: payload.work_plans || [],
        log_items: payload.log_items || [],
      });
      // Fetch OPAL scheduled programs from legacy clients.alloc in background
      setOpalProgramsLoading(true);
      summitAPI.getOpalPrograms(logDate)
        .then((res) => setOpalPrograms(res || []))
        .catch(() => setOpalPrograms([]))
        .finally(() => setOpalProgramsLoading(false));
    } catch (e) {
      if (e.response?.status === 404) setDayError(`No summit log for ${logDate}`);
      else {
        const msg = formatApiError(e.response?.data?.detail) || e.message;
        setDayError(msg);
        notify(msg);
      }
    } finally { setDayLoading(false); }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadDay = useCallback(async (logDate, { updateUrl = true } = {}) => {
    if (updateUrl && isValidLogDate(logDate)) {
      const view = searchParams.get('view');
      const item = searchParams.get('item');
      const qs = new URLSearchParams();
      if (view && view !== 'summary') qs.set('view', view);
      if (item) qs.set('item', item);
      const suffix = qs.toString() ? `?${qs.toString()}` : '';
      navigate(`${paths.summitDay(logDate)}${suffix}`);
    }
    await fetchDay(logDate);
  }, [fetchDay, navigate, searchParams]);

  // ── Calendar navigation ───────────────────────────────────────────────────
  const goPrev = () => { if (month === 1) { setYear(y => y - 1); setMonth(12); } else setMonth(m => m - 1); };
  const goNext = () => { if (month === 12) { setYear(y => y + 1); setMonth(1); } else setMonth(m => m + 1); };
  const goToday = () => {
    const t = new Date();
    setYear(t.getFullYear()); setMonth(t.getMonth() + 1);
    loadDay(fmtDate(t.getFullYear(), t.getMonth() + 1, t.getDate()));
  };

  const handleViewTabChange = (_, v) => {
    // Update state immediately for instant visual feedback, then sync URL.
    // The useEffect below guards against double-update by checking prev value.
    setViewTab(v);
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      if (!v || v === 'summary') next.delete('view');
      else next.set('view', v);
      return next;
    }, { replace: true });
  };

  const openSearchRoute = () => {
    navigate(paths.summitSearch);
  };

  const openYearRoute = (y) => {
    navigate(paths.summitYear(y));
  };

  useEffect(() => {
    // Sync URL → state (for deep links / browser back-forward).
    // Guard against no-op updates to prevent the double-render glitch on tab clicks.
    const v = searchParams.get('view');
    const target = (v && SUMMIT_VIEW_TABS.includes(v)) ? v : 'summary';
    setViewTab((prev) => (prev === target ? prev : target));
  }, [searchParams]);

  useEffect(() => {
    if (!routeDate || !isValidLogDate(routeDate)) return;
    const [y, m] = routeDate.split('-').map(Number);
    setYear(y);
    setMonth(m);
    fetchDay(routeDate);
  }, [routeDate, fetchDay]);

  useEffect(() => {
    const itemId = searchParams.get('item');
    if (!itemId || !selectedDate) return;
    const id = parseInt(itemId, 10);
    if (Number.isNaN(id)) return;
    setHighlightItemId(id);
    const t = setTimeout(() => {
      const el = document.getElementById(`log-item-${id}`);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(() => setHighlightItemId(null), 3000);
    }, 400);
    return () => clearTimeout(t);
  }, [searchParams, selectedDate, dayData]);

  useEffect(() => {
    if (routePanel !== 'year') return;
    const m = location.pathname.match(/\/summit\/years\/(\d+)$/);
    if (m) {
      const y = parseInt(m[1], 10);
      if (!isNaN(y)) {
        setYear(y);
        setYearOverviewOpen(true);
      }
    }
  }, [routePanel, location.pathname]);

  useEffect(() => {
    if (!isSearchRoute) return;
    const t = setTimeout(() => {
      searchSectionRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 200);
    return () => clearTimeout(t);
  }, [isSearchRoute]);

  useEffect(() => {
    if (!isSearchRoute) return;
    const q = searchParams.get('q');
    if (!q?.trim()) return;
    setSearchQ(q);
    setSearchFromDate(searchParams.get('from_date') || '');
    setSearchToDate(searchParams.get('to_date') || '');
    setSearchCrew(searchParams.get('crew_tab') || '');
    const run = async () => {
      setSearchLoading(true);
      setSearchError(null);
      setSearchOffset(0);
      try {
        const params = { q: q.trim(), limit: SEARCH_LIMIT, offset: 0 };
        const from = searchParams.get('from_date');
        const to = searchParams.get('to_date');
        const crew = searchParams.get('crew_tab');
        if (from) params.from_date = from;
        if (to) params.to_date = to;
        if (crew) params.crew_tab = crew;
        setSearchResult(await summitAPI.search(params));
      } catch (e) {
        const msg = e.response?.data?.detail || e.message || 'Search failed';
        setSearchError(msg);
        notify(msg);
      } finally {
        setSearchLoading(false);
      }
    };
    run();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isSearchRoute, searchParams.toString()]);

  const daysInMonth = new Date(year, month, 0).getDate();
  const firstWd = new Date(year, month - 1, 1).getDay();
  const calCells = [];
  for (let i = 0; i < firstWd; i++) calCells.push({ key: `p${i}`, empty: true });
  for (let d = 1; d <= daysInMonth; d++) calCells.push({ key: `d${d}`, day: d });

  // ── Day header edit ───────────────────────────────────────────────────────
  const startEditHeader = () => {
    setHeaderForm({
      day_label: dayData?.day_label || '',
      history_text: dayData?.history_text || '',
      zoom_meeting_id: dayData?.zoom_meeting_id || '',
      zoom_password: dayData?.zoom_password || '',
      zoom_join_url: dayData?.zoom_join_url || '',
    });
    setEditingHeader(true);
  };
  const saveHeader = async () => {
    setHeaderSaving(true);
    try {
      await summitAPI.patchDay(selectedDate, {
        day_label: headerForm.day_label || null,
        history_text: headerForm.history_text || null,
        zoom_meeting_id: headerForm.zoom_meeting_id || null,
        zoom_password: headerForm.zoom_password || null,
        zoom_join_url: headerForm.zoom_join_url || null,
      });
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
      const body = { log_date: newDayDate };
      if (newDayLabel.trim()) body.day_label = newDayLabel.trim();
      if (newDayHistory.trim()) body.history_text = newDayHistory.trim();
      await summitAPI.createDay(body);
      notify('Summit day created', 'success');
      setCreateDayOpen(false); setNewDayDate(''); setNewDayLabel(''); setNewDayHistory('');
      await loadMonthly();
      loadDay(newDayDate);
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to create day'); }
    finally { setCreateDaySaving(false); }
  };

  // ── Log item CRUD ────────────────────────────────────────────────────────
  const beginCreate = (crewTab = 'TO') => {
    setEditor({ ...EMPTY_EDITOR, crewTab, itemTime: nowHSThmm(), createdBy: user?.username || '' });
    setEditorCard(crewTab);
    setEditorOpen(true);
  };
  const beginEdit = (item) => {
    setEditorCard(item.crew_tab || 'TO'); // pin editor to the item's card
    setEditor({
      itemId: item.id, crewTab: item.crew_tab || 'ALL',
      title: item.title || '', body: item.body || '',
      itemType: item.item_type || 'Comment', status: item.status || 'Completed',
      subsystem: item.subsystem || '',
      itemTime: item.item_time ? formatTimeHST(item.item_time) : '',
      downtimeMinutes: item.downtime_minutes != null ? String(item.downtime_minutes) : '',
      createdBy: item.created_by || '',
      summitAccess: item.summit_access || 'Choose',
      historyText: item.history_text || '',
      commentText: item.comment_text || '',
      workPlanId: item.work_plan_id || '',
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
        summit_access: editor.summitAccess === 'Choose' ? null : (editor.summitAccess || null),
        history_text: editor.historyText || null,
        comment_text: editor.commentText || null,
        work_plan_id: editor.workPlanId || null,
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
      setEditorOpen(false); setEditorCard(null); setEditor(EMPTY_EDITOR);
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to save'); }
    finally { setEditorSaving(false); }
  };
  const deleteItem = async (itemId) => {
    if (!window.confirm('Delete this log entry?')) return;
    try {
      await summitAPI.deleteLogItem(itemId);
      notify('Deleted', 'success');
      await loadDay(selectedDate);
      if (editor.itemId === itemId) { setEditorOpen(false); setEditorCard(null); setEditor(EMPTY_EDITOR); }
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
      if (crewForm.id) { await summitAPI.updateCrew(crewForm.id, selectedDate, payload); notify('Crew updated', 'success'); }
      else { await summitAPI.createCrew(selectedDate, payload); notify('Crew added', 'success'); }
      setCrewDialogOpen(false);
      await loadDay(selectedDate);
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to save crew'); }
    finally { setCrewSaving(false); }
  };
  const deleteCrew = async (id) => {
    if (!window.confirm('Remove this crew member?')) return;
    try { await summitAPI.deleteCrew(id, selectedDate); notify('Crew removed', 'success'); await loadDay(selectedDate); }
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

  // Pre-fill the Add Program dialog from an OPAL Programs row (clients.alloc)
  const copyOpalProgram = (op) => {
    setProgramEditing({
      instr: op.instr || 'Choose', alloc: 'Choose', pi: op.pi || '',
      ao1: '', ao2: '', gid: op.gid || '', propid: op.propid || '',
      slotStart: '', slotEnd: '',
      // Observers: remote goes into obs1, on-site into obs2
      obs1: op.remote || '', obs1loc: op.remote ? 'Remote' : '',
      obs2: op.observers || '', obs2loc: op.observers ? 'Summit' : '',
      obs3: '', obs3loc: '', obs4: '', obs4loc: '',
      // Staff astronomers
      ss: op.staff || '', ssloc: '', ss2: '', ss2loc: '',
      others1: '', others1loc: '', others2: '', others2loc: '',
      notes: '', comment_text: op.comment || '',
    });
    setProgramDialogOpen(true);
  };
  const openEditProgram = (p) => {
    setProgramEditing({
      id: p.id, instr: p.instr || 'Choose', alloc: p.alloc || 'Choose', pi: p.pi || '',
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
      id: wp.id,
      comptitle: wp.comptitle || '', plan_text: wp.plan_text || '',
      requestor: wp.requestor || '', contact2: wp.contact2 || '', others: wp.others || '',
      wp_status: wp.wp_status || 'Planned', wp_type: wp.wp_type || 'Comment',
      wp_subsystem: wp.wp_subsystem || '-none-',
      windowStart: wp.window_start ? formatTimeHST(wp.window_start) : '',
      windowEnd: wp.window_end ? formatTimeHST(wp.window_end) : '',
      day_warning: wp.day_warning || '', nite_warning: wp.nite_warning || '',
      location: wp.location || '.none', location2: wp.location2 || '.none', location3: wp.location3 || '.none',
      assigned1: wp.assigned1 || '.none', assigned2: wp.assigned2 || '',
      dcassist: wp.dcassist || '.none', notify: wp.notify || '.none',
      teampass: wp.teampass || '', otherreq: wp.otherreq || '',
      realstart: wp.realstart ? formatTimeHST(wp.realstart) : '',
      realend: wp.realend ? formatTimeHST(wp.realend) : '',
      completion_title: wp.completion_title || '', comptext: wp.comptext || '',
      req_flags: wp.req_flags || '', lockout_flags: wp.lockout_flags || '',
      nite_effect: wp.nite_effect || '', day_effect: wp.day_effect || '',
      intervene: wp.intervene || 'Choose', melco: wp.melco || '', fai: wp.fai || '',
      master: wp.master != null ? String(wp.master) : '',
      notes: wp.notes || '',
    });
    setWpDialogOpen(true);
  };
  const saveWP = async (form) => {
    setWpSaving(true);
    try {
      const n = (v) => v || null;
      const numOrNull = (v) => {
        if (v === '' || v == null || v === undefined) return null;
        const x = Number(v);
        return Number.isNaN(x) ? null : x;
      };
      const dot = (v) => (v === '.none' || v === '-none-' || v === '' || v == null) ? null : v;
      const payload = {
        comptitle: n(form.comptitle), plan_text: n(form.plan_text),
        requestor: n(form.requestor), contact1: n(form.requestor), contact2: n(form.contact2), others: n(form.others),
        wp_status: n(form.wp_status), wp_type: n(form.wp_type),
        wp_subsystem: dot(form.wp_subsystem),
        day_warning: n(form.day_warning), nite_warning: n(form.nite_warning),
        teampass: n(form.teampass), otherreq: n(form.otherreq),
        req_flags: n(form.req_flags), lockout_flags: n(form.lockout_flags),
        nite_effect: n(form.nite_effect), day_effect: n(form.day_effect),
        location: dot(form.location), location2: dot(form.location2), location3: dot(form.location3),
        assigned1: dot(form.assigned1), assigned2: n(form.assigned2),
        dcassist: dot(form.dcassist), notify: dot(form.notify),
        intervene: form.intervene === 'Choose' ? null : n(form.intervene),
        melco: n(form.melco), fai: n(form.fai),
        master: numOrNull(form.master),
        completion_title: n(form.completion_title), comptext: n(form.comptext),
        notes: n(form.notes),
        window_start: form.windowStart ? toUtcIso(selectedDate, form.windowStart) : null,
        window_end: form.windowEnd ? toUtcIso(selectedDate, form.windowEnd) : null,
        realstart: form.realstart ? toUtcIso(selectedDate, form.realstart) : null,
        realend: form.realend ? toUtcIso(selectedDate, form.realend) : null,
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

  // ── Copy Work Plan ────────────────────────────────────────────────────────
  const openCopyWP = async () => {
    setCopyWPOpen(true);
    if (recentWPs.length > 0) return;   // already loaded
    setRecentWPsLoading(true);
    try {
      const username = user?.username || '';
      const data = await summitAPI.getRecentWorkPlans(username, 20);
      setRecentWPs(data);
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to load recent work plans'); }
    finally { setRecentWPsLoading(false); }
  };
  const copyWP = async (planId) => {
    if (!selectedDate) return;
    try {
      await summitAPI.copyWorkPlan(planId, selectedDate);
      notify('Work plan copied to ' + selectedDate, 'success');
      setCopyWPOpen(false);
      await loadDay(selectedDate);
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to copy work plan'); }
  };

  // ── Send Email ────────────────────────────────────────────────────────────
  const sendEmail = async (emailType) => {
    if (!selectedDate) return;
    setEmailSending(emailType);
    try {
      const result = await summitAPI.sendEmail(selectedDate, emailType);
      notify(result.message || 'Email sent', 'success');
      await loadDay(selectedDate);
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to send email'); }
    finally { setEmailSending(null); }
  };

  const viewEmailPreview = async (emailType) => {
    if (!selectedDate) return;
    setEmailPreviewLoading(true);
    setEmailPreview(null);
    try {
      const res = await summitAPI.previewEmail(selectedDate, emailType);
      setEmailPreview({ type: emailType, body: res.body });
    } catch (e) { notify(e.response?.data?.detail || e.message || 'Failed to load preview'); }
    finally { setEmailPreviewLoading(false); }
  };

  // ── Search ────────────────────────────────────────────────────────────────
  const runSearch = async (offsetOverride = 0) => {
    const q = searchQ.trim();
    if (!q) return;
    const off = offsetOverride;
    if (off === 0) {
      const qs = new URLSearchParams({ q });
      if (searchFromDate) qs.set('from_date', searchFromDate);
      if (searchToDate) qs.set('to_date', searchToDate);
      if (searchCrew) qs.set('crew_tab', searchCrew);
      const target = `${paths.summitSearch}?${qs.toString()}`;
      if (location.pathname + location.search !== target) {
        navigate(target);
        if (!isSearchRoute) return;
      }
    }
    setSearchLoading(true);
    setSearchError(null);
    setSearchOffset(off);
    try {
      const params = { q, limit: SEARCH_LIMIT, offset: off };
      if (searchFromDate) params.from_date = searchFromDate;
      if (searchToDate) params.to_date = searchToDate;
      if (searchCrew) params.crew_tab = searchCrew;
      const data = await summitAPI.search(params);
      setSearchResult(off === 0 ? data : (prev) => ({ total: data.total, items: [...(prev?.items || []), ...data.items] }));
    } catch (e) {
      const msg = e.response?.data?.detail || e.message || 'Search failed';
      setSearchError(msg);
      notify(msg);
    } finally {
      setSearchLoading(false);
    }
  };

  // ── Derived filtered lists ────────────────────────────────────────────────
  const toRows = useMemo(() => (dayData?.log_items || []).filter(i => i.crew_tab === 'TO'), [dayData]);
  const ioRows = useMemo(() => (dayData?.log_items || []).filter(i => i.crew_tab === 'IO'), [dayData]);
  const dcRows = useMemo(() => (dayData?.log_items || []).filter(i => i.crew_tab === 'DC'), [dayData]);
  const wpRows = useMemo(() => (dayData?.log_items || []).filter(i => i.crew_tab === 'WP'), [dayData]);
  const troubleRows = useMemo(() => (dayData?.log_items || []).filter(i => (i.item_type || '').toLowerCase() === 'trouble'), [dayData]);
  const dayIsEmpty = useMemo(() => {
    if (!dayData) return false;
    return (
      (dayData.entry_count ?? dayData.log_items?.length ?? 0) === 0
      && (dayData.crew_assignments || []).length === 0
      && (dayData.programs || []).length === 0
    );
  }, [dayData]);

  const renderEmptyDayHint = () => (
    <Alert severity="info" sx={{ m: 2 }}>
      No log entries or crew recorded for {selectedDate} yet.
      {(monthPayload?.days || []).some((d) => (d.entry_count || 0) > 0) && (
        <> Select a highlighted date on the calendar to view historical summit logs, or add crew and entries below.</>
      )}
    </Alert>
  );

  const totalDowntime = useMemo(
    () => (dayData?.log_items || []).reduce((s, i) => s + (Number(i.downtime_minutes) || 0), 0),
    [dayData],
  );

  const openFatsFromItem = useCallback((item, logDate) => {
    if (onCreateFatsFromSummit) onCreateFatsFromSummit({ item, logDate });
  }, [onCreateFatsFromSummit]);

  // ── Render helpers ────────────────────────────────────────────────────────
  // showAddButton: set false when the parent renders the button / editor itself
  const renderLogList = (rows, defaultCrew, showAddButton = true) => (
    <>
      {showAddButton && !editorOpen && (
        <Button variant="contained" size="small" startIcon={<AddIcon />} sx={{ mb: 1.5, borderRadius: 2, fontWeight: 600 }}
          onClick={() => beginCreate(defaultCrew)}>
          New {defaultCrew} Entry
        </Button>
      )}
      {/* Editor inside section – only for tabs that pass showAddButton=true (DC, WP, …) */}
      {showAddButton && editorOpen && (
        <LogItemEditor editor={editor} setEditor={setEditor} onSave={saveEditor}
          onCancel={() => { setEditorOpen(false); setEditorCard(null); setEditor(EMPTY_EDITOR); }}
          saving={editorSaving} selectedDate={selectedDate}
          workPlans={dayData?.work_plans || []}
          showDowntime={defaultCrew !== 'DC'} />
      )}
      {rows.length === 0 ? (
        <Typography variant="body2" color="text.secondary">No {defaultCrew} entries for this day.</Typography>
      ) : (
        rows.map((item) => (
          <LogItemRow
            key={item.id}
            item={item}
            onEdit={beginEdit}
            onDelete={deleteItem}
            onCreateFatsFromSummit={onCreateFatsFromSummit ? openFatsFromItem : undefined}
            logDate={selectedDate}
            highlighted={highlightItemId === item.id}
          />
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
                const hasEntries = has && (stats?.entry_count || 0) > 0;
                const isSel = selectedDate === logDate;
                const hasDowntime = hasEntries && stats?.total_downtime > 0;
                return (
                  <Tooltip key={cell.key}
                    title={hasEntries ? `${stats?.entry_count || 0} entries · ${stats?.total_downtime || 0} min downtime` : has ? 'Day record (no entries yet)' : 'No log'}
                    placement="top" arrow>
                    <Box sx={{ textAlign: 'center' }}>
                      <Button fullWidth size="small"
                        onClick={() => loadDay(logDate)}
                        sx={{
                          minWidth: 0, py: 0.5, flexDirection: 'column', lineHeight: 1.1, fontSize: '0.8rem',
                          borderRadius: 1.5, fontWeight: isSel ? 700 : hasEntries ? 600 : has ? 500 : 400,
                          background: isSel
                            ? 'linear-gradient(135deg, #00695c, #00897b)'
                            : hasEntries ? 'rgba(0,105,92,0.08)' : has ? 'rgba(0,105,92,0.03)' : 'transparent',
                          color: isSel ? '#fff' : hasEntries ? '#00695c' : has ? '#546e7a' : 'text.secondary',
                          border: hasEntries && !isSel ? '1px solid #00897b55' : isSel ? 'none' : '1px solid transparent',
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

      {/* ── Year at a glance ── */}
      <Paper elevation={2} sx={{ mb: 2.5, borderRadius: 2.5, overflow: 'hidden' }}>
        <Box sx={{
          px: 2, py: 1.25,
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          flexWrap: 'wrap', gap: 1,
          background: 'linear-gradient(90deg,#eceff1,#e3f2fd)',
          borderBottom: yearOverviewOpen ? '1px solid' : 'none',
          borderColor: 'divider',
        }}>
          <Typography variant="subtitle2" fontWeight={700} sx={{ color: 'text.secondary' }}>
            Annual overview
          </Typography>
          <Button
            size="small"
            variant="outlined"
            endIcon={yearOverviewOpen ? <ExpandLess /> : <ExpandMore />}
            onClick={() => {
              if (yearOverviewOpen) {
                setYearOverviewOpen(false);
                if (routePanel === 'year') {
                  if (selectedDate) navigate(paths.summitDay(selectedDate));
                  else navigate(paths.summitToday());
                }
              } else {
                openYearRoute(year);
                setYearOverviewOpen(true);
              }
            }}
            sx={{ fontWeight: 600, textTransform: 'none', borderRadius: 2 }}
          >
            {year} at a glance
          </Button>
        </Box>
        <Collapse in={yearOverviewOpen}>
          <Box sx={{ p: 2 }}>
            {yearLoading && (
              <Box sx={{ display: 'flex', justifyContent: 'center', py: 2 }}><CircularProgress size={26} /></Box>
            )}
            {yearError && <Alert severity="error" sx={{ mb: 1 }}>{yearError}</Alert>}
            {!yearLoading && !yearError && yearPayload && (yearPayload.days || []).length === 0 && (
              <Alert severity="info">No summit days recorded for {year}.</Alert>
            )}
            {!yearLoading && !yearError && yearPayload && (yearPayload.days || []).length > 0 && (
              <TableContainer sx={{ maxHeight: 420 }}>
                <Table size="small" stickyHeader>
                  <TableHead>
                    <TableRow>
                      <TableCell sx={{ fontWeight: 700 }}>Date</TableCell>
                      <TableCell sx={{ fontWeight: 700 }}>Label</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 700 }}>Entries</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 700 }}>Downtime</TableCell>
                      <TableCell sx={{ fontWeight: 700 }}>1st instr.</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {(yearPayload.days || []).map((row) => {
                      const d = parseDate(row.log_date);
                      return (
                        <TableRow
                          key={row.id || d}
                          hover
                          sx={{ cursor: 'pointer', '&:last-child td': { borderBottom: 0 } }}
                          onClick={() => {
                            const [y, m] = d.split('-').map(Number);
                            setYear(y);
                            setMonth(m);
                            loadDay(d);
                          }}
                        >
                          <TableCell>
                            {(() => {
                              try {
                                return new Date(`${d}T12:00:00`).toLocaleDateString(undefined, {
                                  weekday: 'short', month: 'short', day: 'numeric', year: 'numeric',
                                });
                              } catch {
                                return d;
                              }
                            })()}
                          </TableCell>
                          <TableCell>{row.day_label || '—'}</TableCell>
                          <TableCell align="right">{row.entry_count ?? 0}</TableCell>
                          <TableCell align="right">
                            {(row.total_downtime > 0) ? `${row.total_downtime} min` : '—'}
                          </TableCell>
                          <TableCell sx={{ color: row.first_instr ? 'text.primary' : 'text.disabled' }}>
                            {row.first_instr || '—'}
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
            {!yearLoading && !yearError && yearPayload && (
              <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
                Click a row to open that day in the calendar and detail panel below.
              </Typography>
            )}
          </Box>
        </Collapse>
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
                <Typography variant="caption" sx={{ opacity: 0.9, fontWeight: 600 }}>Video meeting (optional)</Typography>
                <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1}>
                  <TextField size="small" label="Zoom meeting ID" value={headerForm.zoom_meeting_id}
                    onChange={(e) => setHeaderForm(p => ({ ...p, zoom_meeting_id: e.target.value }))}
                    sx={{ flex: 1, '& .MuiInputBase-root': { color: '#fff', bgcolor: 'rgba(255,255,255,0.15)' },
                      '& .MuiInputLabel-root': { color: 'rgba(255,255,255,0.8)' },
                      '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255,255,255,0.4)' } }} />
                  <TextField size="small" label="Zoom password" value={headerForm.zoom_password}
                    onChange={(e) => setHeaderForm(p => ({ ...p, zoom_password: e.target.value }))}
                    sx={{ flex: 1, '& .MuiInputBase-root': { color: '#fff', bgcolor: 'rgba(255,255,255,0.15)' },
                      '& .MuiInputLabel-root': { color: 'rgba(255,255,255,0.8)' },
                      '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255,255,255,0.4)' } }} />
                </Stack>
                <TextField size="small" fullWidth label="Join URL" value={headerForm.zoom_join_url}
                  onChange={(e) => setHeaderForm(p => ({ ...p, zoom_join_url: e.target.value }))}
                  sx={{ '& .MuiInputBase-root': { color: '#fff', bgcolor: 'rgba(255,255,255,0.15)' },
                    '& .MuiInputLabel-root': { color: 'rgba(255,255,255,0.8)' },
                    '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255,255,255,0.4)' } }} />
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
                  {(dayData?.zoom_meeting_id || dayData?.zoom_join_url) && (
                    <Stack direction="row" spacing={1} alignItems="center" flexWrap="wrap" useFlexGap sx={{ mt: 1 }}>
                      {dayData.zoom_meeting_id && (
                        <Chip size="small" label={`Zoom: ${dayData.zoom_meeting_id}`}
                          sx={{ bgcolor: 'rgba(255,255,255,0.18)', color: '#fff', fontWeight: 600 }} />
                      )}
                      {dayData.zoom_password && (
                        <Chip size="small" label={`PW: ${dayData.zoom_password}`}
                          sx={{ bgcolor: 'rgba(255,255,255,0.12)', color: '#fff' }} />
                      )}
                      {dayData.zoom_join_url && (
                        <Link href={dayData.zoom_join_url} target="_blank" rel="noopener noreferrer"
                          sx={{ color: '#b3e5fc', fontWeight: 600, fontSize: '0.85rem' }}>
                          Open join link
                        </Link>
                      )}
                    </Stack>
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
          {dayIsEmpty && !dayLoading && !dayError && renderEmptyDayHint()}

          {!dayLoading && dayData && (
            <Box sx={{ px: 0 }}>
              <Tabs value={viewTab} onChange={handleViewTabChange} variant="scrollable" scrollButtons="auto"
                TabScrollButtonProps={{ sx: { opacity: 1 } }}
                sx={{ borderBottom: '1px solid', borderColor: 'divider', px: 1,
                  minHeight: 44,
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
              <Box sx={{ p: 2, minHeight: 400 }}>

              {/* ── Summary Tab ── */}
              {viewTab === 'summary' && (() => {
                const troubleItems = (dayData.log_items || []).filter(i => i.item_type === 'Trouble');
                const totalDowntime = troubleItems.reduce((s, i) => s + (i.downtime_minutes || 0), 0);
                return (
                <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '3fr 2fr' }, gap: 2 }}>
                  <Box>
                    <SectionCard title={`All Log Entries (${(dayData.log_items || []).length})`} accent={SUMMIT_GRADIENT}>
                      {(dayData.log_items || []).length === 0
                        ? <Typography variant="body2" color="text.secondary">No entries yet.</Typography>
                        : (dayData.log_items || []).map((item) => (
                          <LogItemRow
                            key={item.id}
                            item={item}
                            onEdit={beginEdit}
                            onDelete={deleteItem}
                            onCreateFatsFromSummit={onCreateFatsFromSummit ? openFatsFromItem : undefined}
                            logDate={selectedDate}
                            highlighted={highlightItemId === item.id}
                          />
                        ))
                      }
                    </SectionCard>
                  </Box>
                  <Stack spacing={2}>
                    {/* Trouble summary */}
                    <SectionCard
                      title={`⚠ Trouble Summary${totalDowntime > 0 ? ` — ${totalDowntime} min downtime` : ''}`}
                      accent="linear-gradient(90deg,#b71c1c,#c62828)"
                    >
                      {troubleItems.length === 0
                        ? <Typography variant="body2" color="text.secondary">No trouble entries.</Typography>
                        : (<>
                          <TableContainer>
                            <Table size="small">
                              <TableHead>
                                <TableRow>
                                  <TableCell sx={{ fontWeight: 700, fontSize: '0.72rem', py: 0.5 }}>Time</TableCell>
                                  <TableCell sx={{ fontWeight: 700, fontSize: '0.72rem', py: 0.5 }}>Subsystem</TableCell>
                                  <TableCell sx={{ fontWeight: 700, fontSize: '0.72rem', py: 0.5 }}>Title</TableCell>
                                  <TableCell sx={{ fontWeight: 700, fontSize: '0.72rem', py: 0.5 }}>DT(m)</TableCell>
                                </TableRow>
                              </TableHead>
                              <TableBody>
                                {troubleItems.map(it => (
                                  <TableRow key={it.id} sx={{ '&:last-child td': { borderBottom: 0 } }}>
                                    <TableCell sx={{ fontSize: '0.75rem', whiteSpace: 'nowrap', py: 0.5 }}>
                                      {formatTimeHST(it.item_time)}
                                    </TableCell>
                                    <TableCell sx={{ fontSize: '0.75rem', py: 0.5 }}>
                                      {it.subsystem || '—'}
                                    </TableCell>
                                    <TableCell sx={{ fontSize: '0.75rem', py: 0.5, maxWidth: 200 }}>
                                      <Typography variant="inherit" noWrap title={it.title}>{it.title || '—'}</Typography>
                                    </TableCell>
                                    <TableCell sx={{ fontSize: '0.75rem', py: 0.5 }}>
                                      {it.downtime_minutes > 0 ? it.downtime_minutes : '—'}
                                    </TableCell>
                                  </TableRow>
                                ))}
                              </TableBody>
                            </Table>
                          </TableContainer>
                          <Typography variant="caption" sx={{ mt: 0.5, display: 'block', color: 'error.dark', fontWeight: 700 }}>
                            Total downtime: {totalDowntime} min
                          </Typography>
                        </>)
                      }
                    </SectionCard>
                    {/* Observation Programs summary */}
                    <SectionCard title={`🔭 Observation Programs (${(dayData.programs || []).length})`}
                      accent="linear-gradient(90deg,#00695c,#00897b)">
                      {(dayData.programs || []).length === 0
                        ? <Typography variant="body2" color="text.secondary">No programs scheduled.</Typography>
                        : (
                          <TableContainer>
                            <Table size="small">
                              <TableHead>
                                <TableRow>
                                  {['Seq','Program','Instr','Alloc','PI','Time'].map(h => (
                                    <TableCell key={h} sx={{ fontWeight: 700, fontSize: '0.72rem', py: 0.5 }}>{h}</TableCell>
                                  ))}
                                </TableRow>
                              </TableHead>
                              <TableBody>
                                {(dayData.programs || []).map(p => (
                                  <TableRow key={p.id} sx={{ '&:last-child td': { borderBottom: 0 } }}>
                                    <TableCell sx={{ fontSize: '0.75rem', py: 0.5 }}>{p.sort_order + 1}</TableCell>
                                    <TableCell sx={{ fontSize: '0.75rem', py: 0.5, fontWeight: 600 }}>{p.program_code || p.gid || '—'}</TableCell>
                                    <TableCell sx={{ fontSize: '0.75rem', py: 0.5 }}>{p.instr || '—'}</TableCell>
                                    <TableCell sx={{ fontSize: '0.75rem', py: 0.5 }}>{p.alloc || '—'}</TableCell>
                                    <TableCell sx={{ fontSize: '0.75rem', py: 0.5 }}>
                                      <Typography variant="inherit" noWrap title={p.pi} sx={{ maxWidth: 80 }}>{p.pi || '—'}</Typography>
                                    </TableCell>
                                    <TableCell sx={{ fontSize: '0.75rem', py: 0.5, whiteSpace: 'nowrap' }}>
                                      {formatTimeHST(p.slot_start)}
                                      {p.slot_end ? ` – ${formatTimeHST(p.slot_end)}` : ''}
                                    </TableCell>
                                  </TableRow>
                                ))}
                              </TableBody>
                            </Table>
                          </TableContainer>
                        )
                      }
                    </SectionCard>
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
                    {/* Email status — always shown */}
                    <SectionCard title="✉ Email Delivery" accent="linear-gradient(90deg,#4527a0,#5e35b1)">
                      {/* Send / View buttons */}
                      {[
                        { type: 'to',    label: 'Night Log (TO)',  color: '#1565c0' },
                        { type: 'dc',    label: 'Day Crew (DC)',   color: '#e65100' },
                        { type: 'smoka', label: 'SMOKA Archive',   color: '#1b5e20' },
                      ].map(({ type, label, color }) => (
                        <Stack key={type} direction="row" spacing={0.75} sx={{ mb: 0.75 }} alignItems="center">
                          <Button
                            size="small"
                            variant="outlined"
                            startIcon={emailSending === type ? <CircularProgress size={14} /> : <EmailIcon fontSize="small" />}
                            disabled={!!emailSending}
                            onClick={() => sendEmail(type)}
                            sx={{ borderRadius: 2, fontSize: '0.72rem', borderColor: color, color, minWidth: 140,
                              '&:hover': { bgcolor: `${color}12` } }}
                          >
                            {emailSending === type ? 'Sending…' : `Send ${label}`}
                          </Button>
                          <Tooltip title={`Preview ${label} before sending`}>
                            <Button
                              size="small"
                              variant="outlined"
                              disabled={emailPreviewLoading}
                              startIcon={<VisibilityIcon fontSize="small" />}
                              onClick={() => viewEmailPreview(type)}
                              sx={{
                                fontSize: '0.72rem', borderRadius: 2,
                                borderColor: '#7b1fa2', color: '#7b1fa2',
                                '&:hover': { bgcolor: '#7b1fa210' },
                              }}
                            >
                              {emailPreviewLoading ? 'Loading…' : 'Preview'}
                            </Button>
                          </Tooltip>
                        </Stack>
                      ))}
                      <Box sx={{ mb: 1 }} />
                      {!dayData.email_delivery ? (
                        <Typography variant="body2" color="text.secondary">
                          No email delivery record for this day yet.
                        </Typography>
                      ) : (
                        <Stack spacing={0.75}>
                          {[
                            ['Night digest',  dayData.email_delivery.mailed,    dayData.email_delivery.mailtime],
                            ['Smoka archive', dayData.email_delivery.mailsmoka,  dayData.email_delivery.smokatime],
                            ['Day digest',    dayData.email_delivery.mailday,    dayData.email_delivery.maildtime],
                          ].map(([label, flag, ts]) => (
                            <Stack key={label} direction="row" spacing={1} alignItems="center">
                              <Typography variant="caption" sx={{ minWidth: 90, color: 'text.secondary' }}>{label}</Typography>
                              <Chip size="small" label={flag === 'Y' ? 'Sent' : 'Pending'}
                                color={flag === 'Y' ? 'success' : 'default'} variant="outlined"
                                sx={{ fontSize: '0.67rem', height: 20 }} />
                              {flag === 'Y' && ts && (
                                <Typography variant="caption" color="text.secondary">{formatDateHST(ts)}</Typography>
                              )}
                            </Stack>
                          ))}
                          {dayData.email_delivery.last_error && (
                            <Alert severity="warning" sx={{ py: 0.25, px: 1, fontSize: '0.72rem', mt: 0.5 }}>
                              Last error: {dayData.email_delivery.last_error}
                            </Alert>
                          )}
                        </Stack>
                      )}
                    </SectionCard>
                  </Stack>
                </Box>
                );
              })()}

              {/* ── TO / IO Tab — combined chronological view ── */}
              {viewTab === 'toio' && (() => {
                const toioRows = [...toRows, ...ioRows].sort((a, b) => {
                  const at = a.item_time ? new Date(a.item_time).getTime() : 0;
                  const bt = b.item_time ? new Date(b.item_time).getTime() : 0;
                  return at - bt;
                });
                return (
                  <SectionCard
                    title={`🔭🎯 TO / IO Combined Timeline (${toioRows.length} entries — TO: ${toRows.length}, IO: ${ioRows.length})`}
                    accent="linear-gradient(90deg,#1a237e,#283593)"
                    action={
                      <Stack direction="row" spacing={0.75}>
                        {!(editorOpen && editorCard === 'TO') && (
                          <Button size="small" startIcon={<AddIcon />} onClick={() => beginCreate('TO')}
                            sx={{ color: '#fff', bgcolor: 'rgba(25,118,210,0.5)', borderRadius: 1.5, fontSize: '0.73rem',
                              '&:hover': { bgcolor: 'rgba(25,118,210,0.8)' } }}>
                            + TO
                          </Button>
                        )}
                        {!(editorOpen && editorCard === 'IO') && (
                          <Button size="small" startIcon={<AddIcon />} onClick={() => beginCreate('IO')}
                            sx={{ color: '#fff', bgcolor: 'rgba(46,125,50,0.5)', borderRadius: 1.5, fontSize: '0.73rem',
                              '&:hover': { bgcolor: 'rgba(46,125,50,0.8)' } }}>
                            + IO
                          </Button>
                        )}
                      </Stack>
                    }
                  >
                    {editorOpen && (editorCard === 'TO' || editorCard === 'IO') && (
                      <LogItemEditor editor={editor} setEditor={setEditor} onSave={saveEditor}
                        onCancel={() => { setEditorOpen(false); setEditorCard(null); setEditor(EMPTY_EDITOR); }}
                        saving={editorSaving} selectedDate={selectedDate}
                        workPlans={dayData?.work_plans || []} />
                    )}
                    {toioRows.length === 0
                      ? <Typography variant="body2" color="text.secondary">No TO or IO entries for this day.</Typography>
                      : toioRows.map((item) => (
                        <Box key={item.id} sx={{ display: 'flex', gap: 1, alignItems: 'flex-start', mb: 0.5 }}>
                          <Chip
                            size="small"
                            label={item.crew_tab}
                            color={item.crew_tab === 'TO' ? 'primary' : 'success'}
                            sx={{ mt: 0.5, minWidth: 36, fontWeight: 700, fontSize: '0.7rem' }}
                          />
                          <Box sx={{ flex: 1 }}>
                            <LogItemRow
                              item={item}
                              onEdit={beginEdit}
                              onDelete={deleteItem}
                              onCreateFatsFromSummit={onCreateFatsFromSummit ? openFatsFromItem : undefined}
                              logDate={selectedDate}
                              highlighted={highlightItemId === item.id}
                            />
                          </Box>
                        </Box>
                      ))
                    }
                  </SectionCard>
                );
              })()}

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
                    <Stack direction="row" spacing={0.75}>
                      <Button size="small" startIcon={<AddIcon />} onClick={openAddWP} sx={{ color: '#fff' }}>New</Button>
                      <Button size="small" startIcon={<ContentCopyIcon />} onClick={openCopyWP}
                        sx={{ color: '#fff', bgcolor: 'rgba(255,255,255,0.15)', borderRadius: 1.5, fontSize: '0.72rem',
                          '&:hover': { bgcolor: 'rgba(255,255,255,0.3)' } }}>
                        Copy from Previous
                      </Button>
                    </Stack>
                  }>
                    {(dayData.work_plans || []).length === 0
                      ? <Typography variant="body2" color="text.secondary">No work plans for this day.</Typography>
                      : (dayData.work_plans || []).map((wp) => (
                          <Paper key={wp.id} elevation={2} onClick={() => openEditWP(wp)} sx={{
                            mb: 1.5, borderRadius: 1.5, overflow: 'hidden',
                            borderLeft: '4px solid #7b1fa2',
                            cursor: 'pointer',
                            transition: 'box-shadow 0.2s, transform 0.1s',
                            '&:hover': { boxShadow: 6, transform: 'translateY(-1px)', borderLeft: '4px solid #ab47bc' },
                          }}>
                            {/* WP card header */}
                            <Box sx={{ px: 1.5, py: 1, background: 'linear-gradient(90deg,#f3e5f5,#fce4ec)', borderBottom: '1px solid #e1bee7' }}>
                              <Stack direction="row" alignItems="center" justifyContent="space-between">
                                <Stack direction="row" spacing={1} alignItems="center" flexWrap="wrap" useFlexGap>
                                  <Typography variant="subtitle2" fontWeight={700} sx={{ color: '#6a1b9a' }}>
                                    {wp.comptitle || wp.plan_text || wp.contact1 || wp.requestor || `Work plan #${wp.id}`}
                                  </Typography>
                                  {(wp.window_start || wp.window_end) && (
                                    <Chip size="small" label={`${formatTimeHST(wp.window_start)} – ${formatTimeHST(wp.window_end)} HST`}
                                      sx={{ bgcolor: '#ede7f6', color: '#6a1b9a', fontWeight: 600, fontSize: '0.68rem', height: 20 }} />
                                  )}
                                  {wp.intervene === 'Yes' && (
                                    <Chip size="small" label="⛰ Summit Access" color="warning"
                                      sx={{ fontWeight: 700, fontSize: '0.68rem', height: 20 }} />
                                  )}
                                  {wp.melco && (
                                    <Chip size="small" label={`Melco: ${wp.melco}`} variant="outlined"
                                      sx={{ fontSize: '0.67rem', height: 20, borderColor: '#7b1fa2', color: '#7b1fa2' }} />
                                  )}
                                  {wp.fai && (
                                    <Chip size="small" label={`FAI: ${wp.fai}`} variant="outlined"
                                      sx={{ fontSize: '0.67rem', height: 20, borderColor: '#7b1fa2', color: '#7b1fa2' }} />
                                  )}
                                  {wp.master != null && (
                                    <Chip size="small" label={`Master: ${wp.master}`} variant="outlined"
                                      sx={{ fontSize: '0.67rem', height: 20, borderColor: '#7b1fa2', color: '#6a1b9a' }} />
                                  )}
                                  {wp.seats != null && (
                                    <Chip size="small" label={`Seats: ${wp.seats}`} variant="outlined"
                                      sx={{ fontSize: '0.67rem', height: 20, borderColor: '#7b1fa2', color: '#6a1b9a' }} />
                                  )}
                                  {wp.seats2 != null && (
                                    <Chip size="small" label={`S+2: ${wp.seats2}`} variant="outlined"
                                      sx={{ fontSize: '0.67rem', height: 20, borderColor: '#7b1fa2', color: '#6a1b9a' }} />
                                  )}
                                  {wp.pseats != null && (
                                    <Chip size="small" label={`P-seats: ${wp.pseats}`} variant="outlined"
                                      sx={{ fontSize: '0.67rem', height: 20, borderColor: '#7b1fa2', color: '#6a1b9a' }} />
                                  )}
                                </Stack>
                                <Stack direction="row" spacing={0.25} flexShrink={0}>
                                  <Tooltip title="Delete">
                                    <IconButton size="small" color="error"
                                      onClick={(e) => { e.stopPropagation(); deleteWP(wp.id); }}>
                                      <DeleteIcon fontSize="small" />
                                    </IconButton>
                                  </Tooltip>
                                </Stack>
                              </Stack>
                            </Box>
                            {/* WP card body */}
                            <Box sx={{ px: 1.5, py: 1 }}>
                              <Stack spacing={0.4}>
                                {(wp.nite_effect || wp.day_effect) && (
                                  <Stack direction="row" spacing={2} flexWrap="wrap" useFlexGap>
                                    {wp.nite_effect && <Typography variant="body2"><strong>Night:</strong> {wp.nite_effect}</Typography>}
                                    {wp.day_effect && <Typography variant="body2"><strong>Day:</strong> {wp.day_effect}</Typography>}
                                  </Stack>
                                )}
                                {(wp.requestor || wp.contact1) && (
                                  <Typography variant="body2">
                                    <strong>Requestor:</strong> {wp.requestor || wp.contact1}
                                    {wp.contact2 && `, ${wp.contact2}`}
                                  </Typography>
                                )}
                                {(() => { const a1 = wp.assigned1 && wp.assigned1 !== '.none' ? wp.assigned1 : null;
                                          const a2 = wp.assigned2 && wp.assigned2 !== '.none' ? wp.assigned2 : null;
                                          const dc = wp.dcassist && wp.dcassist !== '.none' ? wp.dcassist : null;
                                          return (a1 || dc) ? (
                                            <Typography variant="body2">
                                              <strong>Assigned:</strong> {[a1, a2].filter(Boolean).join(', ')}
                                              {dc && ` · DC: ${dc}`}
                                            </Typography>
                                          ) : null; })()}
                                {(() => { const locs = [wp.location, wp.location2, wp.location3]
                                            .filter(l => l && l !== '.none');
                                          return locs.length ? (
                                            <Typography variant="body2">
                                              <strong>Location:</strong> {locs.join(' / ')}
                                            </Typography>
                                          ) : null; })()}
                                {wp.plan_text && (
                                  <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                                    {wp.plan_text}
                                  </Typography>
                                )}
                                {wp.req_flags && (
                                  <Typography variant="body2">
                                    <strong>Required:</strong>{' '}
                                    {wp.req_flags.split(',').filter(Boolean).map(f => (
                                      <Chip key={f} label={f} size="small"
                                        sx={{ mr: 0.4, mb: 0.2, bgcolor: '#e3f2fd', color: '#1565c0', fontWeight: 600, fontSize: '0.65rem', height: 18 }} />
                                    ))}
                                  </Typography>
                                )}
                                {wp.lockout_flags && (
                                  <Typography variant="body2">
                                    <strong>LockOuts:</strong>{' '}
                                    {wp.lockout_flags.split(',').filter(Boolean).map(f => (
                                      <Chip key={f} label={f} size="small"
                                        sx={{ mr: 0.4, mb: 0.2, bgcolor: '#ffcdd2', color: '#c62828', fontWeight: 600, fontSize: '0.65rem', height: 18 }} />
                                    ))}
                                  </Typography>
                                )}
                                {wp.comptext && (
                                  <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'pre-wrap', mt: 0.25 }}>
                                    {wp.comptext}
                                  </Typography>
                                )}
                                {wp.pass_text && (
                                  <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'pre-wrap' }}>
                                    <strong>Pass:</strong> {wp.pass_text}
                                  </Typography>
                                )}
                                {wp.rpass_text && (
                                  <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'pre-wrap' }}>
                                    <strong>R-pass:</strong> {wp.rpass_text}
                                  </Typography>
                                )}
                                {wp.notes && (
                                  <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'pre-wrap', fontStyle: 'italic' }}>
                                    {wp.notes}
                                  </Typography>
                                )}
                              </Stack>
                            </Box>
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

                  {/* ── OPAL Programs from Legacy DB (clients.alloc) ── */}
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="subtitle2" fontWeight={700} sx={{ mb: 1, color: '#e65100' }}>
                    📋 OPAL Programs for {selectedDate || '—'} — Legacy Schedule
                  </Typography>
                  {opalProgramsLoading && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <CircularProgress size={16} />
                      <Typography variant="body2" color="text.secondary">Loading from legacy DB…</Typography>
                    </Box>
                  )}
                  {!opalProgramsLoading && opalPrograms.length === 0 && (
                    <Typography variant="body2" color="text.secondary">
                      No programs found in the legacy schedule for this date.
                    </Typography>
                  )}
                  {!opalProgramsLoading && opalPrograms.length > 0 && (
                    <TableContainer>
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            {['GID','PropID','Instr','PI','Observers','Remote','Staff',''].map((h) => (
                              <TableCell key={h} sx={{ fontWeight: 700, fontSize: '0.72rem', py: 0.5 }}>{h}</TableCell>
                            ))}
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {opalPrograms.map((op) => (
                            <TableRow key={op.alloc_id} sx={{ '&:last-child td': { borderBottom: 0 }, '&:hover': { bgcolor: '#fff3e0' } }}>
                              <TableCell sx={{ fontSize: '0.75rem', fontWeight: 600, py: 0.5 }}>{op.gid || '—'}</TableCell>
                              <TableCell sx={{ fontSize: '0.75rem', py: 0.5 }}>{op.propid || '—'}</TableCell>
                              <TableCell sx={{ fontSize: '0.75rem', py: 0.5 }}>
                                {op.instr ? <Chip size="small" label={op.instr} color="primary" sx={{ fontSize: '0.68rem', height: 20 }} /> : '—'}
                              </TableCell>
                              <TableCell sx={{ fontSize: '0.75rem', py: 0.5 }}>{op.pi || '—'}</TableCell>
                              <TableCell sx={{ fontSize: '0.75rem', py: 0.5, maxWidth: 140 }}>
                                <Typography variant="inherit" noWrap title={op.observers}>{op.observers || '—'}</Typography>
                              </TableCell>
                              <TableCell sx={{ fontSize: '0.75rem', py: 0.5, maxWidth: 120 }}>
                                <Typography variant="inherit" noWrap title={op.remote}>{op.remote || '—'}</Typography>
                              </TableCell>
                              <TableCell sx={{ fontSize: '0.75rem', py: 0.5, maxWidth: 140 }}>
                                <Typography variant="inherit" noWrap title={op.staff}>{op.staff || '—'}</Typography>
                              </TableCell>
                              <TableCell sx={{ py: 0.5 }}>
                                <Button
                                  size="small"
                                  variant="contained"
                                  onClick={() => copyOpalProgram(op)}
                                  sx={{
                                    fontSize: '0.68rem', py: 0.25, px: 1, borderRadius: 1.5,
                                    bgcolor: '#e65100', '&:hover': { bgcolor: '#bf360c' },
                                    whiteSpace: 'nowrap',
                                  }}
                                >
                                  Copy-Program
                                </Button>
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  )}
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
                        <Box key={item.id} id={`log-item-${item.id}`} sx={{
                          mb: 1.5, borderRadius: 1.5, px: 1, pt: 0.5,
                          backgroundColor: highlightItemId === item.id ? '#fff9c4' : undefined,
                          transition: 'background-color 0.4s',
                        }}>
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
                                {item.summit_access === 'Yes' && (
                                  <Chip size="small" label="⛰ Access" color="warning" sx={{ fontSize: '0.67rem', height: 20 }} />
                                )}
                              </Stack>
                              {item.title && <Typography variant="subtitle2">{item.title}</Typography>}
                              {item.body && <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'pre-wrap' }}>{item.body}</Typography>}
                            </Box>
                            <Stack direction="row">
                              {onCreateFatsFromSummit && (
                                <Tooltip title="Create FATS from this entry">
                                  <IconButton size="small" onClick={() => openFatsFromItem(item, selectedDate)}
                                    sx={{ color: '#1565c0' }}>
                                    <PostAddIcon fontSize="small" />
                                  </IconButton>
                                </Tooltip>
                              )}
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
      <Paper ref={searchSectionRef} elevation={3} sx={{ borderRadius: 2.5, overflow: 'hidden' }}>
        <Box sx={{ px: 2.5, py: 1.75, background: 'linear-gradient(90deg, #004d40 0%, #00695c 100%)', color: '#fff', display: 'flex', alignItems: 'center', gap: 1 }}>
          <Typography variant="subtitle1" fontWeight={700} sx={{ letterSpacing: 0.3, flex: 1 }}>🔍 Search Log Entries</Typography>
          {!isSearchRoute && (
            <Button size="small" variant="outlined" onClick={openSearchRoute}
              sx={{ color: '#fff', borderColor: 'rgba(255,255,255,0.5)', textTransform: 'none', fontWeight: 600 }}>
              Open search page
            </Button>
          )}
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
                            setYear(y); setMonth(m);
                            setHighlightItemId(item.id);
                            navigate(`${paths.summitDay(ld)}?item=${item.id}`);
                            loadDay(ld, { updateUrl: false }).then(() => {
                              setTimeout(() => {
                                const el = document.getElementById(`log-item-${item.id}`);
                                if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                              }, 300);
                              setTimeout(() => setHighlightItemId(null), 3000);
                            });
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
      <Dialog open={createDayOpen} onClose={() => { setCreateDayOpen(false); setNewDayDate(''); setNewDayLabel(''); setNewDayHistory(''); }} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ background: SUMMIT_GRADIENT, color: '#fff', py: 1.5 }}>
          🌙 Create New Summit Day
        </DialogTitle>
        <DialogContent>
          <Stack spacing={1.5} sx={{ mt: 1.5 }}>
            <TextField type="date" fullWidth label="Date" InputLabelProps={{ shrink: true }}
              value={newDayDate} onChange={(e) => setNewDayDate(e.target.value)} />
            <TextField fullWidth size="small" label="Day Label (optional)"
              placeholder="e.g. Night ops, Engineering, ToO"
              inputProps={{ maxLength: 80 }}
              value={newDayLabel} onChange={(e) => setNewDayLabel(e.target.value)} />
            <TextField fullWidth size="small" multiline minRows={2} label="Notes / History (optional)"
              placeholder="Free-form notes about this day"
              value={newDayHistory} onChange={(e) => setNewDayHistory(e.target.value)} />
          </Stack>
        </DialogContent>
        <DialogActions sx={{ px: 2, py: 1.5 }}>
          <Button onClick={() => { setCreateDayOpen(false); setNewDayDate(''); setNewDayLabel(''); setNewDayHistory(''); }}
            sx={{ borderRadius: 2 }}>Cancel</Button>
          <Button variant="contained" onClick={createDay} disabled={!newDayDate || createDaySaving}
            sx={{ borderRadius: 2, background: SUMMIT_GRADIENT, fontWeight: 600 }}>
            {createDaySaving ? 'Creating…' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Crew dialog */}
      <Dialog open={crewDialogOpen} onClose={() => setCrewDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ background: 'linear-gradient(90deg,#1565c0,#1976d2)', color: '#fff', py: 1.5 }}>
          {crewForm.id ? '✏️ Edit Crew Member' : '👤 Add Crew Member'}
        </DialogTitle>
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
            <Stack direction="row" spacing={1} alignItems="flex-end">
              <Box sx={{ flex: 1 }}>
                <TextField size="small" fullWidth label="Time In HST (HH:MM)" value={crewForm.time_in}
                  onChange={(e) => setCrewForm(p => ({ ...p, time_in: e.target.value }))} />
              </Box>
              <Tooltip title="Set Time In to now (HST)">
                <Button size="small" variant="outlined" onClick={() => setCrewForm(p => ({ ...p, time_in: nowHSThmm() }))}
                  startIcon={<AccessTimeIcon fontSize="small" />}
                  sx={{ whiteSpace: 'nowrap', fontSize: '0.7rem', borderRadius: 1.5 }}>
                  In Now
                </Button>
              </Tooltip>
            </Stack>
            <Stack direction="row" spacing={1} alignItems="flex-end">
              <Box sx={{ flex: 1 }}>
                <TextField size="small" fullWidth label="Time Out HST (HH:MM)" value={crewForm.time_out}
                  onChange={(e) => setCrewForm(p => ({ ...p, time_out: e.target.value }))} />
              </Box>
              <Tooltip title="Set Time Out to now (HST)">
                <Button size="small" variant="outlined" onClick={() => setCrewForm(p => ({ ...p, time_out: nowHSThmm() }))}
                  startIcon={<AccessTimeIcon fontSize="small" />}
                  sx={{ whiteSpace: 'nowrap', fontSize: '0.7rem', borderRadius: 1.5 }}>
                  Out Now
                </Button>
              </Tooltip>
            </Stack>
          </Stack>
        </DialogContent>
        <DialogActions sx={{ px: 2, py: 1.5 }}>
          <Button onClick={() => setCrewDialogOpen(false)} startIcon={<CancelIcon />} sx={{ borderRadius: 2 }}>Cancel</Button>
          <Button variant="contained" onClick={saveCrew} disabled={crewSaving} startIcon={<SaveIcon />}
            sx={{ borderRadius: 2, background: 'linear-gradient(90deg,#1565c0,#1976d2)', fontWeight: 600 }}>
            {crewSaving ? 'Saving…' : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Weather dialog */}
      <Dialog open={weatherEditOpen} onClose={() => setWeatherEditOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ background: 'linear-gradient(90deg,#00838f,#0097a7)', color: '#fff', py: 1.5 }}>
          {dayData?.weather ? '✏️ Edit Weather' : '🌤 Add Weather'}
        </DialogTitle>
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
        <DialogActions sx={{ px: 2, py: 1.5 }}>
          <Button onClick={() => setWeatherEditOpen(false)} startIcon={<CancelIcon />} sx={{ borderRadius: 2 }}>Cancel</Button>
          <Button variant="contained" onClick={saveWeather} disabled={weatherSaving} startIcon={<SaveIcon />}
            sx={{ borderRadius: 2, background: 'linear-gradient(90deg,#00838f,#0097a7)', fontWeight: 600 }}>
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
        currentUsername={user?.username || ''}
      />

      {/* Copy Work Plan from Previous dialog */}
      <Dialog open={copyWPOpen} onClose={() => setCopyWPOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ background: 'linear-gradient(90deg,#6a1b9a,#7b1fa2)', color: '#fff', py: 1.5 }}>
          <Stack direction="row" alignItems="center" spacing={1}>
            <ContentCopyIcon fontSize="small" />
            <span>Copy Work Plan from Previous</span>
          </Stack>
        </DialogTitle>
        <DialogContent sx={{ p: 0 }}>
          {recentWPsLoading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress size={30} />
            </Box>
          )}
          {!recentWPsLoading && recentWPs.length === 0 && (
            <Box sx={{ p: 3 }}>
              <Typography variant="body2" color="text.secondary">
                No recent work plans found for your username. Work plans where you are listed as
                Requestor or Assigned will appear here.
              </Typography>
            </Box>
          )}
          {!recentWPsLoading && recentWPs.length > 0 && (
            <List dense disablePadding>
              {recentWPs.map((item) => {
                const wp = item;
                const logDate = wp.log_date || '';
                const title = wp.comptitle || wp.plan_text || '(untitled)';
                const status = wp.wp_status || '';
                const req = wp.requestor || '';
                return (
                  <ListItem key={wp.id} disablePadding divider>
                    <ListItemButton onClick={() => copyWP(wp.id)} sx={{ py: 1.25 }}>
                      <ListItemText
                        primary={
                          <Stack direction="row" spacing={1} alignItems="center" flexWrap="wrap" useFlexGap>
                            <Typography variant="body2" fontWeight={600}>{title}</Typography>
                            {status && (
                              <Chip size="small" label={status} variant="outlined"
                                sx={{ fontSize: '0.65rem', height: 18 }} />
                            )}
                          </Stack>
                        }
                        secondary={
                          <Typography variant="caption" color="text.secondary">
                            {logDate}  ·  Requestor: {req || '—'}
                          </Typography>
                        }
                      />
                    </ListItemButton>
                  </ListItem>
                );
              })}
            </List>
          )}
        </DialogContent>
        <DialogActions sx={{ px: 2, py: 1.25 }}>
          <Button onClick={() => setCopyWPOpen(false)} startIcon={<CancelIcon />} sx={{ borderRadius: 2 }}>Cancel</Button>
        </DialogActions>
      </Dialog>

      {/* ── Email Preview Dialog ── */}
      <Dialog open={!!emailPreview} onClose={() => setEmailPreview(null)} maxWidth="md" fullWidth>
        <DialogTitle sx={{ pb: 1 }}>
          {emailPreview?.type === 'to' && '📧 Night Log (TO) — Email Preview'}
          {emailPreview?.type === 'dc' && '📧 Day Crew (DC) — Email Preview'}
          {emailPreview?.type === 'smoka' && '📧 SMOKA Archive — Email Preview'}
        </DialogTitle>
        <DialogContent dividers>
          <Box
            component="pre"
            sx={{
              fontFamily: 'monospace', fontSize: '0.82rem', whiteSpace: 'pre-wrap',
              wordBreak: 'break-word', m: 0, p: 0, lineHeight: 1.6,
            }}
          >
            {emailPreview?.body || ''}
          </Box>
        </DialogContent>
        <DialogActions sx={{ px: 2, py: 1.25 }}>
          <Button
            size="small"
            onClick={() => {
              if (emailPreview?.body) {
                navigator.clipboard.writeText(emailPreview.body);
              }
            }}
            startIcon={<ContentCopyIcon />}
            sx={{ borderRadius: 2 }}
          >
            Copy to Clipboard
          </Button>
          <Button onClick={() => setEmailPreview(null)} startIcon={<CancelIcon />} sx={{ borderRadius: 2 }}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
