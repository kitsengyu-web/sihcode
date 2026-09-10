import { EnvVarWarning } from "@/components/env-var-warning";
import { AuthButton } from "@/components/auth-button";
import { PixelBlastBackground } from "@/components/pixel-blast-wrapper";
import { hasEnvVars } from "@/lib/utils";
import { Suspense } from "react";
import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <main className="relative min-h-screen flex flex-col items-center overflow-hidden bg-black text-white">
      {/* Background Interactive PixelBlast */}
      <PixelBlastBackground />

      {/* Foreground Navigation Bar */}
      <div className="relative z-10 w-full flex flex-col items-center">
        <nav className="w-full flex justify-center border-b border-zinc-800/50 h-16 bg-black/40 backdrop-blur-md">
          <div className="w-full max-w-5xl flex justify-between items-center p-3 px-5 text-sm text-zinc-100">
            
            {/* Left: Pramaan Logo */}
            <Link href="/" className="flex items-center gap-2.5 transition-opacity hover:opacity-90">
              <div className="relative h-8 w-8 overflow-hidden rounded-lg bg-white p-0.5">
                <Image
                  src="@/components/pramaan_logo.png"
                  alt="Pramaan Logo"
                  fill
                  className="object-contain p-0.5"
                  priority
                />
              </div>
              <span className="text-base font-semibold tracking-tight text-white font-sans">
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
