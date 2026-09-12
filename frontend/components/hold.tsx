"use client";

import { useRef } from "react";
import VariableProximity from "@/components/headtxt";

export function HeroSection() {
  const containerRef = useRef<HTMLDivElement>(null);

  return (
    <div
      ref={containerRef}
      className="relative z-10 my-auto flex items-center justify-center p-8 text-center"
    >
      <div className="group relative transition-transform duration-300 ease-out hover:scale-[1.03]">
        {/* Soft glow layer behind the text, fades in on hover */}
        <div
          className="pointer-events-none absolute inset-0 -z-10 blur-2xl opacity-0 transition-opacity duration-500 group-hover:opacity-60"
          style={{
            background:
              "radial-gradient(circle, rgba(82,39,255,0.55) 0%, rgba(82,39,255,0) 70%)",
          }}
        />

        <VariableProximity
          label={"The Solution for Procurement of Official Standards details are here"}
          className="variable-proximity-demo text-2xl md:text-4xl font-extrabold cursor-pointer transition-colors duration-300 group-hover:text-purple-200"
          fromFontVariationSettings="'wght' 700, 'opsz' 9"
          toFontVariationSettings="'wght' 1000, 'opsz' 40"
          containerRef={containerRef}
          radius={100}
          falloff="linear"
        />
      </div>
    </div>
  );
}
