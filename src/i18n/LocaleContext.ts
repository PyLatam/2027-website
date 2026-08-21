import { createContext } from 'react';
import type { Locale } from './locales';
import type { MessageKey } from './dictionary';

export interface LocaleContextValue {
  readonly locale: Locale;
  readonly setLocale: (next: Locale) => void;
  /** Translates a key, optionally interpolating `{placeholder}` tokens. */
  readonly t: (key: MessageKey, values?: Readonly<Record<string, string>>) => string;
}

export const LocaleContext = createContext<LocaleContextValue | null>(null);
