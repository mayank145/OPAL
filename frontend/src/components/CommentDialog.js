import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  Typography,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
  IconButton,
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { fatsAPI } from '../services/api';
import { formatHSTTimestamp } from '../utils/timezone';

const CommentDialog = ({ open, fatsId, onClose, onSave, mode = 'add', editingComment = null }) => {
  const [commentText, setCommentText] = useState('');
  const [commenter, setCommenter] = useState('');
  const [todo, setTodo] = useState('');
  const [solution, setSolution] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [comments, setComments] = useState([]);
  const [loadingComments, setLoadingComments] = useState(false);
  const [currentMode, setCurrentMode] = useState(mode);
  const [currentEditingComment, setCurrentEditingComment] = useState(editingComment);

  // Helper function to strip HTML tags and decode entities
  const stripHtml = (html) => {
    if (!html) return '';
    const tmp = document.createElement('DIV');
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || '';
  };

  useEffect(() => {
    if (open && fatsId) {
      loadComments();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, fatsId]);

  // Update form when mode or editingComment changes
  useEffect(() => {
    setCurrentMode(mode);
    setCurrentEditingComment(editingComment);
    
    if (mode === 'edit' && editingComment) {
      // Strip HTML from comment text when editing
      setCommentText(stripHtml(editingComment.comment_text) || '');
      setCommenter(editingComment.commenter || '');
      setTodo(editingComment.todo || '');
      setSolution(editingComment.solution || '');
    } else {
      setCommentText('');
      setCommenter('');
      setTodo('');
      setSolution('');
    }
  }, [mode, editingComment]);

  const loadComments = async () => {
    try {
      setLoadingComments(true);
      const data = await fatsAPI.getComments(fatsId);
      setComments(data);
    } catch (err) {
      console.error('Error loading comments:', err);
    } finally {
      setLoadingComments(false);
    }
  };

  const handleSubmit = async () => {
    if (!commentText.trim()) {
      setError('Comment text is required');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Build comment data
      const commentData = {
        comment_text: commentText.trim(),
        commenter: commenter?.trim() || 'Anonymous',
      };

      // Only include optional fields if they have values
      if (todo && todo.trim()) {
        commentData.todo = todo.trim();
      }
      if (solution && solution.trim()) {
        commentData.solution = solution.trim();
      }

      if (currentMode === 'edit' && currentEditingComment) {
        // Update existing comment
        await fatsAPI.updateComment(currentEditingComment.id, commentData);
      } else {
        // Add new comment
        await fatsAPI.addComment(fatsId, commentData);
      }
      
      // Clear form and switch back to add mode
      setCommentText('');
      setCommenter('');
      setTodo('');
      setSolution('');
      setCurrentMode('add');
      setCurrentEditingComment(null);
      
      // Reload comments
      await loadComments();
      
      if (onSave) onSave(fatsId);
    } catch (err) {
      setError(err.message || `Failed to ${currentMode === 'edit' ? 'update' : 'add'} comment`);
    } finally {
      setLoading(false);
    }
  };

  const handleEditComment = (comment) => {
    setCurrentMode('edit');
    setCurrentEditingComment(comment);
    // Strip HTML from comment text when editing
    setCommentText(stripHtml(comment.comment_text) || '');
    setCommenter(comment.commenter || '');
    setTodo(comment.todo || '');
    setSolution(comment.solution || '');
    setError(null);
  };

  const handleCancelEdit = () => {
    setCurrentMode('add');
    setCurrentEditingComment(null);
    setCommentText('');
    setCommenter('');
    setTodo('');
    setSolution('');
    setError(null);
  };

  const handleDeleteComment = async (commentId) => {
    if (!window.confirm('Are you sure you want to delete this comment? This action cannot be undone.')) {
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      await fatsAPI.deleteComment(commentId);
      
      // If we were editing this comment, cancel the edit
      if (currentEditingComment && currentEditingComment.id === commentId) {
        handleCancelEdit();
      }
      
      // Reload comments
      await loadComments();
      
      if (onSave) onSave(fatsId);
    } catch (err) {
      setError(err.message || 'Failed to delete comment');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setCommentText('');
    setCommenter('');
    setTodo('');
    setSolution('');
    setError(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {currentMode === 'edit' ? 'Edit Comment' : `Add Comment to FATS: ${fatsId}`}
      </DialogTitle>
      <DialogContent>
        <Box sx={{ mt: 2 }}>
          <TextField
            fullWidth
            label="Commenter"
            value={commenter}
            onChange={(e) => setCommenter(e.target.value)}
            placeholder="Your name"
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Comment Text *"
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            multiline
            rows={4}
            required
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="TODO"
            value={todo}
            onChange={(e) => setTodo(e.target.value)}
            placeholder="Optional TODO item"
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Solution"
            value={solution}
            onChange={(e) => setSolution(e.target.value)}
            placeholder="Optional solution"
            sx={{ mb: 2 }}
          />

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Typography variant="h6" sx={{ mt: 3, mb: 1 }}>
            Previous Comments
          </Typography>
          <Divider sx={{ mb: 2 }} />

          {loadingComments ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
              <CircularProgress size={24} />
            </Box>
          ) : comments.length === 0 ? (
            <Typography variant="body2" color="text.secondary">
              No comments yet
            </Typography>
          ) : (
            <List>
              {comments.map((comment) => (
                <React.Fragment key={comment.id}>
                  <ListItem 
                    alignItems="flex-start"
                    secondaryAction={
                      <Box sx={{ display: 'flex', gap: 0.5 }}>
                        <IconButton 
                          onClick={() => handleEditComment(comment)}
                          title="Edit comment"
                          size="small"
                          disabled={loading}
                        >
                          <EditIcon fontSize="small" />
                        </IconButton>
                        <IconButton 
                          onClick={() => handleDeleteComment(comment.id)}
                          title="Delete comment"
                          size="small"
                          color="error"
                          disabled={loading}
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </Box>
                    }
                  >
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="subtitle2">
                            {comment.commenter || 'Anonymous'}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {formatHSTTimestamp(comment.created_at)}
                          </Typography>
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" sx={{ mt: 1, whiteSpace: 'pre-wrap' }}>
                            {stripHtml(comment.comment_text)}
                          </Typography>
                          {comment.todo && (
                            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 0.5 }}>
                              TODO: {comment.todo}
                            </Typography>
                          )}
                          {comment.solution && (
                            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 0.5 }}>
                              Solution: {comment.solution}
                            </Typography>
                          )}
                        </Box>
                      }
                    />
                  </ListItem>
                  <Divider />
                </React.Fragment>
              ))}
            </List>
          )}
        </Box>
      </DialogContent>
      <DialogActions>
        {currentMode === 'edit' && (
          <Box sx={{ mr: 'auto', display: 'flex', gap: 1 }}>
            <Button onClick={handleCancelEdit}>
              Cancel Edit
            </Button>
            <Button 
              onClick={() => {
                setCommentText('');
                setTodo('');
                setSolution('');
              }}
              color="warning"
            >
              Clear Fields
            </Button>
          </Box>
        )}
        <Button onClick={handleClose}>Close</Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={loading || !commentText.trim()}
        >
          {loading 
            ? (currentMode === 'edit' ? 'Updating...' : 'Adding...') 
            : (currentMode === 'edit' ? 'Update Comment' : 'Add Comment')}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default CommentDialog;

