import typer


app = typer.Typer()

@app.command()
def play(csv_path: str):
    
    # Placeholder for playing the game
    pass

@app.command()
def demo():
    print("Demo completed")

if __name__ == "__main__":
    app()
