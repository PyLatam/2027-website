import { useId, useMemo } from 'react';

import { namespaceSvgIds, svgInnerMarkup, svgViewBox } from '@/lib/svg';
import type { DecorProps } from '@/types/decor';

import { DECOR_SHAPES, type DecorShapeName } from './shapes';

interface BrandShapeProps extends DecorProps {
  readonly name: DecorShapeName;
  /**
   * Tint for shapes drawn with `currentColor`. Ignored by the multi-colour
   * shapes, which keep the brand colours they shipped with.
   */
  readonly color?: string | undefined;
}

/**
 * Inlines one of the official decorative SVGs.
 *
 * Inlined rather than referenced with `<img>` so the shape can be tinted, and
 * so the page makes no extra requests. Ids are namespaced per instance, which
 * is what lets the same shape appear more than once without its clip paths
 * fighting each other.
 */
export function BrandShape({ name, color, className, style }: BrandShapeProps) {
  const uid = useId().replace(/:/g, '');
  const markup = DECOR_SHAPES[name];

  const inner = useMemo(
    () => namespaceSvgIds(svgInnerMarkup(markup), uid),
    [markup, uid],
  );

  return (
    <svg
      viewBox={svgViewBox(markup)}
      className={className}
      style={color ? { color, ...style } : style}
      aria-hidden="true"
      focusable="false"
      dangerouslySetInnerHTML={{ __html: inner }}
    />
  );
}
