import Link from "next/link";
import { Button } from "./ui/button";
import { createClient } from "@/lib/supabase/server";
import { LogoutButton } from "./logout-button";

export async function AuthButton() {
  const supabase = await createClient();

  // You can also use getUser() which will be slower.
  const { data } = await supabase.auth.getClaims();

  const user = data?.claims;

  return user ? (
    <div className="flex items-center gap-4 text-white">
      Hey, {user.email}!
      <LogoutButton />
    </div>
  ) : (
    <div className="flex gap-2">
      <Button
        asChild
        size="sm"
        className="bg-zinc-900 text-white border border-zinc-700 hover:bg-zinc-800 hover:text-white"
      >
        <Link href="/auth/login">Sign in</Link>
      </Button>
      <Button
        asChild
        size="sm"
        className="bg-black text-white border border-zinc-600 hover:bg-zinc-900 hover:text-white"
      >
        <Link href="/auth/sign-up">Sign up</Link>
      </Button>
    </div>
  );
}
