/**
 * AuthContext — global authentication state for OPAL.
 *
 * Mirrors the PHP session lifecycle:
 *   - On mount: calls GET /api/v1/auth/me to restore an existing session cookie.
 *   - login()  → POST /api/v1/auth/login  (server sets httpOnly cookie)
 *   - logout() → POST /api/v1/auth/logout (server clears cookie)
 *
 * Consumers:
 *   const { user, isLoading, login, logout } = useAuth();
 */

import React, { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);       // { username, privy, logcrew, uid }
  const [isLoading, setIsLoading] = useState(true); // true while checking existing session

  // ── Restore session on page load ────────────────────────────────────────────
  useEffect(() => {
    authAPI
      .me()
      .then((res) => setUser(res.data))
      .catch(() => setUser(null))
      .finally(() => setIsLoading(false));
  }, []);

  // ── Login ────────────────────────────────────────────────────────────────────
  const login = useCallback(async (username, password) => {
    const res = await authAPI.login(username, password);
    setUser(res.data);
    return res.data;
  }, []);

  // ── Logout ───────────────────────────────────────────────────────────────────
  const logout = useCallback(async () => {
    try {
      await authAPI.logout();
    } catch {
      // Cookie may already be gone — still clear local state
    } finally {
      setUser(null);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>');
  return ctx;
}
