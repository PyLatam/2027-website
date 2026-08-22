/**
 * Extracts the viewBox value from an SVG document string.
 */
export function svgViewBox(markup: string): string {
  const match = markup.match(/viewBox=["']([^"']+)["']/i);
  return match?.[1] ?? '0 0 100 100';
}

/**
 * Extracts inner SVG markup by stripping the outer <svg> and </svg> tags.
 */
export function svgInnerMarkup(markup: string): string {
  return markup
    .replace(/^<svg[^>]*>/i, '')
    .replace(/<\/svg>\s*$/i, '')
    .trim();
}

/**
 * Namespaces all `id` attributes and their references (`url(#...)`, `href="#..."`,
 * `xlink:href="#..."`) within an SVG markup string with a given unique suffix.
 */
export function namespaceSvgIds(markup: string, uid: string): string {
  const idRegex = /\bid=["']([^"']+)["']/g;
  const ids = new Set<string>();
  let match: RegExpExecArray | null;

  while ((match = idRegex.exec(markup)) !== null) {
    if (match[1]) {
      ids.add(match[1]);
    }
  }

  let result = markup;
  for (const id of ids) {
    const namespaced = `${id}-${uid}`;
    result = result.replace(new RegExp(`\\bid=["']${id}["']`, 'g'), `id="${namespaced}"`);
    result = result.replace(new RegExp(`url\\(#${id}\\)`, 'g'), `url(#${namespaced})`);
    result = result.replace(new RegExp(`(href=["'])#${id}(["'])`, 'g'), `$1#${namespaced}$2`);
  }

  return result;
}
