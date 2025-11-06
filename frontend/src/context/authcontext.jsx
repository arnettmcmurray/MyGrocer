import React, { createContext, useState } from "react";
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

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export default AuthContext;
