import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  Box,
  Button,
} from '@mui/material';
import { Close as CloseIcon, ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import { fatsAPI } from '../services/api';
import FATSDetailInline from './FATSDetailInline';

const FullFaultsList = ({ open, onClose }) => {
  const [faults, setFaults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedFaultId, setSelectedFaultId] = useState(null);

  useEffect(() => {
    if (open) {
      loadAllFaults();
    }
  }, [open]);

  const loadAllFaults = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch ALL faults (no limit)
      const results = await fatsAPI.getAll({ limit: 10000 });
      setFaults(results || []);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load faults');
      console.error('Error loading all faults:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    try {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    } catch (e) {
      return dateString;
    }
  };

  const stripHtml = (html) => {
    if (!html) return '';
    const tmp = document.createElement('div');
    tmp.innerHTML = html;
    return (tmp.textContent || tmp.innerText || '').trim();
  };

  return (
    <Dialog 
      open={open} 
      onClose={onClose}
      maxWidth="xl"
      fullWidth
      PaperProps={{
        sx: { height: '90vh' }
      }}
    >
      <DialogTitle>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          {selectedFaultId ? (
            <Button
              startIcon={<ArrowBackIcon />}
              onClick={() => setSelectedFaultId(null)}
              sx={{ mr: 2 }}
            >
              Back to List
            </Button>
          ) : (
            <Typography variant="h6">All Faults List</Typography>
          )}
          <IconButton onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>
      
      <DialogContent dividers>
        {selectedFaultId ? (
          <FATSDetailInline fatsId={selectedFaultId} />
        ) : loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : (
          <>
            <Typography variant="body2" sx={{ mb: 2 }}>
              Total Faults: <strong>{faults.length}</strong>
            </Typography>
            
            <TableContainer 
              component={Paper} 
              sx={{ 
                maxHeight: 'calc(90vh - 200px)', 
                overflowY: 'auto',
                overflowX: 'hidden',
              }}
            >
              <Table size="small" stickyHeader>
                <TableHead>
                  <TableRow>
                    <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5', width: '8%' }}>IDNo</TableCell>
                    <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5', width: '12%' }}>Date</TableCell>
                    <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5', width: '20%' }}>Section</TableCell>
                    <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5', width: '25%' }}>Issue</TableCell>
                    <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5', width: '35%' }}>Solution</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {faults.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} align="center">
                        <Typography variant="body2" color="text.secondary">
                          No faults found
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ) : (
                    faults.map((fault) => (
                      <TableRow key={fault.idno} hover sx={{ cursor: 'pointer' }} onClick={() => setSelectedFaultId(fault.idno)}>
                        <TableCell sx={{ width: '8%' }}>
                          <Typography 
                            variant="body2" 
                            sx={{ 
                              color: 'primary.main',
                              fontWeight: 'bold',
                              '&:hover': { textDecoration: 'underline' }
                            }}
                          >
                            {fault.idno}
                          </Typography>
                        </TableCell>
                        <TableCell sx={{ width: '12%' }}>
                          <Typography variant="body2" sx={{ whiteSpace: 'nowrap', fontSize: '0.85rem' }}>
                            {formatDate(fault.datein)}
                          </Typography>
                        </TableCell>
                        <TableCell sx={{ width: '20%' }}>
                          <Typography variant="body2" sx={{ wordBreak: 'break-word', fontSize: '0.85rem' }}>
                            {fault.section || fault.section2 || '.none'}
                          </Typography>
                        </TableCell>
                        <TableCell sx={{ width: '25%' }}>
                          <Typography 
                            variant="body2" 
                            sx={{ 
                              color: 'primary.main', 
                              wordBreak: 'break-word',
                              '&:hover': { textDecoration: 'underline' }
                            }}
                          >
                            {fault.issue || ''}
                          </Typography>
                        </TableCell>
                        <TableCell sx={{ width: '35%' }}>
                          <Typography variant="body2" sx={{ wordBreak: 'break-word' }}>
                            {fault.solution || 'N/A'}
                          </Typography>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default FullFaultsList;

