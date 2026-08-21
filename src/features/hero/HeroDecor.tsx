import { CircuitTraces } from '@/components/decor/CircuitTraces';
import { Coral } from '@/components/decor/Coral';
import { PalmLeaf } from '@/components/decor/PalmLeaf';
import { SandCove } from '@/components/decor/SandCove';
import { Shoreline } from '@/components/decor/Shoreline';

import styles from './HeroDecor.module.css';

/**
 * Frames the hero with the key art's motifs, painted back to front:
 * circuit traces, canopy palms, then the surf, the beach, and finally the reef
 * that sits in front of the water.
 *
 * Everything here is `aria-hidden` and non-interactive — the message must read
 * identically with images and CSS backgrounds stripped away.
 */
export function HeroDecor() {
  return (
    <div className={styles.layer} aria-hidden="true">
      {/* --- background texture --- */}
      <CircuitTraces className={`${styles.traces} ${styles.tracesTopLeft}`} />
      <CircuitTraces className={`${styles.traces} ${styles.tracesRight}`} />

      {/* --- canopy --- */}
      <PalmLeaf
        color="var(--c-aqua-500)"
        colorTo="var(--c-ocean-400)"
        className={`${styles.item} ${styles.leafTopLeft} ${styles.float}`}
      />
      <PalmLeaf
        color="var(--c-sun-500)"
        colorTo="var(--c-coral-500)"
        leaflets={10}
        className={`${styles.item} ${styles.leafTopLeftAccent} ${styles.floatSlow}`}
      />
      <PalmLeaf
        color="var(--c-aqua-500)"
        colorTo="var(--c-ocean-500)"
        className={`${styles.item} ${styles.leafTopRight} ${styles.floatSlow}`}
      />
      <PalmLeaf
        color="var(--c-sun-400)"
        colorTo="var(--c-sun-500)"
        leaflets={10}
        className={`${styles.item} ${styles.leafTopRightAccent} ${styles.float}`}
      />

      {/* --- shore --- */}
      <Shoreline className={styles.shoreline} />
      <SandCove className={styles.sand} />

      {/* --- reef, in front of the water --- */}
      <Coral
        color="var(--c-coral-500)"
        className={`${styles.item} ${styles.coralLeft}`}
      />
      <Coral
        color="var(--c-aqua-500)"
        variant="fan"
        className={`${styles.item} ${styles.coralLeftFan}`}
      />
      <Coral
        color="var(--c-coral-300)"
        className={`${styles.item} ${styles.coralRight}`}
      />
      <PalmLeaf
        color="var(--c-aqua-600)"
        colorTo="var(--c-aqua-300)"
        className={`${styles.item} ${styles.leafBottomRight} ${styles.float}`}
      />
      <PalmLeaf
        color="var(--c-coral-500)"
        colorTo="var(--c-coral-300)"
        leaflets={9}
        className={`${styles.item} ${styles.leafBottomRightAccent} ${styles.floatSlow}`}
      />
    </div>
  );
}
