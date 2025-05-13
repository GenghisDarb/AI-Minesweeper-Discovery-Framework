import typer

app = typer.Typer()

@app.command()
def play(csv_path: str):
    board = BoardBuilder.from_csv(csv_path)
    # Placeholder for playing the game
    pass

@app.command()
def demo():
    print("Demo completed")

if __name__ == "__main__":
    app()
