import React from "react";
import { Button } from "@/components/ui/Button";

// Basic functional root component (to be extended with actual UI)
export default function App() {
  return (
    <div className="min-h-screen bg-white text-slate-900 p-8">
      <h1 className="text-2xl font-bold mb-4">Hello, AI Minesweeper!</h1>
      <Button>Click me</Button>
    </div>
  );
}
