import { Suspense } from "react";
import Link from "next/link";
import { EnvVarWarning } from "@/components/env-var-warning";
import { AuthButton } from "@/components/auth-button";
import { PixelBlastBackground } from "@/components/pixel-blast-wrapper";
import { HeroSection } from "@/components/hold";
import TextType from "@/components/testtype";
import { hasEnvVars } from "@/lib/utils";
import CardSwap, { Card } from "@/components/cardswap";
import { Stats2 } from "@/components/stats";

const PramaanLogoIcon = () => (
  <svg
    viewBox="0 0 200 200"
    className="h-full w-full text-black fill-current"
    xmlns="https://cdn.uploadtourl.com/5d09f7d6_02_mark_white_on_dark.svg"
  >
    <path d="M43.5 138.8L59.3 46.2C60.5 39 67.2 34 74.5 35.2L124.6 43.6C131.8 44.8 136.8 51.5 135.6 58.7L129.8 92.6C128.6 99.8 121.9 104.8 114.7 103.6L86.4 98.9L79.1 141.2C77.9 148.4 71.2 153.4 63.9 152.2L49.5 149.8C42.3 148.6 37.3 141.9 38.5 134.7L43.5 138.8Z" />
  </svg>
);

export default async function Home() {
  return (
    <main className="w-full bg-black text-white flex flex-col overflow-x-hidden">
      {/* SECTION 1: PixelBlast Hero Section */}
      <section className="relative min-h-screen w-full flex flex-col justify-between items-center overflow-hidden">
        {/* PixelBlast is scoped solely to this hero section */}
        <PixelBlastBackground />

        {/* Hero Content Layer */}
        <div className="relative z-10 w-full flex flex-col min-h-screen justify-between items-center">
          {/* Navigation Bar */}
          <nav className="w-full flex justify-center border-b border-zinc-800/50 h-16 bg-black/40 backdrop-blur-md">
            <div className="w-full max-w-7xl flex justify-between items-center p-3 px-4 sm:px-6 text-sm text-zinc-100">
              <Link
                href="/"
                className="flex items-center gap-2.5 transition-opacity hover:opacity-90"
              >
                <div className="h-8 w-8 overflow-hidden rounded-xl bg-white p-1 flex items-center justify-center shrink-0">
                  <PramaanLogoIcon />
                </div>
                <span className="text-base font-bold tracking-tight text-white font-sans">
                  Pramaan
                </span>
              </Link>

              <div className="flex items-center">
                {!hasEnvVars ? (
                  <EnvVarWarning />
                ) : (
                  <Suspense>
                    <AuthButton />
                  </Suspense>
                )}
              </div>
            </div>
          </nav>

          {/* Hero Content */}
          <HeroSection />
        </div>

        {/* Decorative stacked-card accent, anchored to the hero section's corner */}
        
      </section>

      {/* SECTION 2: RippleGrid Section (Appears cleanly below PixelBlast) */}
      <section className="relative w-full h-[500px] bg-black border-t border-zinc-800/50 overflow-hidden z-20">
        <RippleGrid
          enableRainbow={false}
          gridColor="#5227FF"
          rippleIntensity={0.05}
          gridSize={10}
          gridThickness={15}
          mouseInteraction
          mouseInteractionRadius={0.8}
          opacity={1}
          fadeDistance={1.5}
          vignetteStrength={2}
          glowIntensity={0.1}
          gridRotation={0}
        />
          

      </section>

      
      {/* SECTION 3: CardSwap Feature Section (text left, cards bleeding off right edge) */}
      <section className="relative z-20 w-full bg-black border-t border-zinc-800/40 py-24 px-6 md:px-12">
        <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-16 items-center">
          {/* Left: heading + typing subtext */}
          <div className="text-left max-w-md">
            <h2 className="text-3xl md:text-4xl font-semibold text-white leading-tight mb-4">
              Built for accuracy,
              <br />
              trusted for certainty
            </h2>
            <TextType
              text={[
                "Empowering intelligent workflows with Pramaan AI.",
                "Deep reasoning, clean interactions, and modern design.",
                "Start building your next conversation today."
              ]}
              typingSpeed={45}
              deletingSpeed={25}
              pauseDuration={2200}
              loop={true}
              startOnVisible={true}
              className="text-base md:text-lg font-medium text-zinc-400"
              cursorCharacter="▋"
              cursorClassName="text-amber-400 font-bold"
            />
          </div>

          {/* Right: card stack, given generous room so nothing clips, nudged toward the edge via flex */}
          <div className="relative h-[420px] md:h-[480px] w-full flex items-center justify-center md:justify-end overflow-visible">
            <div className="relative md:mr-[-20px] lg:mr-[-60px]">
              <CardSwap
                width={340}
                height={220}
                cardDistance={50}
                verticalDistance={55}
                delay={4000}
                pauseOnHover={true}
              >
                <Card customClass="p-6 flex flex-col justify-between">
                  <h3 className="text-lg font-semibold text-white">Semantic Matching</h3>
                  <p className="text-sm text-zinc-400">
                    Finds the right Indian Standard by meaning, not keywords.
                  </p>
                </Card>
                <Card customClass="p-6 flex flex-col justify-between">
                  <h3 className="text-lg font-semibold text-white">Allied Standards</h3>
                  <p className="text-sm text-zinc-400">
                    Surfaces normative, safety, and test-method references automatically.
                  </p>
                </Card>
                <Card customClass="p-6 flex flex-col justify-between">
                  <h3 className="text-lg font-semibold text-white">Certification Info</h3>
                  <p className="text-sm text-zinc-400">
                    Flags BIS, CRS, and Hallmarking requirements up front.
                  </p>
                </Card>
              </CardSwap>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 4: Footer */}
      <footer className="relative z-20 w-full py-12 px-6 border-t border-zinc-800/40 bg-black text-center">
        <div className="max-w-4xl mx-auto flex flex-col items-center justify-center gap-3">
          <Stats2 />

          <p className="text-xs text-zinc-600 mt-2">
            © 2026 Pramaan AI
          </p>
        </div>
      </footer>
    </main>
  );
}
