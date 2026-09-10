import { EnvVarWarning } from "@/components/env-var-warning";
import { AuthButton } from "@/components/auth-button";
import { Hero } from "@/components/hero";
import { ThemeSwitcher } from "@/components/theme-switcher";
import { ConnectSupabaseSteps } from "@/components/tutorial/connect-supabase-steps";
import { SignUpUserSteps } from "@/components/tutorial/sign-up-user-steps";
import { PixelBlastBackground } from "@/components/pixel-blast-wrapper";
import { hasEnvVars } from "@/lib/utils";
import { Suspense } from "react";

export default function Home() {
  return (
    <main className="relative min-h-screen flex flex-col items-center overflow-hidden bg-black text-white">
      {/* Background Interactive PixelBlast */}
      <PixelBlastBackground />

      {/* Foreground Content */}
      <div className="relative z-10 flex-1 w-full flex flex-col gap-20 items-center">
        {/* Navigation Bar */}
        <nav className="w-full flex justify-center border-b border-zinc-800 h-16 bg-black/80 backdrop-blur-md">
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

        {/* Main Content */}
        <div className="flex-1 flex flex-col gap-20 max-w-5xl p-5 text-zinc-100">
          <Hero />
          <section className="flex-1 flex flex-col gap-6 px-4">
            <h2 className="font-medium text-xl mb-4 text-white">Next steps</h2>
            {hasEnvVars ? <SignUpUserSteps /> : <ConnectSupabaseSteps />}
          </section>
        </div>

        {/* Footer */}
        <footer className="w-full flex items-center justify-center border-t border-zinc-800 mx-auto text-center text-xs gap-8 py-16 bg-black/80 backdrop-blur-md text-zinc-400">
          <p>
            Powered by{" "}
            <a
              href="https://supabase.com/?utm_source=create-next-app&utm_medium=template&utm_term=nextjs"
              target="_blank"
              className="font-bold hover:underline text-white"
              rel="noreferrer"
            >
              Supabase
            </a>
          </p>
          <ThemeSwitcher />
        </footer>
      </div>
    </main>
  );
}
