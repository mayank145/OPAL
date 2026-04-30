/**
 * ProtectedRoute — replaces PHP's door.php guard.
 *
 * While the session check is in-flight → show a full-screen spinner.
 * If no authenticated user → show <LoginPage />.
 * If authenticated → render the app children.
 */

import React from 'react';
import { Box, CircularProgress } from '@mui/material';
import { useAuth } from '../context/AuthContext';
import LoginPage from './LoginPage';

export default function ProtectedRoute({ children }) {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(135deg, #0d47a1 0%, #0277bd 100%)',
        }}
      >
        <CircularProgress size={52} sx={{ color: 'rgba(255,255,255,0.85)' }} />
      </Box>
    );
  }

  if (!user) {
    return <LoginPage />;
  }

  return children;
}
