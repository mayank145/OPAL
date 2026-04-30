/**
 * LoginPage — OPAL login screen.
 *
 * Mirrors login.php (form) + login2.php (error handling) from the legacy system.
 * Uses MUI components to match the rest of the OPAL design.
 */

import React, { useState } from 'react';
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Divider,
  IconButton,
  InputAdornment,
  Paper,
  TextField,
  Typography,
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';

const CREW_LABELS = {
  TO: 'Telescope Operator',
  DC: 'Day Crew',
  WP: 'Work Plan',
};

export default function LoginPage() {
  const { login } = useAuth();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!username.trim() || !password) {
      setError('Please enter both username and password.');
      return;
    }

    setLoading(true);
    try {
      await login(username.trim(), password);
      // AuthContext sets user → ProtectedRoute renders the app automatically
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (err.response?.status === 403) {
        setError('This account type is not permitted to log in.');
      } else if (err.response?.status === 401) {
        setError(detail || 'Username/Password is invalid!');
      } else {
        setError('Login failed. Please try again or contact support.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #0277bd 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 2,
      }}
    >
      <Paper
        elevation={12}
        sx={{
          width: '100%',
          maxWidth: 420,
          borderRadius: 3,
          overflow: 'hidden',
        }}
      >
        {/* Header banner */}
        <Box
          sx={{
            background: 'linear-gradient(135deg, #0d47a1 0%, #0277bd 100%)',
            px: 4,
            py: 3,
            display: 'flex',
            alignItems: 'center',
            gap: 2,
          }}
        >
          <Box
            sx={{
              width: 52,
              height: 52,
              borderRadius: '50%',
              background: 'rgba(255,255,255,0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 28,
              flexShrink: 0,
            }}
          >
            🔭
          </Box>
          <Box>
            <Typography
              variant="h5"
              fontWeight={800}
              color="white"
              letterSpacing={1}
              lineHeight={1.1}
            >
              OPAL
            </Typography>
            <Typography
              variant="caption"
              color="rgba(255,255,255,0.75)"
              letterSpacing={1.5}
              textTransform="uppercase"
              fontSize="0.62rem"
            >
              Subaru Telescope Network
            </Typography>
          </Box>
        </Box>

        {/* Form area */}
        <Box
          component="form"
          onSubmit={handleSubmit}
          sx={{ px: 4, pt: 3, pb: 4 }}
          noValidate
          autoComplete="off"
        >
          <Typography
            variant="subtitle1"
            fontWeight={600}
            color="text.secondary"
            mb={2.5}
            textAlign="center"
          >
            Summit Calendar · Logs · Cars
          </Typography>

          {/* Error alert — mirrors PHP "$warn" message */}
          {error && (
            <Alert severity="error" sx={{ mb: 2, borderRadius: 2 }}>
              {error}
            </Alert>
          )}

          <TextField
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            fullWidth
            required
            autoFocus
            autoComplete="username"
            disabled={loading}
            sx={{ mb: 2 }}
            inputProps={{ name: 'username' }}
          />

          <TextField
            label="Password"
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            fullWidth
            required
            disabled={loading}
            autoComplete="current-password"
            sx={{ mb: 3 }}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    onClick={() => setShowPassword((v) => !v)}
                    edge="end"
                    tabIndex={-1}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          <Button
            type="submit"
            variant="contained"
            fullWidth
            size="large"
            disabled={loading}
            sx={{
              borderRadius: 2,
              fontWeight: 700,
              fontSize: '1rem',
              py: 1.4,
              background: 'linear-gradient(135deg, #0d47a1 0%, #0277bd 100%)',
              '&:hover': {
                background: 'linear-gradient(135deg, #0a3880 0%, #01579b 100%)',
              },
            }}
          >
            {loading ? (
              <CircularProgress size={22} color="inherit" />
            ) : (
              'Login'
            )}
          </Button>

          <Divider sx={{ my: 3 }} />

          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="caption" color="text.disabled" display="block">
              Use your STN (Subaru Telescope Network) login and password.
            </Typography>
            <Typography variant="caption" color="text.disabled" display="block" mt={0.5}>
              Sessions expire after 24 hours.
            </Typography>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
}
