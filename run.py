from app import app
from app.interaction import Console



def main():
    console = Console()
    console.run()
    app.run()


if __name__ == "__main__":
    main()
