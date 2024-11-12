// import { createStore, Module } from "vuex";
import { createStore } from "vuex";
import { User } from "./types";

// Define RootState directly in `index.ts`
export interface RootState {
  user: User | null;
}

const store = createStore<RootState>({
  state: () => ({
    user: null,
  }),
  getters: {
    getUsername(state): string | null {
      return state.user ? state.user.username : null;
    },
    getUsertoken(state): string | null {
      return state.user ? state.user.access_token : null;
    },
  },
  mutations: {
    setUser(state, user: User) {
      state.user = user;
      localStorage.setItem("user", JSON.stringify(user));
    },
    clearUser(state) {
      state.user = null;
      localStorage.removeItem("user");
    },
  },
  actions: {
    login({ commit }, userData: User) {
      commit("setUser", userData);
    },
    checkStoredUser({ commit }) {
      const userJSON = localStorage.getItem("user");
      if (userJSON) {
        try {
          const user = JSON.parse(userJSON) as User;
          commit("setUser", user);
        } catch (error) {
          console.error("Error parsing user JSON from localStorage:", error);
          commit("clearUser");
        }
      } else {
        commit("clearUser");
      }
    },
    logout({ commit }) {
      commit("clearUser");
    },
  },
});

export default store;
