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
} from '@mui/material';
import { Close as CloseIcon } from '@mui/icons-material';
import FATSList from './components/FATSList';
import FATSDetail from './components/FATSDetail';
import FATSDetailInline from './components/FATSDetailInline';
import CommentDialog from './components/CommentDialog';
import ConfirmationDialog from './components/ConfirmationDialog';
import FullFaultsList from './components/FullFaultsList';
// import { fatsAPI } from './services/api'; // Available for future use

function App() {
  const [fatsDetailOpen, setFatsDetailOpen] = useState(false);
  const [fatsDetailMode, setFatsDetailMode] = useState('view');
  const [selectedFatsId, setSelectedFatsId] = useState(null);
  const [commentDialogOpen, setCommentDialogOpen] = useState(false);
  const [commentFatsId, setCommentFatsId] = useState(null);
  const [confirmationOpen, setConfirmationOpen] = useState(false);
  const [confirmationData, setConfirmationData] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const [fullFaultsListOpen, setFullFaultsListOpen] = useState(false);
  
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
      // Switch to existing tab
      setActiveTab(existingTabIndex);
    } else {
      // Create new tab
      const newTab = { id: `fats-${idno}`, label: `Fault ${idno}`, fatsId: idno };
      setOpenTabs([...openTabs, newTab]);
      setActiveTab(openTabs.length); // Switch to new tab
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
          <Box sx={{ mb: 2, display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
            <button
              onClick={() => setFullFaultsListOpen(true)}
              style={{
                padding: '10px 20px',
                backgroundColor: '#1976d2',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '14px',
              }}
            >
              Faults List
            </button>
            <button
              onClick={handleCreateFATS}
              style={{
                padding: '10px 20px',
                backgroundColor: '#1976d2',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '14px',
              }}
            >
              + Create New FATS
            </button>
          </Box>
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
              />
            </Box>
          );
        })}
      </Box>
    );
  };

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', backgroundColor: '#f5f5f5' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Fault Tracking System
          </Typography>
        </Toolbar>
      </AppBar>

      {/* Tabs Bar */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', bgcolor: 'background.paper' }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          aria-label="fault tabs"
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
                        '&:hover': { bgcolor: 'rgba(0,0,0,0.1)' }
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

      <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
        {renderTabContent()}

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

export default App;
