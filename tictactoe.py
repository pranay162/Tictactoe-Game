import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Scrollbar, Text
from PIL import Image, ImageTk
import os

class TicTacToePro:
    def __init__(self, root):
        self.root = root
        self.root.title("🏆 Ultimate Tic Tac Toe")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        self.bg_image = Image.open("background.jpg")
        self.bg_image = self.bg_image.resize((600, 750))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.current_player = "X"
        self.timer_seconds = 20
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.timer_running = False
        self.player_X = simpledialog.askstring("Player X", "Enter name for Player X:")
        self.player_O = simpledialog.askstring("Player O", "Enter name for Player O:")
        self.player_X = self.player_X or "Player X"
        self.player_O = self.player_O or "Player O"
        self.scores = {"X": 0, "O": 0}
        self.status_label = tk.Label(root, text=f"{self.player_X}'s Turn (X)", font=("Arial", 18, "bold"),
                                     bg="#000000", fg="#f5c518")
        self.status_label.place(x=20, y=20)

        self.timer_label = tk.Label(root, text=f"⏱️ Time left: {self.timer_seconds}s", font=("Arial", 14),
                                    bg="#000000", fg="lightblue")
        self.timer_label.place(x=400, y=25)

        self.score_label = tk.Label(root, text=self.get_score_text(), font=("Arial", 14),
                                    bg="#000000", fg="white")
        self.score_label.place(x=20, y=60)

        self.build_board()
        self.reset_btn = tk.Button(root, text="🔁 Reset Game", font=("Arial", 12), command=self.reset_game)
        self.reset_btn.place(x=20, y=670)

        self.view_lb_btn = tk.Button(root, text="📊 View Leaderboard", font=("Arial", 12),
                                     command=self.show_leaderboard)
        self.view_lb_btn.place(x=160, y=670)

        self.clear_lb_btn = tk.Button(root, text="🧹 Clear Leaderboard", font=("Arial", 12),
                                      command=self.clear_leaderboard)
        self.clear_lb_btn.place(x=340, y=670)

        self.start_timer()

    def build_board(self):
        board_frame = tk.Frame(self.root, bg="#000000")
        board_frame.place(x=80, y=120)
        for i in range(3):
            for j in range(3):
                btn = tk.Button(board_frame, text="", font=("Helvetica", 32, "bold"),
                                bg="#1f1f2e", fg="white", width=4, height=2,
                                activebackground="#3a3a5a",
                                command=lambda r=i, c=j: self.make_move(r, c))
                btn.grid(row=i, column=j, padx=15, pady=15)
                self.buttons[i][j] = btn

    def get_score_text(self):
        return f"⭐ {self.player_X} (X): {self.scores['X']}   |   {self.player_O} (O): {self.scores['O']} ⭐"

    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            self.stop_timer()

            if self.check_winner(row, col):
                self.highlight_winner(self.winning_cells)
                winner_name = self.player_X if self.current_player == "X" else self.player_O
                self.scores[self.current_player] += 1
                self.status_label.config(text=f"🎉 {winner_name} Wins!")
                self.score_label.config(text=self.get_score_text())
                self.save_leaderboard(winner_name)
                self.disable_all_buttons()
                return

            elif self.is_draw():
                self.status_label.config(text="🤝 It's a Draw!")
                return

            self.switch_player()
            self.start_timer()

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        next_name = self.player_X if self.current_player == "X" else self.player_O
        self.status_label.config(text=f"{next_name}'s Turn ({self.current_player})")

    def check_winner(self, row, col):
        b = self.board
        p = self.current_player

        if all(b[row][c] == p for c in range(3)):
            self.winning_cells = [(row, c) for c in range(3)]
            return True
        if all(b[r][col] == p for r in range(3)):
            self.winning_cells = [(r, col) for r in range(3)]
            return True
        if row == col and all(b[i][i] == p for i in range(3)):
            self.winning_cells = [(i, i) for i in range(3)]
            return True
        if row + col == 2 and all(b[i][2 - i] == p for i in range(3)):
            self.winning_cells = [(i, 2 - i) for i in range(3)]
            return True
        return False

    def is_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def highlight_winner(self, cells):
        for r, c in cells:
            self.buttons[r][c].config(bg="#27ae60")

    def disable_all_buttons(self):
        self.stop_timer()
        for row in self.buttons:
            for btn in row:
                btn.config(state=tk.DISABLED)

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.status_label.config(text=f"{self.player_X}'s Turn (X)")
        for i in range(3):
            for j in range(3):
                btn = self.buttons[i][j]
                btn.config(text="", state=tk.NORMAL, bg="#1f1f2e")
        self.start_timer()

    def start_timer(self):
        self.time_left = self.timer_seconds
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.timer_label.config(text=f"⏱️ Time left: {self.time_left}s")
            if self.time_left <= 0:
                self.timer_label.config(text="⏱️ Time's up!")
                messagebox.showinfo("⏳ Timeout", f"{self.get_current_name()} ran out of time!")
                self.switch_player()
                self.start_timer()
                return
            self.time_left -= 1
            self.root.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_running = False

    def get_current_name(self):
        return self.player_X if self.current_player == "X" else self.player_O

    def save_leaderboard(self, winner_name):
        with open("leaderboard.txt", "a") as f:
            f.write(f"{winner_name} won a game!\n")

    def show_leaderboard(self):
        if not os.path.exists("leaderboard.txt"):
            messagebox.showinfo("Leaderboard", "No games played yet.")
            return

        lb_window = Toplevel(self.root)
        lb_window.title("📊 Leaderboard")
        lb_window.geometry("400x300")

        text_box = Text(lb_window, font=("Arial", 12))
        text_box.pack(expand=True, fill="both")

        with open("leaderboard.txt", "r") as f:
            content = f.read()
            text_box.insert("1.0", content)

        text_box.config(state=tk.DISABLED)

    def clear_leaderboard(self):
        if os.path.exists("leaderboard.txt"):
            os.remove("leaderboard.txt")
            messagebox.showinfo("Leaderboard", "Leaderboard cleared!")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToePro(root)
    root.mainloop()
