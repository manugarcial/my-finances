import axios, { AxiosResponse } from "axios";
import { Store } from "vuex"; // Ensure this is imported
import { User } from "../store/types";

const API_URL = process.env.VUE_APP_API_BASE_URL as string; // Backend URL

// Define the expected structure of the login response data
interface LoginResponse {
  access_token: string;
}

// Login function
export const userlogin = (
  username: string,
  password: string
): Promise<LoginResponse> => {
  return axios
    .post<LoginResponse>(`${API_URL}/login`, { username, password })
    .then((response: AxiosResponse<LoginResponse>) => {
      if (response.data.access_token) {
        console.log("userlogin response");
        console.log(response);
        // Return the user data object if access_token is present
        return {
          access_token: response.data.access_token,
        };
      } else {
        // If access_token is not found, throw an error
        throw new Error("No access token received");
      }
    })
    .catch((error) => {
      console.error("Error during login:", error);
      // Optionally, you can throw the error further up the chain for handling
      throw error; // Re-throw the error to be handled in the calling function
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
// export const getCurrentUser = (): User | null => {
//   const user = localStorage.getItem("user");
//   return user ? (JSON.parse(user) as User) : null;
// };
export const getCurrentUser = (store: Store<any>): User | null => {
  console.log("get current user API");
  console.log(store.state.user);
  return store.state.user || null;
};
