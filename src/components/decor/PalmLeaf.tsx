import { useId } from 'react';

import type { DecorProps } from '@/types/decor';

interface PalmLeafProps extends DecorProps {
  /** Solid color, or a two-stop gradient when `colorTo` is provided. */
  readonly color: string;
  readonly colorTo?: string | undefined;
  /** Number of leaflets on each side of the rachis. */
  readonly leaflets?: number | undefined;
}

/** Quadratic Bezier point for the rachis (the frond's central stem). */
function stemPoint(t: number): readonly [number, number] {
  const p0 = [8, 94] as const;
  const c = [26, 58] as const;
  const p1 = [94, 8] as const;
  const inv = 1 - t;
  return [
    inv * inv * p0[0] + 2 * inv * t * c[0] + t * t * p1[0],
    inv * inv * p0[1] + 2 * inv * t * c[1] + t * t * p1[1],
  ];
}

/** An asymmetric lens shape: organic enough to read as a leaflet. */
function leafletPath(
  base: readonly [number, number],
  tip: readonly [number, number],
  width: number,
): string {
  const [bx, by] = base;
  const [tx, ty] = tip;
  const dx = tx - bx;
  const dy = ty - by;
  const length = Math.hypot(dx, dy) || 1;
  const nx = -dy / length;
  const ny = dx / length;

  const belly = 0.38;
  const c1x = bx + dx * belly + nx * width;
  const c1y = by + dy * belly + ny * width;
  const c2x = bx + dx * belly - nx * width * 0.5;
  const c2y = by + dy * belly - ny * width * 0.5;

  return `M${bx.toFixed(2)} ${by.toFixed(2)} Q${c1x.toFixed(2)} ${c1y.toFixed(2)} ${tx.toFixed(2)} ${ty.toFixed(2)} Q${c2x.toFixed(2)} ${c2y.toFixed(2)} ${bx.toFixed(2)} ${by.toFixed(2)}`;
}

/**
 * A tropical palm frond, generated rather than hand-drawn so the silhouette
 * stays smooth at any size and the density can be tuned with one prop.
 */
export function PalmLeaf({
  color,
  colorTo,
  leaflets = 12,
  className,
  style,
}: PalmLeafProps) {
  const gradientId = useId();
  const fill = colorTo ? `url(#${gradientId})` : color;

  const fronds: string[] = [];

  for (let i = 0; i < leaflets; i += 1) {
    const t = (i + 0.6) / leaflets;
    const base = stemPoint(t);
    const ahead = stemPoint(Math.min(t + 0.04, 1));
    const dirX = ahead[0] - base[0];
    const dirY = ahead[1] - base[1];
    const norm = Math.hypot(dirX, dirY) || 1;

    // Leaflets are longest mid-frond and sweep backwards toward the base.
    const length = 34 * Math.sin(Math.PI * (0.18 + 0.82 * t)) ** 0.75;
    const sweep = 0.85;

    for (const side of [1, -1] as const) {
      const ux = dirX / norm;
      const uy = dirY / norm;
      const px = -uy * side;
      const py = ux * side;
      const tip = [
        base[0] + (px * sweep + ux * -0.42) * length,
        base[1] + (py * sweep + uy * -0.42) * length,
      ] as const;
      fronds.push(leafletPath(base, tip, length * 0.2 * side));
    }
  }

  const tip = stemPoint(1);
  const preTip = stemPoint(0.94);

  return (
    <svg
      viewBox="0 0 100 100"
      className={className}
      style={style}
      aria-hidden="true"
      focusable="false"
    >
      {colorTo && (
        <defs>
          <linearGradient id={gradientId} x1="0" y1="1" x2="1" y2="0">
            <stop offset="0%" stopColor={color} />
            <stop offset="100%" stopColor={colorTo} />
          </linearGradient>
        </defs>
      )}
      <g fill={fill}>
        {fronds.map((d) => (
          <path key={d} d={d} />
        ))}
        <path d={leafletPath(preTip, [tip[0] + 6, tip[1] - 8], 2.6)} />
      </g>
      <path
        d={`M${stemPoint(0)[0]} ${stemPoint(0)[1]} Q26 58 ${tip[0]} ${tip[1]}`}
        fill="none"
        stroke={fill}
        strokeWidth="2.2"
        strokeLinecap="round"
      />
    </svg>
  );
}
