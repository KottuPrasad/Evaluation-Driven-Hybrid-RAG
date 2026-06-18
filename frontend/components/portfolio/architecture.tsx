type BoxProps = {
  cx: number
  top: number
  title: string
  subtitle?: string
  width?: number
  height?: number
  primary?: boolean
  small?: boolean
}

function Box({
  cx,
  top,
  title,
  subtitle,
  width = 180,
  height = 50,
  primary = false,
  small = false,
}: BoxProps) {
  const x = cx - width / 2
  const titleY = subtitle ? top + 24 : top + height / 2 + (small ? 3 : 4)

  return (
    <g>
      <rect
        x={x}
        y={top}
        width={width}
        height={height}
        rx={small ? 6 : 9}
        fill={primary ? "var(--primary)" : "var(--card)"}
        fillOpacity={primary ? 0.14 : 1}
        stroke={primary ? "var(--primary)" : "var(--foreground)"}
        strokeOpacity={primary ? 0.55 : 0.14}
        strokeWidth={1.5}
      />

      <text
        x={cx}
        y={titleY}
        textAnchor="middle"
        fontSize={small ? 9.5 : 13}
        fontWeight={600}
        fill="var(--foreground)"
      >
        {title}
      </text>

      {subtitle && (
        <text
          x={cx}
          y={top + 41}
          textAnchor="middle"
          fontSize={11}
          fill="var(--muted-foreground)"
          fontFamily="var(--font-mono)"
        >
          {subtitle}
        </text>
      )}
    </g>
  )
}

function Line({ d }: { d: string }) {
  return (
    <path
      d={d}
      fill="none"
      stroke="var(--foreground)"
      strokeOpacity={0.28}
      strokeWidth={1.5}
      strokeLinecap="round"
      strokeLinejoin="round"
      markerEnd="url(#arrow)"
    />
  )
}

function Plain({ d }: { d: string }) {
  return (
    <path
      d={d}
      fill="none"
      stroke="var(--foreground)"
      strokeOpacity={0.28}
      strokeWidth={1.5}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  )
}

export function Architecture() {
  return (
    <section
      id="architecture"
      className="border-b border-border/60 bg-background"
    >
      <div className="mx-auto max-w-6xl px-4 py-24 sm:px-6">
        <div className="max-w-2xl">
          <p className="mb-3 font-mono text-xs uppercase tracking-widest text-primary">
            System architecture
          </p>

          <h2 className="text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
            From Query to Answer
          </h2>

          <p className="mt-5 text-pretty leading-relaxed text-muted-foreground">
            Queries are classified, routed into specialized retrieval
            pipelines, and evaluated using a benchmark dataset of 30 manually
            labeled queries.
          </p>
        </div>

        <div className="mt-14 overflow-x-auto rounded-2xl border border-border bg-card/30 p-4 sm:p-8">
          <svg
            viewBox="0 0 1000 990"
            className="mx-auto w-full"
            style={{ maxWidth: "80%", height: "auto" }}
          >
            <defs>
              <marker
                id="arrow"
                viewBox="0 0 8 8"
                refX={7}
                refY={4}
                markerWidth={4}
                markerHeight={4}
                orient="auto"
              >
                <path
                  d="M0,0 L8,4 L0,8 z"
                  fill="var(--foreground)"
                  fillOpacity={0.35}
                />
              </marker>
            </defs>

            {/* USER QUERY */}
            <Box cx={480} top={20} width={240} title="USER QUERY" primary />

            <Line d="M480,76 L480,92" />

            {/* QUERY PROCESSOR */}
            <Box
              cx={480}
              top={98}
              width={360}
              height={58}
              title="QUERY PROCESSOR"
              subtitle="Classification · Normalization · Version Extraction"
            />

            {/* SPLIT BUS TO THREE ROUTES */}
            <Plain d="M480,162 L480,194" />
            <Plain d="M200,194 L760,194" />
            <Plain d="M200,194 L200,206" />
            <Plain d="M480,194 L480,206" />
            <Plain d="M760,194 L760,206" />

            {/* LABELS */}
            <text x={200} y={222} textAnchor="middle" fontSize={18} fontWeight={500} fill="var(--foreground)">
              Documentation
            </text>
            <text x={480} y={222} textAnchor="middle" fontSize={18} fontWeight={500} fill="var(--foreground)">
              Release Notes
            </text>
            <text x={760} y={222} textAnchor="middle" fontSize={18} fontWeight={500} fill="var(--foreground)">
              Mixed
            </text>

            {/* DOCUMENTATION PATH */}
            <Line d="M200,232 L200,238" />
            <Box cx={200} top={244} width={210} title="BM25 + Vector" subtitle="BM25 Top 15 + Vector Top 15" />

            <Line d="M200,300 L200,316" />
            <Box cx={200} top={322} width={170} title="RRF Fusion" subtitle="Top 15 Chunks" />

            <Line d="M200,378 L200,394" />
            <Box cx={200} top={400} width={190} title="Cross Encoder" subtitle="Final Top 8" />

            {/* RELEASE NOTES PATH */}
            <Line d="M480,232 L480,238" />
            <Box cx={480} top={244} width={190} title="BM25" subtitle="Top 20 Chunks" />

            <Line d="M480,300 L480,316" />
            <Box cx={480} top={322} width={200} title="Version Filter" subtitle="Filtered by Version" />

            <Line d="M480,378 L480,394" />
            <Box cx={480} top={400} width={150} title="Top 5 Chunks" />

            {/* MIXED PATH */}
            <Line d="M760,232 L760,238" />
            <Box cx={760} top={244} width={210} title="BM25 + Vector" subtitle="Top 15 Chunks + Top 15 Chunks" />

            <Line d="M760,300 L760,316" />
            <Box cx={760} top={322} width={170} title="RRF Fusion" subtitle="Top 15 Chunks" />

            <Line d="M760,378 L760,394" />
            <Box cx={760} top={400} width={190} title="Split RRF Results" />

            {/* MIXED SPLIT - full-size boxes */}
            <Plain d="M760,450 L760,476" />
            <Plain d="M650,476 L870,476" />
            <Plain d="M650,476 L650,488" />
            <Plain d="M870,476 L870,488" />

            <Line d="M650,488 L650,504" />
            <Box cx={650} top={510} width={200} title="Documentation Chunks" subtitle="Keep All" />

            <Line d="M870,488 L870,504" />
            <Box cx={870} top={510} width={200} title="Release Note Chunks" subtitle="Version Filter" />

            {/* both branches converge */}
            <Plain d="M650,560 L650,612" />
            <Plain d="M870,560 L870,612" />
            <Plain d="M650,612 L870,612" />

            <Line d="M760,612 L760,634" />
            <Box cx={760} top={640} width={190} title="Merge Results" />

            <Line d="M760,690 L760,716" />
            <Box cx={760} top={722} width={150} title="Top 8 Chunks" />

            {/* MERGE ALL THREE ROUTES */}
            <Plain d="M200,456 L200,816" />
            <Plain d="M480,456 L480,816" />
            <Plain d="M760,772 L760,816" />

            <Plain d="M200,816 L760,816" />

            <Line d="M480,816 L480,834" />

            {/* RESPONSE GENERATOR */}
            <Box cx={480} top={840} width={336} title="RESPONSE GENERATOR" />

            <Line d="M480,896 L480,912" />

            {/* ANSWER */}
            <Box cx={480} top={918} width={240} title="ANSWER" primary />
          </svg>
        </div>
      </div>
    </section>
  )
}
