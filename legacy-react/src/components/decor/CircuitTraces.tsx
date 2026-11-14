import type { DecorProps } from '@/types/decor';

type CircuitTracesProps = DecorProps;

/**
 * The faint PCB traces from the key art: the "tech" half of the tropical/tech
 * pairing. Deliberately low-contrast — it is texture, never content.
 */
export function CircuitTraces({ className, style }: CircuitTracesProps) {
  const traces = [
    'M0 30 H60 L80 50 H140 L160 30 H240',
    'M20 90 H90 L110 70 H180 L200 90 H260',
    'M0 140 H50 L70 120 H130 L150 140 H230 L250 160',
    'M40 190 H110 L130 170 H210',
    'M110 0 V40 L130 60 V110',
    'M190 10 V60 L170 80 V130',
  ];

  const nodes = [
    [60, 30],
    [140, 50],
    [90, 90],
    [180, 70],
    [50, 140],
    [230, 140],
    [110, 40],
    [190, 60],
  ] as const;

  const chips = [
    [16, 46],
    [28, 46],
    [16, 58],
    [204, 104],
    [216, 104],
    [204, 116],
    [96, 158],
    [108, 158],
  ] as const;

  return (
    <svg
      viewBox="0 0 260 200"
      className={className}
      style={style}
      aria-hidden="true"
      focusable="false"
    >
      <g
        fill="none"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        {traces.map((d) => (
          <path key={d} d={d} />
        ))}
      </g>
      <g fill="none" stroke="currentColor" strokeWidth="1.6">
        {nodes.map(([cx, cy]) => (
          <circle key={`${cx}-${cy}`} cx={cx} cy={cy} r="3.4" />
        ))}
      </g>
      <g fill="currentColor" opacity="0.65">
        {chips.map(([x, y]) => (
          <rect key={`${x}-${y}`} x={x} y={y} width="8" height="8" rx="1.5" />
        ))}
      </g>
    </svg>
  );
}
