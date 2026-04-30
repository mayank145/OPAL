/**
 * LoginPage — OPAL login screen with full-image wallpaper slideshow.
 *
 * All Subaru Telescope photos cycle as a crossfade slideshow.
 * Each image is shown in full (object-fit: contain) with a matching
 * blurred backdrop to fill the remaining screen area.
 */

import React, { useEffect, useState } from 'react';
import { keyframes } from '@emotion/react';
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

// ─── Slideshow images ─────────────────────────────────────────────────────────

const SLIDES = [
  { src: '/slideshow/s01.png', credit: 'Comet Tsuchinshan-ATLAS over Subaru Telescope' },
  { src: '/slideshow/s02.png', credit: 'Milky Way above Subaru Telescope' },
  { src: '/slideshow/s03.png', credit: 'Subaru Telescope at sunset' },
  { src: '/slideshow/s04.png', credit: 'Summit sunset, Maunakea' },
  { src: '/slideshow/s05.png', credit: 'Milky Way — Subaru Telescope wide' },
  { src: '/slideshow/s06.png', credit: 'Milky Way with laser guide star' },
  { src: '/slideshow/s07.png', credit: 'Laser guide star — Subaru Telescope' },
  { src: '/slideshow/s08.png', credit: 'Comet and laser over Maunakea' },
  { src: '/slideshow/s09.png', credit: 'Subaru Telescope — Maunakea summit in snow' },
  { src: '/slideshow/s10.png', credit: 'Subaru Telescope at golden sunset' },
  { src: '/slideshow/s11.png', credit: 'Aerial view — Subaru Telescope, Maunakea' },
];

const INTERVAL_MS   = 6000;   // time each slide is shown
const FADE_MS       = 1500;   // crossfade duration

// ─── Card animations ──────────────────────────────────────────────────────────

const fadeUp = keyframes`
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0);    }
`;

// ─── Slideshow hook ───────────────────────────────────────────────────────────

function useSlideshow(total) {
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setCurrent(i => (i + 1) % total);
    }, INTERVAL_MS);
    return () => clearInterval(id);
  }, [total]);

  return current;
}

// ─── Component ────────────────────────────────────────────────────────────────

export default function LoginPage() {
  const { login } = useAuth();
  const current   = useSlideshow(SLIDES.length);

  const [username, setUsername]           = useState('');
  const [password, setPassword]           = useState('');
  const [showPassword, setShowPassword]   = useState(false);
  const [loading, setLoading]             = useState(false);
  const [error, setError]                 = useState('');

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
        backgroundColor: '#000',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 2,
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* ── Slideshow layers — all stacked, only current is opaque ── */}
      {SLIDES.map((slide, i) => (
        <Box
          key={slide.src}
          sx={{
            position: 'absolute',
            inset: 0,
            opacity: i === current ? 1 : 0,
            transition: `opacity ${FADE_MS}ms ease-in-out`,
            zIndex: 0,
          }}
        >
          {/* Blurred backdrop fills any letterbox areas */}
          <Box
            sx={{
              position: 'absolute',
              inset: -30,
              backgroundImage: `url(${slide.src})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              filter: 'blur(24px) brightness(0.35) saturate(1.2)',
              transform: 'scale(1.08)',
            }}
          />

          {/* Full image — not cropped */}
          <Box
            component="img"
            src={slide.src}
            alt={slide.credit}
            sx={{
              position: 'absolute',
              inset: 0,
              width: '100%',
              height: '100%',
              objectFit: 'contain',
              objectPosition: 'center',
            }}
          />

          {/* Subtle dark vignette so the card is always readable */}
          <Box
            sx={{
              position: 'absolute',
              inset: 0,
              background:
                'radial-gradient(ellipse at center, rgba(0,0,0,0.08) 40%, rgba(0,0,0,0.55) 100%)',
            }}
          />
        </Box>
      ))}

      {/* ── Slide indicators (dots) ── */}
      <Box
        sx={{
          position: 'absolute',
          bottom: 18,
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: 1,
          zIndex: 5,
        }}
      >
        {SLIDES.map((_, i) => (
          <Box
            key={i}
            sx={{
              width: i === current ? 20 : 7,
              height: 7,
              borderRadius: 4,
              backgroundColor: i === current ? 'rgba(255,255,255,0.95)' : 'rgba(255,255,255,0.35)',
              transition: 'all 0.4s ease',
              cursor: 'pointer',
            }}
          />
        ))}
      </Box>

      {/* ── Photo credit ── */}
      <Box
        sx={{
          position: 'absolute',
          bottom: 40,
          right: 16,
          zIndex: 5,
        }}
      >
        <Typography
          variant="caption"
          sx={{
            color: 'rgba(255,255,255,0.45)',
            fontSize: '0.62rem',
            fontStyle: 'italic',
          }}
        >
          {SLIDES[current].credit}
        </Typography>
      </Box>

      {/* ── Login card — frosted dark glass ── */}
      <Paper
        elevation={0}
        sx={{
          width: '100%',
          maxWidth: 420,
          borderRadius: 3,
          overflow: 'hidden',
          position: 'relative',
          zIndex: 10,
          animation: `${fadeUp} 0.8s ease-out both`,
          background: 'rgba(8, 18, 40, 0.72)',
          backdropFilter: 'blur(22px)',
          WebkitBackdropFilter: 'blur(22px)',
          border: '1px solid rgba(255,255,255,0.12)',
          boxShadow: '0 8px 48px rgba(0,0,0,0.6)',
        }}
      >
        {/* Header */}
        <Box
          sx={{
            background: 'linear-gradient(135deg, rgba(13,71,161,0.70) 0%, rgba(2,119,189,0.70) 100%)',
            borderBottom: '1px solid rgba(255,255,255,0.10)',
            px: 4,
            py: 3,
            display: 'flex',
            alignItems: 'center',
            gap: 2,
          }}
        >
          <Box
            component="img"
            src="/subaru_logo.png"
            alt="Subaru Telescope"
            sx={{
              width: 58,
              height: 58,
              flexShrink: 0,
              objectFit: 'contain',
              filter: 'drop-shadow(0 2px 6px rgba(0,0,0,0.4))',
            }}
          />
          <Box>
            <Typography variant="h5" fontWeight={800} color="white" letterSpacing={1} lineHeight={1.1}>
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
            mb={2.5}
            textAlign="center"
            sx={{ color: 'rgba(255,255,255,0.65)' }}
          >
            Summit Calendar · Logs · Cars
          </Typography>

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
            inputProps={{ name: 'username' }}
            sx={{
              mb: 2,
              '& .MuiOutlinedInput-root': {
                color: 'white',
                '& fieldset':             { borderColor: 'rgba(255,255,255,0.2)' },
                '&:hover fieldset':       { borderColor: 'rgba(255,255,255,0.45)' },
                '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
              },
              '& .MuiInputLabel-root':            { color: 'rgba(255,255,255,0.5)' },
              '& .MuiInputLabel-root.Mui-focused': { color: '#90caf9' },
            }}
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
            sx={{
              mb: 3,
              '& .MuiOutlinedInput-root': {
                color: 'white',
                '& fieldset':             { borderColor: 'rgba(255,255,255,0.2)' },
                '&:hover fieldset':       { borderColor: 'rgba(255,255,255,0.45)' },
                '&.Mui-focused fieldset': { borderColor: '#42a5f5' },
              },
              '& .MuiInputLabel-root':            { color: 'rgba(255,255,255,0.5)' },
              '& .MuiInputLabel-root.Mui-focused': { color: '#90caf9' },
            }}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    onClick={() => setShowPassword((v) => !v)}
                    edge="end"
                    tabIndex={-1}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                    sx={{ color: 'rgba(255,255,255,0.45)' }}
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
              boxShadow: '0 4px 20px rgba(2,119,189,0.45)',
              '&:hover': {
                background: 'linear-gradient(135deg, #0a3880 0%, #01579b 100%)',
                boxShadow: '0 4px 28px rgba(2,119,189,0.65)',
              },
            }}
          >
            {loading ? <CircularProgress size={22} color="inherit" /> : 'Login'}
          </Button>

          <Divider sx={{ my: 3, borderColor: 'rgba(255,255,255,0.1)' }} />

          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="caption" display="block" sx={{ color: 'rgba(255,255,255,0.35)' }}>
              Use your STN (Subaru Telescope Network) login and password.
            </Typography>
            <Typography variant="caption" display="block" mt={0.5} sx={{ color: 'rgba(255,255,255,0.25)' }}>
              Sessions expire after 24 hours.
            </Typography>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
}
