import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App";

const container = document.getElementById("root");
// Create a React root and render the top-level App component into it
createRoot(container).render(<App />);
