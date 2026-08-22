import type { DecorProps } from '@/types/decor';

type ShorelineProps = Pick<DecorProps, 'className'>;

/**
 * The four broad water planes from the key art, back to front.
 *
 * Their shared crest-valley-rise rhythm matters more than small surface
 * details: it is what makes the lower edge read as one rolling Caribbean sea
 * instead of a stack of nearly horizontal stripes.
 */
const BANDS = [
  {
    d: 'M0 180 C150 170 225 72 360 22 C480 -18 565 92 690 154 C805 210 910 152 1044 90 C1168 34 1300 48 1440 72 V280 H0 Z',
    fill: 'var(--c-foam-200)',
  },
  {
    d: 'M0 220 C180 210 260 126 400 72 C525 24 610 148 735 210 C850 266 950 212 1080 150 C1200 94 1320 104 1440 122 V280 H0 Z',
    fill: 'var(--c-foam-300)',
  },
  {
    d: 'M0 258 C200 250 310 184 440 132 C560 86 650 210 775 264 C900 318 1000 264 1120 202 C1230 146 1340 154 1440 166 V280 H0 Z',
    fill: 'var(--c-ocean-200)',
  },
  {
    d: 'M0 282 C220 278 340 238 480 190 C600 150 690 252 820 292 C950 332 1050 302 1170 250 C1280 202 1365 204 1440 214 V280 H0 Z',
    fill: 'var(--c-ocean-300)',
  },
] as const;

/**
 * A shallower version for stacked layouts. Compressing the desktop geometry
 * into a phone makes its tall first crest look like a pointed mountain; these
 * planes retain the same rhythm with wider, gentler changes in elevation.
 */
const COMPACT_BANDS = [
  {
    d: 'M0 132 C220 130 380 114 560 100 C720 88 880 104 1040 122 C1200 140 1320 120 1440 106 V280 H0 Z',
    fill: 'var(--c-foam-200)',
  },
  {
    d: 'M0 170 C240 168 420 150 600 136 C760 124 920 142 1080 160 C1220 176 1340 158 1440 144 V280 H0 Z',
    fill: 'var(--c-foam-300)',
  },
  {
    d: 'M0 208 C260 206 450 188 640 174 C800 162 960 180 1120 198 C1260 212 1360 196 1440 182 V280 H0 Z',
    fill: 'var(--c-ocean-200)',
  },
  {
    d: 'M0 242 C280 240 480 224 680 212 C840 202 1000 218 1160 234 C1290 246 1380 232 1440 220 V280 H0 Z',
    fill: 'var(--c-ocean-300)',
  },
] as const;

export function Shoreline({ className }: ShorelineProps) {
  return (
    <svg
      className={className}
      viewBox="0 0 1440 280"
      preserveAspectRatio="none"
      aria-hidden="true"
      focusable="false"
    >
      <g data-wide-bands>
        {BANDS.map((band) => (
          <path key={band.d} d={band.d} fill={band.fill} />
        ))}
      </g>
      <g data-compact-bands>
        {COMPACT_BANDS.map((band) => (
          <path key={band.d} d={band.d} fill={band.fill} />
        ))}
      </g>
    </svg>
  );
}
