import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { UserProvider } from "./context/UserContext";
import LoginPage from "./pages/LoginPage";
import QuizListPage from "./pages/QuizListPage";
import QuizPage from "./pages/QuizPage";

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Called after successful login/register
  const handleLogin = () => setIsAuthenticated(true);

  return (
    <UserProvider>
      <Router>
        <Routes>
          <Route
            path="/"
            element={
              isAuthenticated ? (
                <Navigate to="/quizzes" replace />
              ) : (
                <LoginPage onAuth={handleAuth} />  
              )
            }
          />

          <Route
            path="/quizzes"
            element={
              isAuthenticated ? <QuizListPage /> : <Navigate to="/" replace />
            }
          />
          <Route
            path="/quiz/:quizId"
            element={
              isAuthenticated ? <QuizPage /> : <Navigate to="/" replace />
            }
          />
          {/* Optional: catch-all redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </UserProvider>
  );
};

export default App;
