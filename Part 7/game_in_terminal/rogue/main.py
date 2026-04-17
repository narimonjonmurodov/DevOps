from rogue.presentation.curses_ui import CursesApp


# Launch the text UI and start the game loop
def main() -> None:
    CursesApp().run()


# Run main when executed directly
if __name__ == "__main__":
    main()

