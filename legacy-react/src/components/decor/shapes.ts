import coralBranch from '@/assets/decor/coral-branch.svg?raw';
import coralFan from '@/assets/decor/coral-fan.svg?raw';
import coralStaghorn from '@/assets/decor/coral-staghorn.svg?raw';
import dotCluster from '@/assets/decor/dot-cluster.svg?raw';
import leafFrond01 from '@/assets/decor/leaf-frond-01.svg?raw';
import leafFrond02 from '@/assets/decor/leaf-frond-02.svg?raw';
import leafFrondTrio from '@/assets/decor/leaf-frond-trio.svg?raw';
import seaRock from '@/assets/decor/sea-rock.svg?raw';

/**
 * The official decorative artwork, delivered by the design team and normalised
 * into `src/assets/decor/`.
 *
 * Single-colour shapes were rewritten to `fill="currentColor"`, so they are
 * tinted with the CSS `color` property. Multi-colour shapes keep the brand
 * colours they shipped with.
 *
 * To add a shape: drop the file in `src/assets/decor/` and add it here. Never
 * redraw one of these by hand.
 */
export const DECOR_SHAPES = {
  'coral-branch': coralBranch,
  'coral-fan': coralFan,
  'coral-staghorn': coralStaghorn,
  'dot-cluster': dotCluster,
  'leaf-frond-01': leafFrond01,
  'leaf-frond-02': leafFrond02,
  'leaf-frond-trio': leafFrondTrio,
  'sea-rock': seaRock,
} as const;

export type DecorShapeName = keyof typeof DECOR_SHAPES;

/**
 * `sea-rock` is kept in the catalogue but the scene draws its own `SeaRock`:
 * the supplied artwork is cut for larger placements than the hero gives it.
 */
