import type { DecorProps } from '@/types/decor';

type ShorelineProps = Pick<DecorProps, 'className'>;

/**
 * The layered surf that anchors the bottom of the hero. Bands are stretched
 * with `preserveAspectRatio="none"` so the shoreline spans any viewport width
 * without changing the composition's vertical rhythm.
 */
export function Shoreline({ className }: ShorelineProps) {
  const bands = [
    {
      d: 'M0 78 C220 34 420 116 700 74 C920 41 1120 96 1440 58 V200 H0 Z',
      fill: 'var(--c-foam-200)',
    },
    {
      d: 'M0 110 C240 68 460 146 720 106 C960 69 1180 128 1440 92 V200 H0 Z',
      fill: 'var(--c-foam-300)',
    },
    {
      d: 'M0 142 C260 104 480 172 760 138 C1000 109 1200 158 1440 130 V200 H0 Z',
      fill: 'var(--c-ocean-200)',
    },
    {
      d: 'M0 176 C300 146 520 196 800 172 C1040 152 1220 184 1440 166 V200 H0 Z',
      fill: 'var(--c-ocean-300)',
    },
  ];

  const curls = [
    'M120 96 C180 84 232 108 300 96',
    'M520 90 C580 78 632 100 700 88',
    'M900 126 C960 114 1012 136 1080 124',
    'M280 158 C340 148 392 166 460 156',
    'M1080 66 C1130 56 1174 74 1230 64',
  ];

  return (
    <svg
      className={className}
      viewBox="0 0 1440 200"
      preserveAspectRatio="none"
      aria-hidden="true"
      focusable="false"
    >
      {bands.map((band) => (
        <path key={band.d} d={band.d} fill={band.fill} />
      ))}
      <g
        fill="none"
        stroke="var(--c-paper)"
        strokeWidth="3"
        strokeLinecap="round"
        opacity="0.75"
        vectorEffect="non-scaling-stroke"
      >
        {curls.map((d) => (
          <path key={d} d={d} />
        ))}
      </g>
    </svg>
  );
}
