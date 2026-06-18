import { Button } from "@/components/ui/button"
import { GithubIcon } from "@/components/portfolio/brand-icons"

const links = [
  { label: "Why", href: "#why" },
  { label: "Capabilities", href: "#capabilities" },
  { label: "Architecture", href: "#architecture" },
  { label: "Evaluation", href: "#evaluation" },
  { label: "Demo", href: "#demo" },
]

export function Nav() {
  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-border/60 bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
        <a href="#top" className="flex items-center gap-2.5">
          <span className="flex size-7 items-center justify-center rounded-md bg-primary text-xs font-bold text-primary-foreground">
            R
          </span>
          <span className="hidden text-sm font-semibold tracking-tight sm:inline">
            Hybrid RAG
          </span>
        </a>

        <nav className="hidden items-center gap-7 md:flex">
          {links.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              {link.label}
            </a>
          ))}
        </nav>

        <a
          href="https://github.com/KottuPrasad/Evaluation-Driven-Hybrid-RAG"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Button
            size="sm"
            variant="outline"
            className="gap-2 border-border bg-card text-foreground hover:bg-secondary"
          >
            <GithubIcon className="size-4" />
            GitHub
          </Button>
        </a>
      </div>
    </header>
  )
}
