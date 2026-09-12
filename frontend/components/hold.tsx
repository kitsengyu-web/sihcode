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
      <VariableProximity
        label={"The Solution for Procurement of Official Standards details are here"}
        className="variable-proximity-demo text-4xl md:text-6xl lg:text-7xl font-extrabold cursor-pointer max-w-5xl"
        fromFontVariationSettings="'wght' 700, 'opsz' 9"
        toFontVariationSettings="'wght' 1000, 'opsz' 40"
        containerRef={containerRef}
        radius={100}
        falloff="linear"
      />
    </div>
  );
}
