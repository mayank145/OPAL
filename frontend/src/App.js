import React, { useState, useEffect, useRef } from 'react';
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
import FATSList from './components/FATSList';
import FATSDetail from './components/FATSDetail';
import FATSDetailInline from './components/FATSDetailInline';
import CommentDialog from './components/CommentDialog';
import ConfirmationDialog from './components/ConfirmationDialog';
import FullFaultsList from './components/FullFaultsList';
import SummitLog from './components/SummitLog';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
// import { fatsAPI } from './services/api'; // Available for future use

function AppContent() {
  const { user, logout } = useAuth();
  const [fatsDetailOpen, setFatsDetailOpen] = useState(false);
  const [fatsDetailMode, setFatsDetailMode] = useState('view');
  const [selectedFatsId, setSelectedFatsId] = useState(null);
  const [commentDialogOpen, setCommentDialogOpen] = useState(false);
  const [commentFatsId, setCommentFatsId] = useState(null);
  const [confirmationOpen, setConfirmationOpen] = useState(false);
  const [confirmationData, setConfirmationData] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const [fullFaultsListOpen, setFullFaultsListOpen] = useState(false);
  
  // Main area: FATS vs Summit Log
  const [mainView, setMainView] = useState('fats');

  // Tab management
  const [activeTab, setActiveTab] = useState(0);
  const [openTabs, setOpenTabs] = useState([{ id: 'main', label: 'FATS Entries' }]);
  
  // Ref for FATSList component to trigger refresh
  const fatsListRef = useRef(null);

  const showSnackbar = (message, severity = 'success') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleViewFATS = (idno) => {
    // Check if tab already exists
    const existingTabIndex = openTabs.findIndex(tab => tab.id === `fats-${idno}`);
    
    if (existingTabIndex !== -1) {
      // Tab exists - do nothing, user stays on current tab
      // User can manually click the tab if they want to view it
      return;
    } else {
      // Create new tab in background - don't switch to it
      const newTab = { id: `fats-${idno}`, label: `Fault ${idno}`, fatsId: idno };
      setOpenTabs([...openTabs, newTab]);
      // Don't call setActiveTab - user stays on current tab
    }
  };

  // Expose handleViewFATS globally for internal fault links
  useEffect(() => {
    window.handleViewFATS = handleViewFATS;
    return () => {
      delete window.handleViewFATS;
    };
  }, [openTabs]);

  // Check URL on mount for #fault-XXXX and auto-open that fault
  useEffect(() => {
    const hash = window.location.hash;
    if (hash && hash.startsWith('#fault-')) {
      const faultId = hash.replace('#fault-', '');
      const faultIdNum = parseInt(faultId);
      if (!isNaN(faultIdNum)) {
        // Clear the hash from URL
        window.history.replaceState(null, '', window.location.pathname);
        // Open the fault
        handleViewFATS(faultIdNum);
      }
    }
  }, []); // Run only once on mount

  const handleCloseTab = (tabIndex, event) => {
    event.stopPropagation(); // Prevent tab switch on close
    
    if (openTabs.length === 1) return; // Don't close last tab
    
    const newTabs = openTabs.filter((_, index) => index !== tabIndex);
    setOpenTabs(newTabs);
    
    // Adjust active tab if needed
    if (activeTab >= tabIndex) {
      setActiveTab(Math.max(0, activeTab - 1));
    }
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleEditFATS = (idno) => {
    setSelectedFatsId(idno);
    setFatsDetailMode('edit');
    setFatsDetailOpen(true);
  };

  const handleCreateFATS = () => {
    setSelectedFatsId(null);
    setFatsDetailMode('create');
    setFatsDetailOpen(true);
  };

  const handleAddComment = (fatsId) => {
    setCommentFatsId(fatsId);
    setCommentDialogOpen(true);
  };

  const handleFATSSave = () => {
    showSnackbar('FATS entry saved successfully!');
    // Refresh the main FATS list
    if (fatsListRef.current) {
      fatsListRef.current.refresh();
    }
    // Switch back to main tab if on a different tab
    setActiveTab(0);
  };

  const handleCommentSave = (fatsId) => {
    showSnackbar('Comment added successfully!');
    // Trigger a re-render by updating a timestamp or counter
    // This will cause FATSDetailInline components to reload
    setCommentDialogOpen(false);
    
    // Force re-render of the fault detail by updating a key
    // Find the tab with this fatsId and update it
    setOpenTabs(prevTabs => prevTabs.map(tab => {
      if (tab.fatsId === fatsId) {
        return { ...tab, lastUpdated: Date.now() };
      }
      return tab;
    }));
  };

  const renderTabContent = () => {
    const currentTab = openTabs[activeTab];
    
    if (!currentTab) return null;
    
    return (
      <Box>
        {/* Main FATS List page - Keep mounted but hide when not active */}
        <Box sx={{ display: currentTab.id === 'main' ? 'block' : 'none' }}>
          <Stack direction="row" justifyContent="flex-end" spacing={1.5} sx={{ mb: 2 }}>
            <Button variant="outlined" onClick={() => setFullFaultsListOpen(true)}
              sx={{ borderRadius: 2, fontWeight: 600, textTransform: 'none' }}>
              📋 Faults List
            </Button>
            <Button variant="contained" onClick={handleCreateFATS}
              sx={{ borderRadius: 2, fontWeight: 600, textTransform: 'none' }}>
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
        
        {/* Fault detail tabs - Render all open fault tabs */}
        {openTabs.map((tab, index) => {
          if (tab.id === 'main') return null;
          
          return (
            <Box 
              key={tab.id} 
              sx={{ display: activeTab === index ? 'block' : 'none' }}
            >
              {/* Use lastUpdated as key to force re-render when comments are added */}
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
  };

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', backgroundColor: '#f0f2f5' }}>
      <AppBar position="static" elevation={0}
        sx={{ background: 'linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #0277bd 100%)', borderBottom: '1px solid rgba(255,255,255,0.12)' }}>
        <Toolbar sx={{ minHeight: 60 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, flexGrow: 1 }}>
            <Box
              component="img"
              src="/subaru_logo.png"
              alt="Subaru Telescope"
              sx={{ width: 42, height: 42, objectFit: 'contain', flexShrink: 0, filter: 'drop-shadow(0 1px 4px rgba(0,0,0,0.4))' }}
            />
            <Box>
              <Typography variant="h6" component="div" sx={{ fontWeight: 700, letterSpacing: 0.5, lineHeight: 1.1 }}>
                OPAL
              </Typography>
              <Typography variant="caption" sx={{ opacity: 0.75, letterSpacing: 1, textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Subaru Telescope Operations
              </Typography>
            </Box>
          </Box>
          <ToggleButtonGroup
            value={mainView}
            exclusive
            size="small"
            onChange={(e, v) => v != null && setMainView(v)}
            aria-label="main view"
            sx={{
              bgcolor: 'rgba(0,0,0,0.2)',
              borderRadius: 2,
              '& .MuiToggleButton-root': {
                color: 'rgba(255,255,255,0.7)',
                border: 'none',
                px: 2,
                py: 0.6,
                fontSize: '0.82rem',
                fontWeight: 600,
                textTransform: 'none',
                borderRadius: '8px !important',
                transition: 'all 0.2s',
              },
              '& .MuiToggleButton-root.Mui-selected': {
                bgcolor: 'rgba(255,255,255,0.2)',
                color: '#fff',
                boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.2)',
              },
            }}
          >
            <ToggleButton value="fats">⚡ FATS</ToggleButton>
            <ToggleButton value="summit">🌙 Summit Log</ToggleButton>
          </ToggleButtonGroup>

          {/* User info + logout */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, ml: 2 }}>
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
                onClick={logout}
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

      {/* Tabs Bar (FATS only) */}
      {mainView === 'fats' && (
        <Box sx={{ borderBottom: '2px solid', borderColor: 'divider', bgcolor: '#fff', boxShadow: '0 1px 4px rgba(0,0,0,0.08)' }}>
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
                        sx={{
                          ml: 0.5,
                          p: 0.25,
                          '&:hover': { bgcolor: 'rgba(0,0,0,0.1)' },
                        }}
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
        {mainView === 'summit' ? (
          <SummitLog onError={(msg, severity) => showSnackbar(msg, severity)} />
        ) : (
          renderTabContent()
        )}

        {/* FATS Detail Dialog */}
        <FATSDetail
          open={fatsDetailOpen}
          fatsId={selectedFatsId}
          mode={fatsDetailMode}
          onClose={() => setFatsDetailOpen(false)}
          onSave={handleFATSSave}
          onFaultReferenceClick={handleViewFATS}
        />

        {/* Comment Dialog */}
        <CommentDialog
          open={commentDialogOpen}
          fatsId={commentFatsId}
          onClose={() => setCommentDialogOpen(false)}
          onSave={handleCommentSave}
        />

        {/* Confirmation Dialog */}
        <ConfirmationDialog
          open={confirmationOpen}
          title={confirmationData?.title}
          message={confirmationData?.message}
          onConfirm={() => {
            if (confirmationData?.onConfirm) {
              confirmationData.onConfirm();
            }
            setConfirmationOpen(false);
          }}
          onCancel={() => setConfirmationOpen(false)}
        />

        {/* Full Faults List Dialog */}
        <FullFaultsList
          open={fullFaultsListOpen}
          onClose={() => setFullFaultsListOpen(false)}
        />

        {/* Snackbar for notifications */}
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
      <ProtectedRoute>
        <AppContent />
      </ProtectedRoute>
    </AuthProvider>
  );
}

export default App;
