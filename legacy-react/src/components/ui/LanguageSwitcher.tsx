import { cx } from '@/lib/cx';
import { LOCALES, LOCALE_LABELS, type Locale } from '@/i18n/locales';
import { useTranslation } from '@/i18n/useTranslation';
import type { MessageKey } from '@/i18n/dictionary';

import styles from './LanguageSwitcher.module.css';

const SHORT_LABEL_KEY: Record<Locale, MessageKey> = {
  es: 'lang.short.es',
  en: 'lang.short.en',
};

interface LanguageSwitcherProps {
  readonly className?: string | undefined;
}

/**
 * A two-state toggle rather than a select: with exactly two languages, both
 * options stay visible and reachable in a single tap.
 */
export function LanguageSwitcher({ className }: LanguageSwitcherProps) {
  const { locale, setLocale, t } = useTranslation();

  return (
    <div
      className={cx(styles.switcher, className)}
      role="group"
      aria-label={t('lang.legend')}
    >
      {LOCALES.map((option) => (
        <button
          key={option}
          type="button"
          lang={option}
          className={styles.option}
          aria-pressed={locale === option}
          aria-label={t('lang.switchTo', { language: LOCALE_LABELS[option] })}
          onClick={() => setLocale(option)}
        >
          {t(SHORT_LABEL_KEY[option])}
        </button>
      ))}
    </div>
  );
}
