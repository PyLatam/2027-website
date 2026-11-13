import { useId, useMemo } from 'react';

import markup from '@/assets/pycon-latam-rd-mark.svg?raw';
import { namespaceSvgIds, svgInnerMarkup, svgViewBox } from '@/lib/svg';

interface BrandMarkProps {
  /** Accessible name. Comes from the dictionary, never hardcoded. */
  readonly title: string;
  readonly className?: string | undefined;
}

const VIEW_BOX = svgViewBox(markup);
const INNER = svgInnerMarkup(markup);

/**
 * The official PyCon Latam RD mark, inlined verbatim from the designer's
 * export in `src/assets/`.
 *
 * It is deliberately **not** redrawn or re-coloured here: to update the logo,
 * replace that file. Its ids are namespaced at render time (see
 * `namespaceSvgIds`) because the export ships generic ids like `clip-path`.
 */
export function BrandMark({ title, className }: BrandMarkProps) {
  const uid = useId().replace(/:/g, '');
  const inner = useMemo(() => namespaceSvgIds(INNER, uid), [uid]);

  return (
    <svg
      viewBox={VIEW_BOX}
      className={className}
      role="img"
      aria-label={title}
      dangerouslySetInnerHTML={{ __html: inner }}
    />
  );
}
