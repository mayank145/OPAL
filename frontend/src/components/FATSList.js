import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Button,
  Chip,
  IconButton,
  Typography,
  InputAdornment,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Tooltip,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Search as SearchIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Edit as EditIcon,
  AddComment as CommentIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { fatsAPI, referenceAPI } from '../services/api';

const FATSList = ({ onViewFATS, onEditFATS, onAddComment, onRefresh }) => {
  const [fatsList, setFatsList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeSearchTerm, setActiveSearchTerm] = useState(''); // The term actually used for search
  const [sectionFilter, setSectionFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [statistics, setStatistics] = useState(null);
  const [sections, setSections] = useState([]); // All available sections from fsection table

  const loadFATS = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      // If search term looks like an IDNo, use search endpoint
      if (activeSearchTerm.trim() && activeSearchTerm.trim().length >= 3) {
        const results = await fatsAPI.searchByIdno(activeSearchTerm.trim());
        setFatsList(results || []);
      } else {
        const params = {
          search: activeSearchTerm || undefined,
          section: sectionFilter || undefined,
          status: statusFilter || undefined,
          limit: 20, // Reduced to 20 for faster loading and to prevent timeouts
        };
        const results = await fatsAPI.getAll(params);
        setFatsList(results || []);
      }
      
      // Load statistics (only once, not on every search)
      if (!statistics) {
        try {
          const stats = await fatsAPI.getStatistics();
          setStatistics(stats);
        } catch (statsErr) {
          // Don't fail the whole load if stats fail
          console.warn('Failed to load statistics:', statsErr);
        }
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to load FATS entries';
      setError(errorMsg);
      console.error('Error loading FATS:', err);
      console.error('Error details:', {
        message: err.message,
        code: err.code,
        response: err.response?.data,
        status: err.response?.status
      });
      setFatsList([]); // Set empty list on error
    } finally {
      setLoading(false);
    }
  }, [activeSearchTerm, sectionFilter, statusFilter, statistics]);

  // Load sections from API on mount (only once)
  useEffect(() => {
    const loadSections = async () => {
      try {
        if (process.env.NODE_ENV === 'development') {
          console.log('Loading sections...');
        }
        const sectionsData = await referenceAPI.getSections();
        if (process.env.NODE_ENV === 'development') {
          console.log('Sections loaded:', sectionsData?.length || 0);
        }
        setSections(sectionsData || []);
      } catch (err) {
        console.warn('Failed to load sections:', err);
        // Set empty array on error
        setSections([]);
      }
    };
    loadSections();
  }, []);

  // Load FATS when filters or search term changes
  useEffect(() => {
    if (process.env.NODE_ENV === 'development') {
      console.log('FATS load triggered:', { activeSearchTerm, sectionFilter, statusFilter });
    }
    loadFATS();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeSearchTerm, sectionFilter, statusFilter]); // Removed loadFATS from deps to prevent infinite loop

  const handleSearch = () => {
    // Update active search term to trigger search
    setActiveSearchTerm(searchTerm);
  };

  const handleDeleteBlank = async () => {
    if (window.confirm('Are you sure you want to delete all blank FATS entries?\n\nThis will delete entries where Issue, Description, and Solution are all N/A (or empty).')) {
      try {
        const result = await fatsAPI.deleteBlank();
        alert(`Deleted ${result.deleted_count} blank FATS entries`);
        loadFATS();
        if (onRefresh) onRefresh();
      } catch (err) {
        alert(`Error: ${err.message}`);
      }
    }
  };

  // Status color helper
  const getStatusColor = (status) => {
    switch (status) {
      case 'Active':
        return 'success';
      case 'Canceled':
        return 'default';
      default:
        return 'warning';
    }
  };


  // Strip HTML tags from text
  const stripHtml = (html) => {
    if (!html) return 'N/A';
    // Create a temporary div element
    const tmp = document.createElement('div');
    tmp.innerHTML = html;
    // Get text content and clean up whitespace
    const text = tmp.textContent || tmp.innerText || '';
    return text.trim().replace(/\s+/g, ' ') || 'N/A';
  };

  // Remove date prefixes from description (e.g., "(9/16/2025) Moritani:")
  const cleanDescription = (text) => {
    if (!text || text === 'N/A') return 'N/A';
    // Remove patterns like "(MM/DD/YYYY) Name:" or "(MM/DD/YY) Name:"
    // Matches: (9/16/2025) Moritani: or (8/28/2025) Kumura-san:
    const datePattern = /^\(\d{1,2}\/\d{1,2}\/\d{2,4}\)\s*[^:]+:\s*/i;
    return text.replace(datePattern, '').trim() || 'N/A';
  };

  // Format date for display
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      // Format as YYYY-MM-DD HH:MM
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${year}-${month}-${day} ${hours}:${minutes}`;
    } catch (e) {
      return dateString; // Return as-is if parsing fails
    }
  };

  return (
    <Box>
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h5" component="h2">
            FATS Entries
          </Typography>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Tooltip title="Delete Blank FATS">
              <Button
                variant="outlined"
                color="error"
                size="small"
                onClick={handleDeleteBlank}
                startIcon={<DeleteIcon />}
              >
                Delete Blank
              </Button>
            </Tooltip>
            <Button
              variant="outlined"
              onClick={loadFATS}
              startIcon={<RefreshIcon />}
              size="small"
            >
              Refresh
            </Button>
          </Box>
        </Box>

        {statistics && (
          <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
            <Chip label={`Total: ${statistics.total_fats}`} color="primary" />
          </Box>
        )}

        <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
          <TextField
            placeholder="Search by issue..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            size="small"
            sx={{ flexGrow: 1, minWidth: 300 }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
          <Button
            variant="contained"
            onClick={handleSearch}
            startIcon={<SearchIcon />}
          >
            Search
          </Button>
            <FormControl size="small" sx={{ minWidth: 200 }}>
              <InputLabel>Section</InputLabel>
              <Select
                value={sectionFilter}
                label="Section"
                onChange={(e) => setSectionFilter(e.target.value)}
              >
                <MenuItem value="">All Sections</MenuItem>
                {sections.map((section) => (
                  <MenuItem key={section} value={section}>
                    {section === '.none' ? 'None' : section}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Status</InputLabel>
            <Select
              value={statusFilter}
              label="Status"
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <MenuItem value="">All Status</MenuItem>
              <MenuItem value="Active">Active</MenuItem>
              <MenuItem value="Canceled">Canceled</MenuItem>
            </Select>
          </FormControl>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>IDNo</TableCell>
                  <TableCell>Date</TableCell>
                  <TableCell>Issue</TableCell>
                  <TableCell>Description</TableCell>
                  <TableCell>Solution</TableCell>
                  <TableCell align="center">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {fatsList.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center">
                      <Typography variant="body2" color="text.secondary">
                        No FATS entries found
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  fatsList.map((fats) => (
                    <TableRow key={fats.idno} hover>
                      <TableCell>
                        <Typography
                          variant="body2"
                          component="span"
                          sx={{
                            fontWeight: 'bold',
                            cursor: 'pointer',
                            color: 'primary.main',
                            '&:hover': {
                              textDecoration: 'underline',
                            },
                          }}
                          onClick={() => onViewFATS(fats.idno)}
                        >
                          {fats.idno}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" sx={{ fontSize: '0.875rem', whiteSpace: 'nowrap' }}>
                          {formatDate(fats.datein)}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography
                          variant="body2"
                          noWrap
                          sx={{
                            maxWidth: 300,
                            cursor: 'pointer',
                            color: 'primary.main',
                            '&:hover': {
                              textDecoration: 'underline',
                            },
                          }}
                          onClick={() => onViewFATS(fats.idno)}
                        >
                          {fats.issue || 'N/A'}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" noWrap sx={{ maxWidth: 400 }}>
                          {cleanDescription(stripHtml(fats.idescribe))}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" noWrap sx={{ maxWidth: 300 }}>
                          {stripHtml(fats.sdescribe) || fats.solution || 'N/A'}
                        </Typography>
                      </TableCell>
                      <TableCell align="center">
                        <Tooltip title="View Details">
                          <IconButton
                            size="small"
                            onClick={() => onViewFATS(fats.idno)}
                            color="primary"
                          >
                            <ViewIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Edit">
                          <IconButton
                            size="small"
                            onClick={() => onEditFATS(fats.idno)}
                            color="info"
                          >
                            <EditIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Add Comment">
                          <IconButton
                            size="small"
                            onClick={() => onAddComment(fats.idno)}
                            color="success"
                          >
                            <CommentIcon />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>
    </Box>
  );
};

export default FATSList;

