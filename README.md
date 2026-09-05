# Pipe Maze 3D — website & web build

Astro site published on GitHub Pages at https://kuragestudios.github.io/pipe-maze-3d/

- `/` landing page (features, shapes, themes, screenshots, download links)
- `/play/` the game, full window (shows a "coming soon" note until a web build is published)
- `/game/` the raw Unity WebGL build (copied from the Unity project by `Deploy/github-pages/publish-web.sh`)

```sh
npm install
npm run dev      # http://localhost:4321/pipe-maze-3d/
npm run build    # dist/
```

`scripts/themes.py` regenerates `src/data/themes.json` (the colour swatches of the 23 graphic themes)
from the Unity project's theme ScriptableObjects and materials.

Deploy: push to `main`; `.github/workflows/deploy.yml` builds and publishes to Pages
(Settings > Pages > Source: GitHub Actions).
