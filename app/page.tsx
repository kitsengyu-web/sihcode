import { Suspense } from "react";
import Link from "next/link";
import { EnvVarWarning } from "@/components/env-var-warning";
import { AuthButton } from "@/components/auth-button";
import { PixelBlastBackground } from "@/components/pixel-blast-wrapper";
import { HeroSection } from "@/components/hold";
import TextType from "@/components/testtype";
import { hasEnvVars } from "@/lib/utils";

const PramaanLogoIcon = () => (
  <svg
    viewBox="0 0 200 200"
    className="h-full w-full text-black fill-current"
    xmlns="https://i.postimg.cc/vTnSjdYh/pramaan-logo.png"
  >
    <path d="M43.5 138.8L59.3 46.2C60.5 39 67.2 34 74.5 35.2L124.6 43.6C131.8 44.8 136.8 51.5 135.6 58.7L129.8 92.6C128.6 99.8 121.9 104.8 114.7 103.6L86.4 98.9L79.1 141.2C77.9 148.4 71.2 153.4 63.9 152.2L49.5 149.8C42.3 148.6 37.3 141.9 38.5 134.7L43.5 138.8Z" />
  </svg>
);

export default async function Home() {
  return (
    <main className="relative min-h-screen flex flex-col justify-between items-center overflow-hidden bg-black text-white">
      {/* Background Canvas Layer */}
      <PixelBlastBackground />

      {/* Foreground Content Container (Layered above background) */}
      <div className="relative z-10 w-full flex flex-col min-h-screen justify-between items-center">
        {/* Navigation Bar */}
        <nav className="w-full flex justify-center border-b border-zinc-800/50 h-16 bg-black/40 backdrop-blur-md">
          <div className="w-full max-w-7xl flex justify-between items-center p-3 px-4 sm:px-6 text-sm text-zinc-100">
            {/* Left: Logo */}
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

            {/* Right: Auth Action */}
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

        {/* Hero Interactive Text Section */}
        <HeroSection />

        {/* Bottom Section containing TextType */}
        <footer className="w-full py-12 px-6 border-t border-zinc-800/40 bg-black/70 backdrop-blur-md text-center">
          <div className="max-w-4xl mx-auto flex flex-col items-center justify-center gap-3">
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
              className="text-base md:text-lg font-medium text-zinc-300"
              cursorCharacter="▋"
              cursorClassName="text-amber-400 font-bold"
            />
            <p className="text-xs text-zinc-600 mt-2">
              © 2026 Pramaan AI
            </p>
          </div>
        </footer>
      </div>
    </main>
  );
}
