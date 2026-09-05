// @ts-check
import { defineConfig } from 'astro/config';

// GitHub Pages project site: https://kuragestudios.github.io/pipe-maze-3d/
// If you attach a custom domain later, set `site` to it and remove `base`.
export default defineConfig({
  site: 'https://kuragestudios.github.io',
  base: '/pipe-maze-3d',
  trailingSlash: 'always',
  build: { format: 'directory' },
});
