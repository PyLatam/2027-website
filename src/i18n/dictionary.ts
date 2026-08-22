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
    'PyCon Latam 2027 nos lleva a Punta Cana, República Dominicana del 26 al 29 de agosto de 2027. La conferencia de la comunidad Python de Latinoamérica.',

  'hero.eyebrow': 'PyCon Latam 2027',
  'hero.lead': 'Nos vemos en',
  'hero.city': 'Punta Cana,',
  'hero.country': 'República Dominicana',
  'hero.dates': '26 – 29 de agosto, 2027',
  'hero.aria':
    'PyCon Latam 2027. Nos vemos en Punta Cana, República Dominicana del 26 al 29 de agosto de 2027.',

  'venue.country': 'República Dominicana',

  'logo.alt': 'Logotipo de PyCon Latam RD, Punta Cana',

  'lang.legend': 'Idioma',
  'lang.switchTo': 'Cambiar idioma a {language}',
  'lang.short.es': 'ES',
  'lang.short.en': 'EN',

  'skip.toContent': 'Saltar al contenido',

  'footer.rights': 'Todos los derechos reservados.',
  'social.x': 'X (Twitter) de PyCon Latam',
  'social.instagram': 'Instagram de PyCon Latam',
  'social.linkedin': 'LinkedIn de PyCon Latam',
  'social.facebook': 'Facebook de PyCon Latam',
} as const;

export type MessageKey = keyof typeof es;
export type Messages = Record<MessageKey, string>;

const en: Messages = {
  'meta.title': 'PyCon Latam 2027 — Punta Cana, Dominican Republic',
  'meta.description':
    'PyCon Latam 2027 takes us to Punta Cana, Dominican Republic from August 26 to 29, 2027. The conference of the Latin American Python community.',

  'hero.eyebrow': 'PyCon Latam 2027',
  'hero.lead': 'See you in',
  'hero.city': 'Punta Cana,',
  'hero.country': 'Dominican Republic',
  'hero.dates': 'August 26 – 29, 2027',
  'hero.aria':
    'PyCon Latam 2027. See you in Punta Cana, Dominican Republic from August 26 to 29, 2027.',

  'venue.country': 'Dominican Republic',

  'logo.alt': 'PyCon Latam RD logo, Punta Cana',

  'lang.legend': 'Language',
  'lang.switchTo': 'Switch language to {language}',
  'lang.short.es': 'ES',
  'lang.short.en': 'EN',

  'skip.toContent': 'Skip to content',

  'footer.rights': 'All rights reserved.',
  'social.x': 'PyCon Latam on X (Twitter)',
  'social.instagram': 'PyCon Latam on Instagram',
  'social.linkedin': 'PyCon Latam on LinkedIn',
  'social.facebook': 'PyCon Latam on Facebook',
};

export const DICTIONARIES: Record<Locale, Messages> = { es, en };

/** Replaces `{placeholder}` tokens with the given values. */
export function interpolate(
  template: string,
  values: Readonly<Record<string, string>> = {},
): string {
  return template.replace(/\{(\w+)\}/g, (match, key: string) => values[key] ?? match);
}
