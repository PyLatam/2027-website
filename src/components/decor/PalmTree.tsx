import { ribbonPath, type SpinePoint } from '@/lib/svg';
import type { DecorProps } from '@/types/decor';

interface PalmTreeProps extends DecorProps {
  readonly trunkColor: string;
  readonly crownColor: string;
  /** Fronds in the crown. */
  readonly fronds?: number | undefined;
  /** Mirrors the tree, so a grove is not one tree repeated. */
  readonly flip?: boolean | undefined;
}

/** Where the trunk ends and the crown begins. */
const CROWN = { x: 86, y: 98 } as const;

/**
 * A thin, slightly leaning trunk.
 *
 * The key art draws its palms as delicate silhouettes, so this is deliberately
 * spindly: a thicker trunk with a denser crown turns into visual noise at the
 * size these appear.
 */
const TRUNK: readonly SpinePoint[] = [
  [130, 340, 5.2],
  [124, 292, 4.4],
  [115, 242, 3.7],
  [104, 192, 3],
  [94, 146, 2.5],
  [88, 114, 2.1],
  [86, 100, 1.9],
];

/**
 * One drooping crown blade, drawn from the crown outward along +x.
 *
 * Broad rather than hairline: thin blades spread evenly around a point read as
 * a pinwheel, not as a palm.
 */
const BLADE: readonly SpinePoint[] = [
  [0, 0, 3.5],
  [16, -11, 11],
  [35, -12, 10.5],
  [53, -3, 6.5],
  [68, 17, 0],
];

const BLADE_PATH = ribbonPath(BLADE);
const TRUNK_PATH = ribbonPath(TRUNK);

/**
 * A coconut palm: a thin trunk with a small fan of drooping blades. Both are
 * built from the ribbon primitive, so the whole tree is two shapes.
 */
export function PalmTree({
  trunkColor,
  crownColor,
  fronds = 7,
  flip = false,
  className,
  style,
}: PalmTreeProps) {
  // Weighted to the upper half, with the outermost pair drooping: a real crown
  // is not an even circle.
  const angles = Array.from(
    { length: fronds },
    (_, index) => -180 + (index * 252) / Math.max(fronds - 1, 1),
  );

  return (
    <svg
      viewBox="0 0 200 344"
      className={className}
      style={style}
      aria-hidden="true"
      focusable="false"
    >
      <g transform={flip ? 'translate(200 0) scale(-1 1)' : undefined}>
        <path d={TRUNK_PATH} fill={trunkColor} />
        <g fill={crownColor}>
          {angles.map((angle) => {
            // A blade droops clockwise from the direction it points in. On the
            // left half of the crown that would arc *upwards*, so those blades
            // are mirrored — without this every frond curls the same way and
            // the crown reads as a pinwheel.
            const pointsLeft = Math.cos((angle * Math.PI) / 180) < 0;
            return (
              <g
                key={angle}
                transform={`translate(${CROWN.x} ${CROWN.y}) rotate(${angle})${
                  pointsLeft ? ' scale(1 -1)' : ''
                }`}
              >
                <path d={BLADE_PATH} />
              </g>
            );
          })}
          {/* Hides the point every blade radiates from. */}
          <circle cx={CROWN.x} cy={CROWN.y} r="5.5" />
        </g>
        {/* Coconuts, tucked under the crown. */}
        <g fill={trunkColor}>
          <circle cx={CROWN.x - 5} cy={CROWN.y + 8} r="3.4" />
          <circle cx={CROWN.x + 3} cy={CROWN.y + 10} r="3.1" />
          <circle cx={CROWN.x - 1} cy={CROWN.y + 15} r="2.8" />
        </g>
      </g>
    </svg>
  );
}
