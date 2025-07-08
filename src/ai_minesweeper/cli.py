import typer


app = typer.Typer()


@app.command()
def play(csv_path: str):
    """Play Minesweeper using a CSV board."""
    try:
        with open(csv_path, "r") as file:
            board = [line.strip().split(",") for line in file]
        print("Loaded board:")
        for row in board:
            print(" ".join(row))
        print("Game logic not yet implemented.")
    except FileNotFoundError:
        print(f"Error: File '{csv_path}' not found.")


@app.command()
def demo():
    print("Demo completed")


if __name__ == "__main__":
    app()
