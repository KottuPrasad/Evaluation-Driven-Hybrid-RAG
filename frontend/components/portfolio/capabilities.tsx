import {
  Brain,
  Route,
  Combine,
  Merge,
  ArrowUpDown,
  LineChart,
} from "lucide-react"

const capabilities = [
  {
    icon: Brain,
    title: "Query Understanding",
    body: "LLM-powered intent classification and query normalization.",
  },
  {
    icon: Route,
    title: "Adaptive Query Routing",
    body: "Selects the most appropriate retrieval pipeline based on query intent.",
  },
  {
    icon: Combine,
    title: "Hybrid Retrieval",
    body: "Combines BM25 keyword retrieval and dense vector retrieval.",
  },
  {
    icon: Merge,
    title: "RRF Fusion",
    body: "Merges multiple rankings using Reciprocal Rank Fusion.",
  },
  {
    icon: ArrowUpDown,
    title: "Cross Encoder Reranking",
    body: "Second-stage reranking for improved retrieval precision.",
  },
  {
    icon: LineChart,
    title: "Evaluation Framework",
    body: "Benchmark dataset with manually labeled relevance judgments.",
  },
]

export function Capabilities() {
  return (
    <section id="capabilities" className="border-b border-border/60">
      <div className="mx-auto max-w-6xl px-4 py-24 sm:px-6">
        <div className="max-w-2xl">
          <p className="mb-3 font-mono text-xs uppercase tracking-widest text-primary">
            Key capabilities
          </p>
          <h2 className="text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
            A Pipeline Built From Composable Stages
          </h2>
        </div>

        <div className="mt-14 grid gap-px overflow-hidden rounded-xl border border-border bg-border sm:grid-cols-2 lg:grid-cols-3">
          {capabilities.map((cap) => (
            <div
              key={cap.title}
              className="group bg-card p-7 transition-colors hover:bg-secondary"
            >
              <span className="mb-5 flex size-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                <cap.icon className="size-5" />
              </span>
              <h3 className="text-base font-medium">{cap.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                {cap.body}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
