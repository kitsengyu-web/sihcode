import { EnvVarWarning } from "@/components/env-var-warning";
import { AuthButton } from "@/components/auth-button";
import { PixelBlastBackground } from "@/components/pixel-blast-wrapper";
import { hasEnvVars } from "@/lib/utils";
import { Suspense } from "react";

export default function Home() {
  return (
    <main className="relative min-h-screen flex flex-col items-center overflow-hidden bg-black text-white">
      {/* Background Interactive PixelBlast */}
      <PixelBlastBackground />

      {/* Foreground Navigation Bar */}
      <div className="relative z-10 w-full flex flex-col items-center">
        <nav className="w-full flex justify-center border-b border-zinc-800/50 h-16 bg-black/40 backdrop-blur-md">
          <div className="w-full max-w-5xl flex justify-end items-center p-3 px-5 text-sm text-zinc-100">
            {!hasEnvVars ? (
              <EnvVarWarning />
            ) : (
              <Suspense>
                <AuthButton />
              </Suspense>
            )}
          </div>
        </nav>
      </div>
    </main>
  );
}
