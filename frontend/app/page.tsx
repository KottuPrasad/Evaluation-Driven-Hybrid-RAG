import { Nav } from "@/components/portfolio/nav"
import { Hero } from "@/components/portfolio/hero"
import { WhyExists } from "@/components/portfolio/why-exists"
import { Capabilities } from "@/components/portfolio/capabilities"
import { Architecture } from "@/components/portfolio/architecture"
import { Evaluation } from "@/components/portfolio/evaluation"
import { Demo } from "@/components/portfolio/demo"
import { Footer } from "@/components/portfolio/footer"

export default function Page() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Nav />
      <main>
        <Hero />
        <WhyExists />
        <Capabilities />
        <Architecture />
        <Evaluation />
        <Demo />
      </main>
      <Footer />
    </div>
  )
}
