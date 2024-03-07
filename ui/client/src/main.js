import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import MarkdownIt from "markdown-it";
import 'highlight.js/styles/atom-one-dark.css';

const app = createApp(App)
app.use(router,MarkdownIt)
app.mount('#app')