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
        label={"Hover me! And then star React Bits on GitHub, or else..."}
        className={"variable-proximity-demo text-2xl md:text-4xl font-bold cursor-pointer"}
        fromFontVariationSettings="'wght' 400, 'opsz' 9"
        toFontVariationSettings="'wght' 1000, 'opsz' 40"
        containerRef={containerRef}
        radius={100}
        falloff="linear"
      />
    </div>
  );
}
