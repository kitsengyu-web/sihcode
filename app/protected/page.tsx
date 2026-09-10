"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client"; // Adjust path to your Supabase client
import { ClaudeChatInput } from "@/components/chat";
import { LogOut, User } from "lucide-react";
import type { User as SupabaseUser } from "@supabase/supabase-js";

export default function ProtectedChatPage() {
  const [user, setUser] = useState<SupabaseUser | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const supabase = createClient();

  useEffect(() => {
    const getUser = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();

      if (!user) {
        router.push("/login");
      } else {
        setUser(user);
      }
      setLoading(false);
    };

    getUser();

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      if (!session) {
        router.push("/login");
      } else {
        setUser(session?.user ?? null);
      }
    });

    return () => subscription.unsubscribe();
  }, [router, supabase]);

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    router.push("/login");
  };

  const handleSendMessage = (data: {
    message: string;
    files: any[];
    pastedContent: any[];
    isThinkingEnabled: boolean;
  }) => {
    console.log("Submitting payload with user ID:", user?.id, data);
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#0d0d0e]">
        <div className="flex flex-col items-center gap-3">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-zinc-700 border-t-white" />
          <p className="text-sm font-medium text-zinc-400">Loading session...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-[#0d0d0e] text-zinc-100">
      <header className="flex h-14 items-center justify-between border-b border-zinc-800 px-4 md:px-6">
        <div className="flex items-center gap-2">
          <div className="h-2 w-2 rounded-full bg-emerald-500" />
          <span className="text-sm font-semibold tracking-wide text-zinc-200">
            Workspace
          </span>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 rounded-full bg-zinc-900 border border-zinc-800 px-3 py-1">
            <User className="h-3.5 w-3.5 text-zinc-400" />
            <span className="text-xs text-zinc-300 font-medium">
              {user?.email || "User"}
            </span>
          </div>

          <button
            onClick={handleSignOut}
            className="inline-flex items-center gap-1.5 rounded-lg border border-zinc-800 bg-zinc-900 px-2.5 py-1.5 text-xs text-zinc-400 hover:bg-zinc-800 hover:text-white transition-colors"
            type="button"
          >
            <LogOut className="h-3.5 w-3.5" />
            <span>Sign out</span>
          </button>
        </div>
      </header>

      <main className="flex flex-1 flex-col items-center justify-center p-4 md:p-6">
        <div className="w-full max-w-4xl space-y-6">
          <div className="text-center space-y-1.5">
            <h1 className="text-2xl font-semibold tracking-tight text-white">
              What would you like to explore today?
            </h1>
            <p className="text-xs text-zinc-400">
              Enter a prompt or upload content to begin.
            </p>
          </div>

          <ClaudeChatInput onSendMessage={handleSendMessage} />
        </div>
      </main>
    </div>
  );
}
