import tkinter as tk

MAZE_WIDTH = 14
MAZE_HEIGHT = 14

MAZE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
    [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
]

GAME_DURATION: int = 15


def is_valid_move(x, y):
    if 0 <= x < MAZE_HEIGHT and 0 <= y < MAZE_WIDTH and MAZE[x][y] == 1:
        return True
    return False


class MazeSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Marvel Game")

        self.front_page_image = tk.PhotoImage(file="front_page_image.png")
        self.front_page_label = tk.Label(self.root, image=self.front_page_image)
        self.front_page_label.pack()
        self.canvas = tk.Canvas(self.root, width=MAZE_WIDTH * 40, height=MAZE_HEIGHT * 40)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_game)
        self.start_button.pack()
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_game)
        self.stop_button.pack()
        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game, state=tk.DISABLED)
        self.restart_button.pack()
        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo_move, state=tk.DISABLED)
        self.undo_button.pack()
        self.timer_label = tk.Label(self.root, text="Time Remaining: ")
        self.timer_label.pack()

        self.game_running = False
        self.timer = GAME_DURATION
        self.moves = []
        self.current_position = (1, 1)
        self.canvas.pack()
    def draw_maze(self):
        self.canvas.delete("all")
        for i in range(MAZE_HEIGHT):
            for j in range(MAZE_WIDTH):
                x1 = j * 40
                y1 = i * 40
                x2 = x1 + 40
                y2 = y1 + 40
                if MAZE[i][j] == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                elif (i, j) == self.current_position:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                elif (i, j) in self.moves:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow")

    def start_game(self):
        self.front_page_label.pack_forget()
        self.game_running = True
        self.start_button.configure(state=tk.DISABLED)
        self.restart_button.configure(state=tk.NORMAL)
        self.undo_button.configure(state=tk.NORMAL)
        self.timer = GAME_DURATION
        self.moves = []
        self.current_position = (1, 1)
        self.draw_maze()
        self.update_timer()

    def restart_game(self):
        self.timer_label.configure(text="Time Remaining: ")
        self.start_game()

    def undo_move(self):
        if len(self.moves) > 0:
            self.moves.pop()
            self.current_position = self.moves[-1]
            self.draw_maze()
    def stop_game(self):
        self.stop()

    def update_timer(self):
        if self.game_running and self.timer > 0:
            self.timer -= 1
            self.timer_label.configure(text=f"Time Remaining: {self.timer} seconds")
            self.root.after(1000, self.update_timer)
        elif self.timer == 0:
            self.timer_label.configure(text="Time's up!")
            self.game_running = False
            self.start_button.configure(state=tk.NORMAL)
            self.restart_button.configure(state=tk.DISABLED)
            self.undo_button.configure(state=tk.DISABLED)

    def move(self, dx, dy):
        if not self.game_running:
            return
        new_x = self.current_position[0] + dx
        new_y = self.current_position[1] + dy
        if is_valid_move(new_x, new_y):
            self.moves.append(self.current_position)
            self.current_position = (new_x, new_y)
            self.draw_maze()
        if (new_x, new_y) == (MAZE_HEIGHT - 2, MAZE_WIDTH - 2):
            self.game_running = False
            self.timer_label.configure(text="Congratulations! Maze solved.")
            self.start_button.configure(state=tk.NORMAL)
            self.restart_button.configure(state=tk.DISABLED)
            self.undo_button.configure(state=tk.DISABLED)

    def keypress_handler(self, event):
        if event.keysym == "Up":
            self.move(-1, 0)
        elif event.keysym == "Down":
            self.move(1, 0)
        elif event.keysym == "Left":
            self.move(0, -1)
        elif event.keysym == "Right":
            self.move(0, 1)

    def run(self):
        self.root.bind("<KeyPress>", self.keypress_handler)
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    maze_solver = MazeSolverGUI(root)
    maze_solver.run()
