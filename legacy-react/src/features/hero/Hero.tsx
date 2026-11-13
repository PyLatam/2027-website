import { BrandMark } from '@/components/decor';
import { cx } from '@/lib/cx';
import { useTranslation } from '@/i18n/useTranslation';

import { HeroDecor } from './HeroDecor';
import styles from './Hero.module.css';

/**
 * The whole announcement, in one screen.
 *
 * The four typographic lines are a single `<h1>`: assistive technology reads
 * one sentence (`hero.aria`) while sighted visitors get the poster's four-beat
 * rhythm. Adding lines here means adding keys to the dictionary, never literals.
 */
export function Hero() {
  const { t } = useTranslation();

  return (
    <section className={styles.hero} id="content">
      <HeroDecor />

      <div className={styles.inner}>
        <BrandMark title={t('logo.alt')} className={styles.emblem} />

        <h1 className={styles.copy}>
          <span className="visually-hidden">{t('hero.aria')}</span>
          <span className={cx(styles.eyebrow, styles.reveal)} aria-hidden="true">
            {t('hero.eyebrow')}
          </span>
          <span className={cx(styles.lead, styles.reveal)} aria-hidden="true">
            {t('hero.lead')}
          </span>
          <span className={cx(styles.city, styles.reveal)} aria-hidden="true">
            {t('hero.city')}
          </span>
          <span className={cx(styles.country, styles.reveal)} aria-hidden="true">
            {t('hero.country')}
          </span>
          <span className={cx(styles.dates, styles.reveal)} aria-hidden="true">
            {t('hero.dates')}
          </span>
        </h1>
      </div>
    </section>
  );
}
