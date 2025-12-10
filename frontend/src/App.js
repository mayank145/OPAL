import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  AppBar,
  Toolbar,
  Snackbar,
  Alert,
} from '@mui/material';
import FATSList from './components/FATSList';
import FATSDetail from './components/FATSDetail';
import CommentDialog from './components/CommentDialog';
import ConfirmationDialog from './components/ConfirmationDialog';
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

  const showSnackbar = (message, severity = 'success') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleViewFATS = (idno) => {
    setSelectedFatsId(idno);
    setFatsDetailMode('view');
    setFatsDetailOpen(true);
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
    // Refresh would happen automatically if we had state management
  };

  const handleCommentSave = () => {
    showSnackbar('Comment added successfully!');
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

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Box>
          <Box sx={{ mb: 2, display: 'flex', justifyContent: 'flex-end' }}>
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
            onViewFATS={handleViewFATS}
            onEditFATS={handleEditFATS}
            onAddComment={handleAddComment}
          />
        </Box>

        {/* FATS Detail Dialog */}
        <FATSDetail
          open={fatsDetailOpen}
          fatsId={selectedFatsId}
          mode={fatsDetailMode}
          onClose={() => setFatsDetailOpen(false)}
          onSave={handleFATSSave}
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
