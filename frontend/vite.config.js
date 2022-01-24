import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

export default {
  plugins: [vue()],

  server: {
    proxy: {
      '/api': 'http://127.0.0.1/5000'
    }

  }
}
