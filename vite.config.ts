import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/**
 * `base` must point to the public path where the site is served from.
 *
 * - Local development and manual builds use `/`.
 * - GitHub Pages project sites set `/<repo>/` through the deploy workflow.
 * - Custom domains keep `/` through that same workflow.
 *
 * The deploy workflow computes this value automatically.
 */
const base = process.env.VITE_BASE_PATH ?? '/';

export default defineConfig({
  base,
  plugins: [react()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  build: {
    target: 'es2022',
    outDir: 'dist',
    sourcemap: false,
  },
});
