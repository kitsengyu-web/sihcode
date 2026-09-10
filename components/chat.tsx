"use client";

import React, { useState, useRef, useEffect, useCallback } from "react";
import { Plus, ChevronDown, ArrowUp, X, FileText, Loader2, Check, Archive } from "lucide-react";

/* --- ICONS --- */
export const Icons = {
  Logo: (props: React.SVGProps<SVGSVGElement>) => (
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" role="presentation" {...props}>
      <defs>
        <ellipse id="petal-pair" cx="100" cy="100" rx="90" ry="22" />
      </defs>
      <g fill="#D46B4F" fillRule="evenodd">
        <use href="#petal-pair" transform="rotate(0 100 100)" />
        <use href="#petal-pair" transform="rotate(45 100 100)" />
        <use href="#petal-pair" transform="rotate(90 100 100)" />
        <use href="#petal-pair" transform="rotate(135 100 100)" />
      </g>
    </svg>
  ),
  Plus: Plus,
  Thinking: (props: React.SVGProps<SVGSVGElement>) => (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" {...props}>
      <path d="M10.3857 2.50977C14.3486 2.71054 17.5 5.98724 17.5 10C17.5 14.1421 14.1421 17.5 10 17.5C5.85786 17.5 2.5 14.1421 2.5 10C2.5 9.72386 2.72386 9.5 3 9.5C3.27614 9.5 3.5 9.72386 3.5 10C3.5 13.5899 6.41015 16.5 10 16.5C13.5899 16.5 16.5 13.5899 16.5 10C16.5 6.5225 13.7691 3.68312 10.335 3.50879L10 3.5L9.89941 3.49023C9.67145 3.44371 9.5 3.24171 9.5 3C9.5 2.72386 9.72386 2.5 10 2.5L10.3857 2.50977ZM10 5.5C10.2761 5.5 10.5 5.72386 10.5 6V9.69043L13.2236 11.0527C13.4706 11.1762 13.5708 11.4766 13.4473 11.7236C13.3392 11.9397 13.0957 12.0435 12.8711 11.9834L12.7764 11.9473L9.77637 10.4473C9.60698 10.3626 9.5 10.1894 9.5 10V6C9.5 5.72386 9.72386 5.5 10 5.5ZM3.66211 6.94141C4.0273 6.94159 4.32303 7.23735 4.32324 7.60254C4.32324 7.96791 4.02743 8.26446 3.66211 8.26465C3.29663 8.26465 3 7.96802 3 7.60254C3.00021 7.23723 3.29676 6.94141 3.66211 6.94141ZM4.95605 4.29395C5.32146 4.29404 5.61719 4.59063 5.61719 4.95605C5.6171 5.3214 5.3214 5.61709 4.95605 5.61719C4.59063 5.61719 4.29403 5.32146 4.29395 4.95605C4.29395 4.59057 4.59057 4.29395 4.95605 4.29395ZM7.60254 3C7.96802 3 8.26465 3.29663 8.26465 3.66211C8.26446 4.02743 7.96791 4.32324 7.60254 4.32324C7.23736 4.32302 6.94159 4.0273 6.94141 3.66211C6.94141 3.29676 7.23724 3.00022 7.60254 3Z"></path>
    </svg>
  ),
  SelectArrow: ChevronDown,
  ArrowUp: ArrowUp,
  X: X,
  FileText: FileText,
  Loader2: Loader2,
  Check: Check,
  Archive: Archive,
};

/* --- UTILS --- */
const formatFileSize = (bytes: number) => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

/* --- TYPES --- */
interface AttachedFile {
  id: string;
  file: File;
  type: string;
  preview: string | null;
  uploadStatus: string;
  content?: string;
}

interface PastedContentItem {
  id: string;
  content: string;
  timestamp: Date;
}

/* --- COMPONENTS --- */

// 1. File Preview Card
interface FilePreviewCardProps {
  file: AttachedFile;
  onRemove: (id: string) => void;
}

const FilePreviewCard: React.FC<FilePreviewCardProps> = ({ file, onRemove }) => {
  const isImage = file.type.startsWith("image/") && file.preview;

  return (
    <div className="relative group flex-shrink-0 w-24 h-24 rounded-xl overflow-hidden border border-zinc-700 bg-zinc-800 transition-all hover:border-zinc-500">
      {isImage ? (
        <div className="w-full h-full relative">
          <img src={file.preview!} alt={file.file.name} className="w-full h-full object-cover" />
          <div className="absolute inset-0 bg-black/20 group-hover:bg-black/0 transition-colors" />
        </div>
      ) : (
        <div className="w-full h-full p-3 flex flex-col justify-between">
          <div className="flex items-center gap-2">
            <div className="p-1.5 bg-zinc-700 rounded">
              <Icons.FileText className="w-4 h-4 text-zinc-300" />
            </div>
            <span className="text-[10px] font-medium text-zinc-400 uppercase tracking-wider truncate">
              {file.file.name.split(".").pop()}
            </span>
          </div>
          <div className="space-y-0.5">
            <p className="text-xs font-medium text-zinc-200 truncate" title={file.file.name}>
              {file.file.name}
            </p>
            <p className="text-[10px] text-zinc-400">{formatFileSize(file.file.size)}</p>
          </div>
        </div>
      )}

      <button
        onClick={() => onRemove(file.id)}
        className="absolute top-1 right-1 p-1 bg-black/50 hover:bg-black/70 rounded-full text-white opacity-0 group-hover:opacity-100 transition-opacity"
      >
        <Icons.X className="w-3 h-3" />
      </button>

      {file.uploadStatus === "uploading" && (
        <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
          <Icons.Loader2 className="w-5 h-5 text-white animate-spin" />
        </div>
      )}
    </div>
  );
};

// 2. Pasted Content Card
interface PastedContentCardProps {
  content: PastedContentItem;
  onRemove: (id: string) => void;
}

const PastedContentCard: React.FC<PastedContentCardProps> = ({ content, onRemove }) => {
  return (
    <div className="relative group flex-shrink-0 w-28 h-28 rounded-2xl overflow-hidden border border-zinc-700 bg-zinc-800 p-3 flex flex-col justify-between shadow-sm">
      <div className="overflow-hidden w-full">
        <p className="text-[10px] text-zinc-400 leading-[1.4] font-mono break-words whitespace-pre-wrap line-clamp-4 select-none">
          {content.content}
        </p>
      </div>

      <div className="flex items-center justify-between w-full mt-2">
        <div className="inline-flex items-center justify-center px-1.5 py-[2px] rounded border border-zinc-700 bg-zinc-900">
          <span className="text-[9px] font-bold text-zinc-400 uppercase tracking-wider font-sans">PASTED</span>
        </div>
      </div>

      <button
        onClick={() => onRemove(content.id)}
        className="absolute top-2 right-2 p-[3px] bg-zinc-800 border border-zinc-700 rounded-full text-zinc-400 hover:text-white transition-colors opacity-0 group-hover:opacity-100"
      >
        <Icons.X className="w-2.5 h-2.5" />
      </button>
    </div>
  );
};

// 3. Model Selector
interface Model {
  id: string;
  name: string;
  description: string;
  badge?: string;
}

interface ModelSelectorProps {
  models: Model[];
  selectedModel: string;
  onSelect: (modelId: string) => void;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({ models, selectedModel, onSelect }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const currentModel = models.find((m) => m.id === selectedModel) || models[0];

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`inline-flex items-center justify-center relative shrink-0 transition duration-200 h-8 rounded-xl px-3 min-w-[4rem] active:scale-[0.98] whitespace-nowrap text-xs gap-1 ${
          isOpen
            ? "bg-zinc-700 text-white"
            : "text-zinc-300 hover:text-white hover:bg-zinc-800"
        }`}
      >
        <div className="inline-flex gap-[3px] text-[14px] leading-none items-baseline">
          <span className="whitespace-nowrap select-none font-medium">{currentModel.name}</span>
        </div>
        <Icons.SelectArrow className={`w-4 h-4 opacity-75 transition-transform duration-200 ${isOpen ? "rotate-180" : ""}`} />
      </button>

      {isOpen && (
        <div className="absolute bottom-full right-0 mb-2 w-[260px] bg-zinc-900 border border-zinc-700 rounded-2xl shadow-2xl overflow-hidden z-50 flex flex-col p-1.5 origin-bottom-right">
          {models.map((model) => (
            <button
              key={model.id}
              onClick={() => {
                onSelect(model.id);
                setIsOpen(false);
              }}
              className="w-full text-left px-3 py-2.5 rounded-xl flex items-start justify-between group transition-colors hover:bg-zinc-800"
            >
              <div className="flex flex-col gap-0.5">
                <div className="flex items-center gap-2">
                  <span className="text-[13px] font-semibold text-white">{model.name}</span>
                  {model.badge && (
                    <span
                      className={`px-1.5 py-[1px] rounded-full text-[10px] font-medium border ${
                        model.badge === "Upgrade"
                          ? "border-blue-500/30 text-blue-400 bg-blue-500/10"
                          : "border-zinc-700 text-zinc-400"
                      }`}
                    >
                      {model.badge}
                    </span>
                  )}
                </div>
                <span className="text-[11px] text-zinc-400">{model.description}</span>
              </div>
              {selectedModel === model.id && <Icons.Check className="w-4 h-4 text-blue-400 mt-1" />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

// 4. Main Input Component
interface ClaudeChatInputProps {
  onSendMessage?: (data: {
    message: string;
    files: AttachedFile[];
    pastedContent: PastedContentItem[];
    model: string;
    isThinkingEnabled: boolean;
  }) => void;
}

export const ClaudeChatInput: React.FC<ClaudeChatInputProps> = ({ onSendMessage }) => {
  const [message, setMessage] = useState("");
  const [files, setFiles] = useState<AttachedFile[]>([]);
  const [pastedContent, setPastedContent] = useState<PastedContentItem[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [selectedModel, setSelectedModel] = useState("sonnet-4.5");
  const [isThinkingEnabled, setIsThinkingEnabled] = useState(false);

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const models = [
    { id: "opus-4.5", name: "Opus 4.5", description: "Most capable for complex work" },
    { id: "sonnet-4.5", name: "Sonnet 4.5", description: "Best for everyday tasks" },
    { id: "haiku-4.5", name: "Haiku 4.5", description: "Fastest for quick answers" },
  ];

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 384) + "px";
    }
  }, [message]);

  const handleFiles = useCallback((newFilesList: FileList | File[]) => {
    const newFiles = Array.from(newFilesList).map((file) => {
      const isImage = file.type.startsWith("image/") || /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(file.name);
      return {
        id: Math.random().toString(36).substr(2, 9),
        file,
        type: isImage ? "image/unknown" : file.type || "application/octet-stream",
        preview: isImage ? URL.createObjectURL(file) : null,
        uploadStatus: "pending",
      };
    });

    setFiles((prev) => [...prev, ...newFiles]);

    newFiles.forEach((f) => {
      setTimeout(() => {
        setFiles((prev) => prev.map((p) => (p.id === f.id ? { ...p, uploadStatus: "complete" } : p)));
      }, 800 + Math.random() * 1000);
    });
  }, []);

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };
  const onDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };
  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files) handleFiles(e.dataTransfer.files);
  };

  const handlePaste = (e: React.ClipboardEvent) => {
    const items = e.clipboardData.items;
    const pastedFiles: File[] = [];
    for (let i = 0; i < items.length; i++) {
      if (items[i].kind === "file") {
        const file = items[i].getAsFile();
        if (file) pastedFiles.push(file);
      }
    }

    if (pastedFiles.length > 0) {
      e.preventDefault();
      handleFiles(pastedFiles);
      return;
    }

    const text = e.clipboardData.getData("text");
    if (text.length > 300) {
      e.preventDefault();
      const snippet = {
        id: Math.random().toString(36).substr(2, 9),
        content: text,
        timestamp: new Date(),
      };
      setPastedContent((prev) => [...prev, snippet]);
    }
  };

  const handleSend = () => {
    if (!message.trim() && files.length === 0 && pastedContent.length === 0) return;
    if (onSendMessage) {
      onSendMessage({ message, files, pastedContent, model: selectedModel, isThinkingEnabled });
    }
    setMessage("");
    setFiles([]);
    setPastedContent([]);
    if (textareaRef.current) textareaRef.current.style.height = "auto";
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const hasContent = message.trim() || files.length > 0 || pastedContent.length > 0;

  return (
    <div
      className="relative w-full max-w-3xl mx-auto transition-all duration-300 font-sans"
      onDragOver={onDragOver}
      onDragLeave={onDragLeave}
      onDrop={onDrop}
    >
      <div className="flex flex-col mx-2 md:mx-0 items-stretch transition-all duration-200 relative z-10 rounded-2xl border border-zinc-800 bg-[#18181b] p-3 shadow-2xl">
        {(files.length > 0 || pastedContent.length > 0) && (
          <div className="flex gap-3 overflow-x-auto pb-2 px-1">
            {pastedContent.map((content) => (
              <PastedContentCard
                key={content.id}
                content={content}
                onRemove={(id) => setPastedContent((prev) => prev.filter((c) => c.id !== id))}
              />
            ))}
            {files.map((file) => (
              <FilePreviewCard
                key={file.id}
                file={file}
                onRemove={(id) => setFiles((prev) => prev.filter((f) => f.id !== id))}
              />
            ))}
          </div>
        )}

        <div className="relative mb-2">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onPaste={handlePaste}
            onKeyDown={handleKeyDown}
            placeholder="How can I help you today?"
            className="w-full bg-transparent border-0 outline-none text-white text-[16px] placeholder:text-zinc-500 resize-none py-1 leading-relaxed block font-normal antialiased min-h-[2.5rem]"
            rows={1}
            autoFocus
          />
        </div>

        <div className="flex gap-2 w-full items-center justify-between pt-1">
          <div className="flex items-center gap-1">
            <button
              onClick={() => fileInputRef.current?.click()}
              className="inline-flex items-center justify-center h-8 w-8 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors"
              type="button"
            >
              <Icons.Plus className="w-5 h-5" />
            </button>

            <button
              onClick={() => setIsThinkingEnabled(!isThinkingEnabled)}
              className={`h-8 w-8 flex items-center justify-center rounded-lg transition-all ${
                isThinkingEnabled ? "text-amber-400 bg-amber-400/10" : "text-zinc-400 hover:text-white hover:bg-zinc-800"
              }`}
              type="button"
            >
              <Icons.Thinking className="w-5 h-5" />
            </button>
          </div>

          <div className="flex items-center gap-2">
            <ModelSelector models={models} selectedModel={selectedModel} onSelect={setSelectedModel} />

            <button
              onClick={handleSend}
              disabled={!hasContent}
              className={`inline-flex items-center justify-center h-8 w-8 rounded-xl transition-all ${
                hasContent ? "bg-white text-black hover:bg-zinc-200" : "bg-zinc-800 text-zinc-600 cursor-not-allowed"
              }`}
              type="button"
            >
              <Icons.ArrowUp className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {isDragging && (
        <div className="absolute inset-0 bg-zinc-900/90 border-2 border-dashed border-zinc-500 rounded-2xl z-50 flex flex-col items-center justify-center backdrop-blur-sm pointer-events-none">
          <Icons.Archive className="w-10 h-10 text-zinc-300 mb-2 animate-bounce" />
          <p className="text-zinc-200 font-medium">Drop files to upload</p>
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        multiple
        className="hidden"
        onChange={(e) => {
          if (e.target.files) handleFiles(e.target.files);
          e.target.value = "";
        }}
      />

      <div className="text-center mt-3">
        <p className="text-xs text-zinc-500">AI can make mistakes. Please check important information.</p>
      </div>
    </div>
  );
};

export default function ChatPage() {
  return (
    <div className="w-full flex-1 flex flex-col justify-center items-center p-4">
      <ClaudeChatInput />
    </div>
  );
}
