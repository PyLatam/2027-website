import { Footer } from '@/components/ui/Footer';
import { LanguageSwitcher } from '@/components/ui/LanguageSwitcher';
import { Hero } from '@/features/hero/Hero';
import { useTranslation } from '@/i18n/useTranslation';

import styles from './App.module.css';

export function App() {
  const { t } = useTranslation();

  return (
    <div className={styles.shell}>
      <a className={styles.skipLink} href="#content">
        {t('skip.toContent')}
      </a>
      <LanguageSwitcher className={styles.toolbar} />
      <main>
        <Hero />
      </main>
      <Footer />
    </div>
  );
}
