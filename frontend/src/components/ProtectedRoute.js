/**
 * ProtectedRoute — requires an authenticated session.
 * Unauthenticated users are sent to /login with return location preserved.
 */

import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { Box, CircularProgress } from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { paths } from '../routes/paths';

export default function ProtectedRoute({ children }) {
  const { user, isLoading } = useAuth();
  const location = useLocation();

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
    return <Navigate to={paths.login} replace state={{ from: location }} />;
  }

  return children;
}
