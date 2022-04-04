from tkinter import *
from agent import Agent
from world import World
# from pandas import *
from grid_label import Grid_Label
import time


def solve_wumpus_world(master, world_file):
    world = World()
    # generating world with the given world input file
    world.generate_world(world_file)
    # print(DataFrame(world.world))
    label_grid = [[Grid_Label(master, i, j) for j in range(
        world.cols)] for i in range(world.rows)]
    agent = Agent(world, label_grid)

    # Agent Solving
    while agent.exited == False:
        agent.explore_world()
        if agent.found_gold == True:
            agent.leave_cave()
        break
    # print("You have exited with the gold!")
    agent.rebuild_world()
    agent.knowledge_base[agent.world.agent_row][agent.world.agent_col].remove(
        'A')
    time.sleep(1.5)
    agent.rebuild_world()


master = Tk()
master.title("Wumpus👾 World")

world = World()
world.generate_world("world.txt")
label_grid = [[Grid_Label(master, i, j)for j in range(world.cols)]
              for i in range(world.rows)]
# agent = Agent(world, label_grid)

# start = Button(master, text="Start", command= lambda: solve_wumpus_world(master, "world_1.txt"))
world1 = Button(master, text="World 1",  command=lambda: solve_wumpus_world(master, "test1.txt"), width=8,
                font="Helvetica 14 bold", bg="gray80", fg="gray40", borderwidth=0, activeforeground="white", activebackground="gray40")
world2 = Button(master, text="World 2",  command=lambda: solve_wumpus_world(master, "test2.txt"), width=8,
                font="Helvetica 14 bold", bg="gray80", fg="gray40", borderwidth=0, activeforeground="white", activebackground="gray40")
world3 = Button(master, text="World 3",  command=lambda: solve_wumpus_world(master, "test3.txt"), width=8,
                font="Helvetica 14 bold", bg="gray80", fg="gray40", borderwidth=0, activeforeground="white", activebackground="gray40")
world4 = Button(master, text="World 4",  command=lambda: solve_wumpus_world(master, "test4.txt"), width=8,
                font="Helvetica 14 bold", bg="gray80", fg="gray40", borderwidth=0, activeforeground="white", activebackground="gray40")


agent_legend = Label(master, text="A - Agent")
wumpus_legend = Label(master, text="W - Wumpus")
breeze_legend = Label(master, text="B - Breeze")
pit_legend = Label(master, text="P - Pit")
gold_legend = Label(master, text="G - Gold")
stench_legend = Label(master, text="S - Stench")

# start.grid(row = 0, column = len(label_grid[0]), sticky = W, pady = 1)
world1.grid(row=0, column=len(label_grid[0]))
world2.grid(row=1, column=len(label_grid[0]))
world3.grid(row=2, column=len(label_grid[0]))
world4.grid(row=3, column=len(label_grid[0]))
agent_legend.grid(row=4, column=0)
wumpus_legend.grid(row=4, column=1)
breeze_legend.grid(row=4, column=2)
pit_legend.grid(row=4, column=3)
gold_legend.grid(row=4, column=4)
stench_legend.grid(row=4, column=5)

mainloop()
