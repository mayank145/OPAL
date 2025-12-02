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
  Chip,
} from '@mui/material';
import { fatsAPI } from '../services/api';

const CommentDialog = ({ open, fatsId, onClose, onSave }) => {
  const [commentText, setCommentText] = useState('');
  const [commenter, setCommenter] = useState('');
  const [todo, setTodo] = useState('');
  const [solution, setSolution] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [comments, setComments] = useState([]);
  const [loadingComments, setLoadingComments] = useState(false);

  useEffect(() => {
    if (open && fatsId) {
      loadComments();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, fatsId]);

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

      // Build comment data - don't include fats_id (it's in the URL path)
      // Also, omit undefined/null/empty values to avoid validation issues
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

      await fatsAPI.addComment(fatsId, commentData);
      
      // Clear form
      setCommentText('');
      setCommenter('');
      setTodo('');
      setSolution('');
      
      // Reload comments
      await loadComments();
      
      if (onSave) onSave();
    } catch (err) {
      setError(err.message || 'Failed to add comment');
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
        Add Comment to FATS: {fatsId}
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
                  <ListItem alignItems="flex-start">
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="subtitle2">
                            {comment.commenter || 'Anonymous'}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {comment.created_at
                              ? new Date(comment.created_at).toLocaleString()
                              : ''}
                          </Typography>
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" sx={{ mt: 1 }}>
                            {comment.comment_text}
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
        <Button onClick={handleClose}>Close</Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={loading || !commentText.trim()}
        >
          {loading ? 'Adding...' : 'Add Comment'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default CommentDialog;

