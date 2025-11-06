import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import HouseholdsView from "./views/HouseholdsView";
import { AuthProvider } from "./context/AuthContext";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/households" element={<HouseholdsView />} />
          <Route path="*" element={<Navigate to="/households" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
