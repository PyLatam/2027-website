#!/usr/bin/env node
/**
 * Generates the golden JSON the Python scene port is tested against.
 *
 * It loads the *real* TypeScript and TSX from `legacy-react/src/` through
 * Vite's SSR loader (same alias, same `?raw` imports, same React), runs the
 * SVG generators and renders every decor component with
 * `react-dom/server`. The output is committed next to this script, so the
 * Python tests need no Node and outlive `legacy-react/`.
 *
 * CSS Module class names are generated as `<prefix>-<kebab-name>`, the rule
 * the Django port follows (`HeroDecor.module.css` `.palmTreeFar` →
 * `hero-decor-palm-tree-far`), so the hero markup can be compared verbatim.
 *
 * Run from the repo root, inside WSL, with nvm loaded:
 *
 *   node web/golden/generate.mjs
 *
 * It reads `legacy-react/` and writes only to `web/golden/`.
 */
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { tmpdir } from 'node:os';
import { basename, dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const REACT_ROOT = resolve(HERE, '../../legacy-react');
const requireFromReact = createRequire(join(REACT_ROOT, 'package.json'));

const { createServer } = await import(pathToFileURL(requireFromReact.resolve('vite')).href);
const React = requireFromReact('react');
const { renderToStaticMarkup } = requireFromReact('react-dom/server');

/** CSS Module file → class prefix in Django, and which class is the bare root. */
const CSS_MODULES = {
  'Hero.module.css': { prefix: 'hero', root: 'hero' },
  'HeroDecor.module.css': { prefix: 'hero-decor', root: 'layer' },
  'App.module.css': { prefix: 'app', root: null },
  'Footer.module.css': { prefix: 'footer', root: 'footer' },
  'LanguageSwitcher.module.css': { prefix: 'language-switcher', root: 'switcher' },
};

const kebab = (name) => name.replace(/[A-Z]/g, (c) => `-${c.toLowerCase()}`);

function scopedName(name, filename) {
  const file = basename(filename.split('?')[0]);
  const rule = CSS_MODULES[file];
  if (!rule) throw new Error(`No prefix rule for ${file}`);
  return name === rule.root ? rule.prefix : `${rule.prefix}-${kebab(name)}`;
}

const vite = await createServer({
  root: REACT_ROOT,
  configFile: join(REACT_ROOT, 'vite.config.ts'),
  cacheDir: join(tmpdir(), 'pyconlatam-golden-vite'),
  logLevel: 'warn',
  appType: 'custom',
  server: { middlewareMode: true, hmr: false, watch: null },
  css: { modules: { generateScopedName: scopedName } },
});

try {
  const svg = await vite.ssrLoadModule('/src/lib/svg/index.ts');
  const decor = await vite.ssrLoadModule('/src/components/decor/index.ts');
  const { HeroDecor } = await vite.ssrLoadModule('/src/features/hero/HeroDecor.tsx');
  const { Hero } = await vite.ssrLoadModule('/src/features/hero/Hero.tsx');
  const { LocaleContext } = await vite.ssrLoadModule('/src/i18n/LocaleContext.ts');
  const { DICTIONARIES, interpolate } = await vite.ssrLoadModule('/src/i18n/dictionary.ts');

  const h = React.createElement;
  const render = (element) => renderToStaticMarkup(element);

  // ------------------------------------------------------------------ numbers
  // A fixed pool of awkward doubles: exact ties, values just either side of a
  // tie, negative zero, tiny negatives that round to `-0.00`, and the
  // exponent-notation boundaries of `Number.prototype.toString`.
  const rand = svg.createRandom(20270826);
  const pool = [
    0, -0, 1, -1, 3, 0.1, 0.2, 0.1 + 0.2, 0.125, -0.125, 0.375, 1.005, 2.675, 1.115, 0.005,
    -0.005, -0.001, -0.004999, 0.0049999, 0.015, 0.045, 10.235, 99.995, 199.995, -199.995,
    1 / 3, 2 / 3, -2 / 3, 100 / 6, 0.49999999999999994, 0.5, 1.5, 2.5, -0.5, -1.5, -2.5,
    1234.5678, 1e-7, 1.5e-7, 9.99e-8, 1e-6, 123e-20, 1e20, 1e21, 1.5e21, 123e25, -1e21,
    2 ** 53, 2 ** 53 + 2, Number.MAX_SAFE_INTEGER, Number.MIN_VALUE, Number.MAX_VALUE,
    Number.EPSILON, 4294967296, 0.000001234, 1e300 * 1e-300,
  ];
  for (let i = 0; i < 400; i++) {
    const magnitude = 10 ** Math.floor(rand() * 8 - 3);
    pool.push((rand() - 0.5) * 2 * magnitude);
    // Values on a 0.005 grid, where `toFixed(2)` ties live.
    pool.push(Math.round((rand() - 0.5) * 200000) / 1000 + 0.005);
  }
  const finite = pool.filter(Number.isFinite);
  const numbers = {
    toString: finite.map((n) => [n, String(n)]),
    toFixed2: finite.map((n) => [n, Number(n.toFixed(2)).toString()]),
    round: finite
      .filter((n) => Math.abs(n) < 2 ** 52)
      .map((n) => [n, Math.round(n)]),
    // V8's `Math.hypot` differs from Python's `math.hypot` in the last bit for
    // about a third of inputs, so the port is checked bit for bit.
    hypot: [
      [0, 0], [3, 4], [-3, 4], [0, -5], [1e-300, 1e-300], [1e300, 1e300], [5e-324, 0],
      ...Array.from({ length: 600 }, () => [(rand() - 0.5) * 1800, (rand() - 0.5) * 1800]),
      ...Array.from({ length: 200 }, () => [(rand() - 0.5) * 4, (rand() - 0.5) * 900]),
    ].map(([x, y]) => [x, y, Math.hypot(x, y)]),
  };

  // --------------------------------------------------------------------- PRNG
  const seeds = [0, 1, 7, 21, 122, 42, 20270826, 2 ** 31, 2 ** 32 - 1, 2 ** 32 + 5, -1, -21, 3.7, -3.7];
  const prng = seeds.map((seed) => {
    const next = svg.createRandom(seed);
    return { seed, values: Array.from({ length: 64 }, () => next()) };
  });

  // ------------------------------------------------------------------- ribbon
  // Every spine the scene draws, then edge cases, then seeded random spines.
  const sceneSpines = [
    [[130, 340, 5.2], [124, 292, 4.4], [115, 242, 3.7], [104, 192, 3], [94, 146, 2.5], [88, 114, 2.1], [86, 100, 1.9]],
    [[0, 0, 3.5], [16, -11, 11], [35, -12, 10.5], [53, -3, 6.5], [68, 17, 0]],
    [[0, 153, 0], [90, 148, 3], [190, 137, 5], [270, 134, 6], [315, 143, 5], [330, 155, 4], [302, 174, 6], [250, 194, 5], [205, 211, 4], [180, 229, 2], [193, 245, 0]],
    [[0, 180, 0], [100, 172, 3], [205, 157, 5], [268, 164, 5], [292, 175, 4], [266, 193, 5], [218, 208, 4], [171, 223, 3], [148, 240, 2], [166, 257, 0]],
    [[0, 210, 0], [88, 201, 3], [176, 181, 5], [222, 187, 5], [246, 198, 4], [226, 212, 5], [184, 225, 4], [142, 238, 3], [121, 253, 2], [137, 269, 0]],
    [[40, 40, 0], [50, 34, 1.6], [60, 33, 1.8], [70, 37, 1.3], [78, 42, 0]],
    [[16, 66, 0], [28, 58, 1.7], [42, 55, 2], [56, 57, 1.7], [68, 62, 1.2], [76, 66, 0]],
    [[12, 82, 0], [26, 76, 1.6], [40, 74, 1.8], [54, 77, 1.6], [66, 82, 1.2], [74, 86, 0]],
  ];
  const edgeSpines = [
    [],
    [[1, 2, 3]],
    [[0, 0, 1], [10, 0, 1]],
    [[0, 0, 1], [0, 0, 1], [0, 0, 1]],
    [[0.125, 0.375, 0.125], [1.005, 2.675, 0.005], [-0.005, -0.125, 0.0049]],
    [[-3, -4, 0], [3, 4, 2.5], [9, -4, 1.25]],
  ];
  const spineRand = svg.createRandom(1440);
  const randomSpines = Array.from({ length: 40 }, () => {
    const length = 2 + Math.floor(spineRand() * 10);
    return Array.from({ length }, () => [
      (spineRand() - 0.5) * 900,
      (spineRand() - 0.5) * 900,
      spineRand() * 30,
    ]);
  });
  const ribbon = [...sceneSpines, ...edgeSpines, ...randomSpines].map((spine) => ({
    spine,
    d: svg.ribbonPath(spine),
  }));

  // ------------------------------------------------------------------- canopy
  const canopyOptions = [
    { seed: 21, count: 28, from: [196, 126], to: [462, 26], minRadius: 10, maxRadius: 26, scatter: 22 },
    { seed: 122, count: 26, from: [246, 116], to: [462, 6], minRadius: 9, maxRadius: 24, scatter: 20 },
    { seed: 7, count: 1, from: [0, 0], to: [100, 0], minRadius: 5, maxRadius: 5, scatter: 0 },
    { seed: 3, count: 0, from: [0, 0], to: [100, 0], minRadius: 5, maxRadius: 9, scatter: 4 },
    { seed: 9, count: 12, from: [50, 50], to: [50, 50], minRadius: 1, maxRadius: 3, scatter: 7 },
    { seed: -5, count: 40, from: [-300, 120], to: [300, -120], minRadius: 0.5, maxRadius: 40, scatter: 33.3 },
  ];
  const canopy = canopyOptions.map((options) => ({ options, blobs: svg.canopyBlobs(options) }));

  // ------------------------------------------------------------------- markup
  const shapeNames = Object.keys(decor.DECOR_SHAPES);
  const markupHelpers = {
    viewBox: shapeNames.map((name) => [name, svg.svgViewBox(decor.DECOR_SHAPES[name])]),
    namespace: shapeNames.map((name) => [
      name,
      svg.namespaceSvgIds(svg.svgInnerMarkup(decor.DECOR_SHAPES[name]), 'UID'),
    ]),
  };

  const withLocale = (locale, child) => {
    const t = (key, values) => interpolate(DICTIONARIES[locale][key], values);
    return h(LocaleContext.Provider, { value: { locale, setLocale() {}, t } }, child);
  };

  const components = {
    'BrandMark/es': h(decor.BrandMark, { title: DICTIONARIES.es['logo.alt'] }),
    'BrandMark/class': h(decor.BrandMark, { title: 'A & "B"', className: 'x y' }),
    ...Object.fromEntries(
      shapeNames.flatMap((name) => [
        [`BrandShape/${name}`, h(decor.BrandShape, { name })],
        [
          `BrandShape/${name}/color`,
          h(decor.BrandShape, { name, color: 'var(--c-aqua-500)', className: 'item' }),
        ],
      ]),
    ),
    'BrandShape/twice': h(
      'div',
      null,
      h(decor.BrandShape, { name: 'sea-rock' }),
      h(decor.BrandShape, { name: 'sea-rock' }),
    ),
    CircuitTraces: h(decor.CircuitTraces, {}),
    'CircuitTraces/class': h(decor.CircuitTraces, { className: 'traces left' }),
    PalmTree: h(decor.PalmTree, { trunkColor: 'var(--c-aqua-600)', crownColor: 'var(--c-aqua-600)' }),
    'PalmTree/flip8': h(decor.PalmTree, {
      trunkColor: 'var(--c-ocean-400)',
      crownColor: 'var(--c-ocean-400)',
      fronds: 8,
      flip: true,
      className: 'palm',
    }),
    ...Object.fromEntries(
      [1, 2, 3, 5, 12].map((fronds) => [
        `PalmTree/fronds${fronds}`,
        h(decor.PalmTree, { trunkColor: 'red', crownColor: 'blue', fronds }),
      ]),
    ),
    SandCove: h(decor.SandCove, {}),
    'SandCove/seed7': h(decor.SandCove, { seed: 7, className: 'sand' }),
    SeaRock: h(decor.SeaRock, { className: 'rock' }),
    Shoreline: h(decor.Shoreline, { className: 'shore' }),
    HeroDecor: h(HeroDecor, {}),
    'Hero/es': withLocale('es', h(Hero, {})),
    'Hero/en': withLocale('en', h(Hero, {})),
  };
  const markup = Object.fromEntries(
    Object.entries(components).map(([key, element]) => [key, render(element)]),
  );

  // ------------------------------------------------------------------- assets
  const assetFiles = [
    'pycon-latam-rd-mark.svg',
    ...shapeNames.map((name) => `decor/${name}.svg`),
  ];
  const assets = Object.fromEntries(
    assetFiles.map((file) => [
      file,
      createHash('sha256').update(readFileSync(join(REACT_ROOT, 'src/assets', file))).digest('hex'),
    ]),
  );

  // ---------------------------------------------------------------------- css
  // The hero's CSS Modules compiled with the Django class names (keyframes are
  // scoped the same way). `web/static/css/hero*.css` must match these once
  // comments and whitespace are normalised.
  const css = {};
  for (const [file, path] of [
    ['hero.css', '/src/features/hero/Hero.module.css'],
    ['hero-decor.css', '/src/features/hero/HeroDecor.module.css'],
  ]) {
    css[file] = (await vite.ssrLoadModule(`${path}?inline`)).default;
  }

  const write = (name, data) =>
    writeFileSync(join(HERE, name), `${JSON.stringify(data, null, 1)}\n`);
  write('css.json', css);
  write('numbers.json', numbers);
  write('prng.json', prng);
  write('ribbon.json', ribbon);
  write('canopy.json', canopy);
  write('markup.json', { helpers: markupHelpers, components: markup });
  write('assets.json', assets);
  console.log(
    `golden: ${finite.length} numbers, ${prng.length} seeds, ${ribbon.length} spines, ` +
      `${canopy.length} canopies, ${Object.keys(markup).length} components, ${assetFiles.length} assets`,
  );
} finally {
  await vite.close();
}
