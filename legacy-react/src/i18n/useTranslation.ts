import { useContext } from 'react';
import { LocaleContext, type LocaleContextValue } from './LocaleContext';

export function useTranslation(): LocaleContextValue {
  const context = useContext(LocaleContext);

  if (context === null) {
    throw new Error('useTranslation must be used inside a <LocaleProvider>.');
  }

  return context;
}
