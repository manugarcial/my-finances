// types.ts
export interface User {
  // id: string;
  username: string;
  // email: string;
  // token: string;
  access_token: string;
  // Add any other properties that are part of the user data
}

export interface RootState {
  user: User | null; // User can be `null` when not logged in
}
