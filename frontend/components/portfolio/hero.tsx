import { ArrowUpRight, Sparkles, Workflow } from "lucide-react"
import { Button } from "@/components/ui/button"

const techBadges = [
  "Python",
  "FastAPI",
  "FAISS",
  "BM25",
  "Cross Encoder",
  "Groq",
]

export function Hero() {
  return (
    <section
      id="top"
      className="relative overflow-hidden border-b border-border/60"
    >
      {/* subtle grid backdrop */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 opacity-[0.18] [background-image:linear-gradient(to_right,oklch(1_0_0/0.08)_1px,transparent_1px),linear-gradient(to_bottom,oklch(1_0_0/0.08)_1px,transparent_1px)] [background-size:56px_56px] [mask-image:radial-gradient(ellipse_at_center,black,transparent_75%)]"
      />

      <div className="relative mx-auto max-w-6xl px-4 pb-24 pt-36 sm:px-6 sm:pt-44">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-xs font-medium text-primary">
            <span className="size-1.5 rounded-full bg-primary" />
            Retrieval Engineering, Not a Chatbot Wrapper
          </div>

          <h1 className="text-balance text-4xl font-semibold leading-[1.08] tracking-tight sm:text-6xl">
            Evaluation-Driven Hybrid RAG System{" "}
            <span className="text-muted-foreground">for FastAPI Documentation</span>
          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-pretty text-base leading-relaxed text-muted-foreground sm:text-lg">
            A retrieval-focused RAG system that combines Adaptive Query routing, Hybrid Search, Rank Fusion,
            and Cross Encoder reranking to improve retrieval performance on FastAPI documentation.
          </p>

          <div className="mt-8 flex flex-wrap items-center justify-center gap-2">
            {techBadges.map((tech) => (
              <span
                key={tech}
                className="rounded-full border border-border bg-card px-3 py-1 font-mono text-xs text-muted-foreground"
              >
                {tech}
              </span>
            ))}
          </div>

          <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <a href="#demo">
              <Button size="lg" className="w-full gap-2 sm:w-auto">
                <Sparkles className="size-4" />
                Try the System
                <ArrowUpRight className="size-4 opacity-70" />
              </Button>
            </a>
            <a href="#architecture">
              <Button
                size="lg"
                variant="outline"
                className="w-full gap-2 border-border bg-transparent sm:w-auto"
              >
                <Workflow className="size-4" />
                View Architecture
              </Button>
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
