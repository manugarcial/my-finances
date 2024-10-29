// api.ts
import axios, { AxiosResponse } from "axios";

const API_URL = process.env.VUE_APP_API_BASE_URL as string; // Backend URL

// Define the expected structure of the login response data
interface LoginResponse {
  access_token: string;
}

// Define the expected structure of the stored user data
interface User {
  access_token: string;
  // Add any additional fields that the user object might have
}

/**
 * Login function
 * Sends username and password to the backend and stores the access token if login is successful.
 *
 * @param username - The username of the user
 * @param password - The password of the user
 * @returns A promise that resolves with the login response data
 */
export const userlogin = (
  username: string,
  password: string
): Promise<LoginResponse> => {
  return axios
    .post<LoginResponse>(`${API_URL}/login`, { username, password })
    .then((response: AxiosResponse<LoginResponse>) => {
      if (response.data.access_token) {
        localStorage.setItem("user", JSON.stringify(response.data));
      }
      return response.data;
    });
};

/**
 * Logout function
 * Removes the user from local storage to "log out" the user.
 */
export const userlogout = (): void => {
  localStorage.removeItem("user");
};

/**
 * Get Current User
 * Retrieves and parses the current user data from local storage.
 *
 * @returns The user data or null if no user is logged in
 */
export const getCurrentUser = (): User | null => {
  const user = localStorage.getItem("user");
  return user ? (JSON.parse(user) as User) : null;
};
