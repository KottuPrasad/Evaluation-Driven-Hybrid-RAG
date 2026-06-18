"use client"

import { useState } from "react"
import {
  ArrowDown,
  ChevronDown,
  CornerDownLeft,
  FileText,
  Sparkles,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

type PipelineStep = { label: string; meta?: string }

type Source = {
  title: string
  section: string
  subsection: string
}

type ApiResponse = {
  answer: string
  query_type: string
  version: string | null
  normalized_query: string
  route: string
  pipeline: PipelineStep[]
  sources: Source[]
}

type Scenario = {
  query: string
  route: "Documentation" | "Release Notes" | "Mixed"
  queryType: string
  normalized: string
  version: string
  answer: string
  pipeline: PipelineStep[]
  chunks: { title: string; section: string; subsection: string }[]
}

const ROUTE_BADGE: Record<string, string> = {
  documentation:
    "border-primary/40 bg-primary/10 text-primary",

  release_notes:
    "border-border bg-secondary text-foreground",

  mixed:
    "border-border bg-secondary text-foreground",
}

export function Demo() {
  const [input, setInput] = useState("")
  const [active, setActive] = useState<ApiResponse | null>(null)

  const [loading, setLoading] = useState(false)

  async function run(text: string) {

    const trimmed = text.trim()

    if (!trimmed) return

    try {

      setLoading(true)

      const response = await fetch(
        "https://prasadkottu-evaluation-based-hybrid-rag.hf.space/ask",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            query: trimmed,
          }),
        },
      )

      const data: ApiResponse =
        await response.json()

      setInput(trimmed)

      setActive(data)

    } catch (error) {

      console.error(error)

      alert(
        "Failed to connect to backend."
      )

    } finally {

      setLoading(false)

    }
  }

  return (
    <section id="demo" className="border-b border-border/60">
      <div className="mx-auto max-w-5xl px-4 py-24 sm:px-6">
        <div className="max-w-2xl">
          <p className="mb-3 font-mono text-xs uppercase tracking-widest text-primary">
            Interactive demo
          </p>

          <h2 className="text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
            Try the System
          </h2>

          <p className="mt-5 text-pretty leading-relaxed text-muted-foreground">
            Ask a FastAPI documentation question and inspect the retrieval
            pipeline.
          </p>
        </div>

        <form
          className="mt-10"
          onSubmit={(e) => {
            e.preventDefault()
            run(input)
          }}
        >
          <div className="flex flex-col gap-3 rounded-xl border border-border bg-card p-3">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault()
                  run(input)
                }
              }}
              rows={2}
              placeholder="Ask about FastAPI..."
              className="w-full resize-none bg-transparent px-3 py-2 text-sm outline-none"
            />

            <div className="flex items-center justify-end gap-3 border-t border-border pt-3">
              <Button type="submit" className="gap-2">
                {loading ? "Thinking..." : "Ask"}
                <CornerDownLeft className="size-4" />
              </Button>
            </div>
          </div>
        </form>

        <div className="mt-3 flex flex-wrap items-center gap-2">
          <span className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">
            Try:
          </span>

          {[
            "How do I use a class as a dependency in FastAPI?",
            "What updates were added in 0.121.1?",
            "What is strict content type checking in FastAPI and when was it added?"
          ].map((query) => (
            <button
              key={query}
              type="button"
              onClick={() => run(query)}
              className="rounded-full border border-border bg-card px-2.5 py-1 text-[11px] text-muted-foreground transition-colors hover:border-primary/40 hover:text-foreground"
            >
              {query}
            </button>
          ))}
        </div>

        {active ? (
          <div className="mt-12 space-y-6">

            {/* Answer */}
            <div className="rounded-2xl border border-border bg-card p-7">
              <div className="mb-4 flex items-center gap-2 text-sm font-medium text-primary">
                <Sparkles className="size-4" />
                Generated Answer
              </div>
              <div
                className="
                  max-w-none

                  [&_h1]:text-3xl
                  [&_h1]:font-bold

                  [&_h2]:text-2xl
                  [&_h2]:font-semibold
                  [&_h2]:mt-6
                  [&_h2]:mb-3

                  [&_h3]:text-xl
                  [&_h3]:font-semibold

                  [&_p]:mb-4
                  [&_p]:leading-relaxed

                  [&_ul]:list-disc
                  [&_ul]:pl-6

                  [&_ol]:list-decimal
                  [&_ol]:pl-6

                  [&_pre]:overflow-x-auto
                  [&_pre]:rounded-lg
                  [&_pre]:border
                  [&_pre]:border-border
                  [&_pre]:p-4
                "
              >
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {active.answer}
                </ReactMarkdown>
              </div>
            </div>

            {/* Insights + Pipeline */}
            <div className="grid gap-6 lg:grid-cols-2">

              <div className="rounded-2xl border border-border bg-card p-7">
                <h3 className="text-sm font-medium">
                  Retrieval Insights
                </h3>

                <dl className="mt-5 space-y-4">

                  <InsightRow
                    label="Normalized Query"
                    value={active.normalized_query}
                    mono
                  />

                  <InsightRow
                    label="Version"
                    value={active.version ?? "Not specified"}
                    mono
                  />

                  <div className="flex items-center justify-between gap-4 border-t border-border pt-4">
                    <dt className="text-sm text-muted-foreground">
                      Route Selected
                    </dt>

                    <dd>
                      <span
                        className={`rounded-md border px-2.5 py-1 text-xs font-medium ${ROUTE_BADGE[active.route.toLowerCase()]
                          }`}
                      >
                        {active.route}
                      </span>
                    </dd>
                  </div>
                </dl>
              </div>

              <div className="rounded-2xl border border-border bg-card p-7">
                <h3 className="text-sm font-medium">
                  Pipeline Used
                </h3>

                <div className="mt-5 flex flex-col items-center">
                  {active.pipeline.map((step, i) => (
                    <div
                      key={`${step.label}-${i}`}
                      className="flex w-full flex-col items-center"
                    >
                      <div className="w-full max-w-xs rounded-lg border border-border bg-background px-4 py-2.5 text-center">
                        <p className="text-sm font-medium">
                          {step.label}
                        </p>

                        {step.meta && (
                          <p className="font-mono text-[11px] text-muted-foreground">
                            {step.meta}
                          </p>
                        )}
                      </div>

                      {i < active.pipeline.length - 1 && (
                        <ArrowDown className="my-1.5 size-4 text-muted-foreground" />
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <RetrievedChunks chunks={active.sources} />
          </div>
        ) : (
          <p className="mt-12 rounded-2xl border border-dashed border-border bg-card/40 px-6 py-16 text-center text-sm text-muted-foreground">
            Ask a question or pick an example to inspect the retrieval pipeline.
          </p>
        )}
      </div>
    </section >
  )

}

function InsightRow({
  label,
  value,
  mono = false,
}: {
  label: string
  value: string
  mono?: boolean
}) {
  return (
    <div className="flex items-start justify-between gap-4 border-t border-border pt-4 first:border-t-0 first:pt-0">
      <dt className="text-sm text-muted-foreground">
        {label}
      </dt>

      <dd
        className={`max-w-[60%] text-right text-sm ${mono
          ? "font-mono text-foreground/90"
          : "text-foreground/90"
          }`}
      >
        {value}
      </dd>
    </div>
  )
}

function RetrievedChunks({
  chunks,
}: {
  chunks: {
    title: string
    section: string
    subsection: string
  }[]
}) {
  const [open, setOpen] = useState(true)

  return (
    <div className="overflow-hidden rounded-2xl border border-border bg-card">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center justify-between px-7 py-5 text-left"
      >
        <span className="flex items-center gap-2 text-sm font-medium">
          <FileText className="size-4 text-primary" />
          Retrieved Sources Used For Generation ({chunks.length})
        </span>

        <ChevronDown
          className={`size-4 text-muted-foreground transition-transform ${open ? "rotate-180" : ""
            }`}
        />
      </button>

      {open && (
        <div className="border-t border-border">
          {chunks.map((chunk, i) => (
            <div
              key={`${chunk.title}-${i}`}
              className="px-7 py-5 [&:not(:first-child)]:border-t [&:not(:first-child)]:border-border"
            >
              <div className="mb-3 flex items-center justify-between">
                <span className="rounded-md border border-border px-2 py-1 text-xs font-medium">
                  Retrieved Chunk #{i + 1}
                </span>
              </div>

              <div className="space-y-3">
                <div>
                  <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
                    Title
                  </p>

                  <p className="text-sm font-medium">
                    {chunk.title}
                  </p>
                </div>

                {chunk.section && (
                  <div>
                    <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
                      Section
                    </p>

                    <p className="text-sm">
                      {chunk.section}
                    </p>
                  </div>
                )}

                {chunk.subsection && (
                  <div>
                    <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
                      Subsection
                    </p>

                    <p className="text-sm">
                      {chunk.subsection}
                    </p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}