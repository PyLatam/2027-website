import type { CSSProperties } from 'react';

/**
 * Props every decorative SVG accepts, so composition and placement stay the
 * parent's concern and the shapes themselves remain position-agnostic.
 *
 * `| undefined` is explicit because the project runs with
 * `exactOptionalPropertyTypes`.
 */
export interface DecorProps {
  readonly className?: string | undefined;
  readonly style?: CSSProperties | undefined;
}
