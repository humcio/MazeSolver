from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze solv")

        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)

        self.__running = False
        

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

class Point:
    def __init__(self, x, y): #x0 y0 is topleft corner
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
    
    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width = 5)

class Cell:
    def __init__(self, win=None):
        self._win = win

        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None

        self.has_left_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_top_wall = True

        self.visited = False

    
    def draw(self, x1, y1, x2, y2): #x y of topleft corner and bottom right corner
        if self._win is None:
            return
        
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, "white")
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, "white")
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, "white")
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        middle_x = (self._x1 + self._x2)/2
        middle_y = (self._y1 + self._y2)/2
        target_middle_x = (to_cell._x1 + to_cell._x2)/2
        target_middle_y = (to_cell._y1 + to_cell._y2)/2
        fill_color = "red"
        if undo:
             fill_color = "gray"

        self._win.draw_line(Line(Point(middle_x, middle_y), Point(target_middle_x, target_middle_y)), fill_color)

class Maze:
    def __init__(self,
                 x1,
                 y1,
                 num_rows,
                 num_columns,
                 cell_size_x,
                 cell_size_y,
                 win = None,
                 seed = None
                ):
        self._cells = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_columns
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed:
            random.seed(seed)


        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self.num_cols):
            col_cells = []
            for j in range(self.num_rows):
                col_cells.append(Cell(self.win))
            self._cells.append(col_cells)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self.win is None:
            return
        cell_x = self.x1 + i * self.cell_size_x #top left
        cell_y = self.y1 + j * self.cell_size_y
        cell_x2 = cell_x + self.cell_size_x #bot right
        cell_y2 = cell_y + self.cell_size_y

        self._cells[i][j].draw(cell_x, cell_y, cell_x2, cell_y2)
        self._animate()

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self): #can add logic to decide which side to remove, for now removes only top  from 0,0 and bot from num, num
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_cols -1][self.num_rows -1].has_bottom_wall = False
        self._draw_cell(self.num_cols-1, self.num_rows-1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index = []

            #determines where to go next
            if i > 0 and not self._cells[i -1][j].visited: #left
                next_index.append((i-1, j))
            if i < self.num_cols - 1 and not self._cells[i+1][j].visited: #right
                next_index.append((i+1, j))
            if j > 0 and not self._cells[i][j - 1].visited: #up
                next_index.append((i, j - 1))
            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited: #down
                next_index.append((i, j + 1))

            if len(next_index) == 0: #if all cells exhausted we are done
                self._draw_cell(i, j)
                return
            
            direction_index = random.randrange(len(next_index)) #randomizes direction where to go
            next = next_index[direction_index]

            if next[0] == i + 1: #breaks walls between cells, needs to hit current + adjecent node to remove wall, otherwise one of them will visually keep wall in place
                self._cells[i][j].has_right_wall = False #right wall
                self._cells[i+1][j].has_left_wall = False
            if next[0] == i - 1:
                self._cells[i][j].has_left_wall = False #left wall
                self._cells[i-1][j].has_right_wall = False
            if next[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False #bottom wall
                self._cells[i][j+1].has_top_wall = False
            if next[1] == j-1:
                self._cells[i][j].has_top_wall = False #top wall
                self._cells[i][j-1].has_bottom_wall = False        

            self._break_walls_r(next[0], next[1]) #do the same for the next wall

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False


    def solve(self):
        return self._solve_r(0,0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        if i == self.num_cols - 1 and j == self.num_rows -1:
            return True
        
        #left, check if we are not on the edge and then if there is no wall and has not been visited, if all good we go
        if (i > 0
             and not self._cells[i][j].has_left_wall
             and not self._cells[i-1][j].visited):
            
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
        #right, check if we are not on the edge and then if there is no wall and has not been visited, if all good we go
        if (i < self.num_cols - 1
             and not self._cells[i][j].has_right_wall
             and not self._cells[i+1][j].visited):
            
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)
        #bottom, check if we are not on the edge and then if there is no wall and has not been visited, if all good we go
        if (j < self.num_rows - 1
             and not self._cells[i][j].has_bottom_wall
             and not self._cells[i][j+1].visited):
            
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
        #top, check if we are not on the edge and then if there is no wall and has not been visited, if all good we go
        if (j > 0 
             and not self._cells[i][j].has_top_wall
             and not self._cells[i][j-1].visited):
            
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)
        #all checked, if we didnt get all trues in the chat then maze is unsolveable
        return False
    





        
