import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import {
  Container,
  Typography,
  Box,
  AppBar,
  Toolbar,
  Snackbar,
  Alert,
  Tabs,
  Tab,
  IconButton,
  ToggleButton,
  ToggleButtonGroup,
  Button,
  Stack,
  Chip,
  Tooltip,
} from '@mui/material';
import { Close as CloseIcon, Logout as LogoutIcon } from '@mui/icons-material';
import {
  Routes,
  Route,
  Navigate,
  useNavigate,
  useLocation,
} from 'react-router-dom';
import FATSList from './components/FATSList';
import FATSDetail from './components/FATSDetail';
import FATSDetailInline from './components/FATSDetailInline';
import CommentDialog from './components/CommentDialog';
import ConfirmationDialog from './components/ConfirmationDialog';
import FullFaultsList from './components/FullFaultsList';
import SummitLog from './components/SummitLog';
import WorkPlanCalendar from './components/WorkPlanCalendar';
import LoginPage from './components/LoginPage';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import {
  paths,
  mainSectionFromPath,
  parseLegacyFaultHash,
  isValidLogDate,
  todayHST,
} from './routes/paths';

// Feature flag — set REACT_APP_ENABLE_SUMMIT=false in .env to hide Summit Log and WP Calendar
const ENABLE_SUMMIT = process.env.REACT_APP_ENABLE_SUMMIT !== 'false';

const MAIN_TAB = { id: 'main', label: 'FATS Entries' };

function LoginRoute() {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(135deg, #0d47a1 0%, #0277bd 100%)',
        }}
      >
        <Box sx={{ color: 'rgba(255,255,255,0.85)' }}>Loading…</Box>
      </Box>
    );
  }

  if (user) {
    const from = location.state?.from?.pathname;
    return <Navigate to={from && from !== paths.login ? from : paths.home} replace />;
  }

  return <LoginPage />;
}

function SummitTodayRedirect() {
  return <Navigate to={paths.summitDay(todayHST())} replace />;
}

function SummitInvalidDateRedirect() {
  return <Navigate to={paths.summitToday()} replace />;
}

function AppShell() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [fatsDetailOpen, setFatsDetailOpen] = useState(false);
  const [fatsDetailMode, setFatsDetailMode] = useState('view');
  const [selectedFatsId, setSelectedFatsId] = useState(null);
  const [commentDialogOpen, setCommentDialogOpen] = useState(false);
  const [commentFatsId, setCommentFatsId] = useState(null);
  const [confirmationOpen, setConfirmationOpen] = useState(false);
  const [confirmationData, setConfirmationData] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const [fullFaultsListOpen, setFullFaultsListOpen] = useState(false);
  const [fatsCreateDraft, setFatsCreateDraft] = useState(null);

  const [activeTab, setActiveTab] = useState(0);
  const [openTabs, setOpenTabs] = useState([MAIN_TAB]);

  const fatsListRef = useRef(null);
  const tabScrollPositions = useRef({});
  const mainView = mainSectionFromPath(location.pathname);

  const routeFatsIdno = useMemo(() => {
    const m = location.pathname.match(/^\/fats\/(\d+)(?:\/edit)?$/);
    if (!m) return null;
    const n = parseInt(m[1], 10);
    return Number.isNaN(n) ? null : n;
  }, [location.pathname]);

  const showSnackbar = (message, severity = 'success') => {
    setSnackbar({ open: true, message, severity });
  };

  const ensureFaultTab = useCallback((idno) => {
    setOpenTabs((prev) => {
      if (prev.some((t) => t.fatsId === idno)) return prev;
      return [...prev, { id: `fats-${idno}`, label: `Fault ${idno}`, fatsId: idno }];
    });
  }, []);

  const handleViewFATS = useCallback(
    (idno) => {
      ensureFaultTab(idno);
      navigate(paths.fatsDetail(idno));
    },
    [ensureFaultTab, navigate],
  );

  useEffect(() => {
    window.handleViewFATS = handleViewFATS;
    return () => {
      delete window.handleViewFATS;
    };
  }, [handleViewFATS]);

  // Legacy #fault-XXXX → /fats/XXXX
  useEffect(() => {
    const legacyId = parseLegacyFaultHash(window.location.hash);
    if (legacyId != null) {
      window.history.replaceState(null, '', location.pathname + location.search);
      handleViewFATS(legacyId);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Sync open tabs + active tab from /fats/:idno routes
  useEffect(() => {
    if (!location.pathname.startsWith('/fats')) return;

    if (location.pathname === paths.fats || location.pathname === paths.fatsNew) {
      setActiveTab(0);
      return;
    }

    if (routeFatsIdno != null) {
      setOpenTabs((prev) => {
        let tabs = prev;
        if (!prev.some((t) => t.fatsId === routeFatsIdno)) {
          tabs = [
            ...prev,
            { id: `fats-${routeFatsIdno}`, label: `Fault ${routeFatsIdno}`, fatsId: routeFatsIdno },
          ];
        }
        const idx = tabs.findIndex((t) => t.fatsId === routeFatsIdno);
        if (idx >= 0) setActiveTab(idx);
        return tabs;
      });
    }
  }, [location.pathname, routeFatsIdno]);

  // Open create/edit dialog from route
  useEffect(() => {
    if (location.pathname === paths.fatsNew) {
      setFatsCreateDraft(null);
      setSelectedFatsId(null);
      setFatsDetailMode('create');
      setFatsDetailOpen(true);
      return;
    }
    if (routeFatsIdno != null && location.pathname.endsWith('/edit')) {
      setFatsCreateDraft(null);
      setSelectedFatsId(routeFatsIdno);
      setFatsDetailMode('edit');
      setFatsDetailOpen(true);
      return;
    }
    if (location.pathname.endsWith('/new') || location.pathname.endsWith('/edit')) return;
    if (fatsDetailOpen && (fatsDetailMode === 'create' || fatsDetailMode === 'edit')) {
      setFatsDetailOpen(false);
      setFatsCreateDraft(null);
    }
  }, [location.pathname, routeFatsIdno, fatsDetailOpen, fatsDetailMode]);

  const handleCloseTab = (tabIndex, event) => {
    event.stopPropagation();
    if (openTabs.length === 1) return;

    const closing = openTabs[tabIndex];
    // Clear saved scroll position for the closed tab
    delete tabScrollPositions.current[closing.id];
    const newTabs = openTabs.filter((_, index) => index !== tabIndex);
    setOpenTabs(newTabs);

    let newActive = activeTab;
    if (activeTab >= tabIndex) newActive = Math.max(0, activeTab - 1);
    setActiveTab(newActive);

    if (activeTab === tabIndex) {
      const target = newTabs[newActive];
      if (target.id === 'main') navigate(paths.fats);
      else navigate(paths.fatsDetail(target.fatsId));
    } else if (closing.fatsId === routeFatsIdno) {
      const target = newTabs[activeTab >= tabIndex ? newActive : activeTab];
      if (target.id === 'main') navigate(paths.fats);
      else navigate(paths.fatsDetail(target.fatsId));
    }
  };

  const handleTabChange = (event, newValue) => {
    // Save scroll position of the tab we're leaving
    const currentTab = openTabs[activeTab];
    if (currentTab) {
      tabScrollPositions.current[currentTab.id] = window.scrollY;
    }

    setActiveTab(newValue);
    const tab = openTabs[newValue];
    if (!tab) return;
    if (tab.id === 'main') navigate(paths.fats);
    else navigate(paths.fatsDetail(tab.fatsId));

    // Restore scroll position of the tab we're switching to
    const savedScroll = tabScrollPositions.current[tab.id] ?? 0;
    requestAnimationFrame(() => {
      window.scrollTo({ top: savedScroll, behavior: 'instant' });
    });
  };

  const handleEditFATS = (idno) => {
    navigate(paths.fatsEdit(idno));
  };

  const handleCreateFATS = () => {
    navigate(paths.fatsNew);
  };

  const escapeHtmlForFats = (s) => {
    if (!s) return '';
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  };

  const handleCreateFatsFromSummit = ({ item, logDate }) => {
    const title = (item.title && String(item.title).trim()) || 'Summit log entry';
    const body = (item.body && String(item.body).trim()) || '';
    const idescribe = body
      ? `<p>${escapeHtmlForFats(body).replace(/\n/g, '<br/>')}</p>`
      : `<p><em>Summit log ${logDate}</em></p>`;
    const todoParts = [
      `From summit log ${logDate}`,
      item.crew_tab ? `Tab: ${item.crew_tab}` : null,
      item.item_type ? `Type: ${item.item_type}` : null,
      item.subsystem && item.subsystem !== 'None' ? `Subsystem: ${item.subsystem}` : null,
      item.downtime_minutes > 0 ? `Downtime: ${item.downtime_minutes} min` : null,
    ].filter(Boolean);
    setFatsCreateDraft({
      issue: title.slice(0, 500),
      idescribe,
      todo: todoParts.join(' · '),
      operator: user?.username || '',
    });
    setSelectedFatsId(null);
    setFatsDetailMode('create');
    setFatsDetailOpen(true);
    navigate(paths.fatsNew);
  };

  const handleFatsDetailClose = () => {
    setFatsDetailOpen(false);
    setFatsCreateDraft(null);
    if (location.pathname === paths.fatsNew) {
      navigate(paths.fats);
    } else if (routeFatsIdno != null && location.pathname.endsWith('/edit')) {
      navigate(paths.fatsDetail(routeFatsIdno));
    }
  };

  const handleAddComment = (fatsId) => {
    setCommentFatsId(fatsId);
    setCommentDialogOpen(true);
  };

  const handleFATSSave = () => {
    showSnackbar('FATS entry saved successfully!');
    if (fatsListRef.current) fatsListRef.current.refresh();
    setActiveTab(0);
    navigate(paths.fats);
    setFatsDetailOpen(false);
    setFatsCreateDraft(null);
  };

  const handleCommentSave = (fatsId) => {
    showSnackbar('Comment added successfully!');
    setCommentDialogOpen(false);
    setOpenTabs((prevTabs) =>
      prevTabs.map((tab) =>
        tab.fatsId === fatsId ? { ...tab, lastUpdated: Date.now() } : tab,
      ),
    );
  };

  const handleMainViewChange = (e, v) => {
    if (v == null) return;
    if (v === 'fats') navigate(paths.fats);
    else if (v === 'summit') navigate(paths.summitToday());
    else if (v === 'wpcalendar') {
      const t = new Date();
      navigate(paths.summitCalendar(t.getFullYear(), t.getMonth() + 1));
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate(paths.login, { replace: true });
  };

  const renderFatsContent = () => (
    <Box>
      <Box sx={{ display: activeTab === 0 ? 'block' : 'none' }}>
        <Stack direction="row" justifyContent="flex-end" spacing={1.5} sx={{ mb: 2 }}>
          <Button
            variant="outlined"
            onClick={() => setFullFaultsListOpen(true)}
            sx={{ borderRadius: 2, fontWeight: 600, textTransform: 'none' }}
          >
            📋 Faults List
          </Button>
          <Button
            variant="contained"
            onClick={handleCreateFATS}
            sx={{ borderRadius: 2, fontWeight: 600, textTransform: 'none' }}
          >
            ＋ Create New FATS
          </Button>
        </Stack>
        <FATSList
          ref={fatsListRef}
          onViewFATS={handleViewFATS}
          onEditFATS={handleEditFATS}
          onAddComment={handleAddComment}
        />
      </Box>
      {openTabs.map((tab, index) => {
        if (tab.id === 'main') return null;
        return (
          <Box key={tab.id} sx={{ display: activeTab === index ? 'block' : 'none' }}>
            <FATSDetailInline
              key={tab.lastUpdated || tab.id}
              fatsId={tab.fatsId}
              onEdit={handleEditFATS}
              onViewFATS={handleViewFATS}
            />
          </Box>
        );
      })}
    </Box>
  );

  const summitDateParam = useMemo(() => {
    const m = location.pathname.match(/^\/summit\/(\d{4}-\d{2}-\d{2})$/);
    return m ? m[1] : null;
  }, [location.pathname]);
  const summitDateValid =
    summitDateParam && isValidLogDate(summitDateParam) ? summitDateParam : null;

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', backgroundColor: '#f0f2f5' }}>
      <AppBar
        position="sticky"
        elevation={2}
        sx={{
          top: 0,
          zIndex: (theme) => theme.zIndex.appBar,
          background: 'linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #0277bd 100%)',
          borderBottom: '1px solid rgba(255,255,255,0.12)',
          overflow: 'visible',
        }}
      >
        <Toolbar
          sx={{
            minHeight: 60,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'nowrap',
            gap: 1,
            px: { xs: 1, sm: 2 },
          }}
        >
          <Box
            component="a"
            href={paths.fats}
            onClick={(e) => {
              e.preventDefault();
              navigate(paths.fats);
            }}
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1.5,
              flexShrink: 0,
              textDecoration: 'none',
              color: 'inherit',
            }}
          >
            <Box
              component="img"
              src="/subaru_logo.png"
              alt="Subaru Telescope"
              sx={{
                width: 42,
                height: 42,
                objectFit: 'contain',
                flexShrink: 0,
                filter: 'drop-shadow(0 1px 4px rgba(0,0,0,0.4))',
              }}
            />
            <Box>
              <Typography variant="h6" component="div" sx={{ fontWeight: 700, letterSpacing: 0.5, lineHeight: 1.1 }}>
                OPAL
              </Typography>
              <Typography
                variant="caption"
                sx={{ opacity: 0.75, letterSpacing: 1, textTransform: 'uppercase', fontSize: '0.6rem' }}
              >
                Subaru Telescope Operations
              </Typography>
            </Box>
          </Box>

          <ToggleButtonGroup
            value={mainView}
            exclusive
            size="small"
            onChange={handleMainViewChange}
            aria-label="main view"
            sx={{
              bgcolor: 'rgba(0,0,0,0.2)',
              borderRadius: 2,
              flexShrink: 0,
              '& .MuiToggleButton-root': {
                color: 'rgba(255,255,255,0.7)',
                border: 'none',
                px: 1.5,
                py: 0.6,
                fontSize: '0.78rem',
                fontWeight: 600,
                textTransform: 'none',
                borderRadius: '8px !important',
                transition: 'all 0.2s',
                whiteSpace: 'nowrap',
              },
              '& .MuiToggleButton-root.Mui-selected': {
                bgcolor: 'rgba(255,255,255,0.2)',
                color: '#fff',
                boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.2)',
              },
            }}
          >
            <ToggleButton value="fats">⚡ FATS</ToggleButton>
            {ENABLE_SUMMIT && <ToggleButton value="summit">🌙 Summit Log</ToggleButton>}
            {ENABLE_SUMMIT && <ToggleButton value="wpcalendar">📅 WP Calendar</ToggleButton>}
          </ToggleButtonGroup>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexShrink: 0 }}>
            {user && (
              <Chip
                label={user.username}
                size="small"
                sx={{
                  color: '#fff',
                  bgcolor: 'rgba(255,255,255,0.15)',
                  fontWeight: 600,
                  fontSize: '0.75rem',
                  border: '1px solid rgba(255,255,255,0.25)',
                }}
              />
            )}
            <Tooltip title="Logout">
              <IconButton
                onClick={handleLogout}
                size="small"
                sx={{ color: 'rgba(255,255,255,0.8)', '&:hover': { color: '#fff' } }}
                aria-label="logout"
              >
                <LogoutIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>
        </Toolbar>
      </AppBar>

      {mainView === 'fats' && (
        <Box
          sx={{
            position: 'sticky',
            top: 60,
            zIndex: (theme) => theme.zIndex.appBar - 1,
            borderBottom: '2px solid',
            borderColor: 'divider',
            bgcolor: '#fff',
            boxShadow: '0 1px 4px rgba(0,0,0,0.08)',
          }}
        >
          <Tabs
            value={activeTab}
            onChange={handleTabChange}
            variant="scrollable"
            scrollButtons="auto"
            aria-label="fault tabs"
            sx={{
              '& .MuiTab-root': { textTransform: 'none', fontWeight: 600, minHeight: 46 },
              '& .MuiTabs-indicator': { height: 3, borderRadius: '3px 3px 0 0' },
            }}
          >
            {openTabs.map((tab, index) => (
              <Tab
                key={tab.id}
                label={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    {tab.label}
                    {tab.id !== 'main' && (
                      <IconButton
                        size="small"
                        onClick={(e) => handleCloseTab(index, e)}
                        sx={{ ml: 0.5, p: 0.25, '&:hover': { bgcolor: 'rgba(0,0,0,0.1)' } }}
                      >
                        <CloseIcon fontSize="small" />
                      </IconButton>
                    )}
                  </Box>
                }
              />
            ))}
          </Tabs>
        </Box>
      )}

      <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
        <Routes>
          <Route path="/" element={<Navigate to={paths.home} replace />} />

          <Route path="/fats" element={renderFatsContent()} />
          <Route path="/fats/new" element={renderFatsContent()} />
          <Route path="/fats/:idno" element={renderFatsContent()} />
          <Route path="/fats/:idno/edit" element={renderFatsContent()} />

          {ENABLE_SUMMIT && (
            <Route
              path="/summit/calendar/:year/:month"
              element={
                <WorkPlanCalendar
                  onOpenSummitLog={(dateStr) => navigate(paths.summitDay(dateStr))}
                />
              }
            />
          )}
          {ENABLE_SUMMIT && (
            <Route
              path="/summit/search"
              element={
                <SummitLog
                  onError={(msg, severity) => showSnackbar(msg, severity)}
                  onCreateFatsFromSummit={handleCreateFatsFromSummit}
                  routePanel="search"
                />
              }
            />
          )}
          {ENABLE_SUMMIT && (
            <Route
              path="/summit/years/:year"
              element={
                <SummitLog
                  onError={(msg, severity) => showSnackbar(msg, severity)}
                  onCreateFatsFromSummit={handleCreateFatsFromSummit}
                  routePanel="year"
                />
              }
            />
          )}
          {ENABLE_SUMMIT && (
            <Route
              path="/summit/:date"
              element={
                summitDateParam && !summitDateValid ? (
                  <SummitInvalidDateRedirect />
                ) : (
                  <SummitLog
                    onError={(msg, severity) => showSnackbar(msg, severity)}
                    onCreateFatsFromSummit={handleCreateFatsFromSummit}
                    routeDate={summitDateValid}
                  />
                )
              }
            />
          )}
          {ENABLE_SUMMIT && <Route path="/summit" element={<SummitTodayRedirect />} />}

          <Route path="*" element={<Navigate to={paths.home} replace />} />
        </Routes>

        <FATSDetail
          open={fatsDetailOpen}
          fatsId={selectedFatsId}
          mode={fatsDetailMode}
          onClose={handleFatsDetailClose}
          onSave={handleFATSSave}
          onFaultReferenceClick={handleViewFATS}
          createDraft={fatsCreateDraft}
        />

        <CommentDialog
          open={commentDialogOpen}
          fatsId={commentFatsId}
          onClose={() => setCommentDialogOpen(false)}
          onSave={handleCommentSave}
        />

        <ConfirmationDialog
          open={confirmationOpen}
          title={confirmationData?.title}
          message={confirmationData?.message}
          onConfirm={() => {
            if (confirmationData?.onConfirm) confirmationData.onConfirm();
            setConfirmationOpen(false);
          }}
          onCancel={() => setConfirmationOpen(false)}
        />

        <FullFaultsList open={fullFaultsListOpen} onClose={() => setFullFaultsListOpen(false)} />

        <Snackbar
          open={snackbar.open}
          autoHideDuration={4000}
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        >
          <Alert
            onClose={() => setSnackbar({ ...snackbar, open: false })}
            severity={snackbar.severity}
            sx={{ width: '100%' }}
          >
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Container>
    </Box>
  );
}

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path={paths.login} element={<LoginRoute />} />
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <AppShell />
            </ProtectedRoute>
          }
        />
      </Routes>
    </AuthProvider>
  );
}

export default App;
