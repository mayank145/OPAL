import React, { useState, useEffect, useCallback, forwardRef, useImperativeHandle } from 'react';
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

const FATSList = forwardRef(({ onViewFATS, onEditFATS, onAddComment, onRefresh }, ref) => {
  const [fatsList, setFatsList] = useState([]);
  const [allFatsList, setAllFatsList] = useState([]); // Store all fetched data for client-side filtering
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeSearchTerm, setActiveSearchTerm] = useState(''); // The term actually used for search
  const [sectionFilter, setSectionFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [statistics, setStatistics] = useState(null);
  const [sections, setSections] = useState([]); // All available sections from fsection table
  
  // Expose refresh method to parent component
  useImperativeHandle(ref, () => ({
    refresh: () => {
      console.log('🔄 Refreshing FATS list...');
      loadFATS();
    }
  }));

  const loadFATS = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      console.log('🔍 Loading FATS - Section:', sectionFilter, 'Search:', activeSearchTerm);
      
      // Check if search term is a pure number (likely an IDNo)
      const isIdSearch = activeSearchTerm && /^\d+$/.test(activeSearchTerm.trim());
      
      let results;
      
      if (isIdSearch) {
        // Use backend searchByIdno for ID searches (searches entire database)
        console.log('🔢 Searching by ID in entire database:', activeSearchTerm.trim());
        results = await fatsAPI.searchByIdno(activeSearchTerm.trim());
        
        // Apply section filter if selected
        if (sectionFilter && results) {
          results = results.filter(fault => 
            fault.section === sectionFilter || fault.section2 === sectionFilter
          );
          console.log('📂 Filtered by section:', results.length, 'results');
        }
      } else if (activeSearchTerm && activeSearchTerm.trim()) {
        const searchTerm = activeSearchTerm.trim();
        
        // Check if it's a phrase search (wrapped in quotes)
        const isPhraseSearch = (searchTerm.startsWith('"') && searchTerm.endsWith('"')) ||
                               (searchTerm.startsWith("'") && searchTerm.endsWith("'"));
        
        if (isPhraseSearch) {
          // Phrase search: Search for exact phrase
          const phrase = searchTerm.slice(1, -1).trim(); // Remove quotes
          console.log('📖 Searching for exact phrase:', phrase);
          
          const params = {
            search: phrase,
            section: sectionFilter || undefined,
            limit: 1000,
          };
          
          results = await fatsAPI.getAll(params);
          console.log('✅ Found:', results.length, 'faults matching phrase:', phrase);
        } else {
          // Keyword search: Use backend with high limit to search entire database
          console.log('🔎 Searching entire database for keywords:', searchTerm);
          
          // Split keywords and search for each one, then combine results
          const keywords = searchTerm.toLowerCase().split(/\s+/).filter(k => k.length > 0);
          const allResults = [];
          const seenIds = new Set();
          
          // Search for each keyword
          for (const keyword of keywords) {
            const params = {
              search: keyword,
              section: sectionFilter || undefined,
              limit: 1000, // High limit to search more records
            };
            
            const keywordResults = await fatsAPI.getAll(params);
            
            // Add unique results only
            keywordResults.forEach(fault => {
              if (!seenIds.has(fault.idno)) {
                seenIds.add(fault.idno);
                allResults.push(fault);
              }
            });
          }
          
          results = allResults;
          console.log('✅ Found:', results.length, 'unique faults for', keywords.length, 'keyword(s)');
        }
      } else {
        // No search term: Just fetch with filters
        const params = {
          section: sectionFilter || undefined,
          limit: 100,
        };
        results = await fatsAPI.getAll(params);
      }
      
      setAllFatsList(results || []);
      
      // Limit to 20 results for display on main page
      const limited = (results || []).slice(0, 20);
      console.log('📊 Displaying:', limited.length, 'faults');
      
      setFatsList(limited);
      
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

  // Truncate text to specified length with ellipsis (for solution titles)
  const truncateText = (text, maxLength = 60) => {
    if (!text) return 'N/A';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength).trim() + '...';
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
            placeholder="Search by ID, keywords (e.g., 4767 camera fault)..."
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
            helperText='Search by ID (4767), keywords (tracking error), or exact phrase ("tracking error")'
          />
          <Button
            variant="contained"
            onClick={handleSearch}
            startIcon={<SearchIcon />}
            size="small"
            sx={{ height: '40px', alignSelf: 'flex-start' }}
          >
            SEARCH
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
                  <TableCell>Section</TableCell>
                  <TableCell>Issue</TableCell>
                  <TableCell>Solution</TableCell>
                  <TableCell align="center">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {fatsList.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center">
                      <Box sx={{ py: 4 }}>
                        <Typography variant="h6" color="text.secondary" gutterBottom>
                          {activeSearchTerm ? '🔍 No Faults Found' : '📋 No FATS Entries'}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                          {activeSearchTerm && /^\d+$/.test(activeSearchTerm.trim()) ? (
                            <>
                              Fault ID <strong>{activeSearchTerm}</strong> does not exist in the database.
                              {sectionFilter && <><br />Section filter: <strong>{sectionFilter}</strong></>}
                              <br /><br />
                              <Typography variant="caption" component="span">
                                💡 Try searching without section filter or verify the ID number.
                              </Typography>
                            </>
                          ) : activeSearchTerm ? (
                            <>
                              No faults found matching: <strong>{activeSearchTerm}</strong>
                              {sectionFilter && <><br />in section: <strong>{sectionFilter}</strong></>}
                              <br /><br />
                              <Typography variant="caption" component="span">
                                💡 Try different keywords, check spelling, or remove section filter.
                              </Typography>
                            </>
                          ) : sectionFilter ? (
                            <>
                              No faults found in section: <strong>{sectionFilter}</strong>
                              <br /><br />
                              <Typography variant="caption" component="span">
                                💡 Try selecting a different section or "All Sections".
                              </Typography>
                            </>
                          ) : (
                            'No FATS entries available'
                          )}
                        </Typography>
                      </Box>
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
                        <Typography variant="body2" noWrap sx={{ maxWidth: 200 }}>
                          {fats.section || fats.section2 || '.none'}
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
                        <Typography variant="body2" sx={{ maxWidth: 300 }}>
                          {truncateText(fats.solution, 60)}
                        </Typography>
                      </TableCell>
                      <TableCell align="center">
                        <Box sx={{ display: 'flex', gap: 0.5, justifyContent: 'center' }}>
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
                        </Box>
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
});

export default FATSList;

