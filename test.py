# import os
# import time

# def print_filled_square(size):
#     for i in range(size):
#         print("█" * size)

# def clear_screen():
#     os.system('cls' if os.name == 'nt' else 'clear')

# def print_static_text(text):
#     lines = text.split('\n')
#     for line in lines:
#         print(line)

# # Set the size of the square, the blink interval, and the static text
# square_size = 5
# blink_interval = 0.5  # in seconds
# static_text = "This is static text.\nIt does not blink."

# while True:
#     clear_screen()
#     print_static_text(static_text)
#     print_filled_square(square_size)
#     time.sleep(blink_interval)
#     clear_screen()
#     print_static_text(static_text)
#     time.sleep(blink_interval)

#192.168.56.1
#192.168.1.27
#python server.py
#python client.py

import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_shooting_star(position, ground_level, star_art, shine_art):
    for i in range(position):
        print()
    print(star_art)
    print(shine_art)
    for i in range(ground_level - position):
        print()

# ASCII art shooting star
star_art = """
         .                      .
         .                      ;
         :                  - --+- -
         !           .          !
         |        .             .
         |_         +
      ,  | `.
--- --+-<#>-+- ---  --  -
      `._|_,'
         T
         |
         !
         :         . : 
         .       *
shooting star
"""

# Fixed ASCII art for shine
shine_art = """
         .                      .
         .                      ;
         :                  - --+- -
         !           .          !
         |        .             .
         |         +            
         |                      
         +                      
         ,        *            
--- --+-<#>-+- ---  --  -
         *                      
         T         +             
         |                      
         !                      
         :         *             
         .        .              
"""

# Set the initial position, ground level, and fall speed
initial_position = 0
ground_level = 10
fall_speed = 0.3  # in seconds

position = initial_position

while position <= ground_level:
    clear_screen()
    print_shooting_star(position, ground_level, star_art, shine_art)
    time.sleep(fall_speed)
    position += 1

clear_screen()
print("Shooting star has merged with the ground!")
