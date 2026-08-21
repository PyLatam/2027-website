import type { DecorProps } from '@/types/decor';

interface CoralProps extends DecorProps {
  readonly color: string;
  readonly variant?: 'branching' | 'fan' | undefined;
}

/**
 * Reef coral rendered as a stroked skeleton with round caps, which keeps the
 * branches soft at every size and avoids fussy filled outlines.
 */
export function Coral({ color, variant = 'branching', className, style }: CoralProps) {
  const branching = [
    'M50 100 C50 78 46 64 40 52',
    'M40 52 C34 42 30 34 30 22',
    'M40 52 C46 44 54 40 62 34',
    'M50 78 C40 72 32 68 24 62',
    'M24 62 C18 56 16 50 16 40',
    'M50 70 C60 64 68 60 74 52',
    'M74 52 C80 46 84 40 84 30',
    'M62 34 C66 28 68 22 68 14',
    'M30 22 C28 16 28 10 30 4',
    'M84 30 C86 24 86 18 84 12',
    'M16 40 C14 34 14 28 16 22',
    'M68 14 C70 10 72 8 76 6',
  ];

  const fan = [
    'M50 100 C50 82 50 70 50 58',
    'M50 58 C38 50 30 40 26 26',
    'M50 58 C62 50 70 40 74 26',
    'M50 58 C48 42 44 30 38 16',
    'M50 58 C52 42 56 30 62 16',
    'M50 58 C50 40 50 26 50 10',
  ];

  const paths = variant === 'fan' ? fan : branching;

  return (
    <svg
      viewBox="0 0 100 100"
      className={className}
      style={style}
      aria-hidden="true"
      focusable="false"
    >
      <g
        fill="none"
        stroke={color}
        strokeWidth="6"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        {paths.map((d) => (
          <path key={d} d={d} />
        ))}
      </g>
    </svg>
  );
}
