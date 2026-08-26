import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

// base './' — чтобы собранная админка работала под любым ADMIN_PATH
export default defineConfig({
  plugins: [react()],
  base: './',
});
