import React, { useState, useContext } from "react";
import { loginUser, registerUser } from "../api/authApi";
import { UserContext } from "../context/UserContext";

const LoginPage = ({ onAuth }) => {
  const { setUser } = useContext(UserContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState("");

  const handleAuth = async () => {
    try {
      const user = isRegister
        ? await registerUser(username, password)
        : await loginUser(username, password);

      setUser(user);
      onAuth(); // ✅ no error now
    } catch (err) {
      setError(err.message || "Auth failed");
    }
  };

  return (
    <div className="login-page">
      <h2>{isRegister ? "Register" : "Login"}</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleAuth}>{isRegister ? "Register" : "Login"}</button>
      <p onClick={() => setIsRegister(!isRegister)}>
        {isRegister ? "Already have an account? Login" : "No account? Register"}
      </p>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default LoginPage;
