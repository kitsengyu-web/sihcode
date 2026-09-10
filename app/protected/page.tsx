import { EnvVarWarning } from "@/components/env-var-warning";
import { AuthButton } from "@/components/auth-button";
import { PixelBlastBackground } from "@/components/pixel-blast-wrapper";
import ChatPage from "@/components/chat";
import { hasEnvVars } from "@/lib/utils";
import { Suspense } from "react";

export default function Home() {
  return (
    <main className="relative min-h-screen w-full flex flex-col items-center overflow-hidden bg-black text-white">
      {/* Background Interactive PixelBlast */}
      <PixelBlastBackground />

      {/* Hidden/Fallback Auth Verification */}
      {!hasEnvVars && (
        <div className="relative z-20 w-full p-4 flex justify-center">
          <EnvVarWarning />
        </div>
      )}

      {/* Main AI Chat Component */}
      <div className="relative z-10 w-full flex-1 flex flex-col items-center justify-center">
        <ChatPage />
      </div>
    </main>
  );
}
