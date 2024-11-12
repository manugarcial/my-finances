import { Module } from "vuex";
import { RootState } from "../types";

export interface LanguageState {
  currentLanguage: string;
}

const language: Module<LanguageState, RootState> = {
  namespaced: true,
  state: {
    currentLanguage: "EN",
  },
  mutations: {
    SET_LANGUAGE(state, language: string) {
      state.currentLanguage = language;
    },
  },
  actions: {
    setLanguage({ commit }, language: string) {
      commit("SET_LANGUAGE", language);
    },
  },
  getters: {
    currentLanguage: (state) => state.currentLanguage,
  },
};

export default language;
