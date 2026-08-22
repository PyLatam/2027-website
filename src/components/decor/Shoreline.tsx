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
    d: 'M0 150 C180 148 300 104 470 72 C620 44 760 84 910 126 C1060 168 1210 132 1440 96 V280 H0 Z',
    fill: 'var(--c-foam-200)',
  },
  {
    d: 'M0 188 C220 184 360 148 520 116 C670 86 820 126 970 166 C1110 202 1260 166 1440 134 V280 H0 Z',
    fill: 'var(--c-foam-300)',
  },
  {
    d: 'M0 224 C240 220 410 190 570 158 C720 130 870 168 1020 204 C1160 236 1300 204 1440 174 V280 H0 Z',
    fill: 'var(--c-ocean-200)',
  },
  {
    d: 'M0 254 C260 250 450 226 620 196 C770 170 920 206 1070 238 C1200 264 1320 238 1440 210 V280 H0 Z',
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
