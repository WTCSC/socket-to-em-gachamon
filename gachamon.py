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
            time.sleep(3)
        elif result <= 90:
            print("Nice pull!")
            time.sleep(3)
        else:
            print("Jackpot!")
            time.sleep(3)

    # def handle_move_result(self, move: str, result: str) -> None:
    #     """
    #     Update game state based on the result of player's move:
    #     - Tracks shots and hits
    #     - Displays appropriate ASCII art for feedback
    #     - Shows victory message if game is won
    #     """
    #     if not result or result in ["invalid", "repeat"]:
    #         return
            
    #     col = ord(move[0].upper()) - ord('A')
    #     row = int(move[1:])
    #     self.shots.add((col, row))
        
    #     if "hit" in result:
    #         self.hits.add((col, row))
    #         print(f"{HIT_ART}")
    #         if "sunk" in result:
    #             print(f"{SUNK_ART}")
    #     elif "miss" in result:
    #         print(f"{MISS_ART}")
    #     elif result == "gameover":
    #         print(f"{WIN_ART}")

    def display_health_bar(health_percentage):
        total_blocks = 20
        filled_blocks = int(total_blocks * (health_percentage / 100))
        empty_blocks = total_blocks - filled_blocks

        health_bar = "[" + "█" * filled_blocks + " " * empty_blocks + "]"
        print(f"Health: {health_bar} {health_percentage}%")





