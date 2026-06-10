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
  Divider,
  IconButton,
  Tooltip,
  Popover,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  FormatBold as BoldIcon,
  FormatItalic as ItalicIcon,
  FormatUnderlined as UnderlineIcon,
  BorderColor as HighlightIcon,
  FormatColorText as TextColorIcon,
} from '@mui/icons-material';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Underline from '@tiptap/extension-underline';
import Highlight from '@tiptap/extension-highlight';
import { TextStyle } from '@tiptap/extension-text-style';
import { Color } from '@tiptap/extension-color';
import { fatsAPI } from '../services/api';
import { formatHSTTimestamp } from '../utils/timezone';

/* ── Color swatches ─────────────────────────────────────────────────────── */
const TEXT_COLORS = [
  { label: 'Default',  color: null },
  { label: 'Black',    color: '#000000' },
  { label: 'Dark grey',color: '#424242' },
  { label: 'Red',      color: '#d32f2f' },
  { label: 'Orange',   color: '#e65100' },
  { label: 'Blue',     color: '#1565c0' },
  { label: 'Green',    color: '#2e7d32' },
  { label: 'Purple',   color: '#6a1b9a' },
  { label: 'Teal',     color: '#00695c' },
];

const HIGHLIGHT_COLORS = [
  { label: 'None',     color: null },
  { label: 'Yellow',   color: '#fff176' },
  { label: 'Lime',     color: '#ccff90' },
  { label: 'Cyan',     color: '#80deea' },
  { label: 'Pink',     color: '#f48fb1' },
  { label: 'Orange',   color: '#ffcc80' },
  { label: 'Lavender', color: '#ce93d8' },
];

/* ── Color picker popover ───────────────────────────────────────────────── */
const ColorPicker = ({ colors, onSelect, onClose, anchorEl }) => (
  <Popover
    open={Boolean(anchorEl)}
    anchorEl={anchorEl}
    onClose={onClose}
    anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
    transformOrigin={{ vertical: 'top', horizontal: 'left' }}
    PaperProps={{ sx: { p: 1, display: 'flex', flexWrap: 'wrap', gap: 0.5, width: 180 } }}
  >
    {colors.map(({ label, color }) => (
      <Tooltip key={label} title={label}>
        <Box
          onMouseDown={(e) => { e.preventDefault(); onSelect(color); onClose(); }}
          sx={{
            width: 24, height: 24, borderRadius: '4px', cursor: 'pointer',
            bgcolor: color || '#fff',
            border: color ? '1px solid rgba(0,0,0,0.18)' : '2px dashed #bbb',
            '&:hover': { transform: 'scale(1.2)', boxShadow: 2 },
            transition: 'transform 0.1s',
          }}
        />
      </Tooltip>
    ))}
  </Popover>
);

/* ── Editor toolbar ─────────────────────────────────────────────────────── */
const Toolbar = ({ editor }) => {
  const [textColorAnchor, setTextColorAnchor] = useState(null);
  const [highlightAnchor, setHighlightAnchor] = useState(null);

  if (!editor) return null;

  const btn = (active, color) => ({
    borderRadius: 1,
    minWidth: 0,
    px: 0.8,
    py: 0.3,
    color: color || (active ? 'primary.main' : 'text.secondary'),
    bgcolor: active ? 'rgba(0,0,0,0.07)' : 'transparent',
    border: '1px solid',
    borderColor: active ? 'rgba(0,0,0,0.20)' : 'divider',
    '&:hover': { bgcolor: 'action.hover' },
  });

  const activeTextColor = editor.getAttributes('textStyle').color;
  const activeHighlight = editor.getAttributes('highlight').color;

  return (
    <Box sx={{ display: 'flex', gap: 0.5, p: 0.75, borderBottom: '1px solid', borderColor: 'divider', flexWrap: 'wrap', alignItems: 'center', bgcolor: '#fafafa' }}>
      {/* Bold */}
      <Tooltip title="Bold (Ctrl+B)">
        <span>
          <IconButton size="small" sx={btn(editor.isActive('bold'))}
            onMouseDown={(e) => { e.preventDefault(); editor.chain().focus().toggleBold().run(); }}>
            <BoldIcon fontSize="small" />
          </IconButton>
        </span>
      </Tooltip>

      {/* Italic */}
      <Tooltip title="Italic (Ctrl+I)">
        <span>
          <IconButton size="small" sx={btn(editor.isActive('italic'))}
            onMouseDown={(e) => { e.preventDefault(); editor.chain().focus().toggleItalic().run(); }}>
            <ItalicIcon fontSize="small" />
          </IconButton>
        </span>
      </Tooltip>

      {/* Underline */}
      <Tooltip title="Underline (Ctrl+U)">
        <span>
          <IconButton size="small" sx={btn(editor.isActive('underline'))}
            onMouseDown={(e) => { e.preventDefault(); editor.chain().focus().toggleUnderline().run(); }}>
            <UnderlineIcon fontSize="small" />
          </IconButton>
        </span>
      </Tooltip>

      <Box sx={{ width: '1px', height: 20, bgcolor: 'divider', mx: 0.25 }} />

      {/* Text color */}
      <Tooltip title="Text color">
        <span>
          <IconButton size="small" sx={btn(!!activeTextColor)}
            onMouseDown={(e) => { e.preventDefault(); setTextColorAnchor(e.currentTarget); }}>
            <Box sx={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
              <TextColorIcon fontSize="small" sx={{ color: activeTextColor || 'text.secondary' }} />
              <Box sx={{ position: 'absolute', bottom: -3, left: 0, right: 0, height: 3, borderRadius: '2px', bgcolor: activeTextColor || '#000', opacity: activeTextColor ? 1 : 0.35 }} />
            </Box>
          </IconButton>
        </span>
      </Tooltip>
      <ColorPicker
        colors={TEXT_COLORS}
        anchorEl={textColorAnchor}
        onClose={() => setTextColorAnchor(null)}
        onSelect={(color) => {
          if (color) editor.chain().focus().setColor(color).run();
          else editor.chain().focus().unsetColor().run();
        }}
      />

      {/* Highlight color */}
      <Tooltip title="Highlight color">
        <span>
          <IconButton size="small" sx={btn(editor.isActive('highlight'))}
            onMouseDown={(e) => { e.preventDefault(); setHighlightAnchor(e.currentTarget); }}>
            <Box sx={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
              <HighlightIcon fontSize="small" sx={{ color: activeHighlight ? '#f57f17' : 'text.secondary' }} />
              <Box sx={{ position: 'absolute', bottom: -3, left: 0, right: 0, height: 3, borderRadius: '2px', bgcolor: activeHighlight || '#fff176', opacity: activeHighlight ? 1 : 0.5 }} />
            </Box>
          </IconButton>
        </span>
      </Tooltip>
      <ColorPicker
        colors={HIGHLIGHT_COLORS}
        anchorEl={highlightAnchor}
        onClose={() => setHighlightAnchor(null)}
        onSelect={(color) => {
          if (color) editor.chain().focus().toggleHighlight({ color }).run();
          else editor.chain().focus().unsetHighlight().run();
        }}
      />
    </Box>
  );
};

/* ── Main component ─────────────────────────────────────────────────────── */
const CommentDialog = ({ open, fatsId, onClose, onSave, mode = 'add', editingComment = null }) => {
  const [commenter, setCommenter] = useState('');
  const [todo, setTodo] = useState('');
  const [solution, setSolution] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [comments, setComments] = useState([]);
  const [loadingComments, setLoadingComments] = useState(false);
  const [currentMode, setCurrentMode] = useState(mode);
  const [currentEditingComment, setCurrentEditingComment] = useState(editingComment);

  const stripHtml = (html) => {
    if (!html) return '';
    const tmp = document.createElement('DIV');
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || '';
  };

  // Same normalization as FATSDetailInline — strips TinyMCE font-size/font-family,
  // collapses empty spans, and wraps plain text in <p> tags
  const normalizeCommentHTML = (text) => {
    if (!text) return '';
    const hasHtmlTags = /<[a-z][\s\S]*>/i.test(text);
    if (hasHtmlTags) {
      let result = text.replace(/style="([^"]*)"/gi, (match, styleValue) => {
        const cleaned = styleValue
          .split(';')
          .map(s => s.trim())
          .filter(s => s && !/^font-size\s*:/i.test(s) && !/^font-family\s*:/i.test(s))
          .join('; ');
        return cleaned ? `style="${cleaned}"` : '';
      });
      let prev = '';
      while (prev !== result) {
        prev = result;
        result = result.replace(/<span\s*(?:style="\s*")?\s*>([\s\S]*?)<\/span>/gi, '$1');
      }
      result = result.replace(/(&nbsp;\s*){2,}/gi, ' ');
      return result;
    }
    return text
      .split(/\n\n+/)
      .map(para => `<p>${para.replace(/\n/g, '<br>')}</p>`)
      .join('');
  };

  const editor = useEditor({
    extensions: [
      StarterKit,
      Underline,
      TextStyle,
      Color,
      Highlight.configure({ multicolor: true }),
    ],
    content: '',
    editorProps: {
      attributes: {
        style: 'min-height: 100px; padding: 10px 12px; font-size: 14px; line-height: 1.6; outline: none;',
      },
    },
  });

  useEffect(() => {
    if (open && fatsId) loadComments();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, fatsId]);

  useEffect(() => {
    setCurrentMode(mode);
    setCurrentEditingComment(editingComment);
    if (mode === 'edit' && editingComment) {
      editor?.commands.setContent(editingComment.comment_text || '');
      setCommenter(editingComment.commenter || '');
      setTodo(editingComment.todo || '');
      setSolution(editingComment.solution || '');
    } else {
      editor?.commands.setContent('');
      setCommenter('');
      setTodo('');
      setSolution('');
    }
  }, [mode, editingComment, editor]);

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
    const html = editor?.getHTML() || '';
    const plain = stripHtml(html).trim();
    if (!plain) { setError('Comment text is required'); return; }

    try {
      setLoading(true);
      setError(null);
      const commentData = {
        comment_text: html,
        commenter: commenter?.trim() || 'Anonymous',
        ...(todo?.trim() && { todo: todo.trim() }),
        ...(solution?.trim() && { solution: solution.trim() }),
      };

      if (currentMode === 'edit' && currentEditingComment) {
        await fatsAPI.updateComment(currentEditingComment.id, commentData);
      } else {
        await fatsAPI.addComment(fatsId, commentData);
      }

      editor?.commands.setContent('');
      setCommenter('');
      setTodo('');
      setSolution('');
      setCurrentMode('add');
      setCurrentEditingComment(null);
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
    editor?.commands.setContent(comment.comment_text || '');
    setCommenter(comment.commenter || '');
    setTodo(comment.todo || '');
    setSolution(comment.solution || '');
    setError(null);
  };

  const handleCancelEdit = () => {
    setCurrentMode('add');
    setCurrentEditingComment(null);
    editor?.commands.setContent('');
    setCommenter('');
    setTodo('');
    setSolution('');
    setError(null);
  };

  const handleDeleteComment = async (commentId) => {
    if (!window.confirm('Are you sure you want to delete this comment? This action cannot be undone.')) return;
    try {
      setLoading(true);
      setError(null);
      await fatsAPI.deleteComment(commentId);
      if (currentEditingComment?.id === commentId) handleCancelEdit();
      await loadComments();
      if (onSave) onSave(fatsId);
    } catch (err) {
      setError(err.message || 'Failed to delete comment');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    editor?.commands.setContent('');
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
        <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            fullWidth
            label="Commenter"
            value={commenter}
            onChange={(e) => setCommenter(e.target.value)}
            placeholder="Your name"
            size="small"
          />

          {/* Rich text editor */}
          <Box>
            <Typography variant="caption" color="text.secondary" sx={{ mb: 0.5, display: 'block' }}>
              Comment Text *
            </Typography>
            <Box sx={{ border: '1px solid', borderColor: 'divider', borderRadius: 1, overflow: 'hidden', '&:focus-within': { borderColor: 'primary.main', boxShadow: '0 0 0 2px rgba(25,118,210,0.15)' } }}>
              <Toolbar editor={editor} />
              <Box sx={{
                '& mark': { backgroundColor: '#fff176', borderRadius: '2px', padding: '1px 2px' },
                '& p': { margin: 0, lineHeight: 1.7 },
                '& strong': { fontWeight: 700 },
              }}>
                <EditorContent editor={editor} />
              </Box>
            </Box>
            <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
              Select text then click a toolbar button to format. Use the highlighter to mark important text.
            </Typography>
          </Box>

          <TextField fullWidth label="TODO" value={todo} onChange={(e) => setTodo(e.target.value)} placeholder="Optional TODO item" size="small" />
          <TextField fullWidth label="Solution" value={solution} onChange={(e) => setSolution(e.target.value)} placeholder="Optional solution" size="small" />

          {error && <Alert severity="error">{error}</Alert>}

          <Typography variant="h6" sx={{ mt: 1, mb: 0 }}>Previous Comments</Typography>
          <Divider />

          {loadingComments ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}><CircularProgress size={24} /></Box>
          ) : comments.length === 0 ? (
            <Typography variant="body2" color="text.secondary">No comments yet</Typography>
          ) : (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
              {comments.map((comment) => (
                <Box key={comment.id} sx={{ border: '1px solid', borderColor: 'divider', borderRadius: 1, overflow: 'hidden' }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', px: 1.5, py: 0.75, bgcolor: 'grey.100', borderBottom: '1px solid', borderColor: 'divider' }}>
                    <Box>
                      <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>{comment.commenter || 'Anonymous'}</Typography>
                      <Typography variant="caption" color="text.secondary">{formatHSTTimestamp(comment.created_at)}</Typography>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 0.5 }}>
                      <IconButton onClick={() => handleEditComment(comment)} size="small" disabled={loading}><EditIcon fontSize="small" /></IconButton>
                      <IconButton onClick={() => handleDeleteComment(comment.id)} size="small" color="error" disabled={loading}><DeleteIcon fontSize="small" /></IconButton>
                    </Box>
                  </Box>
                  <Box sx={{
                    px: 1.5, py: 1,
                    fontSize: '1rem !important',
                    lineHeight: 1.75,
                    color: '#212121',
                    '& *': { fontSize: '1rem !important', fontFamily: 'inherit !important' },
                    '& p': { margin: 0, marginBottom: '0.5rem' },
                    '& p:last-child': { marginBottom: 0 },
                    '& strong, & b': { fontWeight: 700 },
                    '& em, & i': { fontStyle: 'italic' },
                    '& u': { textDecoration: 'underline' },
                    '& mark': { backgroundColor: '#fff176', borderRadius: '2px', padding: '1px 2px' },
                    '& a': { color: '#1565c0', textDecoration: 'underline' },
                  }}
                    dangerouslySetInnerHTML={{ __html: normalizeCommentHTML(comment.comment_text) || '<p style="color:#999;">No comment text</p>' }}
                  />
                  {(comment.todo || comment.solution) && (
                    <Box sx={{ px: 1.5, pb: 1, display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                      {comment.todo && <Typography variant="caption" color="info.main"><strong>TODO:</strong> {comment.todo}</Typography>}
                      {comment.solution && <Typography variant="caption" color="success.main"><strong>Solution:</strong> {comment.solution}</Typography>}
                    </Box>
                  )}
                </Box>
              ))}
            </Box>
          )}
        </Box>
      </DialogContent>
      <DialogActions>
        {currentMode === 'edit' && (
          <Box sx={{ mr: 'auto', display: 'flex', gap: 1 }}>
            <Button onClick={handleCancelEdit}>Cancel Edit</Button>
          </Box>
        )}
        <Button onClick={handleClose}>Close</Button>
        <Button onClick={handleSubmit} variant="contained" disabled={loading}>
          {loading ? (currentMode === 'edit' ? 'Updating...' : 'Adding...') : (currentMode === 'edit' ? 'Update Comment' : 'Add Comment')}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default CommentDialog;
