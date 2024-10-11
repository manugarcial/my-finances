/* eslint-disable */
import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import { createI18n } from 'vue-i18n'

// Translations
const messages = {
    en: {
        title: 'Python Scripts',
        scriptOutput: 'Script Output:',
        executeScript: 'Execute Script',
        script1: 'Script 1',
        PythonScripts: 'Python Scripting',
        welcome: 'welcome2',
    },
    es: {
        title: 'Scripts de Python',
        scriptOutput: 'Resultado del Script:',
        executeScript: 'Ejecutar Script',
        script1: 'Script 1 en Español',
        PythonScripts: 'Python Scripting',
        welcome: 'bienvenido',
    }
}

// Create Vue I18n instance
const i18n = createI18n({
    locale: 'en',  // Default language
    messages,  // Set locale messages
});

createApp(App).use(store).use(router).use(i18n).mount("#app");

// createApp(App).use(store).use(router).mount("#app");