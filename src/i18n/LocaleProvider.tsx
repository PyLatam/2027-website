import { useCallback, useEffect, useMemo, useState, type ReactNode } from 'react';

import { LocaleContext, type LocaleContextValue } from './LocaleContext';
import { DICTIONARIES, interpolate, type MessageKey } from './dictionary';
import { detectLocale, persistLocale } from './detectLocale';
import { LOCALE_TAGS, type Locale } from './locales';

interface LocaleProviderProps {
  readonly children: ReactNode;
}

/**
 * Owns the active locale: resolves it on first paint, persists the visitor's
 * choice, and keeps the document metadata (`lang`, title, description) in sync
 * so screen readers and crawlers see the same language as the page.
 */
export function LocaleProvider({ children }: LocaleProviderProps) {
  const [locale, setLocaleState] = useState<Locale>(detectLocale);

  const setLocale = useCallback((next: Locale) => {
    setLocaleState(next);
    persistLocale(next);
  }, []);

  const t = useCallback(
    (key: MessageKey, values?: Readonly<Record<string, string>>) =>
      interpolate(DICTIONARIES[locale][key], values),
    [locale],
  );

  useEffect(() => {
    const { documentElement } = document;
    documentElement.lang = LOCALE_TAGS[locale];
    document.title = DICTIONARIES[locale]['meta.title'];

    const description = document.querySelector<HTMLMetaElement>(
      'meta[name="description"]',
    );
    if (description) {
      description.content = DICTIONARIES[locale]['meta.description'];
    }
  }, [locale]);

  const value = useMemo<LocaleContextValue>(
    () => ({ locale, setLocale, t }),
    [locale, setLocale, t],
  );

  return <LocaleContext.Provider value={value}>{children}</LocaleContext.Provider>;
}
