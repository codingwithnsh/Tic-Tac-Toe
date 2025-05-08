import tkinter as tk
import random

# Initialize main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

player = "X"
mode = ""
buttons = []
game_over = False

def update_turn_label(p=None, text=None):
    if text:
        turn_label.config(text=text)
    else:
        turn_label.config(text=f"Turn: {'You (X)' if p == 'X' else 'Opponent (O)'}")

def check_winner():
    global game_over
    combos = [(0,1,2), (3,4,5), (6,7,8),
              (0,3,6), (1,4,7), (2,5,8),
              (0,4,8), (2,4,6)]
    for i, j, k in combos:
        if buttons[i]["text"] == buttons[j]["text"] == buttons[k]["text"] != "":
            game_over = True
            update_turn_label(text=f"{buttons[i]['text']} wins!")
            return True
    if all(b["text"] != "" for b in buttons):
        game_over = True
        update_turn_label(text="It's a tie!")
        return True
    return False

def ai_move():
    empty = [i for i, b in enumerate(buttons) if b["text"] == ""]
    if empty:
        index = random.choice(empty)
        buttons[index].config(text="O")
        check_winner()

def on_click(i):
    global player, game_over
    if buttons[i]["text"] != "" or game_over:
        return

    if player == "X":
        buttons[i].config(text="X")
        if not check_winner():
            if mode == "Single":
                update_turn_label(p="O")
                root.after(500, lambda: ai_turn())
            else:
                player = "O"
                update_turn_label(player)
    elif mode == "Two" and player == "O":
        buttons[i].config(text="O")
        if not check_winner():
            player = "X"
            update_turn_label(player)

def ai_turn():
    global player
    ai_move()
    if not check_winner():
        update_turn_label(p="X")
    player = "X"

def reset_game():
    global player, game_over
    for b in buttons:
        b.config(text="")
    game_over = False
    player = "X"
    update_turn_label(player)

def select_mode(chosen_mode):
    global mode
    mode = chosen_mode
    mode_frame.pack_forget()
    game_frame.pack()
    update_turn_label(player)

# Mode selection UI
mode_frame = tk.Frame(root)
tk.Label(mode_frame, text="Choose Mode", font=("Arial", 16)).pack(pady=10)
tk.Button(mode_frame, text="Single Player", font=("Arial", 12), command=lambda: select_mode("Single")).pack(pady=5)
tk.Button(mode_frame, text="Two Player", font=("Arial", 12), command=lambda: select_mode("Two")).pack(pady=5)
mode_frame.pack()

# Game UI (initially hidden)
game_frame = tk.Frame(root)

turn_label = tk.Label(game_frame, text="", font=("Arial", 14))
turn_label.grid(row=0, column=0, columnspan=3)

# Create 9 game buttons
for i in range(9):
    btn = tk.Button(game_frame, text="", font=("Arial", 24), width=5, height=2, command=lambda i=i: on_click(i))
    btn.grid(row=1 + i // 3, column=i % 3)
    buttons.append(btn)

# Reset button
tk.Button(game_frame, text="Reset", font=("Arial", 12), command=reset_game).grid(row=4, column=0, columnspan=3)

root.mainloop()
