import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.js'],
    globals: true,

    coverage: {
      reporter: ['text', 'html'],

      // only measure real source files
      include: [
        'src/modules/**/*.js',
        'src/modules/**/*.jsx'
      ],

      // exclude styling and non-functional files
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.test.*',
        '**/*.spec.*',

        // styles
        '**/*.css',
        '**/*.scss',
        '**/styles/**',

        // assets
        '**/*.svg',
        '**/*.png',
        '**/*.jpg',
        '**/*.jpeg',
        '**/*.gif',
        '**/assets/**',

        // mocks
        '**/__mocks__/**',

        // app bootstrap files
        'src/main.*',
        'src/index.*'
      ]
    }
  },
})
