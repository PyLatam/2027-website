import { useId } from 'react';

import { Coral } from './Coral';
import { PalmLeaf } from './PalmLeaf';

/** Official PSF two-snake mark, upper-left half. */
const SNAKE_TOP =
  'M54.918 0C50.335.02 45.96.4 42.11 1.067c-11.345 2.005-13.405 6.203-13.405 13.943v10.221h26.81v3.407H28.705 18.645c-7.795 0-14.62 4.686-16.756 13.6-2.462 10.22-2.571 16.596 0 27.262 1.908 7.941 6.458 13.6 14.253 13.6h9.217V60.847c0-8.85 7.657-16.657 16.756-16.657h26.778c7.457 0 13.405-6.133 13.405-13.62V15.01c0-7.263-6.128-12.72-13.405-13.943C64.28.298 59.5-.02 54.918 0zM40.421 8.216c2.77 0 5.033 2.3 5.033 5.13 0 2.82-2.264 5.098-5.033 5.098-2.78 0-5.033-2.279-5.033-5.098 0-2.83 2.253-5.13 5.033-5.13z';

/** Official PSF two-snake mark, lower-right half. */
const SNAKE_BOTTOM =
  'M85.83 28.638v14.204c0 9.231-7.826 17.005-16.756 17.005H42.295c-7.337 0-13.404 6.278-13.404 13.62v25.53c0 7.263 6.316 11.535 13.404 13.619 8.487 2.494 16.626 2.946 26.778 0 6.75-1.954 13.405-5.888 13.405-13.62V88.775h-26.78v-3.407h26.78 13.404c7.795 0 10.7-5.436 13.405-13.6 2.794-8.405 2.675-16.488 0-27.262-1.922-7.76-5.6-13.6-13.405-13.6H85.83zM70.76 93.273c2.78 0 5.033 2.279 5.033 5.098 0 2.83-2.253 5.13-5.033 5.13-2.77 0-5.032-2.3-5.032-5.13 0-2.82 2.263-5.098 5.032-5.098z';

/** Sea-current lines carved into the ocean snake. */
const CURRENTS = [
  'M4 34 C16 28 24 40 36 34 C46 29 54 36 66 31',
  'M2 46 C14 40 22 52 34 46 C44 41 52 48 64 43',
  'M6 58 C16 53 24 63 34 58',
  'M24 14 C34 9 42 17 54 12',
];

interface PythonEmblemProps {
  readonly title: string;
  readonly className?: string | undefined;
}

/**
 * The Python mark reimagined as reef and shoreline: the upper snake becomes
 * Caribbean water, the lower one a sunlit sandbank full of coral and palms.
 *
 * The mark's eyes are cut out with `evenodd`, so the page background shows
 * through them exactly as it does in the key art.
 */
export function PythonEmblem({ title, className }: PythonEmblemProps) {
  const uid = useId();
  const topClip = `${uid}-top-clip`;
  const bottomClip = `${uid}-bottom-clip`;
  const oceanFill = `${uid}-ocean`;
  const sandFill = `${uid}-sand`;

  return (
    <svg viewBox="-4 -4 119 119" className={className} role="img" aria-label={title}>
      <defs>
        <linearGradient id={oceanFill} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="var(--c-ocean-400)" />
          <stop offset="55%" stopColor="var(--c-ocean-500)" />
          <stop offset="100%" stopColor="var(--c-ocean-600)" />
        </linearGradient>
        <linearGradient id={sandFill} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="var(--c-sun-300)" />
          <stop offset="55%" stopColor="var(--c-sun-400)" />
          <stop offset="100%" stopColor="var(--c-sun-500)" />
        </linearGradient>

        <clipPath id={topClip}>
          <path d={SNAKE_TOP} clipRule="evenodd" />
        </clipPath>
        <clipPath id={bottomClip}>
          <path d={SNAKE_BOTTOM} clipRule="evenodd" />
        </clipPath>
      </defs>

      {/* Ocean half */}
      <path d={SNAKE_TOP} fill={`url(#${oceanFill})`} fillRule="evenodd" />
      <g clipPath={`url(#${topClip})`}>
        <g
          fill="none"
          stroke="var(--c-foam-100)"
          strokeWidth="2.6"
          strokeLinecap="round"
          opacity="0.9"
        >
          {CURRENTS.map((d) => (
            <path key={d} d={d} />
          ))}
        </g>
      </g>

      {/* Sandbank half */}
      <path d={SNAKE_BOTTOM} fill={`url(#${sandFill})`} fillRule="evenodd" />
      <g clipPath={`url(#${bottomClip})`}>
        <svg x="30" y="58" width="30" height="30" viewBox="0 0 100 100">
          <Coral color="var(--c-coral-500)" />
        </svg>
        <svg x="62" y="82" width="26" height="26" viewBox="0 0 100 100">
          <Coral color="var(--c-coral-300)" variant="fan" />
        </svg>
        <svg x="58" y="34" width="30" height="30" viewBox="0 0 100 100">
          <PalmLeaf color="var(--c-aqua-500)" colorTo="var(--c-aqua-300)" leaflets={9} />
        </svg>
        <svg x="40" y="66" width="26" height="26" viewBox="0 0 100 100">
          <PalmLeaf color="var(--c-aqua-600)" leaflets={8} />
        </svg>
        <svg x="66" y="72" width="24" height="24" viewBox="0 0 100 100">
          <PalmLeaf color="var(--c-ocean-400)" leaflets={8} />
        </svg>
      </g>
    </svg>
  );
}
