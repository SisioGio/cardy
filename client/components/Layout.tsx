
// components/Layout.tsx

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen w-full text-white flex flex-col relative overflow-x-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-gray-900 via-blue-950 to-black bg-[length:300%_300%] animate-gradient-slow opacity-90" />

      {/* Optional top border glow */}
      <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-cyan-400/40 via-blue-400/40 to-purple-400/40" />

      {/* Main Content Wrapper */}
      <main className="flex-1 flex flex-col px-4 sm:px-6 lg:px-8 py-6">
        <div className="mx-auto w-full max-w-7xl">
          {children}
        </div>
      </main>

      {/* Optional footer slot */}
      {/* <footer className="py-4 text-center text-gray-400 text-sm">
        © 2025 Cardy — AI Restaurant Researcher
      </footer> */}
    </div>
  );
}

