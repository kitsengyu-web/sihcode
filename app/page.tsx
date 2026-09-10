import { EnvVarWarning } from "@/components/env-var-warning";
import { AuthButton } from "@/components/auth-button";
import { PixelBlastBackground } from "@/components/pixel-blast-wrapper";
import { hasEnvVars } from "@/lib/utils";
import { Suspense } from "react";
import Link from "next/link";
import Image from "next/image";
export default function Home() {
  return (
    <main className="relative min-h-screen flex flex-col items-center overflow-hidden bg-black text-white">
      {/* Background Interactive PixelBlast */}
      <PixelBlastBackground />

      {/* Foreground Navigation Bar */}
      <div className="relative z-10 w-full flex flex-col items-center">
        <nav className="w-full flex justify-center border-b border-zinc-800/50 h-16 bg-black/40 backdrop-blur-md">
          <div className="w-full max-w-7xl flex justify-between items-center p-3 px-4 sm:px-6 text-sm text-zinc-100">
            
            {/* Left: Pramaan Logo (Positioned far left) */}
            <Link href="/" className="flex items-center gap-2.5 transition-opacity hover:opacity-90">
              <div className="h-8 w-8 overflow-hidden rounded-xl bg-white p-1 flex items-center justify-center shrink-0">
                const PramaanLogoIcon = () => (
  <svg
    viewBox="0 0 200 200"
    className="h-full w-full text-black fill-current"
    xmlns="https://i.postimg.cc/vTnSjdYh/pramaan-logo.png"
  >
    <path d="M43.5 138.8L59.3 46.2C60.5 39 67.2 34 74.5 35.2L124.6 43.6C131.8 44.8 136.8 51.5 135.6 58.7L129.8 92.6C128.6 99.8 121.9 104.8 114.7 103.6L86.4 98.9L79.1 141.2C77.9 148.4 71.2 153.4 63.9 152.2L49.5 149.8C42.3 148.6 37.3 141.9 38.5 134.7L43.5 138.8Z" />
  </svg>
);
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
      </div>
    </main>
  );
}
