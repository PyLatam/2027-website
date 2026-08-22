import {
  BrandShape,
  CircuitTraces,
  PalmTree,
  SandCove,
  SeaRock,
  Shoreline,
} from '@/components/decor';

import styles from './HeroDecor.module.css';

/**
 * The scene the headline sits in, painted strictly back to front:
 *
 *   circuit traces → canopy → water → beach → reef → foreground planting
 *
 * Composition and placement live here; the shapes themselves know nothing
 * about where they end up. Everything is `aria-hidden` and non-interactive —
 * the message must read identically with every image stripped away.
 */
export function HeroDecor() {
  return (
    <div className={styles.layer} aria-hidden="true">
      {/* --- background texture --- */}
      <CircuitTraces className={`${styles.traces} ${styles.tracesLeft}`} />
      <CircuitTraces className={`${styles.traces} ${styles.tracesLowerLeft}`} />
      <CircuitTraces className={`${styles.traces} ${styles.tracesTopLeft}`} />
      <CircuitTraces className={`${styles.traces} ${styles.tracesRight}`} />

      {/*
        Canopy: fronds hanging from the top edge, all pointing down and clearly
        spaced. The key art never overlaps two large leaves — that reads as a
        mess, not as foliage.
      */}
      <BrandShape
        name="leaf-frond-02"
        color="var(--c-aqua-500)"
        className={`${styles.item} ${styles.leafTopLeft} ${styles.float}`}
      />
      <BrandShape
        name="leaf-frond-02"
        color="var(--c-ocean-500)"
        className={`${styles.item} ${styles.leafTopLeftMid} ${styles.floatSlow}`}
      />
      <BrandShape
        name="leaf-frond-01"
        color="var(--c-tangerine-500)"
        className={`${styles.item} ${styles.leafTopLeftAccent} ${styles.float}`}
      />
      <BrandShape
        name="leaf-frond-02"
        color="var(--c-aqua-500)"
        className={`${styles.item} ${styles.leafTopRight} ${styles.floatSlow}`}
      />

      {/* --- water and beach (the jungle is drawn inside SandCove) --- */}
      <Shoreline className={styles.shoreline} />
      <PalmTree
        trunkColor="var(--c-aqua-600)"
        crownColor="var(--c-aqua-600)"
        className={`${styles.item} ${styles.palmTreeFar} ${styles.floatSlow}`}
      />
      <PalmTree
        trunkColor="var(--c-ocean-400)"
        crownColor="var(--c-ocean-400)"
        fronds={8}
        flip
        className={`${styles.item} ${styles.palmTreeNear} ${styles.float}`}
      />
      <SandCove className={styles.sand} />
      <SeaRock className={`${styles.item} ${styles.rock}`} />

      {/* --- reef, in front of the water --- */}
      <BrandShape
        name="coral-staghorn"
        color="var(--c-aqua-500)"
        className={`${styles.item} ${styles.coralTeal}`}
      />
      <BrandShape
        name="coral-branch"
        color="var(--c-coral-500)"
        className={`${styles.item} ${styles.coralRed}`}
      />
      <BrandShape
        name="coral-fan"
        color="var(--c-aqua-600)"
        className={`${styles.item} ${styles.coralFan}`}
      />

      {/* --- foreground: one leaf, entering from the corner --- */}
      <BrandShape
        name="leaf-frond-01"
        color="var(--c-coral-500)"
        className={`${styles.item} ${styles.featherRight} ${styles.floatSlow}`}
      />
    </div>
  );
}
