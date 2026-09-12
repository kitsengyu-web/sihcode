"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const messages = [
  'Received: "Summarize Q3 performance for stakeholder report..."',
  "Chunking input → 847 tokens → 6 embeddings generated",
  "Vector search complete: 5 chunks, avg cosine sim 0.89",
  "Injecting context into prompt template (1,204 tokens)",
  "LLM inference: 3 tool calls dispatched in parallel",
  "Tool: send_email → draft created, 312 words, pending approval",
  "Tool: update_crm → record Q3_2024 flagged as reviewed",
  "Tool: generate_report → PDF queued for 17:00 dispatch",
  "Workflow complete. 3 actions dispatched in 342ms.",
  "Idle. Listening for next trigger event...",
]

function AnimatedDot({
  path,
  duration,
  delay,
  size,
  opacity,
}: {
  path: string
  duration: number
  delay: number
  size: number
  opacity: number
}) {
  return (
    <circle r={size} fill="#0052FF" opacity={opacity}>
      <animateMotion
        dur={`${duration}s`}
        repeatCount="indefinite"
        begin={`${delay}s`}
        path={path}
      />
    </circle>
  )
}

function PulsingDot({
  cx,
  cy,
  color,
  duration,
  delay = 0,
}: {
  cx: number
  cy: number
  color: string
  duration: number
  delay?: number
}) {
  return (
    <motion.circle
      cx={cx}
      cy={cy}
      r={2.8}
      fill={color}
      animate={{ opacity: [0.15, 1, 0.15] }}
      transition={{
        duration,
        delay,
        repeat: Infinity,
        ease: "easeInOut",
      }}
    />
  )
}

function StatusIndicator({
  cx,
  cy,
  color,
  pulsing = false,
  duration = 1.9,
  delay = 0,
}: {
  cx: number
  cy: number
  color: string
  pulsing?: boolean
  duration?: number
  delay?: number
}) {
  if (pulsing) {
    return (
      <motion.circle
        cx={cx}
        cy={cy}
        r={3}
        fill={color}
        animate={{ opacity: [0.3, 1, 0.3] }}
        transition={{
          duration,
          delay,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
    )
  }
  return <circle cx={cx} cy={cy} r={3} fill={color} opacity={0.95} />
}

export default function EnterpriseAIPipeline() {
  const [messageIndex, setMessageIndex] = useState(0)
  const [workflows, setWorkflows] = useState(1247)

  useEffect(() => {
    const messageInterval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % messages.length)
    }, 2700)

    const workflowInterval = setInterval(() => {
      setWorkflows((prev) => prev + 1)
    }, 7200)

    return () => {
      clearInterval(messageInterval)
      clearInterval(workflowInterval)
    }
  }, [])

  const paths = {
    p1: "M116,88 L158,88",
    p2: "M268,88 L306,88",
    p3: "M411,88 C425,88 435,50 448,50",
    p4: "M411,88 L448,88",
    p5: "M411,88 C425,88 435,126 448,126",
  }

  return (
    <div className="bg-[#090909] border border-white/[0.08] rounded-[14px] overflow-hidden font-sans w-[620px] mx-auto">
      {/* Header */}
      <div className="px-[18px] py-[11px] border-b border-white/[0.06] flex items-center justify-between">
        <div className="flex items-center gap-[7px]">
          <motion.span
            className="w-[6px] h-[6px] rounded-full bg-green-500 inline-block"
            animate={{ opacity: [1, 0.2, 1] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
          />
          <span className="text-[10px] text-white/30 tracking-[0.1em] font-mono">
            AGENT PIPELINE · LIVE
          </span>
        </div>
        <span className="text-[10px] text-white/[0.18] font-mono">
          3 agents · 0 errors
        </span>
      </div>

      {/* SVG Pipeline Visualization */}
      <svg width="100%" viewBox="0 0 580 172" className="block">
        <defs>
          <marker
            id="ma"
            viewBox="0 0 10 10"
            refX="8"
            refY="5"
            markerWidth="5"
            markerHeight="5"
            orient="auto"
          >
            <path
              d="M2 1.5L7.5 5L2 8.5"
              fill="none"
              stroke="rgba(0,82,255,0.45)"
              strokeWidth="1.6"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </marker>
        </defs>

        {/* Connection Paths */}
        <path
          d={paths.p1}
          fill="none"
          stroke="rgba(0,82,255,0.22)"
          strokeWidth="1.5"
          strokeDasharray="3 5"
          markerEnd="url(#ma)"
        />
        <path
          d={paths.p2}
          fill="none"
          stroke="rgba(0,82,255,0.22)"
          strokeWidth="1.5"
          strokeDasharray="3 5"
          markerEnd="url(#ma)"
        />
        <path
          d={paths.p3}
          fill="none"
          stroke="rgba(0,82,255,0.15)"
          strokeWidth="1.5"
          strokeDasharray="3 5"
        />
        <path
          d={paths.p4}
          fill="none"
          stroke="rgba(0,82,255,0.15)"
          strokeWidth="1.5"
          strokeDasharray="3 5"
        />
        <path
          d={paths.p5}
          fill="none"
          stroke="rgba(0,82,255,0.15)"
          strokeWidth="1.5"
          strokeDasharray="3 5"
        />

        {/* Animated dots along paths */}
        <AnimatedDot path={paths.p1} duration={1.05} delay={0} size={2.5} opacity={1} />
        <AnimatedDot path={paths.p1} duration={1.05} delay={0.35} size={1.8} opacity={0.65} />
        <AnimatedDot path={paths.p1} duration={1.05} delay={0.7} size={1.3} opacity={0.35} />

        <AnimatedDot path={paths.p2} duration={0.88} delay={0.18} size={2.5} opacity={1} />
        <AnimatedDot path={paths.p2} duration={0.88} delay={0.62} size={1.8} opacity={0.65} />

        <AnimatedDot path={paths.p3} duration={1.3} delay={0.08} size={2.2} opacity={0.9} />
        <AnimatedDot path={paths.p3} duration={1.3} delay={0.65} size={1.5} opacity={0.55} />

        <AnimatedDot path={paths.p4} duration={1.15} delay={0.28} size={2.2} opacity={0.9} />
        <AnimatedDot path={paths.p4} duration={1.15} delay={0.85} size={1.5} opacity={0.55} />

        <AnimatedDot path={paths.p5} duration={1.4} delay={0.45} size={2.2} opacity={0.9} />
        <AnimatedDot path={paths.p5} duration={1.4} delay={1.0} size={1.5} opacity={0.55} />

        {/* Trigger Node */}
        <rect
          x="16"
          y="66"
          width="100"
          height="44"
          rx="8"
          fill="#141414"
          stroke="rgba(255,255,255,0.09)"
          strokeWidth="0.5"
        />
        <text
          x="66"
          y="83"
          textAnchor="middle"
          fontSize="9.5"
          fill="rgba(255,255,255,0.28)"
          fontFamily="system-ui"
          letterSpacing=".07em"
        >
          TRIGGER
        </text>
        <text
          x="66"
          y="100"
          textAnchor="middle"
          fontSize="12"
          fill="rgba(255,255,255,0.82)"
          fontFamily="system-ui"
        >
          User Query
        </text>
        <text
          x="66"
          y="122"
          textAnchor="middle"
          fontSize="8.5"
          fill="rgba(255,255,255,0.18)"
          fontFamily="monospace"
        >
          node-01
        </text>

        {/* Vector DB Node */}
        <rect
          x="158"
          y="66"
          width="110"
          height="44"
          rx="8"
          fill="#141414"
          stroke="rgba(255,255,255,0.09)"
          strokeWidth="0.5"
        />
        <text
          x="213"
          y="83"
          textAnchor="middle"
          fontSize="9.5"
          fill="rgba(255,255,255,0.28)"
          fontFamily="system-ui"
          letterSpacing=".07em"
        >
          VECTOR DB
        </text>
        <text
          x="213"
          y="100"
          textAnchor="middle"
          fontSize="12"
          fill="rgba(255,255,255,0.82)"
          fontFamily="system-ui"
        >
          Semantic Search
        </text>
        <text
          x="213"
          y="122"
          textAnchor="middle"
          fontSize="8.5"
          fill="rgba(255,255,255,0.18)"
          fontFamily="monospace"
        >
          pinecone
        </text>

        {/* LLM Agent Node */}
        <rect
          x="306"
          y="53"
          width="105"
          height="70"
          rx="10"
          fill="#050D1C"
          stroke="#0052FF"
          strokeWidth="1"
        />
        <rect x="318" y="53.5" width="80" height="1" rx="0.5" fill="rgba(51,117,255,0.5)" />
        <text
          x="358"
          y="78"
          textAnchor="middle"
          fontSize="9.5"
          fill="rgba(51,117,255,0.65)"
          fontFamily="system-ui"
          letterSpacing=".07em"
        >
          LLM AGENT
        </text>
        <text
          x="358"
          y="97"
          textAnchor="middle"
          fontSize="13"
          fill="#fff"
          fontFamily="system-ui"
          fontWeight="500"
        >
          Processing
        </text>
        <PulsingDot cx={346} cy={113} color="#0052FF" duration={1.2} delay={0} />
        <PulsingDot cx={358} cy={113} color="#0052FF" duration={1.2} delay={0.4} />
        <PulsingDot cx={370} cy={113} color="#0052FF" duration={1.2} delay={0.8} />
        <text
          x="358"
          y="139"
          textAnchor="middle"
          fontSize="8.5"
          fill="rgba(0,82,255,0.4)"
          fontFamily="monospace"
        >
          claude-3-sonnet
        </text>

        {/* Output Nodes */}
        <rect
          x="448"
          y="35"
          width="116"
          height="30"
          rx="7"
          fill="#111"
          stroke="rgba(255,255,255,0.07)"
          strokeWidth="0.5"
        />
        <text
          x="490"
          y="53.5"
          textAnchor="middle"
          fontSize="11"
          fill="rgba(255,255,255,0.62)"
          fontFamily="system-ui"
        >
          Email Draft
        </text>
        <StatusIndicator cx={550} cy={43} color="#22c55e" />

        <rect
          x="448"
          y="73"
          width="116"
          height="30"
          rx="7"
          fill="#111"
          stroke="rgba(255,255,255,0.07)"
          strokeWidth="0.5"
        />
        <text
          x="490"
          y="91.5"
          textAnchor="middle"
          fontSize="11"
          fill="rgba(255,255,255,0.62)"
          fontFamily="system-ui"
        >
          CRM Update
        </text>
        <StatusIndicator cx={550} cy={81} color="#f59e0b" pulsing duration={1.9} />

        <rect
          x="448"
          y="111"
          width="116"
          height="30"
          rx="7"
          fill="#111"
          stroke="rgba(255,255,255,0.07)"
          strokeWidth="0.5"
        />
        <text
          x="490"
          y="129.5"
          textAnchor="middle"
          fontSize="11"
          fill="rgba(255,255,255,0.62)"
          fontFamily="system-ui"
        >
          Report Gen
        </text>
        <StatusIndicator cx={550} cy={119} color="#f59e0b" pulsing duration={2.2} delay={0.35} />
      </svg>

      {/* Message Display */}
      <div className="border-t border-white/[0.06] px-[18px] py-[9px] h-[52px]">
        <div className="flex gap-2 items-start h-full">
          <span className="text-[#0052FF]/55 font-mono text-[13px] leading-[1.5] shrink-0">
            ›
          </span>
          <div className="relative flex-1 overflow-hidden h-full">
            <AnimatePresence mode="wait">
              <motion.div
                key={messageIndex}
                initial={{ opacity: 0, y: 5 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -5 }}
                transition={{ duration: 0.25 }}
                className="font-mono text-[11px] text-white/[0.42] leading-[1.55] absolute inset-0"
              >
                {messages[messageIndex]}
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>

      {/* Stats Footer */}
      <div className="border-t border-white/[0.06] px-[18px] py-[10px] flex gap-[22px] items-center">
        <div>
          <div className="text-[9px] text-white/20 tracking-[0.09em] mb-[3px]">WORKFLOWS</div>
          <motion.div
            key={workflows}
            initial={{ scale: 1.05 }}
            animate={{ scale: 1 }}
            className="text-[16px] text-white/[0.72] font-mono"
          >
            {workflows.toLocaleString()}
          </motion.div>
        </div>
        <div>
          <div className="text-[9px] text-white/20 tracking-[0.09em] mb-[3px]">TOKENS</div>
          <div className="text-[16px] text-white/[0.72] font-mono">4.2M</div>
        </div>
        <div>
          <div className="text-[9px] text-white/20 tracking-[0.09em] mb-[3px]">AVG LATENCY</div>
          <div className="text-[16px] text-white/[0.72] font-mono">342ms</div>
        </div>
        <div className="ml-auto text-right">
          <div className="text-[9px] text-white/[0.18] tracking-[0.09em] mb-[3px]">STACK</div>
          <div className="text-[10px] text-[#0052FF]/55 font-mono">Claude · Pinecone</div>
        </div>
      </div>
    </div>
  )
}
