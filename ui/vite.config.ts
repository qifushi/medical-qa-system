import { fileURLToPath, URL } from 'node:url'
import type { ProxyOptions } from 'vite'
import { defineConfig, loadEnv } from 'vite'
import path from 'path'

import vue from '@vitejs/plugin-vue'
import DefineOptions from 'unplugin-vue-define-options/vite'
import { viteStaticCopy } from 'vite-plugin-static-copy'
const envDir = './env'
// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const ENV = loadEnv(mode, envDir)
  const proxyConf: Record<string, string | ProxyOptions> = {}
  proxyConf['/api'] = {
    // target: 'https://brain.jrsoft.com.cn',
    target: 'http://localhost:8010',
    changeOrigin: true,
    rewrite: (path) => path.replace(ENV.VITE_BASE_PATH, '/')
  }
  proxyConf['/train_engine'] = {
    // target: 'https://brain.jrsoft.com.cn',
    target: 'http://localhost:8010',
    changeOrigin: true,
  }
  proxyConf['/doc'] = {
    // target: 'https://brain.jrsoft.com.cn',
    target: 'http://localhost:8010',
    changeOrigin: true,
    rewrite: (path) => path.replace(ENV.VITE_BASE_PATH, '/')
  }
  proxyConf['/static'] = {
    // target: 'https://brain.jrsoft.com.cn',
    target: 'http://localhost:8010',
    changeOrigin: true,
    rewrite: (path) => path.replace(ENV.VITE_BASE_PATH, '/')
  }
  // 上传后的图片/文件由 Django 的 MEDIA_ROOT 提供
  proxyConf['/media'] = {
    target: 'http://localhost:8010',
    changeOrigin: true,
  }
  return {
    preflight: false,
    lintOnSave: false,
    base: ENV.VITE_BASE_PATH,
    envDir: envDir,
    plugins: [vue(), DefineOptions(), viteStaticCopy({
      targets: [
        {
          src: 'node_modules/@ricky0123/vad-web/dist/vad.worklet.bundle.min.js',
          dest: './vad'
        },
        {
          src: 'node_modules/@ricky0123/vad-web/dist/silero_vad_v5.onnx',
          dest: './vad'
        },
        {
          src: 'node_modules/@ricky0123/vad-web/dist/silero_vad_legacy.onnx',
          dest: './vad'
        },
        {
          src: 'node_modules/onnxruntime-web/dist/*.wasm',
          dest: './vad'
        }
      ]
    })],
    server: {
      cors: true,
      host: '0.0.0.0',
      port: Number(5173),
      strictPort: true,
      proxy: proxyConf
    },
    build: {
      outDir: 'dist/ui'
    },
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `
          @import '@pptApp/assets/styles/variable.scss';
          @import '@pptApp/assets/styles/mixin.scss';
        `
        },
      },
    },
    optimizeDeps: {
      include: ['@gradio/client']
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
        '@pptApp': fileURLToPath(new URL('./src/views/ppt-app', import.meta.url)),
        https: path.resolve(__dirname, 'src/shims/https-browser.js'),
        '@gradio/client': fileURLToPath(new URL('./node_modules/@gradio/client/dist/index.js', import.meta.url))
      }
    }
  }
})
