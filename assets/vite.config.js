import { defineConfig, loadEnv } from 'vite';
import { resolve, join } from 'path';
import tailwindcss from '@tailwindcss/vite';


export default defineConfig((mode) => {
  const env = loadEnv(mode, process.cwd(), '');

  const INPUT_DIR = '/app/assets';
  const OUTPUT_DIR = '/app/assets_dist';

  return {
    plugins: [
      tailwindcss()
    ],
    resolve: {
      alias: {
        '@': resolve(INPUT_DIR),
      },
    },
    root: resolve(INPUT_DIR),
    base: '/static/',
    css: {},
    server: {
      host: env.DJANGO_VITE_DEV_SERVER_HOST,
      port: env.DJANGO_VITE_DEV_SERVER_PORT,
    },
    build: {
      manifest: true,
      emptyOutDir: true,
      outDir: resolve(OUTPUT_DIR),
      rollupOptions: {
        input: {
          css: join(INPUT_DIR, '/css/main.css'),
          js: [join(INPUT_DIR, '/js/unpoly.js'), join(INPUT_DIR, '/js/alpine.js')],
        },
      },
    },
  };
});