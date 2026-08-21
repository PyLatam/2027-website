import type { Locale } from './locales';

/**
 * All user-facing copy. Keys are flat and namespaced with dots.
 *
 * `Messages` is derived from the Spanish dictionary, so adding a key to `es`
 * makes TypeScript require it in `en` too — translations can never drift.
 */
const es = {
  'meta.title': 'PyCon Latam 2027 — Punta Cana, República Dominicana',
  'meta.description':
    'PyCon Latam 2027 nos lleva a Punta Cana, República Dominicana. La conferencia de la comunidad Python de Latinoamérica.',

  'hero.eyebrow': 'PyCon Latam 2027',
  'hero.lead': 'Nos vemos en',
  'hero.city': 'Punta Cana,',
  'hero.country': 'República Dominicana',
  'hero.aria': 'PyCon Latam 2027. Nos vemos en Punta Cana, República Dominicana.',

  'venue.country': 'República Dominicana',

  'logo.alt': 'Logo de Python en versión tropical caribeña',

  'lang.legend': 'Idioma',
  'lang.switchTo': 'Cambiar idioma a {language}',
  'lang.short.es': 'ES',
  'lang.short.en': 'EN',

  'skip.toContent': 'Saltar al contenido',
} as const;

export type MessageKey = keyof typeof es;
export type Messages = Record<MessageKey, string>;

const en: Messages = {
  'meta.title': 'PyCon Latam 2027 — Punta Cana, Dominican Republic',
  'meta.description':
    'PyCon Latam 2027 takes us to Punta Cana, Dominican Republic. The conference of the Latin American Python community.',

  'hero.eyebrow': 'PyCon Latam 2027',
  'hero.lead': 'See you in',
  'hero.city': 'Punta Cana,',
  'hero.country': 'Dominican Republic',
  'hero.aria': 'PyCon Latam 2027. See you in Punta Cana, Dominican Republic.',

  'venue.country': 'Dominican Republic',

  'logo.alt': 'Python logo in a tropical Caribbean treatment',

  'lang.legend': 'Language',
  'lang.switchTo': 'Switch language to {language}',
  'lang.short.es': 'ES',
  'lang.short.en': 'EN',

  'skip.toContent': 'Skip to content',
};

export const DICTIONARIES: Record<Locale, Messages> = { es, en };

/** Replaces `{placeholder}` tokens with the given values. */
export function interpolate(
  template: string,
  values: Readonly<Record<string, string>> = {},
): string {
  return template.replace(/\{(\w+)\}/g, (match, key: string) => values[key] ?? match);
}
