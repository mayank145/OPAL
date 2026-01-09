import React, { useState, useEffect, useRef } from 'react';
import {
  Paper,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Chip,
  Divider,
  Grid,
  ImageList,
  ImageListItem,
  Dialog,
  DialogContent,
  DialogTitle,
  DialogActions,
  IconButton,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { 
  Close as CloseIcon,
  ZoomIn as ZoomInIcon,
  ZoomOut as ZoomOutIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  Print as PrintIcon,
  Delete as DeleteIcon,
  Share as ShareIcon,
  Edit as EditIcon,
  Link as LinkIcon,
} from '@mui/icons-material';
import DOMPurify from 'dompurify';
import { fatsAPI, referenceAPI } from '../services/api';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const FATSDetailInline = ({ fatsId }) => {
  const [fats, setFats] = useState(null);
  const [images, setImages] = useState([]);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [imageZoom, setImageZoom] = useState(1);
  const [imagePosition, setImagePosition] = useState({ x: 0, y: 0 });
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [imageToDelete, setImageToDelete] = useState(null);
  const [deleteError, setDeleteError] = useState(null);
  const imageContainerRef = useRef(null);
  
  // Edit dialog states
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editFormData, setEditFormData] = useState({});
  const [editLoading, setEditLoading] = useState(false);
  const [editError, setEditError] = useState(null);
  const [sections, setSections] = useState([]);
  const [staff, setStaff] = useState([]); // Staff/operator list

  useEffect(() => {
    loadFATSDetail();
    loadImages();
    loadComments();
    loadSections();
    loadStaff();
  }, [fatsId]);

  // Handle clicks on internal fault links
  useEffect(() => {
    const handleLinkClick = (e) => {
      const target = e.target.closest('a');
      if (!target) return;
      
      const href = target.getAttribute('href');
      
      // Check if it's an internal fault link (#fault-XXXX)
      if (href && href.startsWith('#fault-')) {
        e.preventDefault();
        e.stopPropagation();
        const faultId = href.replace('#fault-', '');
        const faultIdNum = parseInt(faultId);
        
        if (!isNaN(faultIdNum) && window.handleViewFATS) {
          window.handleViewFATS(faultIdNum);
        }
      }
    };

    // Add event listener to the component
    const container = document.getElementById(`fault-detail-${fatsId}`);
    if (container) {
      container.addEventListener('click', handleLinkClick);
      return () => container.removeEventListener('click', handleLinkClick);
    }
  }, [fatsId]);

  const loadFATSDetail = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fatsAPI.getById(fatsId);
      setFats(data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load fault details');
      console.error('Error loading FATS:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadImages = async () => {
    try {
      const imagesData = await fatsAPI.getImages(fatsId);
      setImages(imagesData || []);
    } catch (err) {
      console.error('Error loading images:', err);
      setImages([]);
    }
  };

  const loadComments = async () => {
    try {
      const commentsData = await fatsAPI.getComments(fatsId);
      setComments(commentsData || []);
    } catch (err) {
      console.error('Error loading comments:', err);
      setComments([]);
    }
  };

  const loadSections = async () => {
    try {
      const sectionsData = await referenceAPI.getSections();
      setSections(sectionsData || []);
    } catch (err) {
      console.error('Error loading sections:', err);
      setSections([]);
    }
  };

  const loadStaff = async () => {
    try {
      const staffData = await referenceAPI.getStaff();
      setStaff(staffData || []);
    } catch (err) {
      console.error('Error loading staff:', err);
      setStaff([]);
    }
  };

  const handleKeyPress = (e) => {
    if (!selectedImage || images.length <= 1) return;
    
    const currentIndex = images.findIndex(img => img.filename === selectedImage.filename);
    
    if (e.key === 'ArrowLeft' && currentIndex > 0) {
      setSelectedImage(images[currentIndex - 1]);
      setImageZoom(1);
      setImagePosition({ x: 0, y: 0 });
    } else if (e.key === 'ArrowRight' && currentIndex < images.length - 1) {
      setSelectedImage(images[currentIndex + 1]);
      setImageZoom(1);
      setImagePosition({ x: 0, y: 0 });
    } else if (e.key === 'Escape') {
      setSelectedImage(null);
      setImageZoom(1);
      setImagePosition({ x: 0, y: 0 });
    } else if (e.key === '+' || e.key === '=') {
      setImageZoom(prev => Math.min(prev + 0.25, 3));
    } else if (e.key === '-' || e.key === '_') {
      setImageZoom(prev => Math.max(prev - 0.25, 0.5));
      if (imageZoom <= 1) setImagePosition({ x: 0, y: 0 });
    }
  };

  useEffect(() => {
    if (selectedImage) {
      window.addEventListener('keydown', handleKeyPress);
      return () => window.removeEventListener('keydown', handleKeyPress);
    }
  }, [selectedImage, images, imageZoom]);

  const sanitizeHTML = (html) => {
    if (!html) return '';
    return DOMPurify.sanitize(html, {
      ALLOWED_TAGS: ['p', 'br', 'strong', 'b', 'em', 'i', 'u', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'code', 'pre', 'blockquote', 'span', 'div'],
      ALLOWED_ATTR: ['href', 'target', 'rel', 'class', 'style'],
      ALLOWED_STYLES: {
        '*': {
          'color': [/^#[0-9a-fA-F]{3,6}$/, /^rgb\(/, /^rgba\(/],
          'background-color': [/^#[0-9a-fA-F]{3,6}$/, /^rgb\(/, /^rgba\(/],
          'font-weight': [/^bold$/, /^normal$/, /^\d{3}$/],
          'font-style': [/^italic$/, /^normal$/],
          'text-decoration': [/^underline$/, /^line-through$/],
        }
      }
    });
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch (e) {
      return dateString;
    }
  };

  // Helper function to strip HTML tags and convert to plain text
  const stripHtml = (html) => {
    if (!html) return '';
    // Create a temporary div element
    const tmp = document.createElement('div');
    tmp.innerHTML = html;
    // Get text content (this strips all HTML tags)
    return tmp.textContent || tmp.innerText || '';
  };

  const handleEdit = () => {
    // Initialize form with current FATS data
    // Strip HTML from description fields
    setEditFormData({
      issue: fats.issue || '',
      idescribe: stripHtml(fats.idescribe) || '',
      solution: fats.solution || '',
      sdescribe: stripHtml(fats.sdescribe) || '',
      section: fats.section || '',
      status: fats.status || 'Active',
      operator: fats.operator || '', // Current operator/editor
    });
    setEditError(null);
    setEditDialogOpen(true);
  };

  const handleEditClose = () => {
    setEditDialogOpen(false);
    setEditFormData({});
    setEditError(null);
  };

  const handleEditChange = (field, value) => {
    setEditFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Helper function to convert plain text to HTML
  const textToHtml = (text) => {
    if (!text) return '';
    // Split by newlines and wrap each line in <p> tags
    const lines = text.split('\n').filter(line => line.trim());
    if (lines.length === 0) return '<p></p>';
    return lines.map(line => `<p>${line}</p>`).join('\n');
  };

  const handleEditSave = async () => {
    try {
      setEditLoading(true);
      setEditError(null);
      
      // Prepare data with text converted back to HTML format
      const dataToSave = {
        ...editFormData,
        // Convert plain text descriptions back to HTML
        idescribe: textToHtml(editFormData.idescribe),
        sdescribe: textToHtml(editFormData.sdescribe),
        // Set assigned_to to the selected operator (editor)
        assigned_to: editFormData.operator || fats.operator || 'Unknown User',
      };
      
      // Call the update API
      await fatsAPI.update(fatsId, dataToSave);
      
      // Reload the FATS detail
      await loadFATSDetail();
      
      // Close the dialog
      setEditDialogOpen(false);
      setEditFormData({});
      
      // Show success message
      alert(`Fault #${fatsId} updated successfully!`);
    } catch (err) {
      console.error('Error updating FATS:', err);
      setEditError(err.response?.data?.detail || err.message || 'Failed to update fault');
    } finally {
      setEditLoading(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const handleCopyLink = () => {
    const link = `${window.location.origin}/#fault-${fatsId}`;
    
    // Try modern clipboard API first (requires HTTPS)
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(link).then(() => {
        alert(`Link copied to clipboard!\n\n${link}\n\nShare this link to open Fault #${fatsId} on any device.`);
      }).catch(err => {
        console.error('Failed to copy link:', err);
        copyLinkFallback(link);
      });
    } else {
      // Fallback for HTTP or older browsers
      copyLinkFallback(link);
    }
  };

  const copyLinkFallback = (link) => {
    // Create a temporary textarea element
    const textarea = document.createElement('textarea');
    textarea.value = link;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    textarea.style.top = '0';
    document.body.appendChild(textarea);
    
    try {
      textarea.focus();
      textarea.select();
      const successful = document.execCommand('copy');
      document.body.removeChild(textarea);
      
      if (successful) {
        alert(`Link copied to clipboard!\n\n${link}\n\nShare this link to open Fault #${fatsId} on any device.`);
      } else {
        // If even fallback fails, show link for manual copy
        prompt('Copy this link (Ctrl+C or Cmd+C):', link);
      }
    } catch (err) {
      document.body.removeChild(textarea);
      // Last resort: show in prompt dialog
      prompt('Copy this link (Ctrl+C or Cmd+C):', link);
    }
  };

  const handlePrintImage = () => {
    if (!selectedImage) return;
    
    // Create a new window for printing the image
    const printWindow = window.open('', '_blank');
    const imageUrl = selectedImage.url 
      ? (selectedImage.url.startsWith('http') ? selectedImage.url : `${API_BASE_URL}${selectedImage.url}`)
      : `${API_BASE_URL}/uploads/fats/${selectedImage.filename}`;
    
    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>Print Image - ${selectedImage.filename}</title>
          <style>
            body {
              margin: 0;
              padding: 20px;
              display: flex;
              flex-direction: column;
              align-items: center;
              justify-content: center;
              min-height: 100vh;
            }
            h3 {
              margin-bottom: 20px;
              font-family: Arial, sans-serif;
              color: #333;
            }
            img {
              max-width: 100%;
              max-height: 90vh;
              object-fit: contain;
            }
            @media print {
              body {
                padding: 0;
              }
              h3 {
                page-break-after: avoid;
              }
            }
          </style>
        </head>
        <body>
          <h3>Fault #${fats.idno} - ${selectedImage.filename}</h3>
          <img src="${imageUrl}" alt="${selectedImage.filename}" onload="window.print(); setTimeout(() => window.close(), 100);" />
        </body>
      </html>
    `);
    printWindow.document.close();
  };

  const handleDeleteImageClick = (image, event) => {
    event.stopPropagation(); // Prevent opening the image preview
    setImageToDelete(image);
    setDeleteConfirmOpen(true);
    setDeleteError(null);
  };

  const handleDeleteImageConfirm = async () => {
    if (!imageToDelete) return;
    
    try {
      await fatsAPI.deleteImage(imageToDelete.filename);
      
      // Reload images after successful deletion
      await loadImages();
      
      // Close the preview if the deleted image was being previewed
      if (selectedImage && selectedImage.filename === imageToDelete.filename) {
        setSelectedImage(null);
        setImageZoom(1);
        setImagePosition({ x: 0, y: 0 });
      }
      
      // Close confirmation dialog
      setDeleteConfirmOpen(false);
      setImageToDelete(null);
    } catch (err) {
      console.error('Error deleting image:', err);
      setDeleteError(err.response?.data?.detail || err.message || 'Failed to delete image');
    }
  };

  const handleDeleteImageCancel = () => {
    setDeleteConfirmOpen(false);
    setImageToDelete(null);
    setDeleteError(null);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  if (!fats) {
    return (
      <Alert severity="warning" sx={{ m: 2 }}>
        Fault not found
      </Alert>
    );
  }

  return (
    <>
      {/* Print Styles */}
      <style>
        {`
          @media print {
            body * {
              visibility: hidden;
            }
            .print-area, .print-area * {
              visibility: visible;
            }
            .print-area {
              position: absolute;
              left: 0;
              top: 0;
              width: 100%;
              padding: 20px;
            }
            .print-hide {
              display: none !important;
            }
            .print-area img {
              max-width: 100%;
              page-break-inside: avoid;
            }
            @page {
              margin: 1cm;
            }
          }
        `}
      </style>
      
      <Paper elevation={2} sx={{ p: 3, m: 2 }} className="print-area">
        {/* Header */}
      <Box sx={{ mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Typography variant="h5" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
              Fault #{fats.idno}
            </Typography>
            <Chip 
              label={fats.status || 'Active'} 
              color={fats.status === 'Active' ? 'success' : 'default'}
              size="small"
            />
          </Box>
          <Box sx={{ display: 'flex', gap: 1, '@media print': { display: 'none' } }}>
            <Button
              variant="contained"
              color="primary"
              startIcon={<EditIcon />}
              onClick={handleEdit}
              size="small"
            >
              Edit
            </Button>
            <Button
              variant="outlined"
              color="primary"
              startIcon={<ShareIcon />}
              onClick={handleCopyLink}
              size="small"
            >
              Copy Link
            </Button>
            <Button
              variant="contained"
              color="primary"
              startIcon={<PrintIcon />}
              onClick={handlePrint}
              size="small"
            >
              Print
            </Button>
          </Box>
        </Box>
        <Typography variant="body2" color="text.secondary">
          Created: {formatDate(fats.datein)} | Operator: {fats.operator || 'N/A'}
        </Typography>
      </Box>

      <Divider sx={{ mb: 3 }} />

      {/* SECTION 1: ISSUE INFORMATION */}
      <Paper elevation={2} sx={{ p: 3, mb: 3, bgcolor: '#f8f9fa' }}>
        <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold', color: 'primary.main', borderBottom: '2px solid', borderColor: 'primary.main', pb: 1 }}>
          Issue Information
        </Typography>
        
        <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ fontWeight: 'bold' }}>
          Issue:
        </Typography>
        <Typography variant="body1" sx={{ mb: 2, pl: 1 }}>
          {fats.issue || 'N/A'}
        </Typography>

        <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ fontWeight: 'bold' }}>
          Sections:
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, mb: 2, pl: 1 }}>
          <Chip label={`Section: ${fats.section || '.none'}`} size="small" variant="outlined" />
          {fats.section2 && fats.section2 !== '.none' && (
            <Chip label={`Section 2: ${fats.section2}`} size="small" variant="outlined" />
          )}
        </Box>

        <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ fontWeight: 'bold' }}>
          Issue Description:
        </Typography>
        <Paper variant="outlined" sx={{ p: 2, bgcolor: 'white', mb: 2 }}>
          <Box
            sx={{
              '& p': { marginBottom: '0.5rem', marginTop: 0 },
              '& p:last-child': { marginBottom: 0 },
              '& ul, & ol': { paddingLeft: '1.5rem', marginBottom: '0.5rem', marginTop: '0.5rem' },
              '& li': { marginBottom: '0.25rem' },
              '& strong, & b': { fontWeight: 'bold' },
              '& em, & i': { fontStyle: 'italic' },
              '& u': { textDecoration: 'underline' },
              '& a': { 
                color: '#1976d2', 
                textDecoration: 'underline', 
                cursor: 'pointer',
                '&:hover': { color: '#115293' },
                '&[href^="#fault-"]': {
                  color: '#d32f2f',
                  fontWeight: 600,
                  '&::before': {
                    content: '"🔗 "',
                    fontSize: '0.9em',
                  },
                  '&:hover': {
                    color: '#b71c1c',
                    backgroundColor: 'rgba(211, 47, 47, 0.1)',
                    padding: '2px 4px',
                    borderRadius: '3px',
                  }
                },
              },
              '& h1': { fontSize: '2rem', fontWeight: 'bold', marginTop: '1rem', marginBottom: '0.5rem' },
              '& h2': { fontSize: '1.5rem', fontWeight: 'bold', marginTop: '1rem', marginBottom: '0.5rem' },
              '& h3': { fontSize: '1.25rem', fontWeight: 'bold', marginTop: '0.75rem', marginBottom: '0.5rem' },
            }}
            dangerouslySetInnerHTML={{ 
              __html: sanitizeHTML(fats.idescribe) || '<p style="color: #999;">No issue description provided</p>' 
            }}
          />
        </Paper>
      </Paper>

      {/* SECTION 2: ACTION / RESOLUTION */}
      <Paper elevation={2} sx={{ p: 3, bgcolor: '#f0f7ff' }}>
        <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold', color: 'success.main', borderBottom: '2px solid', borderColor: 'success.main', pb: 1 }}>
          Action / Resolution
        </Typography>

        <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ fontWeight: 'bold' }}>
          Action:
        </Typography>
        <Typography variant="body1" sx={{ mb: 2, pl: 1 }}>
          {fats.todo || 'N/A'}
        </Typography>

        <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ fontWeight: 'bold' }}>
          Solution:
        </Typography>
        <Typography variant="body1" sx={{ mb: 2, pl: 1 }}>
          {fats.solution || 'N/A'}
        </Typography>

        <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ fontWeight: 'bold' }}>
          Solution Description:
        </Typography>
        <Paper variant="outlined" sx={{ p: 2, bgcolor: 'white', mb: 3 }}>
          <Box
            sx={{
              '& p': { marginBottom: '0.5rem', marginTop: 0 },
              '& p:last-child': { marginBottom: 0 },
              '& ul, & ol': { paddingLeft: '1.5rem', marginBottom: '0.5rem', marginTop: '0.5rem' },
              '& li': { marginBottom: '0.25rem' },
              '& strong, & b': { fontWeight: 'bold' },
              '& em, & i': { fontStyle: 'italic' },
              '& u': { textDecoration: 'underline' },
              '& a': { 
                color: '#1976d2', 
                textDecoration: 'underline', 
                cursor: 'pointer',
                '&:hover': { color: '#115293' },
                '&[href^="#fault-"]': {
                  color: '#d32f2f',
                  fontWeight: 600,
                  '&::before': {
                    content: '"🔗 "',
                    fontSize: '0.9em',
                  },
                  '&:hover': {
                    color: '#b71c1c',
                    backgroundColor: 'rgba(211, 47, 47, 0.1)',
                    padding: '2px 4px',
                    borderRadius: '3px',
                  }
                },
              },
              '& h1': { fontSize: '2rem', fontWeight: 'bold', marginTop: '1rem', marginBottom: '0.5rem' },
              '& h2': { fontSize: '1.5rem', fontWeight: 'bold', marginTop: '1rem', marginBottom: '0.5rem' },
              '& h3': { fontSize: '1.25rem', fontWeight: 'bold', marginTop: '0.75rem', marginBottom: '0.5rem' },
              '& code': { 
                backgroundColor: 'rgba(0, 0, 0, 0.05)', 
                padding: '2px 6px', 
                borderRadius: '3px',
                fontFamily: 'monospace',
                fontSize: '0.9em'
              },
              '& pre': { 
                backgroundColor: 'rgba(0, 0, 0, 0.05)', 
                padding: '1rem', 
                borderRadius: '4px',
                overflow: 'auto',
                '& code': { backgroundColor: 'transparent', padding: 0 }
              },
              '& blockquote': { 
                borderLeft: '4px solid #ccc', 
                paddingLeft: '1rem', 
                marginLeft: 0,
                color: '#666',
                fontStyle: 'italic'
              },
            }}
            dangerouslySetInnerHTML={{ 
              __html: sanitizeHTML(fats.sdescribe) || '<p style="color: #999;">No solution description provided</p>' 
            }}
          />
        </Paper>

        {/* Pictures Section */}
        <Divider sx={{ my: 2 }} />
        <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ fontWeight: 'bold' }}>
          Pictures:
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1, pl: 1 }}>
          {images.length} image(s)
        </Typography>
        {images.length > 0 ? (
          <ImageList cols={3} gap={8} sx={{ maxHeight: 400, overflow: 'auto', mt: 2, mb: 3 }}>
            {images.map((image) => (
              <ImageListItem 
                key={image.filename}
                sx={{ 
                  cursor: 'pointer',
                  position: 'relative',
                  '&:hover .delete-overlay': {
                    opacity: 1,
                  }
                }}
                onClick={() => setSelectedImage(image)}
              >
                <img
                  src={image.url ? (image.url.startsWith('http') ? image.url : `${API_BASE_URL}${image.url}`) : `${API_BASE_URL}/uploads/fats/${image.filename}`}
                  alt={image.filename}
                  loading="lazy"
                  style={{ 
                    width: '100%', 
                    height: '200px', 
                    objectFit: 'cover',
                    borderRadius: '4px'
                  }}
                  onError={(e) => {
                    console.error('Image load error:', image.filename);
                    e.target.style.display = 'none';
                  }}
                />
                <Box
                  className="delete-overlay"
                  sx={{
                    position: 'absolute',
                    top: 0,
                    right: 0,
                    opacity: 0,
                    transition: 'opacity 0.2s',
                    zIndex: 1,
                  }}
                >
                  <IconButton
                    size="small"
                    onClick={(e) => handleDeleteImageClick(image, e)}
                    sx={{
                      bgcolor: 'error.main',
                      color: 'white',
                      m: 0.5,
                      '&:hover': {
                        bgcolor: 'error.dark',
                      },
                    }}
                    title="Delete image"
                  >
                    <DeleteIcon fontSize="small" />
                  </IconButton>
                </Box>
              </ImageListItem>
            ))}
          </ImageList>
        ) : (
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2, mb: 3 }}>
            No pictures
          </Typography>
        )}

        {/* Comments Section */}
        <Divider sx={{ my: 2 }} />
        <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ fontWeight: 'bold' }}>
          Comments:
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2, pl: 1 }}>
          {comments.length} comment(s)
        </Typography>
        {comments.length > 0 ? (
          <Box sx={{ mt: 2 }}>
            {comments.map((comment, index) => (
              <Paper 
                key={comment.id || index} 
                variant="outlined" 
                sx={{ p: 2, mb: 2, bgcolor: 'grey.50' }}
              >
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                    {comment.commenter || comment.operator || 'Anonymous'}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {formatDate(comment.created_at || comment.datein)}
                  </Typography>
                </Box>
                <Box
                  sx={{
                    mb: 1,
                    '& p': { marginBottom: '0.5rem', marginTop: 0 },
                    '& p:last-child': { marginBottom: 0 },
                    '& ul, & ol': { paddingLeft: '1.5rem', marginBottom: '0.5rem', marginTop: '0.5rem' },
                    '& li': { marginBottom: '0.25rem' },
                    '& strong, & b': { fontWeight: 'bold' },
                    '& em, & i': { fontStyle: 'italic' },
                    '& u': { textDecoration: 'underline' },
                    '& a': { color: '#1976d2', textDecoration: 'underline' },
                    '& code': { 
                      backgroundColor: 'rgba(0, 0, 0, 0.05)', 
                      padding: '2px 4px', 
                      borderRadius: '3px',
                      fontFamily: 'monospace',
                      fontSize: '0.85em'
                    },
                  }}
                  dangerouslySetInnerHTML={{ 
                    __html: sanitizeHTML(comment.comment_text || comment.sdescribe || comment.comment || comment.content) || '<p style="color: #999;">No comment text</p>' 
                  }}
                />
                {comment.todo && (
                  <Box sx={{ mt: 1, p: 1, bgcolor: 'info.lighter', borderRadius: 1 }}>
                    <Typography variant="caption" sx={{ fontWeight: 'bold', color: 'info.main' }}>
                      TODO:
                    </Typography>
                    <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                      {comment.todo}
                    </Typography>
                  </Box>
                )}
                {comment.solution && (
                  <Box sx={{ mt: 1, p: 1, bgcolor: 'success.lighter', borderRadius: 1 }}>
                    <Typography variant="caption" sx={{ fontWeight: 'bold', color: 'success.main' }}>
                      Solution:
                    </Typography>
                    <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                      {comment.solution}
                    </Typography>
                  </Box>
                )}
              </Paper>
            ))}
          </Box>
        ) : (
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
            No comments yet
          </Typography>
        )}
      </Paper>

      {/* Image Preview Dialog */}
      <Dialog
        open={selectedImage !== null}
        onClose={() => {
          setSelectedImage(null);
          setImageZoom(1);
          setImagePosition({ x: 0, y: 0 });
        }}
        maxWidth="lg"
        fullWidth
        PaperProps={{
          sx: { backgroundColor: 'rgba(0, 0, 0, 0.95)' },
          className: 'print-hide'
        }}
      >
        {selectedImage && (
          <>
            <DialogTitle sx={{ bgcolor: 'rgba(0, 0, 0, 0.95)', color: 'white' }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                  <Typography variant="h6">{selectedImage.filename}</Typography>
                  {images.length > 1 && (
                    <Typography variant="caption" sx={{ opacity: 0.7 }}>
                      {images.findIndex(img => img.filename === selectedImage.filename) + 1} of {images.length}
                    </Typography>
                  )}
                </Box>
                <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                  <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                    {Math.round(imageZoom * 100)}%
                  </Typography>
                  <IconButton
                    onClick={() => setImageZoom(prev => Math.min(prev + 0.25, 3))}
                    disabled={imageZoom >= 3}
                    sx={{ color: 'white' }}
                    title="Zoom In"
                  >
                    <ZoomInIcon />
                  </IconButton>
                  <IconButton
                    onClick={() => {
                      setImageZoom(prev => Math.max(prev - 0.25, 0.5));
                      if (imageZoom <= 1) setImagePosition({ x: 0, y: 0 });
                    }}
                    disabled={imageZoom <= 0.5}
                    sx={{ color: 'white' }}
                    title="Zoom Out"
                  >
                    <ZoomOutIcon />
                  </IconButton>
                  <IconButton
                    onClick={handlePrintImage}
                    sx={{ color: 'white' }}
                    title="Print Image"
                  >
                    <PrintIcon />
                  </IconButton>
                  <IconButton
                    onClick={() => {
                      setSelectedImage(null);
                      setImageZoom(1);
                      setImagePosition({ x: 0, y: 0 });
                    }}
                    sx={{ color: 'white' }}
                  >
                    <CloseIcon />
                  </IconButton>
                </Box>
              </Box>
            </DialogTitle>
            <DialogContent 
              sx={{ 
                textAlign: 'center', 
                p: 0,
                bgcolor: 'rgba(0, 0, 0, 0.95)',
                position: 'relative',
                height: '70vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                overflow: 'hidden',
              }}
            >
              {/* Previous Button */}
              {images.length > 1 && (
                <IconButton
                  onClick={() => {
                    const currentIndex = images.findIndex(img => img.filename === selectedImage.filename);
                    if (currentIndex > 0) {
                      setSelectedImage(images[currentIndex - 1]);
                      setImageZoom(1);
                      setImagePosition({ x: 0, y: 0 });
                    }
                  }}
                  disabled={images.findIndex(img => img.filename === selectedImage.filename) === 0}
                  sx={{
                    position: 'absolute',
                    left: 16,
                    top: '50%',
                    transform: 'translateY(-50%)',
                    color: 'white',
                    bgcolor: 'rgba(0,0,0,0.5)',
                    '&:hover': { bgcolor: 'rgba(0,0,0,0.7)' },
                    zIndex: 1,
                  }}
                  title="Previous Image (←)"
                >
                  <ChevronLeftIcon fontSize="large" />
                </IconButton>
              )}

              {/* Image Container */}
              <Box
                ref={imageContainerRef}
                sx={{
                  width: '100%',
                  height: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  overflow: 'hidden',
                }}
              >
                <img
                  src={selectedImage.url ? (selectedImage.url.startsWith('http') ? selectedImage.url : `${API_BASE_URL}${selectedImage.url}`) : `${API_BASE_URL}/uploads/fats/${selectedImage.filename}`}
                  alt={selectedImage.filename}
                  style={{
                    maxWidth: '100%',
                    maxHeight: '100%',
                    objectFit: 'contain',
                    transform: `scale(${imageZoom}) translate(${imagePosition.x}px, ${imagePosition.y}px)`,
                    transition: 'transform 0.2s ease-in-out',
                    cursor: imageZoom > 1 ? 'move' : 'default',
                  }}
                />
              </Box>

              {/* Next Button */}
              {images.length > 1 && (
                <IconButton
                  onClick={() => {
                    const currentIndex = images.findIndex(img => img.filename === selectedImage.filename);
                    if (currentIndex < images.length - 1) {
                      setSelectedImage(images[currentIndex + 1]);
                      setImageZoom(1);
                      setImagePosition({ x: 0, y: 0 });
                    }
                  }}
                  disabled={images.findIndex(img => img.filename === selectedImage.filename) === images.length - 1}
                  sx={{
                    position: 'absolute',
                    right: 16,
                    top: '50%',
                    transform: 'translateY(-50%)',
                    color: 'white',
                    bgcolor: 'rgba(0,0,0,0.5)',
                    '&:hover': { bgcolor: 'rgba(0,0,0,0.7)' },
                    zIndex: 1,
                  }}
                  title="Next Image (→)"
                >
                  <ChevronRightIcon fontSize="large" />
                </IconButton>
              )}

              {/* Image Info Footer */}
              <Box 
                sx={{ 
                  position: 'absolute',
                  bottom: 0,
                  left: 0,
                  right: 0,
                  bgcolor: 'rgba(0,0,0,0.7)',
                  color: 'white',
                  p: 1,
                  textAlign: 'center',
                }}
              >
                <Typography variant="body2">
                  Uploaded: {selectedImage.uploaded_at ? new Date(selectedImage.uploaded_at).toLocaleString() : 'N/A'}
                </Typography>
                <Typography variant="caption" sx={{ opacity: 0.7, display: 'block', mt: 0.5 }}>
                  💡 Use [←] [→] arrows to navigate | Zoom: {Math.round(imageZoom * 100)}%
                </Typography>
              </Box>
            </DialogContent>
          </>
        )}
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteConfirmOpen}
        onClose={handleDeleteImageCancel}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Delete Image?</DialogTitle>
        <DialogContent>
          <Typography variant="body1" gutterBottom>
            Are you sure you want to delete this image?
          </Typography>
          {imageToDelete && (
            <Box sx={{ mt: 2, textAlign: 'center' }}>
              <img
                src={imageToDelete.url ? (imageToDelete.url.startsWith('http') ? imageToDelete.url : `${API_BASE_URL}${imageToDelete.url}`) : `${API_BASE_URL}/uploads/fats/${imageToDelete.filename}`}
                alt={imageToDelete.filename}
                style={{
                  maxWidth: '100%',
                  maxHeight: '200px',
                  objectFit: 'contain',
                  borderRadius: '4px',
                }}
              />
              <Typography variant="caption" display="block" sx={{ mt: 1, color: 'text.secondary' }}>
                {imageToDelete.filename}
              </Typography>
            </Box>
          )}
          {deleteError && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {deleteError}
            </Alert>
          )}
          <Typography variant="body2" color="error" sx={{ mt: 2, fontWeight: 'bold' }}>
            This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDeleteImageCancel} color="inherit">
            Cancel
          </Button>
          <Button 
            onClick={handleDeleteImageConfirm} 
            color="error" 
            variant="contained"
            startIcon={<DeleteIcon />}
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog
        open={editDialogOpen}
        onClose={handleEditClose}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box>
              <Typography variant="h6">Edit Fault #{fatsId}</Typography>
              <Typography variant="caption" color="text.secondary">
                Current Editor: {editFormData.operator || fats?.operator || 'Not Set'}
              </Typography>
            </Box>
            <IconButton onClick={handleEditClose} size="small">
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent dividers>
          {editError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {editError}
            </Alert>
          )}
          
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            {/* Issue */}
            <TextField
              label="Issue"
              value={editFormData.issue || ''}
              onChange={(e) => handleEditChange('issue', e.target.value)}
              fullWidth
              variant="outlined"
            />

            {/* Issue Description */}
            <Box>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Issue Description
                </Typography>
                <Button
                  size="small"
                  variant="outlined"
                  startIcon={<LinkIcon />}
                  onClick={() => {
                    const url = window.prompt('Enter URL (e.g., https://example.com):');
                    if (url) {
                      const linkText = window.prompt('Enter link text:', url);
                      if (linkText) {
                        const link = `<a href="${url}" target="_blank">${linkText}</a>`;
                        const currentText = editFormData.idescribe || '';
                        handleEditChange('idescribe', currentText + (currentText ? ' ' : '') + link);
                      }
                    }
                  }}
                >
                  Insert Link
                </Button>
              </Box>
              <TextField
                value={editFormData.idescribe || ''}
                onChange={(e) => handleEditChange('idescribe', e.target.value)}
                fullWidth
                multiline
                rows={4}
                variant="outlined"
                helperText="Detailed description of the issue. Use 'Insert Link' button to add hyperlinks."
              />
            </Box>

            {/* Solution */}
            <TextField
              label="Solution"
              value={editFormData.solution || ''}
              onChange={(e) => handleEditChange('solution', e.target.value)}
              fullWidth
              variant="outlined"
            />

            {/* Solution Description */}
            <Box>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Solution Description
                </Typography>
                <Button
                  size="small"
                  variant="outlined"
                  startIcon={<LinkIcon />}
                  onClick={() => {
                    const url = window.prompt('Enter URL (e.g., https://example.com):');
                    if (url) {
                      const linkText = window.prompt('Enter link text:', url);
                      if (linkText) {
                        const link = `<a href="${url}" target="_blank">${linkText}</a>`;
                        const currentText = editFormData.sdescribe || '';
                        handleEditChange('sdescribe', currentText + (currentText ? ' ' : '') + link);
                      }
                    }
                  }}
                >
                  Insert Link
                </Button>
              </Box>
              <TextField
                value={editFormData.sdescribe || ''}
                onChange={(e) => handleEditChange('sdescribe', e.target.value)}
                fullWidth
                multiline
                rows={4}
                variant="outlined"
                helperText="Detailed description of the solution. Use 'Insert Link' button to add hyperlinks."
              />
            </Box>

            {/* Section */}
            <FormControl fullWidth>
              <InputLabel>Section</InputLabel>
              <Select
                value={editFormData.section || ''}
                onChange={(e) => handleEditChange('section', e.target.value)}
                label="Section"
              >
                <MenuItem value="">
                  <em>None</em>
                </MenuItem>
                {sections.map((section) => (
                  <MenuItem key={section} value={section}>
                    {section}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {/* Status */}
            <FormControl fullWidth>
              <InputLabel>Status</InputLabel>
              <Select
                value={editFormData.status || 'Active'}
                onChange={(e) => handleEditChange('status', e.target.value)}
                label="Status"
              >
                <MenuItem value="Active">Active</MenuItem>
                <MenuItem value="Canceled">Canceled</MenuItem>
              </Select>
            </FormControl>

            {/* Editor */}
            <FormControl fullWidth>
              <InputLabel>Editor</InputLabel>
              <Select
                value={editFormData.operator || ''}
                onChange={(e) => handleEditChange('operator', e.target.value)}
                label="Editor"
              >
                <MenuItem value="">
                  <em>Select Editor</em>
                </MenuItem>
                {staff.map((person) => (
                  <MenuItem key={person} value={person}>
                    {person}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={handleEditClose} color="inherit" disabled={editLoading}>
            Cancel
          </Button>
          <Button 
            onClick={handleEditSave} 
            variant="contained" 
            color="primary"
            disabled={editLoading}
            startIcon={editLoading ? <CircularProgress size={20} /> : <EditIcon />}
          >
            {editLoading ? 'Saving...' : 'Save Changes'}
          </Button>
        </DialogActions>
      </Dialog>
    </Paper>
    </>
  );
};

export default FATSDetailInline;

