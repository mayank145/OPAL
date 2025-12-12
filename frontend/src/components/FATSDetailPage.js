import React, { useState, useEffect } from 'react';
import {
  Container,
  AppBar,
  Toolbar,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Button,
} from '@mui/material';
import { ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import FATSDetail from './FATSDetail';

const FATSDetailPage = ({ fatsId }) => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading
    setLoading(false);
  }, [fatsId]);

  const handleBack = () => {
    window.close(); // Close the tab
    // If window.close() doesn't work (opened via link, not window.open), navigate back
    setTimeout(() => {
      window.location.href = '/';
    }, 100);
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="static">
        <Toolbar>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={handleBack}
            sx={{ color: 'white', mr: 2 }}
          >
            Back
          </Button>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            OPAL - Fault Details (ID: {fatsId})
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <FATSDetail
            open={true}
            onClose={handleBack}
            fatsId={fatsId}
            mode="view"
            onSave={() => {}}
            isStandalone={true}
          />
        )}
      </Container>
    </Box>
  );
};

export default FATSDetailPage;

