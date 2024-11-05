import { createStore } from "vuex";
import { User, RootState } from "./types";

const store = createStore<RootState>({
  state: () => ({
    user: null as User | null,
  }),
  getters: {
    // Getter to retrieve the username
    getUsername(state) {
      return state.user ? state.user.username : null; // Return username or null
    },
    getUsertoken(state) {
      return state.user ? state.user.access_token : null; // Return username or null
    },
  },
  mutations: {
    setUser(state, user: User) {
      state.user = user;
      console.log("set User");
      console.log(user);
      console.log(state.user);
      localStorage.setItem("user", JSON.stringify(user)); // Store user in localStorage
    },
    clearUser(state) {
      state.user = null;
      console.log("clear user should be null");
      console.log(state.user);
      localStorage.removeItem("user"); // Clear user from localStorage
    },
  },
  actions: {
    login({ commit }, userData: User) {
      // Commit user data to Vuex store
      console.log("login action, commit");
      console.log(userData);
      commit("setUser", userData);
    },
    checkStoredUser({ commit }) {
      const userJSON = localStorage.getItem("user");
      console.log("check Stored user");
      console.log(userJSON);
      if (userJSON) {
        try {
          const user = JSON.parse(userJSON);
          commit("setUser", user);
        } catch (error) {
          console.error("Error parsing user JSON from localStorage:", error);
          commit("clearUser"); // Clear state if parsing fails
        }
      } else {
        commit("clearUser"); // No user data found
      }
    },
    logout({ commit }) {
      commit("clearUser");
    },
  },
  modules: {},
});

export default store;
