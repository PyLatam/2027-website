/**
 * Joins class names and drops anything falsy.
 *
 * CSS modules hand back one class per rule, so most elements here compose two
 * or three of them. A template literal does the same job right up until one of
 * the values is optional, and then it leaves a stray space or the literal
 * string "undefined" in the DOM.
 */
export function cx(...values: readonly (string | false | null | undefined)[]): string {
  return values.filter(Boolean).join(' ');
}
