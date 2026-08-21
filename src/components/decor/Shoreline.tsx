import { useId } from 'react';

import type { DecorProps } from '@/types/decor';

type ShorelineProps = Pick<DecorProps, 'className'>;

/**
 * Water bands, back to front.
 *
 * Each band carries its own vertical gradient rather than a flat fill: that is
 * what gives the surf its depth in the key art, and it is why the bands can
 * stay this low-frequency without looking like flat paper cut-outs.
 */
const BANDS = [
  {
    d: 'M0 66 C300 16 620 94 960 58 C1180 34 1300 66 1440 46 V280 H0 Z',
    from: 'var(--c-foam-100)',
    to: 'var(--c-foam-200)',
  },
  {
    d: 'M0 108 C280 58 600 138 940 102 C1160 78 1300 112 1440 90 V280 H0 Z',
    from: 'var(--c-foam-200)',
    to: 'var(--c-foam-300)',
  },
  {
    d: 'M0 150 C300 104 620 176 960 146 C1180 124 1310 154 1440 134 V280 H0 Z',
    from: 'var(--c-foam-300)',
    to: 'var(--c-ocean-200)',
  },
  {
    d: 'M0 196 C320 154 640 214 980 186 C1200 166 1320 192 1440 174 V280 H0 Z',
    from: 'var(--c-ocean-200)',
    to: 'var(--c-ocean-300)',
  },
  {
    d: 'M0 240 C340 208 660 252 1000 230 C1220 214 1330 234 1440 220 V280 H0 Z',
    from: 'var(--c-ocean-300)',
    to: 'var(--c-ocean-400)',
  },
] as const;

/** Long, lazy foam streaks. Thin enough to read as glare, not as geometry. */
const FOAM = [
  'M96 92 C190 74 268 100 360 84',
  'M520 78 C610 62 690 86 780 72',
  'M880 122 C980 104 1064 128 1160 112',
  'M232 158 C330 142 410 164 500 150',
  'M660 186 C760 170 846 192 940 178',
  'M1060 62 C1130 50 1196 68 1264 56',
  'M300 224 C400 210 486 228 580 216',
  'M1000 210 C1090 198 1168 214 1250 204',
] as const;

export function Shoreline({ className }: ShorelineProps) {
  const uid = useId();

  return (
    <svg
      className={className}
      viewBox="0 0 1440 280"
      preserveAspectRatio="none"
      aria-hidden="true"
      focusable="false"
    >
      <defs>
        {BANDS.map((band, index) => (
          <linearGradient
            key={band.d}
            id={`${uid}-band-${index}`}
            x1="0"
            y1="0"
            x2="0"
            y2="1"
          >
            <stop offset="0%" stopColor={band.from} />
            <stop offset="100%" stopColor={band.to} />
          </linearGradient>
        ))}
      </defs>

      {BANDS.map((band, index) => (
        <path key={band.d} d={band.d} fill={`url(#${uid}-band-${index})`} />
      ))}

      <g
        fill="none"
        stroke="var(--c-paper)"
        strokeWidth="3"
        strokeLinecap="round"
        opacity="0.7"
        vectorEffect="non-scaling-stroke"
      >
        {FOAM.map((d) => (
          <path key={d} d={d} />
        ))}
      </g>
    </svg>
  );
}
