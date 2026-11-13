import { ribbonPath, type SpinePoint } from '@/lib/svg';
import type { DecorProps } from '@/types/decor';

type SeaRockProps = DecorProps;

const OUTLINE =
  'M3 86 C7 74 22 66 36 56 C48 48 54 30 66 26 C78 22 87 36 93 50 C99 64 103 78 102 88 C74 97 26 96 3 86 Z';

/**
 * Tapered currents wrapping the rock, built from the same ribbon primitive the
 * brand mark uses on its ocean half.
 */
const CURRENTS: readonly (readonly SpinePoint[])[] = [
  [
    [40, 40, 0],
    [50, 34, 1.6],
    [60, 33, 1.8],
    [70, 37, 1.3],
    [78, 42, 0],
  ],
  [
    [16, 66, 0],
    [28, 58, 1.7],
    [42, 55, 2],
    [56, 57, 1.7],
    [68, 62, 1.2],
    [76, 66, 0],
  ],
  [
    [12, 82, 0],
    [26, 76, 1.6],
    [40, 74, 1.8],
    [54, 77, 1.6],
    [66, 82, 1.2],
    [74, 86, 0],
  ],
];

/**
 * The lone rock breaking the surface offshore.
 *
 * Drawn rather than taken from the official set: at the size it appears here
 * this reads better than the supplied `sea-rock` artwork, which is cut for
 * larger placements.
 */
export function SeaRock({ className, style }: SeaRockProps) {
  return (
    <svg
      viewBox="0 0 106 96"
      className={className}
      style={style}
      aria-hidden="true"
      focusable="false"
    >
      <path
        d={OUTLINE}
        fill="var(--c-ocean-500)"
        stroke="var(--c-paper)"
        strokeWidth="5"
        strokeLinejoin="round"
      />
      <g fill="var(--c-paper)">
        {CURRENTS.map((spine) => {
          const d = ribbonPath(spine);
          return <path key={d} d={d} />;
        })}
      </g>
    </svg>
  );
}
