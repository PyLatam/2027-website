import { useId } from 'react';

import { canopyBlobs } from '@/lib/svg';
import type { DecorProps } from '@/types/decor';

interface SandCoveProps extends Pick<DecorProps, 'className'> {
  readonly seed?: number | undefined;
}

/**
 * The beach in the bottom-right corner.
 *
 * Two different geometries are at work here, and mixing them up is what makes
 * a beach look wrong:
 *
 * - `EDGE` is the *local* waterline. The foam follows it.
 * - The golden sand and the jungle behind it are **horizontal** bands. They are
 *   the far shore, so they run with the horizon, not with the local waterline.
 *
 * Everything is clipped to the sand, so no dune and no crown can ever end up
 * floating on the water.
 *
 * `preserveAspectRatio="none"` on purpose: these are abstract curves, and
 * stretching them keeps the whole viewBox visible at every aspect ratio, so
 * placement inside it stays predictable.
 */
const EDGE = 'M266 -14 C252 56 214 112 158 162 C114 202 66 240 14 272';

const SAND = `${EDGE} L440 280 L440 -20 Z`;

/**
 * The far shore, as two horizontal bands. Each fills *downwards* from a softly
 * waving edge, so the jungle above it stays visible against the sky instead of
 * being buried under a slab of sand.
 */
const DUNE = 'M-20 138 C60 126 130 134 210 126 C290 118 350 126 440 120 V280 H-20 Z';
const FORESHORE = 'M-20 186 C60 176 130 184 210 176 C290 168 350 176 440 170 V280 H-20 Z';

/** A pale hill far behind the treeline, for one more plane of depth. */
const FAR_HILL = 'M-20 142 C40 122 96 110 152 116 C204 122 244 134 276 150 V190 H-20 Z';

export function SandCove({ seed = 21, className }: SandCoveProps) {
  const uid = useId();
  const sandClip = `${uid}-sand`;
  const beachClip = `${uid}-beach`;
  const goldFill = `${uid}-gold`;
  const creamFill = `${uid}-cream`;

  // Many small crowns, not a few big ones: the key art's treeline is a
  // scalloped edge, and large discs read as a mountain instead.
  const back = canopyBlobs({
    seed,
    count: 28,
    from: [72, 134],
    to: [462, 82],
    minRadius: 10,
    maxRadius: 26,
    scatter: 26,
  });
  const front = canopyBlobs({
    seed: seed + 101,
    count: 26,
    from: [166, 126],
    to: [462, 66],
    minRadius: 9,
    maxRadius: 24,
    scatter: 22,
  });

  return (
    <svg
      viewBox="0 0 420 270"
      className={className}
      preserveAspectRatio="none"
      aria-hidden="true"
      focusable="false"
    >
      <defs>
        <clipPath id={sandClip}>
          <path d={SAND} />
        </clipPath>
        {/*
          Everything below the dune's edge. The waterline runs the full height
          of the viewBox, but only its lower stretch is actually a beach — the
          rest is behind the jungle, and a foam line drawn up there floats in
          the sky.
        */}
        <clipPath id={beachClip}>
          <path d={DUNE} />
        </clipPath>
        {/*
          Each sand band fades into the next instead of butting against it with
          a hard line — that edge is what made the golden shore read as a strip
          of tape rather than as sand. `userSpaceOnUse` because the paths run
          past the bottom of the viewBox, which makes bounding-box units useless.
        */}
        <linearGradient
          id={goldFill}
          gradientUnits="userSpaceOnUse"
          x1="0"
          y1="120"
          x2="0"
          y2="200"
        >
          <stop offset="0%" stopColor="var(--c-sand-400)" />
          <stop offset="100%" stopColor="var(--c-sand-300)" />
        </linearGradient>
        <linearGradient
          id={creamFill}
          gradientUnits="userSpaceOnUse"
          x1="0"
          y1="168"
          x2="0"
          y2="272"
        >
          <stop offset="0%" stopColor="var(--c-sand-200)" />
          <stop offset="100%" stopColor="var(--c-sand-100)" />
        </linearGradient>
      </defs>

      <g clipPath={`url(#${sandClip})`}>
        {/* Jungle first, against the sky... */}
        <path d={FAR_HILL} fill="var(--c-aqua-300)" opacity="0.85" />
        <g fill="var(--c-aqua-400)">
          {back.map((b) => (
            <circle key={`b-${b.cx}-${b.cy}`} cx={b.cx} cy={b.cy} r={b.r} />
          ))}
        </g>
        <g fill="var(--c-jungle-500)">
          {front.map((b) => (
            <circle key={`f-${b.cx}-${b.cy}`} cx={b.cx} cy={b.cy} r={b.r} />
          ))}
        </g>
        {/* ...then the golden far shore over its base, then the near sand. */}
        <path d={DUNE} fill={`url(#${goldFill})`} />
        <path d={FORESHORE} fill={`url(#${creamFill})`} />
      </g>

      {/* Damp sand just above the waterline, then the foam itself. */}
      <g clipPath={`url(#${beachClip})`}>
        <path
          d={EDGE}
          fill="none"
          stroke="var(--c-sand-300)"
          strokeWidth="16"
          strokeLinecap="round"
          opacity="0.45"
          vectorEffect="non-scaling-stroke"
        />
        <path
          d={EDGE}
          fill="none"
          stroke="var(--c-paper)"
          strokeWidth="8"
          strokeLinecap="round"
          vectorEffect="non-scaling-stroke"
        />
      </g>
    </svg>
  );
}
