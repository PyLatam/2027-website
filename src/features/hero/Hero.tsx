import { BrandMark } from '@/components/decor';
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
          <span className={`${styles.eyebrow} ${styles.reveal}`} aria-hidden="true">
            {t('hero.eyebrow')}
          </span>
          <span className={`${styles.lead} ${styles.reveal}`} aria-hidden="true">
            {t('hero.lead')}
          </span>
          <span className={`${styles.city} ${styles.reveal}`} aria-hidden="true">
            {t('hero.city')}
          </span>
          <span className={`${styles.country} ${styles.reveal}`} aria-hidden="true">
            {t('hero.country')}
          </span>
        </h1>
      </div>
    </section>
  );
}
