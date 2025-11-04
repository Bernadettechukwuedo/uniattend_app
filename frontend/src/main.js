import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia';


createApp(App).use(createPinia()).use(router).mount('#app')

console.log("Backend API:", import.meta.env.VITE_API_BASE_URL);


