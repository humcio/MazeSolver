from graphics import *
import sys
import threading

def main(color="red"):
    num_rows = 50
    num_cols = 50
    margin = 16
    screen_x = 800
    screen_y = 800
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    sys.setrecursionlimit(10000)
    win = Window(screen_x, screen_y, MazeName=color)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    print("maze created")
    is_solvable = maze.solve()
    if is_solvable:
        print(f"solved {color}")
    

    win.wait_for_close()


def thread():
    thread1 = threading.Thread(target=main)
    thread2 = threading.Thread(target=main, args=("blue",))
    thread1.start()
    thread2.start()

thread()