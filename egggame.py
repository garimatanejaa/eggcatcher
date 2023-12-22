#egg catcher
from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font

my_canvas_width = 800
my_canvas_height = 400

my_root = Tk()
my_canvas = Canvas(my_root, width=my_canvas_width, height=my_canvas_height, background="light gray")
my_canvas.create_rectangle(-5, my_canvas_height-100, my_canvas_width+5, my_canvas_height+5, fill="light steel blue", width=0)
my_canvas.create_oval(-80, -80, 120, 120, fill='coral', width=0)
my_canvas.pack()

my_color_cycle = cycle(["light salmon", "light green", "light pink", "light yellow", "light cyan"])
my_egg_width = 45
my_egg_height = 55
my_egg_score = 10
my_egg_speed = 500
my_egg_interval = 4000
my_difficulty = 0.65
my_catcher_color = "dark slate gray"
my_catcher_width = 100
my_catcher_height = 100
my_catcher_start_x = my_canvas_width / 2 - my_catcher_width / 2
my_catcher_start_y = my_canvas_height - my_catcher_height - 20
my_catcher_start_x2 = my_catcher_start_x + my_catcher_width
my_catcher_start_y2 = my_catcher_start_y + my_catcher_height

my_catcher = my_canvas.create_arc(my_catcher_start_x, my_catcher_start_y, my_catcher_start_x2, my_catcher_start_y2, start=200, extent=140, style="arc", outline=my_catcher_color, width=3)
my_game_font = font.nametofont("TkFixedFont")
my_game_font.config(size=18)

my_score = 0
my_score_text = my_canvas.create_text(10, 10, anchor="nw", font=my_game_font, fill="dark orchid", text="Score: "+ str(my_score))

my_lives_remaining = 3
my_lives_text = my_canvas.create_text(my_canvas_width-10, 10, anchor="ne", font=my_game_font, fill="dark orchid", text="Lives: "+ str(my_lives_remaining))

my_eggs = []

# Function to create an egg
def create_egg():
    x = randrange(10, 740)
    y = 40
    new_egg = my_canvas.create_oval(x, y, x+my_egg_width, y+my_egg_height, fill=next(my_color_cycle), width=0)
    my_eggs.append(new_egg)
    my_root.after(my_egg_interval, create_egg)

# Function to move eggs
def move_eggs():
    for egg in my_eggs:
        try:
            (egg_x, egg_y, egg_x2, egg_y2) = my_canvas.coords(egg)
            my_canvas.move(egg, 0, 10)
            if egg_y2 > my_canvas_height:
                egg_dropped(egg)
        except tk.TclError as e:
            # Handle the exception, you can print an error message or take other actions
            print(f"Error in move_eggs: {e}")
    my_root.after(my_egg_speed, move_eggs)


# Function when an egg is dropped
def egg_dropped(egg):
    my_eggs.remove(egg)
    my_canvas.delete(egg)
    lose_a_life()
    if my_lives_remaining == 0:
        messagebox.showinfo("WHOOPS MISSED IT!", "Final Score: "+ str(my_score))
        my_root.destroy()

# Function to lose a life
def lose_a_life():
    global my_lives_remaining
    my_lives_remaining -= 1
    my_canvas.itemconfigure(my_lives_text, text="CHANCES: "+ str(my_lives_remaining))

# Function to check if an egg is caught
def check_catch():
    (catcher_x, catcher_y, catcher_x2, catcher_y2) = my_canvas.coords(my_catcher)
    for egg in my_eggs:
        (egg_x, egg_y, egg_x2, egg_y2) = my_canvas.coords(egg)
        if catcher_x < egg_x and egg_x2 < catcher_x2 and catcher_y2 - egg_y2 < 40:
            my_eggs.remove(egg)
            my_canvas.delete(egg)
            increase_score(my_egg_score)
    my_root.after(100, check_catch)

# Function to increase the score
def increase_score(points):
    global my_score, my_egg_speed, my_egg_interval
    my_score += points
    my_egg_speed = int(my_egg_speed * my_difficulty)
    my_egg_interval = int(my_egg_interval * my_difficulty)
    my_canvas.itemconfigure(my_score_text, text="Score: "+ str(my_score))

# Function to move the catcher to the left
def move_left(event):
    (x1, y1, x2, y2) = my_canvas.coords(my_catcher)
    if x1 > 0:
        my_canvas.move(my_catcher, -20, 0)

# Function to move the catcher to the right
def move_right(event):
    (x1, y1, x2, y2) = my_canvas.coords(my_catcher)
    if x2 < my_canvas_width:
        my_canvas.move(my_catcher, 20, 0)

# Bind key events
my_canvas.bind("<Left>", move_left)
my_canvas.bind("<Right>", move_right)
my_canvas.focus_set()

# Schedule the functions to run
my_root.after(1000, create_egg)
my_root.after(1000, move_eggs)
my_root.after(1000, check_catch)

# Start the Tkinter main loop
my_root.mainloop()
