import { Mail, Phone } from "lucide-react"
import { GithubIcon, LinkedinIcon } from "@/components/portfolio/brand-icons"

const contacts = [
  {
    icon: Phone,
    label: "+91 7989003606",
    href: "tel:+917989003606",
  },
  {
    icon: Mail,
    label: "prasadkottu5164@gmail.com",
    href: "mailto:prasadkottu5164@gmail.com",
  },
]

const socials = [
  {
    icon: GithubIcon,
    label: "GitHub",
    href: "https://github.com/KottuPrasad/Evaluation-Driven-Hybrid-RAG",
  },
  {
    icon: LinkedinIcon,
    label: "LinkedIn",
    href: "https://www.linkedin.com/in/k-v-b-k-prasad/",
  },
]

export function Footer() {
  return (
    <footer className="bg-background">
      <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <div className="flex flex-col gap-12 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <p className="text-lg font-semibold tracking-tight">Hybrid RAG System</p>
            <p className="mt-1 max-w-sm text-sm leading-relaxed text-muted-foreground">
              Evaluation-Driven Retrieval for FastAPI Documentation
            </p>
          </div>

          <div className="flex flex-col gap-10 sm:flex-row sm:gap-16">
            {/* Hire */}
            <div>
              <p className="text-base font-semibold tracking-tight">
                Contact
              </p>
              <ul className="mt-4 flex flex-col gap-3">
                {contacts.map((c) => (
                  <li key={c.label}>
                    <a
                      href={c.href}
                      className="inline-flex items-center gap-2.5 text-sm text-muted-foreground transition-colors hover:text-foreground"
                    >
                      <c.icon className="size-4 shrink-0" />
                      {c.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Socials */}
            <div>
              <p className="mb-4 font-mono text-xs uppercase tracking-widest text-muted-foreground">
                Socials
              </p>
              <ul className="flex flex-col gap-3">
                {socials.map((s) => (
                  <li key={s.label}>
                    <a
                      href={s.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2.5 text-sm text-muted-foreground transition-colors hover:text-foreground"
                    >
                      <s.icon className="size-4 shrink-0" />
                      {s.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="mt-12 border-t border-border pt-6">
          <p className="text-xs text-muted-foreground">
            &copy; {new Date().getFullYear()} Prasad Kottu. Retrieval
            engineering for FastAPI documentation.
          </p>
        </div>
      </div>
    </footer>
  )
}
