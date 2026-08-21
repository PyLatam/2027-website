import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/**
 * `base` must point to the public path where the site is served from.
 *
 * - GitHub Pages project site (default): https://pylatam.github.io/2027-website/
 * - Custom domain (e.g. 2027.pylatam.org): set VITE_BASE_PATH="/"
 *
 * The deploy workflow computes this value automatically.
 */
const base = process.env.VITE_BASE_PATH ?? '/2027-website/';

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
