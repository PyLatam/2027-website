import { useId } from 'react';

import { canopyBlobs, ribbonPath, type SpinePoint } from '@/lib/svg';
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
 * The SVG keeps its native ratio so the generated canopy crowns remain round.
 */
const EDGE =
  'M266 -14 C254 48 222 101 170 128 C235 108 306 108 330 130 C353 153 297 174 240 195 C190 214 176 235 205 253 C225 266 250 272 282 278';

const SAND = `${EDGE} L440 280 L440 -20 Z`;

/**
 * The far shore, as two horizontal bands. Each fills *downwards* from a softly
 * waving edge, so the jungle above it stays visible against the sky instead of
 * being buried under a slab of sand.
 */
const DUNE = 'M-20 142 C70 134 160 134 250 128 C325 122 382 112 440 116 V280 H-20 Z';
const FORESHORE = 'M-20 180 C80 178 170 174 260 166 C335 158 388 148 440 152 V280 H-20 Z';

/** The pointed peninsula visible beneath the scalloped treeline. */
const LAND_TONGUE = 'M126 150 C210 120 302 92 440 58 V156 H126 Z';

/** Pale tapered ribbons that tighten as they enter the cove. */
const SURF: readonly (readonly SpinePoint[])[] = [
  [
    [0, 153, 0],
    [90, 148, 3],
    [190, 137, 5],
    [270, 134, 6],
    [315, 143, 5],
    [330, 155, 4],
    [302, 174, 6],
    [250, 194, 5],
    [205, 211, 4],
    [180, 229, 2],
    [193, 245, 0],
  ],
  [
    [0, 180, 0],
    [100, 172, 3],
    [205, 157, 5],
    [268, 164, 5],
    [292, 175, 4],
    [266, 193, 5],
    [218, 208, 4],
    [171, 223, 3],
    [148, 240, 2],
    [166, 257, 0],
  ],
  [
    [0, 210, 0],
    [88, 201, 3],
    [176, 181, 5],
    [222, 187, 5],
    [246, 198, 4],
    [226, 212, 5],
    [184, 225, 4],
    [142, 238, 3],
    [121, 253, 2],
    [137, 269, 0],
  ],
] as const;

export function SandCove({ seed = 21, className }: SandCoveProps) {
  const uid = useId();
  const sandClip = `${uid}-sand`;
  const beachClip = `${uid}-beach`;

  // Many small crowns, not a few big ones: the key art's treeline is a
  // scalloped edge, and large discs read as a mountain instead.
  const back = canopyBlobs({
    seed,
    count: 28,
    from: [196, 126],
    to: [462, 26],
    minRadius: 10,
    maxRadius: 26,
    scatter: 22,
  });
  const front = canopyBlobs({
    seed: seed + 101,
    count: 26,
    from: [246, 116],
    to: [462, 6],
    minRadius: 9,
    maxRadius: 24,
    scatter: 20,
  });

  return (
    <svg
      viewBox="0 0 420 270"
      className={className}
      preserveAspectRatio="xMaxYMax meet"
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
      </defs>

      {/* The cove's nested surf is painted below the land. */}
      <g data-surf fill="var(--c-foam-100)">
        {SURF.map((spine) => {
          const d = ribbonPath(spine);
          return <path key={d} d={d} />;
        })}
      </g>

      <g clipPath={`url(#${sandClip})`}>
        {/* Jungle first, against the sky... */}
        <path d={LAND_TONGUE} fill="var(--c-jungle-500)" />
        <g fill="var(--c-aqua-400)">
          {back.map((b) => (
            <circle key={`b-${b.cx}-${b.cy}`} cx={b.cx} cy={b.cy} r={b.r} />
          ))}
        </g>
        <g fill="var(--c-aqua-500)">
          {front.map((b) => (
            <circle key={`f-${b.cx}-${b.cy}`} cx={b.cx} cy={b.cy} r={b.r} />
          ))}
        </g>
        {/* ...then the golden far shore over its base, then the near sand. */}
        <path d={DUNE} fill="var(--c-sand-400)" />
        <path d={FORESHORE} fill="var(--c-sand-200)" />
      </g>

      {/* The bright lip where the water meets the beach. */}
      <g clipPath={`url(#${beachClip})`}>
        <path
          data-waterline
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
