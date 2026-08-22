import { EVENT } from '@/content/event';
import { useTranslation } from '@/i18n/useTranslation';

import { IconFacebook, IconInstagram, IconLinkedIn, IconX } from './SocialIcons';
import styles from './Footer.module.css';

interface FooterProps {
  readonly className?: string | undefined;
}

export function Footer({ className }: FooterProps) {
  const { t } = useTranslation();

  const socialLinks = [
    {
      name: t('social.x'),
      href: EVENT.social.x,
      Icon: IconX,
    },
    {
      name: t('social.instagram'),
      href: EVENT.social.instagram,
      Icon: IconInstagram,
    },
    {
      name: t('social.linkedin'),
      href: EVENT.social.linkedin,
      Icon: IconLinkedIn,
    },
    {
      name: t('social.facebook'),
      href: EVENT.social.facebook,
      Icon: IconFacebook,
    },
  ];

  return (
    <footer className={`${styles.footer}${className ? ` ${className}` : ''}`}>
      <div className={styles.inner}>
        <div className={styles.info}>
          <span className={styles.copyright}>
            &copy; {EVENT.year} {EVENT.name}. {t('footer.rights')}
          </span>
          <span className={styles.inclusion}>{t('footer.inclusion')}</span>
        </div>

        <ul className={styles.socialList} aria-label="Social media">
          {socialLinks.map(({ name, href, Icon }) => (
            <li key={href}>
              <a
                href={href}
                className={styles.socialLink}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={name}
                title={name}
              >
                <Icon className={styles.icon} />
              </a>
            </li>
          ))}
        </ul>
      </div>
    </footer>
  );
}
