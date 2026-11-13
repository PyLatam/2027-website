export type SpinePoint =
  | readonly [x: number, y: number, radius: number]
  | [x: number, y: number, radius: number];

interface Point2D {
  readonly x: number;
  readonly y: number;
}

/**
 * Formats a number to 2 decimal places max for compact SVG path output.
 */
function f(n: number): string {
  return Number(n.toFixed(2)).toString();
}

/**
 * Builds a smooth Catmull-Rom cubic Bezier path through a list of points.
 */
function smoothPath(points: readonly Point2D[], isClosed: boolean): string {
  if (points.length === 0) return '';
  if (points.length === 1) return `M ${f(points[0]!.x)} ${f(points[0]!.y)}`;
  if (points.length === 2) {
    return `M ${f(points[0]!.x)} ${f(points[0]!.y)} L ${f(points[1]!.x)} ${f(points[1]!.y)}`;
  }

  const n = points.length;
  let d = `M ${f(points[0]!.x)} ${f(points[0]!.y)}`;

  for (let i = 0; i < (isClosed ? n : n - 1); i++) {
    const p0 = points[(i - 1 + n) % n]!;
    const p1 = points[i % n]!;
    const p2 = points[(i + 1) % n]!;
    const p3 = points[(i + 2) % n]!;

    const cp1x = p1.x + (p2.x - p0.x) / 6;
    const cp1y = p1.y + (p2.y - p0.y) / 6;
    const cp2x = p2.x - (p3.x - p1.x) / 6;
    const cp2y = p2.y - (p3.y - p1.y) / 6;

    d += ` C ${f(cp1x)} ${f(cp1y)}, ${f(cp2x)} ${f(cp2y)}, ${f(p2.x)} ${f(p2.y)}`;
  }

  return d;
}

/**
 * Produces a tapered, variable-width band from an array of spine points.
 *
 * Each point is [x, y, radius]. Normals along the spine are offset by radius
 * to generate left and right edges, forming a closed shape.
 */
export function ribbonPath(spine: readonly SpinePoint[]): string {
  if (spine.length < 2) return '';

  const leftPoints: Point2D[] = [];
  const rightPoints: Point2D[] = [];

  for (let i = 0; i < spine.length; i++) {
    const [x, y, r] = spine[i]!;

    let dx: number;
    let dy: number;

    if (i === 0) {
      const [nextX, nextY] = spine[1]!;
      dx = nextX - x;
      dy = nextY - y;
    } else if (i === spine.length - 1) {
      const [prevX, prevY] = spine[i - 1]!;
      dx = x - prevX;
      dy = y - prevY;
    } else {
      const [prevX, prevY] = spine[i - 1]!;
      const [nextX, nextY] = spine[i + 1]!;
      dx = nextX - prevX;
      dy = nextY - prevY;
    }

    const len = Math.hypot(dx, dy) || 1;
    // Unit normal rotated 90 degrees CCW (-dy, dx)
    const nx = -dy / len;
    const ny = dx / len;

    leftPoints.push({
      x: x + nx * r,
      y: y + ny * r,
    });

    rightPoints.push({
      x: x - nx * r,
      y: y - ny * r,
    });
  }

  // Chain left edge forwards and right edge backwards to form a closed loop
  const loop: Point2D[] = [...leftPoints, ...rightPoints.reverse()];
  return `${smoothPath(loop, true)} Z`;
}
