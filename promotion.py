import tkinter as tk
import ChessEngine as chess
from tkinter import PhotoImage
from PIL import Image, ImageTk
def center_window(window):
    window.update_idletasks()  

    # Get the window size
    window_width = window.winfo_width()
    window_height = window.winfo_height()

    # Get the screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position x and y coordinates
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the dimensions and position of the window
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')

def disable_close():
    pass


class Promotion(tk.Tk):
    def __init__(self,piece):
        super().__init__()
        self.piece = piece
        self.title("PAWN PROMOTION")
        self.promote = "--"
        self.title = "Pawn Promotion"
        self.img_queen = Image.open(f"images/{self.piece}Q.png")
        self.img_queen = ImageTk.PhotoImage(self.img_queen)
        self.img_rook = Image.open(f"images/{self.piece}R.png")
        self.img_rook = ImageTk.PhotoImage(self.img_rook)
        self.img_bishop = Image.open(f"images/{self.piece}B.png")
        self.img_bishop = ImageTk.PhotoImage(self.img_bishop)
        self.img_knight = Image.open(f"images/{self.piece}N.png")
        self.img_knight = ImageTk.PhotoImage(self.img_knight)
        self.protocol("WM_DELETE_WINDOW", disable_close)
        self.resizable(False,False)

        self.window_frame = tk.Frame(self)
        self.window_frame.grid(row=0,column=0)
        self.queenButton = tk.Button(self.window_frame,text="Queen", image=self.img_queen , padx=20,pady=50,command = self.promoteQueen)
        self.queenButton.grid(row=0,column=0)
        self.bishopButton = tk.Button(self.window_frame,text="Bishop",image=self.img_bishop,padx=20,pady=50,command = self.promoteBishop)
        self.bishopButton.grid(row=0,column=1)
        self.rookButton = tk.Button(self.window_frame,text="Rook",image=self.img_rook,padx=20,pady=50,command = self.promoteRook)
        self.rookButton.grid(row=0,column=2)
        self.knightButton = tk.Button(self.window_frame,text="Knight",image=self.img_knight,padx=20,pady=50, command = self.promoteKnight)
        self.knightButton.grid(row=0,column=3)
        center_window(self)
    def promoteQueen(self):
        if self.piece == "w":
            self.promote = "wQ" 
        else:
            self.promote = "bQ"
        self.destroy()
    def promoteBishop(self):
        if self.piece == "w":
            self.promote = "wB" 
        else:
            self.promote = "bB"
        self.destroy()

    def promoteKnight(self):
        if self.piece == "w":
            self.promote = "wN" 
        else:
            self.promote = "bN"
        self.destroy()

    def promoteRook(self):
        if self.piece == "w":
            self.promote = "wR" 
        else:
            self.promote = "bR"
        self.destroy()
    
    def getPromote(self):
        return self.promote
