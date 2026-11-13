/**
 * Deterministic pseudo-random number generator (Mulberry32).
 *
 * Seeded so decorative procedural artwork renders identically across reloads
 * and machines without calling Math.random().
 */
export function createRandom(seed: number): () => number {
  let s = Math.floor(seed) >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
