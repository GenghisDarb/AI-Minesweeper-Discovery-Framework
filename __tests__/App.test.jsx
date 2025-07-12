import React from "react";
import { render, screen } from "@testing-library/react";
import App from "../src/App";

describe("App Component", () => {
  test("renders without crashing", () => {
    render(<App />);
    expect(screen.getByText(/Hello, AI Minesweeper!/i)).toBeInTheDocument();
  });

  // Additional tests can be updated here as needed
});
