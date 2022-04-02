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
world = Button(master, text="Simulate",  command=lambda: solve_wumpus_world(master, "world.txt"), width=8,
               font="Helvetica 14 bold", bg="gray80", fg="gray40", borderwidth=0, activeforeground="white", activebackground="gray40")


legends = """A - Agent\nW - Wumpus\nB - Breeze\nP - Pit\nG - Gold\nS - Stench
          """
label_legends = Label(master, text=legends)

# start.grid(row = 0, column = len(label_grid[0]), sticky = W, pady = 1)
world.grid(row=0, column=len(label_grid[0]))
label_legends.grid(row=1, column=len(label_grid[0]))


mainloop()
