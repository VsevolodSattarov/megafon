from tkinter import *
from copy import deepcopy
import tkinter.messagebox as message
class LifeGame:
    class GameField:
        def __init__(self, game_field, master):
            self.game_field = game_field
            self.master= master
            self.move = 40
            self.generate_field()
            self._steps = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
            self.game_started = False
        def generate_field(self, w = 700, h = 400):
            self.game_started = False
            self.cur_hod = 0
            self._alive = 0
            self.alive_text = self.game_field.create_text(780, 200, text = "Populated cells", font = ("Purisa", 12))
            self.alive_bar = self.game_field.create_text(785, 220, text=self._alive, font = ("Purisa", 20))
            self.status_text = self.game_field.create_text(780, 100, text="Current move", font = ("Purisa", 12))
            self.hod = self.game_field.create_text(785, 120, text=self.cur_hod, font = ("Purisa", 20))
            self.cols = self.check(w, self.move)
            self.rows = self.check(h, self.move)
            self.field_id = []
            self.field_al = []
            self.pointer = []
            for row in range(self.rows):
                full_row = []
                for column in range(self.cols):
                    full_row.append(False)
                self.field_al.append(full_row)
            for row in range(self.rows):
                full_row = []
                for column in range(self.cols):
                    full_row.append((row, column))
                self.pointer.append(full_row)

            for row in range(self.rows):
                full_row = []
                for column in range(self.cols):
                    full_row.append(self.game_field.create_rectangle(5 + self.move * column, 5 + self.move * row, 5 + self.move + self.move * column, 5 + self.move + self.move * row, fill = 'white'))
                    self.game_field.tag_bind(full_row[column], '<Button-1>', self.status_change)
                self.field_id.append(full_row)

        def game_on(self):
            self.game_started = True
            self.start_move()
            self.screen_change()
            if self._alive == 0:
                self.end_game()
        def start_move(self):
            self.next_move = deepcopy(self.field_al)
            self._alive_next = 0
            for row in range(self.rows):
                for col in range(self.cols):
                    s = self.is_alive(row, col)
                    self.next_move[row][col] = s
                    if s:
                        self._alive_next += 1
            self._alive = self._alive_next

        def progress_panel(self):
            self.cur_hod += 1
            self.game_field.itemconfig(self.hod, text = self.cur_hod)
        def alive_panel(self):
            self.game_field.itemconfig(self.alive_bar, text = self._alive)

        def end_game(self):
            message.showinfo("Game is over", "All cells are dead")
        def screen_change(self):
            print(self.field_al)
            self.progress_panel()
            self.alive_panel()
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.next_move[row][col]:
                        self.game_field.itemconfig(self.field_id[row][col], fill='green')
                    if not self.next_move[row][col]:
                        self.game_field.itemconfig(self.field_id[row][col], fill='white')
            self.field_al = self.next_move

        def is_alive(self, row, column):
            check = 0
            for step in self._steps:
                check_row = (row + self.rows + step[0]) % self.rows
                check_column = (column + self.cols + step[1]) % self.cols
                if self.field_al[check_row][check_column]:
                    check += 1
            print(row, column, "\n", check)
            if check == 3 and not self.field_al[row][column]:
                return True
            if check >= 2 and check <= 3 and self.field_al[row][column]:
                return True
            return False
        def neigh(self, row, column):
            check = 0
            for step in self._steps:
                check_row = (row + self.rows + step[0]) % self.rows
                check_column = (column + self.cols + step[1]) % self.cols
                if self.field_al[check_row][check_column]:
                    check += 1
            return check
        def status_change(self, event):
                x, y = event.x, event.y
                #print(x, y)
                column, row = self.check(x-6, self.move), self.check(y-6, self.move)
                if not self.game_started:
                    if not self.field_al[row][column]:
                        self.game_field.itemconfig(self.field_id[row][column], fill='green')
                        self.field_al[row][column] = True
                        self._alive += 1
                    else:
                        self.game_field.itemconfig(self.field_id[row][column], fill='white')
                        self.field_al[row][column] = False
                        self._alive -= 1
                    self.alive_panel()
                    #print(row, column)
                    #print(self.field_al[row][column])
                else:
                    self.cell_info(row, column)
        def reset(self):
            self.game_field.delete(ALL)
            self.generate_field()
        def cell_info(self,row, col):
            info = self.neigh(row, col)
            message.showinfo("Cell information", "Number of neighbors: " + str(info))
            print(row, col)
        def check(self, a, b):
            i = 0
            while a > b * 1:
                i += 1
                a = a - b
            return i
    def __init__(self, master):
        self.master = master
        master.geometry('880x470')
        self.game_frame = Frame(self.master, width = 700, height = 400 )
        self.exit_button = Button(self.master, text = "EXIT", command = self.master.quit)
        self.start_button = Button(self.master, text = "START GAME", command = self.start)
        self.reset_button = Button(self.master, text = "RESET FIELD", command = self.reset)
        #self.stop_button = Button(self.master, text = "stop", command = self.stop)
        self.game_field = Canvas(self.game_frame, width = 860, height = 380, bg = 'white')
        self.game = self.GameField(self.game_field, self.master)

        self.game_field.pack()
        self.game_frame.grid(row= 0, column = 0, columnspan = 5, rowspan = 10, sticky = 'nsew')
        self.start_button.grid(row = 10, column = 0, sticky = 'nsew')
        self.reset_button.grid(row = 10, column = 1, sticky = 'nsew')
        #self.stop_button.grid(row = 10, column = 2, sticky = 'nsew')
        self.exit_button.grid(row = 10, column = 3, sticky = 'nsew')
    def reset(self):
        self.start_button.config(text = "START GAME")
        self.reset_button.config(text = "RESET FIELD")
        self.game.reset()
    def start(self):
        self.start_button.config(text = "NEXT GENERATION")
        self.reset_button.config(text="NEW GAME")
        self.game.game_on()
    def stop(self):
        #self.game_field.itemconfig(self.field[0][0], fill = 'blue')
        pass



root = Tk()
game = LifeGame(root)
root.mainloop()