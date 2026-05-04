"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { Send, Bot, User, LogOut, Paperclip, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { ThemeToggle } from "@/components/theme-toggle";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  file?: {
    name: string;
    size: number;
    type: string;
  };
}

interface UploadedFile {
  file: File;
  id: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content:
        "Hello! I'm your document chat assistant. Ask me anything about your documents.",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [docId, setDocId] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const newFiles: UploadedFile[] = Array.from(files).map((file) => ({
        file,
        id: `${Date.now()}-${file.name}`,
      }));
      setUploadedFiles((prev) => [...prev, ...newFiles]);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const removeFile = (id: string) => {
    setUploadedFiles((prev) => prev.filter((f) => f.id !== id));
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if ((!input.trim() && uploadedFiles.length === 0) || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
      // file:
      //   uploadedFiles.length > 0
      //     ? {
      //         name: uploadedFiles[0].file.name,
      //         size: uploadedFiles[0].file.size,
      //         type: uploadedFiles[0].file.type,
      //       }
      //     : undefined,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      let response;

      if (uploadedFiles.length > 0) {
        const formData = new FormData();
        uploadedFiles.forEach((uploadedFile) => {
          formData.append("file", uploadedFile.file);
        });

        response = await fetch("http://localhost:9000/upload", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();
        setDocId(data.doc_id);
        console.log("doc id: ", docId);
        setUploadedFiles([]);
      } else {
        response = await fetch("http://localhost:9000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            doc_id: docId,
            question: input,
          }),
        });
        const data = await response.json();

        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: data.response || "Sorry, I couldn't process that.",
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Sorry, something went wrong. Please try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      setUploadedFiles([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background overflow-hidden">
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-border bg-card">
        <div className="flex items-center gap-3">
          <Avatar className="h-10 w-10">
            <AvatarFallback className="bg-primary text-primary-foreground">
              <Bot className="h-6 w-6" />
            </AvatarFallback>
          </Avatar>
          <div>
            <h1 className="text-lg font-semibold">Document Chat</h1>
            <p className="text-sm text-muted-foreground">
              Ask questions about your documents
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/">
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </Link>
          </Button>
          <ThemeToggle />
        </div>
      </header>

      {/* Messages */}
      <ScrollArea className="h-[80vh] py-4 px-4">
        <div className="flex flex-col gap-4 max-w-3xl mx-auto">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start gap-3 ${
                message.role === "user" ? "flex-row-reverse" : ""
              }`}
            >
              <Avatar className="h-8 w-8">
                <AvatarFallback
                  className={
                    message.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-secondary text-secondary-foreground"
                  }
                >
                  {message.role === "user" ? (
                    <User className="h-4 w-4" />
                  ) : (
                    <Bot className="h-4 w-4" />
                  )}
                </AvatarFallback>
              </Avatar>
              <div
                className={`max-w-[75%] rounded-2xl px-4 py-3 ${
                  message.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-card border border-border"
                }`}
              >
                <p className="text-sm leading-relaxed">{message.content}</p>
                <p
                  className={`text-xs mt-1 ${
                    message.role === "user"
                      ? "text-primary-foreground/70"
                      : "text-muted-foreground"
                  }`}
                >
                  {message.timestamp.toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </p>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex items-start gap-3">
              <Avatar className="h-8 w-8">
                <AvatarFallback className="bg-secondary text-secondary-foreground">
                  <Bot className="h-4 w-4" />
                </AvatarFallback>
              </Avatar>
              <div className="bg-card border border-border rounded-2xl px-4 py-3">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" />
                  <span
                    className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                    style={{ animationDelay: "0.1s" }}
                  />
                  <span
                    className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  />
                </div>
              </div>
            </div>
          )}
          <div ref={scrollRef} />
        </div>
      </ScrollArea>

      {/* Input */}
      <footer className="border-t border-border bg-card px-4 py-4">
        <div className="max-w-3xl mx-auto">
          {uploadedFiles.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-3">
              {uploadedFiles.map((uploadedFile) => (
                <div
                  key={uploadedFile.id}
                  className="flex items-center gap-2 bg-secondary rounded-md px-3 py-1.5 text-sm"
                >
                  <Paperclip className="h-3.5 w-3.5 text-muted-foreground" />
                  <span className="max-w-37.5 truncate">
                    {uploadedFile.file.name}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    ({formatFileSize(uploadedFile.file.size)})
                  </span>
                  <button
                    type="button"
                    onClick={() => removeFile(uploadedFile.id)}
                    className="ml-1 hover:bg-muted rounded-full p-0.5"
                  >
                    <X className="h-3.5 w-3.5" />
                  </button>
                </div>
              ))}
            </div>
          )}
          <form onSubmit={handleSubmit} className="flex gap-3">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileSelect}
              className="hidden"
              multiple
            />
            <Button
              type="button"
              variant="outline"
              size="icon"
              onClick={() => fileInputRef.current?.click()}
              disabled={isLoading}
              className="shrink-0"
            >
              <Paperclip className="h-4 w-4" />
            </Button>
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1"
              disabled={isLoading}
            />
            <Button
              type="submit"
              size="icon"
              disabled={
                isLoading || (!input.trim() && uploadedFiles.length === 0)
              }
            >
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      </footer>
    </div>
  );
}
