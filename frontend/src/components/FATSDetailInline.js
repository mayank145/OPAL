import React, { useState, useEffect, useRef } from 'react';
import {
  Paper,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Chip,
  Divider,
  ImageList,
  ImageListItem,
  Dialog,
  DialogContent,
  DialogTitle,
  DialogActions,
  IconButton,
  Button,
} from '@mui/material';
import { 
  Close as CloseIcon,
  ZoomIn as ZoomInIcon,
  ZoomOut as ZoomOutIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  Print as PrintIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  AddComment as AddCommentIcon,
} from '@mui/icons-material';
import DOMPurify from 'dompurify';
import { fatsAPI } from '../services/api';
import { formatHSTTimestamp } from '../utils/timezone';
import CommentDialog from './CommentDialog';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const FATSDetailInline = ({ fatsId, onEdit, onViewFATS }) => {
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
  const [commentDialogOpen, setCommentDialogOpen] = useState(false);
  const [commentToEdit, setCommentToEdit] = useState(null);
  const imageContainerRef = useRef(null);

  useEffect(() => {
    loadFATSDetail();
    loadImages();
    loadComments();
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

  const handleEditComment = (comment) => {
    setCommentToEdit(comment);
    setCommentDialogOpen(true);
  };

  const handleCloseCommentDialog = () => {
    setCommentDialogOpen(false);
    setCommentToEdit(null);
  };

  const handleCommentSaved = () => {
    loadComments();
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

  // Handle clicks on fault reference links
  const handleFaultLinkClick = (e) => {
    const faultLink = e.target.closest('.fault-reference-link');
    if (faultLink) {
      e.preventDefault();
      e.stopPropagation();
      const faultId = faultLink.getAttribute('data-fault-id');
      if (faultId && onViewFATS) {
        // Open the referenced fault as a new tab
        onViewFATS(parseInt(faultId));
      }
    }
  };

  const sanitizeHTML = (html) => {
    if (!html) return '';
    
    // Auto-convert plain text URLs to clickable links
    // This regex matches URLs that are NOT already inside <a> tags
    const urlRegex = /(?<!href=["'])(https?:\/\/[^\s<>"]+)(?![^<]*<\/a>)/g;
    let htmlWithLinks = html.replace(urlRegex, (url) => {
      // Clean up URL (remove trailing punctuation that might be part of sentence)
      const cleanUrl = url.replace(/[.,;:!?)]+$/, '');
      return `<a href="${cleanUrl}" target="_blank" rel="noopener noreferrer">${cleanUrl}</a>`;
    });
    
    // Convert internal fault reference links (#fault-XXXX) to functional links
    // These are created by the "#" button in the editor
    // Match both <a href="#fault-XXXX"> and <a target="..." href="#fault-XXXX">
    const faultLinkRegex = /<a\s+([^>]*?)href="(?:#fault-|\/fats\/)(\d+)"([^>]*)>(.*?)<\/a>/gi;
    htmlWithLinks = htmlWithLinks.replace(faultLinkRegex, (match, before, faultId, after, text) => {
      // Strip out ALL attributes and create a clean link - no target="_blank"
      return `<a href="javascript:void(0)" data-fault-id="${faultId}" class="fault-reference-link" style="color: #1976d2; text-decoration: underline; cursor: pointer;">${text}</a>`;
    });
    
    const sanitized = DOMPurify.sanitize(htmlWithLinks, {
      ALLOWED_TAGS: ['p', 'br', 'strong', 'b', 'em', 'i', 'u', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'code', 'pre', 'blockquote', 'span', 'div'],
      ALLOWED_ATTR: ['href', 'target', 'rel', 'class', 'style', 'data-fault-id'],
      ALLOWED_STYLES: {
        '*': {
          'color': [/^#[0-9a-fA-F]{3,6}$/, /^rgb\(/, /^rgba\(/],
          'background-color': [/^#[0-9a-fA-F]{3,6}$/, /^rgb\(/, /^rgba\(/],
          'font-weight': [/^bold$/, /^normal$/, /^\d{3}$/],
          'font-style': [/^italic$/, /^normal$/],
          'text-decoration': [/^underline$/, /^line-through$/],
          'cursor': [/^pointer$/],
        }
      }
    });
    
    // CRITICAL: Remove target attribute from fault-reference-link elements
    // This prevents them from opening in new browser tabs
    const finalHtml = sanitized.replace(/(<a\s+[^>]*?class="fault-reference-link"[^>]*?)\s+target="[^"]*"([^>]*?>)/gi, '$1$2');
    
    return finalHtml;
  };


  const handlePrint = () => {
    window.print();
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
          <Box sx={{ display: 'flex', gap: 1 }}>
            {onEdit && (
              <Button
                variant="contained"
                color="primary"
                startIcon={<EditIcon />}
                onClick={() => onEdit(fats.idno)}
                size="small"
                sx={{ '@media print': { display: 'none' } }}
              >
                Edit
              </Button>
            )}
            <Button
              variant="contained"
              color="primary"
              startIcon={<PrintIcon />}
              onClick={handlePrint}
              size="small"
              sx={{ '@media print': { display: 'none' } }}
            >
              Print
            </Button>
          </Box>
        </Box>
        <Typography variant="body2" color="text.secondary">
          Created: {formatHSTTimestamp(fats.datein)} | Operator: {fats.operator || 'N/A'}
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
            onClick={handleFaultLinkClick}
            sx={{
              '& p': { marginBottom: '0.5rem', marginTop: 0 },
              '& p:last-child': { marginBottom: 0 },
              '& ul, & ol': { paddingLeft: '1.5rem', marginBottom: '0.5rem', marginTop: '0.5rem' },
              '& li': { marginBottom: '0.25rem' },
              '& strong, & b': { fontWeight: 'bold' },
              '& em, & i': { fontStyle: 'italic' },
              '& u': { textDecoration: 'underline' },
              '& a': { color: '#1976d2', textDecoration: 'underline', '&:hover': { color: '#115293' } },
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
            onClick={handleFaultLinkClick}
            sx={{
              '& p': { marginBottom: '0.5rem', marginTop: 0 },
              '& p:last-child': { marginBottom: 0 },
              '& ul, & ol': { paddingLeft: '1.5rem', marginBottom: '0.5rem', marginTop: '0.5rem' },
              '& li': { marginBottom: '0.25rem' },
              '& strong, & b': { fontWeight: 'bold' },
              '& em, & i': { fontStyle: 'italic' },
              '& u': { textDecoration: 'underline' },
              '& a': { color: '#1976d2', textDecoration: 'underline', '&:hover': { color: '#115293' } },
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
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Box>
            <Typography variant="subtitle2" color="text.secondary" sx={{ fontWeight: 'bold' }}>
              Comments:
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ pl: 1 }}>
              {comments.length} comment(s)
            </Typography>
          </Box>
          <Button
            variant="contained"
            color="success"
            size="small"
            startIcon={<AddCommentIcon />}
            onClick={() => {
              setCommentToEdit(null);
              setCommentDialogOpen(true);
            }}
            sx={{ minWidth: '140px' }}
          >
            Add Comment
          </Button>
        </Box>
        {comments.length > 0 ? (
          <Box sx={{ mt: 2 }}>
            {comments.map((comment, index) => (
              <Paper 
                key={comment.id || index} 
                variant="outlined" 
                sx={{ p: 2, mb: 2, bgcolor: 'grey.50' }}
              >
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1, alignItems: 'center' }}>
                  <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                    {comment.commenter || comment.operator || 'Anonymous'}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="caption" color="text.secondary">
                      {formatHSTTimestamp(comment.created_at || comment.datein)}
                    </Typography>
                    <IconButton
                      size="small"
                      onClick={() => handleEditComment(comment)}
                      title="Edit comment"
                      sx={{ ml: 1 }}
                    >
                      <EditIcon fontSize="small" />
                    </IconButton>
                  </Box>
                </Box>
                <Box
                  onClick={handleFaultLinkClick}
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
                  Uploaded: {formatHSTTimestamp(selectedImage.uploaded_at)}
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

      {/* Comment Edit Dialog */}
      <CommentDialog
        open={commentDialogOpen}
        fatsId={fatsId}
        onClose={handleCloseCommentDialog}
        onSave={handleCommentSaved}
        mode={commentToEdit ? 'edit' : 'add'}
        editingComment={commentToEdit}
      />
    </Paper>
    </>
  );
};

export default FATSDetailInline;

