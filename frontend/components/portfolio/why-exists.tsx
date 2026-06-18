import { Layers, GitBranch, Route } from "lucide-react"

const cards = [
  {
    icon: Layers,
    title: "Single Strategy Retrieval",
    body: "Traditional RAG systems rely on one retrieval strategy regardless of query intent.",
  },
  {
    icon: GitBranch,
    title: "Queries Are Different",
    body: "Different user questions require different retrieval strategies. Some depend on keyword matching while others benefit from semantic understanding.",
  },
  {
    icon: Route,
    title: "Adaptive Routing",
    body: "Query understanding dynamically selects the most suitable retrieval pipeline for each query.",
  },
]

export function WhyExists() {
  return (
    <section id="why" className="border-b border-border/60">
      <div className="mx-auto max-w-6xl px-4 py-24 sm:px-6">
        <div className="max-w-2xl">
          <p className="mb-3 font-mono text-xs uppercase tracking-widest text-primary">
            Why this project exists
          </p>
          <h2 className="text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
            Different Queries Need Different Retrieval
          </h2>
          <div className="mt-5 space-y-4 text-pretty leading-relaxed text-muted-foreground">
            <p>
              Traditional RAG systems use a single retrieval strategy for every
              query.
            </p>
            <p>
              This project introduces query understanding and adaptive routing
              to select the most effective retrieval pipeline based on user
              intent.
            </p>
          </div>
        </div>

        <div className="mt-14 grid gap-4 md:grid-cols-3">
          {cards.map((card) => (
            <div
              key={card.title}
              className="rounded-xl border border-border bg-card p-6 transition-colors hover:border-primary/40"
            >
              <span className="mb-5 flex size-10 items-center justify-center rounded-lg border border-border bg-secondary text-primary">
                <card.icon className="size-5" />
              </span>
              <h3 className="text-lg font-medium">{card.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                {card.body}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
