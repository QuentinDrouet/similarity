import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    headers: {
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'require-corp',
    },
    middleware: (req, res, next) => {
      if (req.url.endsWith('.wasm')) {
        res.setHeader('Content-Type', 'application/wasm')
      }
      next()
    }
  },
  optimizeDeps: {
    exclude: ['onnxruntime-web']
  },
  build: {
    commonjsOptions: {
      include: [/onnxruntime-web/, /node_modules/]
    }
  },
  assetsInclude: ['**/*.onnx', '**/*.wasm']
})
