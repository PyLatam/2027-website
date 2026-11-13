import { DEFAULT_LOCALE, isLocale, type Locale } from './locales';

export const LOCALE_STORAGE_KEY = 'pyconlatam.locale';

function fromQueryString(search: string): Locale | null {
  const value = new URLSearchParams(search).get('lang');
  return isLocale(value) ? value : null;
}

function fromStorage(): Locale | null {
  try {
    const value = window.localStorage.getItem(LOCALE_STORAGE_KEY);
    return isLocale(value) ? value : null;
  } catch {
    // Private browsing or blocked site data: fall through to the next source.
    return null;
  }
}

function fromNavigator(languages: readonly string[]): Locale | null {
  for (const language of languages) {
    const base = language.split('-')[0]?.toLowerCase();
    if (isLocale(base)) return base;
  }
  return null;
}

/**
 * Resolution order: explicit `?lang=` link > previous choice > browser
 * preference > Spanish.
 */
export function detectLocale(): Locale {
  if (typeof window === 'undefined') return DEFAULT_LOCALE;

  return (
    fromQueryString(window.location.search) ??
    fromStorage() ??
    fromNavigator([...window.navigator.languages, window.navigator.language]) ??
    DEFAULT_LOCALE
  );
}

export function persistLocale(locale: Locale): void {
  try {
    window.localStorage.setItem(LOCALE_STORAGE_KEY, locale);
  } catch {
    // Persistence is a convenience, never a requirement.
  }
}
