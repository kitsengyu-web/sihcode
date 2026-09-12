export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="w-full min-h-screen bg-black text-white p-0 m-0 overflow-x-hidden">
      {children}
    </div>
  );
}
