"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { api } from "@/lib/api";

interface User {
  id: string;
  email: string;
  full_name: string;
  role: "user" | "admin";
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<any>;
  register: (email: string, password: string, fullName: string) => Promise<any>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Initial load
  useEffect(() => {
    async function loadUser() {
      const storedToken = localStorage.getItem("agrovision_token");
      if (storedToken) {
        try {
          setToken(storedToken);
          const res = await api.getMe();
          if (res.success && res.data) {
            setUser(res.data);
          } else {
            // Clear invalid token
            logout();
          }
        } catch (err) {
          console.error("Auth initialization error:", err);
          logout();
        }
      }
      setLoading(false);
    }
    loadUser();
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const res = await api.loginUser(email, password);
      if (res.success && res.data) {
        const { access_token, user: userData } = res.data;
        localStorage.setItem("agrovision_token", access_token);
        setToken(access_token);
        setUser(userData);
        setLoading(false);
        return res.data;
      } else {
        throw new Error("Kirish muvaffaqiyatsiz tugadi");
      }
    } catch (err) {
      setLoading(false);
      throw err;
    }
  };

  const register = async (email: string, password: string, fullName: string) => {
    setLoading(true);
    try {
      const res = await api.registerUser(email, password, fullName);
      setLoading(false);
      return res;
    } catch (err) {
      setLoading(false);
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem("agrovision_token");
    setToken(null);
    setUser(null);
    setLoading(false);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
