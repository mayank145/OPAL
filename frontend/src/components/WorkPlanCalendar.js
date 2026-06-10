import React, { useState, useEffect, useCallback } from 'react';
import {
  Box, Typography, Paper, Stack, IconButton, Chip,
  CircularProgress, Alert, Tooltip, Dialog, DialogTitle,
  DialogContent, DialogActions, Button, Snackbar,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import TodayIcon from '@mui/icons-material/Today';
import { useNavigate, useParams } from 'react-router-dom';
import { summitAPI } from '../services/api';
import { WorkPlanDialog } from './SummitLog';
import { paths } from '../routes/paths';

// ── helpers (mirrors SummitLog.js) ─────────────────────────────────────────
function toUtcIso(logDate, hhmm) {
  if (!logDate || !hhmm || !hhmm.includes(':')) return null;
  const [y, m, d] = logDate.split('-').map(Number);
  const [hh, mm] = hhmm.split(':').map(Number);
  if ([y, m, d, hh, mm].some(Number.isNaN)) return null;
  return new Date(Date.UTC(y, m - 1, d, hh + 10, mm)).toISOString();
}
function formatTimeHST(ts) {
  if (!ts) return '--:--';
  const d = new Date(ts);
  if (Number.isNaN(d.getTime())) return '--:--';
  return d.toLocaleTimeString('en-US', {
    hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Pacific/Honolulu',
  });
}

const DAYS_OF_WEEK = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

const STATUS_COLORS = {
  Planned:     { bg: '#e3f2fd', color: '#1565c0', border: '#90caf9' },
  InProgress:  { bg: '#fff8e1', color: '#e65100', border: '#ffcc02' },
  Completed:   { bg: '#e8f5e9', color: '#2e7d32', border: '#a5d6a7' },
  Cancelled:   { bg: '#fce4ec', color: '#880e4f', border: '#f48fb1' },
};

function getStatusStyle(status) {
  return STATUS_COLORS[status] || { bg: '#f3e5f5', color: '#6a1b9a', border: '#ce93d8' };
}

// Build a 6-row calendar grid for the given year/month
function buildCalendarGrid(year, month) {
  const firstDay = new Date(year, month - 1, 1);
  const daysInMonth = new Date(year, month, 0).getDate();
  const startDow = firstDay.getDay(); // 0=Sun
  const cells = [];
  for (let i = 0; i < startDow; i++) cells.push(null);
  for (let d = 1; d <= daysInMonth; d++) cells.push(d);
  while (cells.length % 7 !== 0) cells.push(null);
  return cells;
}

function pad2(n) { return String(n).padStart(2, '0'); }

export default function WorkPlanCalendar({ onOpenSummitLog }) {
  const navigate = useNavigate();
  const { year: yearParam, month: monthParam } = useParams();
  const today = new Date();
  const parsedYear = parseInt(yearParam, 10);
  const parsedMonth = parseInt(monthParam, 10);
  const [year, setYear] = useState(
    !Number.isNaN(parsedYear) && parsedYear >= 2000 ? parsedYear : today.getFullYear(),
  );
  const [month, setMonth] = useState(
    !Number.isNaN(parsedMonth) && parsedMonth >= 1 && parsedMonth <= 12 ? parsedMonth : today.getMonth() + 1,
  );
  const [wpByDate, setWpByDate] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [detailDate, setDetailDate] = useState(null); // date string "YYYY-MM-DD"
  // Work plan edit / create dialog
  const [wpDialogOpen, setWpDialogOpen] = useState(false);
  const [wpEditing, setWpEditing]       = useState(null);  // null = new WP
  const [wpEditDate, setWpEditDate]     = useState(null);  // "YYYY-MM-DD"
  const [wpSaving, setWpSaving]         = useState(false);
  const [snack, setSnack]               = useState(null);

  const load = useCallback(async (y, m) => {
    setLoading(true); setError(null);
    try {
      const data = await summitAPI.getMonthlyWorkPlans(y, m);
      setWpByDate(data.work_plans_by_date || {});
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'Failed to load work plans');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(year, month); }, [year, month, load]);

  useEffect(() => {
    const y = parseInt(yearParam, 10);
    const m = parseInt(monthParam, 10);
    if (!Number.isNaN(y) && y >= 2000) setYear(y);
    if (!Number.isNaN(m) && m >= 1 && m <= 12) setMonth(m);
  }, [yearParam, monthParam]);

  const goToMonth = (y, m) => {
    setYear(y);
    setMonth(m);
    navigate(paths.summitCalendar(y, m));
  };

  const prevMonth = () => {
    if (month === 1) goToMonth(year - 1, 12);
    else goToMonth(year, month - 1);
  };
  const nextMonth = () => {
    if (month === 12) goToMonth(year + 1, 1);
    else goToMonth(year, month + 1);
  };
  const goToday = () => goToMonth(today.getFullYear(), today.getMonth() + 1);

  // Open WorkPlanDialog for an existing WP
  const openEditWP = (wp, dateStr) => {
    setWpEditing({
      id: wp.id,
      comptitle: wp.comptitle || '', plan_text: wp.plan_text || '',
      requestor: wp.requestor || wp.contact1 || '', contact2: wp.contact2 || '', others: wp.others || '',
      wp_status: wp.wp_status || 'Planned', wp_type: wp.wp_type || 'Comment',
      wp_subsystem: wp.wp_subsystem || '-none-',
      windowStart: wp.window_start ? formatTimeHST(wp.window_start) : '',
      windowEnd:   wp.window_end   ? formatTimeHST(wp.window_end)   : '',
      day_warning: wp.day_warning || '', nite_warning: wp.nite_warning || '',
      location: wp.location || '.none', location2: wp.location2 || '.none', location3: wp.location3 || '.none',
      assigned1: wp.assigned1 || '.none', assigned2: wp.assigned2 || '',
      dcassist: wp.dcassist || '.none', notify: wp.notify || '.none',
      teampass: wp.teampass || '', otherreq: wp.otherreq || '',
      realstart: wp.realstart ? formatTimeHST(wp.realstart) : '',
      realend:   wp.realend   ? formatTimeHST(wp.realend)   : '',
      completion_title: wp.completion_title || '', comptext: wp.comptext || '',
      req_flags: wp.req_flags || '', lockout_flags: wp.lockout_flags || '',
      nite_effect: wp.nite_effect || '', day_effect: wp.day_effect || '',
      notes: wp.notes || '',
    });
    setWpEditDate(dateStr);
    setDetailDate(null);
    setWpDialogOpen(true);
  };

  // Open WorkPlanDialog to create a new WP for a date
  const openNewWP = (dateStr) => {
    setWpEditing(null);
    setWpEditDate(dateStr);
    setWpDialogOpen(true);
  };

  // Save (create or update) a work plan
  const saveWP = async (form) => {
    if (!wpEditDate) return;
    setWpSaving(true);
    try {
      const n   = (v) => v || null;
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
        completion_title: n(form.completion_title), comptext: n(form.comptext),
        notes: n(form.notes),
        window_start: form.windowStart ? toUtcIso(wpEditDate, form.windowStart) : null,
        window_end:   form.windowEnd   ? toUtcIso(wpEditDate, form.windowEnd)   : null,
        realstart:    form.realstart   ? toUtcIso(wpEditDate, form.realstart)   : null,
        realend:      form.realend     ? toUtcIso(wpEditDate, form.realend)     : null,
      };
      if (wpEditing?.id) {
        await summitAPI.updateWorkPlan(wpEditing.id, payload);
        setSnack('Work plan updated');
      } else {
        await summitAPI.createWorkPlan(wpEditDate, payload);
        setSnack('Work plan created');
      }
      setWpDialogOpen(false);
      setWpEditing(null);
      // Reload the month data so the calendar refreshes
      load(year, month);
    } catch (e) {
      setSnack(e.response?.data?.detail || e.message || 'Failed to save work plan');
    } finally {
      setWpSaving(false);
    }
  };

  const MONTH_NAMES = ['January','February','March','April','May','June',
    'July','August','September','October','November','December'];

  const grid = buildCalendarGrid(year, month);
  const todayStr = `${today.getFullYear()}-${pad2(today.getMonth()+1)}-${pad2(today.getDate())}`;

  const detailWPs = detailDate ? (wpByDate[detailDate] || []) : [];

  return (
    <Box sx={{ p: { xs: 1, sm: 2 }, width: '100%', overflowX: 'auto', overflowY: 'auto' }}>
      {/* Header */}
      <Paper elevation={3} sx={{
        background: 'linear-gradient(135deg,#1a237e,#283593)',
        color: '#fff', borderRadius: 2, px: 3, py: 2, mb: 2,
      }}>
        <Stack direction="row" alignItems="center" justifyContent="space-between">
          <Typography variant="h5" fontWeight={700} letterSpacing={0.5}>
            📅 Work Plan Calendar
          </Typography>
          <Stack direction="row" alignItems="center" spacing={1}>
            <Tooltip title="Previous month">
              <IconButton onClick={prevMonth} sx={{ color: '#fff' }}><ChevronLeftIcon /></IconButton>
            </Tooltip>
            <Typography variant="h6" fontWeight={600} sx={{ minWidth: 200, textAlign: 'center' }}>
              {MONTH_NAMES[month - 1]} {year}
            </Typography>
            <Tooltip title="Next month">
              <IconButton onClick={nextMonth} sx={{ color: '#fff' }}><ChevronRightIcon /></IconButton>
            </Tooltip>
            <Tooltip title="Go to today">
              <IconButton onClick={goToday} sx={{ color: '#fff' }}><TodayIcon /></IconButton>
            </Tooltip>
            {loading && <CircularProgress size={20} sx={{ color: '#fff' }} />}
          </Stack>
        </Stack>
      </Paper>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {/* Legend */}
      <Stack direction="row" spacing={1} sx={{ mb: 1.5 }} flexWrap="wrap" useFlexGap>
        {Object.entries(STATUS_COLORS).map(([s, c]) => (
          <Chip key={s} label={s} size="small"
            sx={{ bgcolor: c.bg, color: c.color, border: `1px solid ${c.border}`, fontWeight: 600, fontSize: '0.7rem' }} />
        ))}
      </Stack>

      {/* Calendar grid */}
      <Paper elevation={2} sx={{ borderRadius: 2, overflow: 'hidden', minWidth: 700 }}>
        {/* Day-of-week header */}
        <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', bgcolor: '#1a237e' }}>
          {DAYS_OF_WEEK.map(d => (
            <Box key={d} sx={{ py: 1, textAlign: 'center' }}>
              <Typography variant="caption" fontWeight={700} sx={{ color: '#fff', letterSpacing: 1 }}>
                {d}
              </Typography>
            </Box>
          ))}
        </Box>

        {/* Cells */}
        <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(7, minmax(0, 1fr))', gap: '1px', bgcolor: '#e0e0e0' }}>
          {grid.map((day, idx) => {
            if (!day) return <Box key={idx} sx={{ bgcolor: '#f5f5f5', minHeight: 110, borderTop: '1px solid #e0e0e0' }} />;
            const dateStr = `${year}-${pad2(month)}-${pad2(day)}`;
            const plans = wpByDate[dateStr] || [];
            const isToday = dateStr === todayStr;
            return (
              <Box key={idx}
                sx={{
                  bgcolor: isToday ? '#f3e5f5' : '#fff',
                  minHeight: 110, p: '6px', position: 'relative',
                  transition: 'background 0.15s', boxSizing: 'border-box',
                  borderTop: isToday ? '3px solid #1a237e' : '1px solid #e0e0e0',
                  '&:hover': { bgcolor: '#f3e5f5' },
                  '&:hover .cal-add-btn': { opacity: 1 },
                }}>
                {/* Date number + add button row */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 4 }}>
                  <div
                    onClick={() => plans.length > 0 && setDetailDate(dateStr)}
                    style={{
                      width: 28, height: 28, borderRadius: '50%', flexShrink: 0,
                      background: isToday ? '#1a237e' : '#5e35b1',
                      color: '#ffffff',
                      fontWeight: 700, fontSize: 13,
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      cursor: plans.length > 0 ? 'pointer' : 'default',
                      userSelect: 'none',
                      boxShadow: '0 1px 3px rgba(0,0,0,0.2)',
                    }}>
                    {day}
                  </div>
                  <Tooltip title={`Add Work Plan for ${dateStr}`}>
                    <IconButton
                      size="small"
                      onClick={(e) => { e.stopPropagation(); openNewWP(dateStr); }}
                      sx={{
                        width: 20, height: 20, p: 0,
                        bgcolor: '#7b1fa2', color: '#fff',
                        '&:hover': { bgcolor: '#4a148c' },
                        borderRadius: '50%',
                      }}>
                      <AddIcon sx={{ fontSize: 14 }} />
                    </IconButton>
                  </Tooltip>
                </div>
                {/* Work plan entries — click individual entry to edit */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                  {plans.slice(0, 4).map((wp, i) => {
                    const style = getStatusStyle(wp.wp_status);
                    const timeLabel = wp.window_start
                      ? new Date(wp.window_start).toLocaleTimeString('en-US', {
                          hour: '2-digit', minute: '2-digit', hour12: false,
                          timeZone: 'Pacific/Honolulu',
                        })
                      : null;
                    return (
                      <Tooltip key={i} title={`Click to edit: ${wp.comptitle || wp.plan_text || '(untitled)'}`} placement="top">
                        <Box onClick={(e) => { e.stopPropagation(); openEditWP(wp, dateStr); }}
                          sx={{
                            bgcolor: style.bg, color: style.color,
                            border: `1px solid ${style.border}`,
                            borderRadius: 0.5, px: 0.5, py: 0.1,
                            fontSize: '0.62rem', fontWeight: 600,
                            display: 'flex', alignItems: 'center', gap: '3px',
                            overflow: 'hidden', whiteSpace: 'nowrap',
                            cursor: 'pointer',
                            '&:hover': { filter: 'brightness(0.9)', borderColor: style.color },
                          }}>
                          {timeLabel && (
                            <Box component="span" sx={{ fontFamily: 'monospace', fontWeight: 700, flexShrink: 0, opacity: 0.85 }}>
                              {timeLabel}
                            </Box>
                          )}
                          <Box component="span" sx={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>
                            {wp.comptitle || wp.plan_text || '(untitled)'}
                          </Box>
                        </Box>
                      </Tooltip>
                    );
                  })}
                  {plans.length > 4 && (
                    <div
                      onClick={() => setDetailDate(dateStr)}
                      style={{ color: '#7b1fa2', fontWeight: 700, fontSize: 10, cursor: 'pointer' }}>
                      +{plans.length - 4} more…
                    </div>
                  )}
                </div>
              </Box>
            );
          })}
        </Box>
      </Paper>

      {/* Work Plan edit / create dialog */}
      <WorkPlanDialog
        open={wpDialogOpen}
        onClose={() => { setWpDialogOpen(false); setWpEditing(null); }}
        onSave={saveWP}
        saving={wpSaving}
        initial={wpEditing || {}}
      />

      {/* Day detail dialog */}
      <Dialog open={!!detailDate} onClose={() => setDetailDate(null)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ background: 'linear-gradient(90deg,#1a237e,#283593)', color: '#fff', py: 1.5 }}>
          📋 Work Plans — {detailDate}
        </DialogTitle>
        <DialogContent dividers sx={{ pt: 1.5 }}>
          <Stack spacing={1.5}>
            {detailWPs.map((wp, i) => {
              const style = getStatusStyle(wp.wp_status);
              const locs = [wp.location, wp.location2, wp.location3].filter(l => l && l !== '.none');
              const assigned = [wp.assigned1, wp.assigned2].filter(a => a && a !== '.none');
              return (
                <Paper key={i} elevation={2} onClick={() => openEditWP(wp, detailDate)} sx={{
                  borderLeft: `4px solid ${style.border}`, borderRadius: 1.5, p: 1.5,
                  cursor: 'pointer', transition: 'box-shadow 0.15s, transform 0.1s',
                  '&:hover': { boxShadow: 6, transform: 'translateY(-1px)', borderLeft: `4px solid ${style.color}` },
                }}>
                  <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 0.5 }}>
                    <Chip label={wp.wp_status || 'Planned'} size="small"
                      sx={{ bgcolor: style.bg, color: style.color, fontWeight: 700, fontSize: '0.7rem' }} />
                    <Typography variant="subtitle2" fontWeight={700}>
                      {wp.comptitle || '(Untitled)'}
                    </Typography>
                    {(wp.window_start || wp.window_end) && (
                      <Typography variant="caption" color="text.secondary">
                        {wp.window_start ? new Date(wp.window_start).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', timeZone: 'Pacific/Honolulu' }) : ''}
                        {' – '}
                        {wp.window_end ? new Date(wp.window_end).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', timeZone: 'Pacific/Honolulu' }) : ''}
                        {' HST'}
                      </Typography>
                    )}
                  </Stack>
                  {wp.plan_text && (
                    <Typography variant="body2" sx={{ mb: 0.5, whiteSpace: 'pre-wrap' }}>{wp.plan_text}</Typography>
                  )}
                  {wp.requestor && (
                    <Typography variant="body2"><strong>Requestor:</strong> {wp.requestor}</Typography>
                  )}
                  {assigned.length > 0 && (
                    <Typography variant="body2">
                      <strong>Assigned:</strong> {assigned.join(', ')}
                      {wp.dcassist && wp.dcassist !== '.none' && ` · DC: ${wp.dcassist}`}
                    </Typography>
                  )}
                  {locs.length > 0 && (
                    <Typography variant="body2"><strong>Location:</strong> {locs.join(' / ')}</Typography>
                  )}
                  {wp.req_flags && (
                    <Stack direction="row" flexWrap="wrap" useFlexGap spacing={0.4} sx={{ mt: 0.5 }}>
                      <Typography variant="caption" fontWeight={700} sx={{ alignSelf: 'center' }}>Required:</Typography>
                      {wp.req_flags.split(',').filter(Boolean).map(f => (
                        <Chip key={f} label={f} size="small"
                          sx={{ bgcolor: '#e3f2fd', color: '#1565c0', fontWeight: 600, fontSize: '0.65rem', height: 18 }} />
                      ))}
                    </Stack>
                  )}
                  {wp.lockout_flags && (
                    <Stack direction="row" flexWrap="wrap" useFlexGap spacing={0.4} sx={{ mt: 0.4 }}>
                      <Typography variant="caption" fontWeight={700} sx={{ alignSelf: 'center' }}>LockOuts:</Typography>
                      {wp.lockout_flags.split(',').filter(Boolean).map(f => (
                        <Chip key={f} label={f} size="small"
                          sx={{ bgcolor: '#ffcdd2', color: '#c62828', fontWeight: 600, fontSize: '0.65rem', height: 18 }} />
                      ))}
                    </Stack>
                  )}
                  {wp.notes && (
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5, fontStyle: 'italic' }}>
                      {wp.notes}
                    </Typography>
                  )}
                  <Typography variant="caption" sx={{ color: style.color, mt: 0.5, display: 'block', opacity: 0.7 }}>
                    Click to edit →
                  </Typography>
                </Paper>
              );
            })}
          </Stack>
        </DialogContent>
        <DialogActions sx={{ px: 2, py: 1.5 }}>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => openNewWP(detailDate)}
            sx={{ borderRadius: 2, mr: 'auto', bgcolor: '#7b1fa2', '&:hover': { bgcolor: '#4a148c' } }}>
            Add Work Plan
          </Button>
          {onOpenSummitLog && (
            <Button variant="outlined" onClick={() => { onOpenSummitLog(detailDate); setDetailDate(null); }}
              sx={{ borderRadius: 2 }}>
              Open in Summit Log
            </Button>
          )}
          <Button onClick={() => setDetailDate(null)} sx={{ borderRadius: 2 }}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for save feedback */}
      <Snackbar
        open={!!snack}
        autoHideDuration={3000}
        onClose={() => setSnack(null)}
        message={snack}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      />
    </Box>
  );
}
