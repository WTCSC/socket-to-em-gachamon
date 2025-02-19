import random
import time
import os


class Gachamon:
    def _init_(self):
        """
        Initialize game with 
        - starter Ui
        - base character
        - inventory
        - spawn
        """
        
        self.status = set()
        
        self.gacha = False

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def pull_animation(self):
        frames = [
            """
              *
            """,
            """
             \\
              *
            """,
            """
              *
             / 
            """,
            """
             \\
              *
             / 
            """,
            """
            \\
             \\ 
             *
              / 
               /
            """,
            """
             \\
              *
             / 
            """,
            """
            \\
             \\ 
              *
              / 
               /
            """,
            """
           *\ / *
            * * *
            * * *
          * * * * *
            """,
            """
           *     *
            * * *
          * * * * *
            """,
            """
            *   *
          *   *  *
            """,
            ""
        ]
        

        for i in range(1):
            for frame in frames:
                self.clear_screen()
                print(frame)
                time.sleep(0.8)

    def gacha(self):
        self.clear_screen()
        print("Starting the gacha pull...")
        self.pull_animation()

        # Random number between 1 and 100
        result = random.randint(1, 100)
        print(f"\nYou pulled a {result}!")
        if result <= 50:
            print("Better luck next time!")
        elif result <= 90:
            print("Nice pull!")
        else:
            print("Jackpot!")


    def draw_ui():
        ui_art = """
    +--------------------------------------+
    |            My Application            |
    +--------------------------------------+
    |  +----------+          +----------+  |
    |  |  Button  |          |  Button  |  |
    |  +----------+          +----------+  |
    +--------------------------------------+
    """
        print(ui_art)




