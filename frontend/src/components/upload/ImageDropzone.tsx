"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, X, Image as ImageIcon, CheckCircle } from "lucide-react";
import { cn, formatFileSize } from "@/lib/utils";

interface ImageDropzoneProps {
  onImageSelect: (file: File) => void;
  onClear?: () => void;
  accept?: string[];
  maxSize?: number;
  label?: string;
  sublabel?: string;
  className?: string;
  disabled?: boolean;
}

export default function ImageDropzone({
  onImageSelect,
  onClear,
  accept = ["image/jpeg", "image/png", "image/webp"],
  maxSize = 10 * 1024 * 1024,
  label = "Drop your image here",
  sublabel = "or click to browse (JPEG, PNG, WebP — max 10MB)",
  className,
  disabled = false,
}: ImageDropzoneProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [fileSize, setFileSize] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      setError(null);
      if (acceptedFiles.length === 0) return;

      const file = acceptedFiles[0];
      if (file.size > maxSize) {
        setError(`File too large. Max size: ${formatFileSize(maxSize)}`);
        return;
      }

      setFileName(file.name);
      setFileSize(file.size);

      const reader = new FileReader();
      reader.onload = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);

      onImageSelect(file);
    },
    [onImageSelect, maxSize]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: accept.reduce((acc, type) => ({ ...acc, [type]: [] }), {}),
    maxFiles: 1,
    disabled,
    onDropRejected: (rejections) => {
      const rejection = rejections[0];
      if (rejection?.errors[0]?.code === "file-too-large") {
        setError(`File too large. Max size: ${formatFileSize(maxSize)}`);
      } else if (rejection?.errors[0]?.code === "file-invalid-type") {
        setError("Invalid file type. Please upload JPEG, PNG, or WebP.");
      } else {
        setError("File rejected. Please try again.");
      }
    },
  });

  const handleClear = (e: React.MouseEvent) => {
    e.stopPropagation();
    setPreview(null);
    setFileName(null);
    setFileSize(0);
    setError(null);
    onClear?.();
  };

  return (
    <div className={cn("w-full", className)}>
      <div
        {...getRootProps()}
        className={cn(
          "upload-zone relative flex flex-col items-center justify-center min-h-[260px] p-8 transition-all duration-300",
          isDragActive && "active scale-[1.01]",
          disabled && "opacity-50 cursor-not-allowed",
          preview && "border-[var(--color-primary)] bg-[var(--color-primary-subtle)]"
        )}
      >
        <input {...getInputProps()} />

        <AnimatePresence mode="wait">
          {preview ? (
            <motion.div
              key="preview"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="relative w-full flex flex-col items-center"
            >
              {/* Clear button */}
              <button
                onClick={handleClear}
                className="absolute -top-2 -right-2 z-10 w-8 h-8 rounded-full bg-[var(--color-accent-red)] flex items-center justify-center hover:scale-110 transition-transform"
              >
                <X className="w-4 h-4 text-white" />
              </button>

              {/* Preview image */}
              <div className="relative w-full max-w-xs aspect-square rounded-xl overflow-hidden border border-[var(--color-border-glow)]">
                <img
                  src={preview}
                  alt="Upload preview"
                  className="w-full h-full object-cover"
                />
                {/* Scan line effect */}
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                  <div
                    className="absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-[var(--color-primary)] to-transparent opacity-60"
                    style={{ animation: "scan-line 2s linear infinite" }}
                  />
                </div>
              </div>

              {/* File info */}
              <div className="mt-4 flex items-center gap-2 text-sm">
                <CheckCircle className="w-4 h-4 text-[var(--color-primary)]" />
                <span className="text-[var(--color-text-secondary)]">
                  {fileName}
                </span>
                <span className="text-[var(--color-text-muted)]">
                  ({formatFileSize(fileSize)})
                </span>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="upload"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center text-center"
            >
              <motion.div
                animate={isDragActive ? { scale: 1.1, y: -5 } : { scale: 1, y: 0 }}
                className="w-16 h-16 rounded-2xl bg-[var(--color-primary-subtle)] border border-[var(--color-border-glow)] flex items-center justify-center mb-4"
              >
                {isDragActive ? (
                  <ImageIcon className="w-7 h-7 text-[var(--color-primary)]" />
                ) : (
                  <Upload className="w-7 h-7 text-[var(--color-primary)]" />
                )}
              </motion.div>

              <p className="text-base font-medium text-[var(--color-text-primary)] mb-1">
                {isDragActive ? "Release to upload" : label}
              </p>
              <p className="text-sm text-[var(--color-text-muted)]">
                {sublabel}
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Error */}
      <AnimatePresence>
        {error && (
          <motion.p
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="mt-2 text-sm text-[var(--color-accent-red)] flex items-center gap-1.5"
          >
            <X className="w-3.5 h-3.5" />
            {error}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
}
