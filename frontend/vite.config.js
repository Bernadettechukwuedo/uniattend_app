import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'


export default defineConfig({
  plugins: [tailwindcss(), vue()],
  server: {
  host: "0.0.0.0",
  port: 5173,
  watch: {
    usePolling: true
  },
  proxy: {'api': 'http://localhost:3000'}
}
})