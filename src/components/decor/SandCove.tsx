import type { DecorProps } from '@/types/decor';

type SandCoveProps = Pick<DecorProps, 'className'>;

/**
 * The sunlit beach that closes the bottom-right corner of the key art:
 * a sand mass, its wet-sand edge, and the foam line where the surf meets it.
 */
export function SandCove({ className }: SandCoveProps) {
  return (
    <svg
      viewBox="0 0 320 220"
      className={className}
      preserveAspectRatio="xMaxYMax slice"
      aria-hidden="true"
      focusable="false"
    >
      <path
        d="M320 40 C246 58 196 92 158 132 C128 164 104 192 74 220 H320 Z"
        fill="var(--c-sand-200)"
      />
      <path
        d="M320 76 C258 92 214 122 182 156 C160 180 140 200 118 220 H320 Z"
        fill="var(--c-sand-300)"
      />
      <path
        d="M320 40 C246 58 196 92 158 132 C128 164 104 192 74 220"
        fill="none"
        stroke="var(--c-paper)"
        strokeWidth="6"
        strokeLinecap="round"
        opacity="0.85"
      />
      <path
        d="M320 58 C252 74 206 106 172 142 C146 170 124 196 100 220"
        fill="none"
        stroke="var(--c-foam-200)"
        strokeWidth="3"
        strokeLinecap="round"
      />
    </svg>
  );
}
