import { createRandom } from './random';

export interface CanopyBlobsOptions {
  readonly seed: number;
  readonly count: number;
  readonly from: readonly [number, number];
  readonly to: readonly [number, number];
  readonly minRadius: number;
  readonly maxRadius: number;
  readonly scatter: number;
}

export interface CanopyBlob {
  readonly cx: number;
  readonly cy: number;
  readonly r: number;
}

/**
 * Produces an array of overlapping circles along a line with seeded scatter.
 */
export function canopyBlobs({
  seed,
  count,
  from,
  to,
  minRadius,
  maxRadius,
  scatter,
}: CanopyBlobsOptions): CanopyBlob[] {
  const rand = createRandom(seed);
  const blobs: CanopyBlob[] = [];
  const [x1, y1] = from;
  const [x2, y2] = to;
  const dx = x2 - x1;
  const dy = y2 - y1;
  const len = Math.hypot(dx, dy) || 1;
  const nx = -dy / len;
  const ny = dx / len;

  for (let i = 0; i < count; i++) {
    const t = count > 1 ? i / (count - 1) : 0.5;
    const baseX = x1 + dx * t;
    const baseY = y1 + dy * t;
    const offsetNormal = (rand() - 0.5) * 2 * scatter;
    const offsetTangent = (rand() - 0.5) * (len / Math.max(count, 1));
    const cx = Math.round((baseX + nx * offsetNormal + (dx / len) * offsetTangent) * 10) / 10;
    const cy = Math.round((baseY + ny * offsetNormal + (dy / len) * offsetTangent) * 10) / 10;
    const r = Math.round((minRadius + rand() * (maxRadius - minRadius)) * 10) / 10;
    blobs.push({ cx, cy, r });
  }

  return blobs;
}
