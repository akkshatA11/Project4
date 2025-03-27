import axios from "axios";

const API_URL = "http://localhost:8000/auth";

// Login with proper error handling
export const login = async (credentials) => {
  try {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await axios.post(`${API_URL}/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || "Login failed");
    }
    throw error;
  }
};

// Sign Up
export const signup = async (userData) => {
  try {
    const response = await axios.post(
      `${API_URL}/signup`,
      {
        username: userData.username,
        email: userData.email,
        password: userData.password,
        auth_provider: userData.auth_provider || null
      },
      {
        headers: { "Content-Type": "application/json" }
      }
    );
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || "Signup failed");
    }
    throw error;
  }
};

// OAuth endpoints
export const googleLogin = () => {
  window.location.href = `${API_URL}/login/google`;
};

export const facebookLogin = () => {
  window.location.href = `${API_URL}/login/facebook`;
};