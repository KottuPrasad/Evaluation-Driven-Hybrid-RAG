import { ChevronRight } from "lucide-react"

const rows = [
  { system: "BM25", recall: "0.5867", hit: "0.8667", mrr: "0.7278", highlight: false },
  { system: "Vector", recall: "0.5022", hit: "0.7000", mrr: "0.6150", highlight: false },
  {
    system: "BM25 + Vector + RRF",
    recall: "0.6478",
    hit: "0.9000",
    mrr: "0.6506",
    highlight: false,
  },
  {
    system: "BM25 + Vector + RRF + Cross Encoder",
    recall: "0.7478",
    hit: "0.9667",
    mrr: "0.8067",
    highlight: false,
  },
  {
    system: "Final System",
    note: "Intent Classification & Adaptive Routing",
    recall: "0.8467",
    hit: "1.0000",
    mrr: "0.8022",
    highlight: true,
  },
]

const definitions = [
  {
    term: "Routing Accuracy",
    body: "Percentage of queries correctly routed to the appropriate retrieval pipeline based on query intent and content type.",
  },
  {
    term: "Recall@5",
    body: "Percentage of relevant chunks retrieved within the top 5 results.",
  },
  {
    term: "Hit Rate@5",
    body: "Percentage of queries with at least one relevant chunk in the top 5.",
  },
  {
    term: "MRR",
    body: "Measures how highly the first relevant result is ranked.",
  },
]

const evolution = [
  "BM25",
  "Vector",
  "Hybrid RRF",
  "Cross Encoder",
  "Query Understanding & Routing",
]

export function Evaluation() {
  return (
    <section id="evaluation" className="border-b border-border/60">
      <div className="mx-auto max-w-6xl px-4 py-24 sm:px-6">
        <div className="max-w-2xl">
          <p className="mb-3 font-mono text-xs uppercase tracking-widest text-primary">
            Evaluation results
          </p>
          <h2 className="text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
            Measured, Not Assumed
          </h2>
          <p className="mt-5 text-pretty leading-relaxed text-muted-foreground">
            A benchmark dataset with manually labeled relevance judgments was
            used to quantify retrieval performance improvements.
          </p>
        </div>

        <div className="mt-14 grid items-start gap-6 lg:grid-cols-[260px_1fr]">

          {/* Benchmark card */}
          <div className="rounded-xl border border-border bg-card p-6">
            <p className="text-sm text-muted-foreground">
              Benchmark Dataset
            </p>

            <p className="mt-1 text-4xl font-semibold tracking-tight">
              30
            </p>

            <p className="text-sm text-muted-foreground">
              Queries
            </p>

            {/* Query Types */}
            <div className="mt-6 border-t border-border pt-4">
              <p className="mb-3 text-xs uppercase tracking-wider text-muted-foreground">
                Type of Queries
              </p>

              {[
                {
                  label: "Documentation",
                  value: 10,
                },
                {
                  label: "Release Notes",
                  value: 10,
                },
                {
                  label: "Mixed",
                  value: 10,
                },
              ].map((d) => (
                <div
                  key={d.label}
                  className="mb-2 flex items-center justify-between text-sm"
                >
                  <span className="text-muted-foreground">
                    {d.label}
                  </span>

                  <span className="font-mono">
                    {d.value}
                  </span>
                </div>
              ))}
            </div>

            {/* Routing Accuracy */}
            <div className="mt-6 border-t border-border pt-4">
              <p className="mb-3 text-xs uppercase tracking-wider text-muted-foreground">
                Routing Accuracy
              </p>

              <p className="text-3xl font-semibold tracking-tight">
                93.33%
              </p>

              <p className="mt-1 text-sm text-muted-foreground">
                28 / 30 Correct Routes
              </p>
            </div>
          </div>

          {/* Evaluation Table */}
          <div className="overflow-x-auto rounded-xl border border-border bg-card">
            <table className="w-full min-w-[520px] text-left text-sm">
              <thead>
                <tr className="border-b border-border text-sm uppercase tracking-wider text-muted-foreground">
                  <th className="px-6 py-5 font-medium">
                    System
                  </th>

                  <th className="px-6 py-5 text-right font-medium">
                    Recall@5
                  </th>

                  <th className="px-6 py-5 text-right font-medium">
                    Hit Rate@5
                  </th>

                  <th className="px-6 py-5 text-right font-medium">
                    MRR
                  </th>
                </tr>
              </thead>

              <tbody>
                {rows.map((row) => (
                  <tr
                    key={row.system}
                    className={
                      row.highlight
                        ? "border-l-2 border-l-primary bg-primary/10"
                        : "border-t border-border"
                    }
                  >
                    <td className="px-6 py-5">
                      <span
                        className={
                          row.highlight
                            ? "text-base font-semibold text-foreground"
                            : "text-base text-foreground"
                        }
                      >
                        {row.system}
                      </span>

                      {row.note ? (
                        <span className="mt-0.5 block text-xs text-muted-foreground">
                          {row.note}
                        </span>
                      ) : null}
                    </td>

                    <td className="px-6 py-5 text-right font-mono text-base tabular-nums">
                      {row.recall}
                    </td>

                    <td className="px-6 py-5 text-right font-mono text-base tabular-nums">
                      {row.hit}
                    </td>

                    <td className="px-6 py-5 text-right font-mono text-base tabular-nums">
                      {row.mrr}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Definitions */}
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {definitions.map((def) => (
            <div
              key={def.term}
              className="rounded-xl border border-border bg-card p-5"
            >
              <p className="font-mono text-sm text-primary">
                {def.term}
              </p>

              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                {def.body}
              </p>
            </div>
          ))}
        </div>

        {/* System evolution */}
        <div className="mt-10">
          <p className="mb-4 font-mono text-xs uppercase tracking-widest text-muted-foreground">
            System evolution
          </p>
          <div className="flex flex-wrap items-center gap-2">
            {evolution.map((stage, i) => (
              <div key={stage} className="flex items-center gap-2">
                <span
                  className={`rounded-lg border px-3 py-1.5 text-sm ${i === evolution.length - 1
                    ? "border-primary/50 bg-primary/10 text-foreground"
                    : "border-border bg-card text-muted-foreground"
                    }`}
                >
                  {stage}
                </span>
                {i < evolution.length - 1 ? (
                  <ChevronRight className="size-4 text-muted-foreground" />
                ) : null}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
