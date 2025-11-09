import React, { createContext, useState, useContext } from "react";
import { setAuthToken } from "../api/axios";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setTokenState] = useState(null);

  function login(jwt) {
    setTokenState(jwt);
    setAuthToken(jwt);
  }

  function logout() {
    setTokenState(null);
    setAuthToken(null);
  }

  function useAuthHeader() {
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  return (
    <AuthContext.Provider value={{ token, login, logout, useAuthHeader }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

export default AuthContext;
