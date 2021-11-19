import curses
from enum import Enum, auto

class Tab(Enum):
    Todo = auto()
    Done = auto()

class UI:
    def __init__(self, label, lst, stdscr):
        self.row = 0
        self.label = label
        self.lst = lst
        self.lst_curr = 0
        self.stdscr = stdscr

    def move(self, direction):
        match direction:
            case "up":
                if self.lst_curr > 0:
                    self.lst_curr -= 1
            case "down":
                if self.lst_curr < len(self.lst)-1:
                    self.lst_curr += 1

    def move_item(self, to_lst):
        to_lst.append(self.lst.pop(self.lst_curr))

    def draw_label(self):
        self.row = 0
        self.stdscr.addstr(self.row, 0, self.label)
        self.stdscr.addstr(self.row+1, 0, "----------------")
        self.row = 2

    def draw_list(self):
        self.draw_label()
        for i in range(len(self.lst)):
            if i == self.lst_curr:
                self.stdscr.addstr(self.row+i, 0, self.lst[i], curses.A_STANDOUT)
            else:
                self.stdscr.addstr(self.row+i, 0, self.lst[i])

def main():
    stdscr = curses.initscr()

    curses.noecho()
    curses.curs_set(0)

    stdscr.clear()
    tab = Tab.Todo
    todos = [
            "item 1",
            "item 2",
            "item 3"
            ]
    dones = [
            "done 1",
            "done 2",
            "done 3"
            ]
    todo = UI("TODO:", todos, stdscr)
    done = UI("DONE:", dones, stdscr)
    ext = False

    while ext == False:

        match tab:
            case Tab.Todo: todo.draw_list()
            case Tab.Done: done.draw_list()


        key = stdscr.getkey()
        match key:
            case 'k': 
                match tab:
                    case Tab.Todo: todo.move("up")
                    case Tab.Done: done.move("up")
            case 'j': 
                match tab:
                    case Tab.Todo: todo.move("down")
                    case Tab.Done: done.move("down")
            case '\t':
                match tab:
                    case Tab.Todo: tab = Tab.Done
                    case Tab.Done: tab = Tab.Todo
                stdscr.erase()
            case '\n':
                match tab:
                    case Tab.Todo: todo.move_item(dones)
                    case Tab.Done: done.move_item(todos)
                stdscr.erase()
            case 'q': ext = True 

        stdscr.refresh()

    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    main()
