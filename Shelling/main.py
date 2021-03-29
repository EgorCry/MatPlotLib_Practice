import copy
import itertools
import matplotlib.pyplot as plt
import random


class Shelling:
    # Initialisation and creating two groups of people(agents)
    def __init__(self, population, size_of_grid, first_to_second, tolerance, steps):
        self.population = population
        self.size_of_grid = size_of_grid
        self.first = int(population * first_to_second)
        self.second = int(population - self.first)
        self.n_empty = size_of_grid**2 - self.first - self.second
        self.tolerance = tolerance
        self.steps = steps
        self.empty_houses = []
        self.agents = {}

        self.all_houses = list(itertools.product(range(self.size_of_grid), range(self.size_of_grid)))
        random.shuffle(self.all_houses)

        self.empty_houses = self.all_houses[:self.n_empty]

        self.remaining_houses = self.all_houses[self.n_empty:]

        houses_by_race = [self.remaining_houses[i::2] for i in range(2)]
        for i in range(2):
            self.agents = dict(
                self.agents.items() |
                dict(zip(houses_by_race[i], [i + 1] * len(houses_by_race[i]))).items()
            )

    # Method for checking if agent is happy
    # If ratio between numbers of other-race-agents and number of all neighbours is higher than tolerance level
    # then agent is not happy
    def is_happy(self, x, y):

        race = self.agents[(x, y)]

        if x == 0 and y == 0:
            count_different = ((1, 0) in self.agents and race != self.agents[(1, 0)]) + \
                              ((0, 1) in self.agents and race != self.agents[(0, 1)]) + \
                              ((1, 1) in self.agents and race != self.agents[(1, 1)])
            test = 3
        elif y == 0 and x != self.size_of_grid-1:
            test = 5
            count_different = ((x-1, y) in self.agents and race != self.agents[(x-1, y)]) + \
                              ((x-1, y+1) in self.agents and race != self.agents[(x-1, y+1)]) + \
                              ((x, y+1) in self.agents and race != self.agents[(x, y+1)]) + \
                              ((x+1, y+1) in self.agents and race != self.agents[(x+1, y+1)]) + \
                              ((x+1, y) in self.agents and race != self.agents[(x+1, y)])
        elif x == self.size_of_grid-1 and y == 0:
            test = 3
            count_different = ((x-1, y) in self.agents and race != self.agents[(x-1, y)]) + \
                              ((x-1, y+1) in self.agents and race != self.agents[(x-1, y+1)]) + \
                              ((x, y+1) in self.agents and race != self.agents[(x, y+1)])
        elif x == 0 and y != self.size_of_grid-1:
            test = 5
            count_different = ((x, y-1) in self.agents and race != self.agents[(x, y-1)]) + \
                              ((x+1, y-1) in self.agents and race != self.agents[(x+1, y-1)]) + \
                              ((x+1, y) in self.agents and race != self.agents[(x+1, y)]) + \
                              ((x+1, y+1) in self.agents and race != self.agents[(x+1, y+1)]) + \
                              ((x, y+1) in self.agents and race != self.agents[(x, y+1)])
        elif x == self.size_of_grid-1 and y != self.size_of_grid - 1:
            test = 5
            count_different = ((x, y-1) in self.agents and race != self.agents[(x, y-1)]) + \
                              ((x-1, y-1) in self.agents and race != self.agents[(x-1, y-1)]) + \
                              ((x-1, y) in self.agents and race != self.agents[(x-1, y)]) + \
                              ((x-1, y+1) in self.agents and race != self.agents[(x-1, y+1)]) + \
                              ((x, y+1) in self.agents and race != self.agents[(x, y+1)])
        elif x == self.size_of_grid-1 and y == self.size_of_grid-1:
            test = 3
            count_different = ((x, y-1) in self.agents and race != self.agents[(x, y-1)]) + \
                              ((x+1, y-1) in self.agents and race != self.agents[(x+1, y-1)]) + \
                              ((x+1, y) in self.agents and race != self.agents[(x+1, y)])
        elif x != self.size_of_grid-1 and y == self.size_of_grid-1:
            test = 5
            count_different = ((x-1, y) in self.agents and race != self.agents[(x-1, y)]) + \
                              ((x-1, y-1) in self.agents and race != self.agents[(x-1, y-1)]) + \
                              ((x, y-1) in self.agents and race != self.agents[(x, y-1)]) + \
                              ((x+1, y-1) in self.agents and race != self.agents[(x+1, y-1)]) + \
                              ((x+1, y) in self.agents and race != self.agents[(x+1, y)])
        elif y == self.size_of_grid-1:
            test = 3
            count_different = ((x, y-1) in self.agents and race != self.agents[(x, y-1)]) + \
                              ((x-1, y-1) in self.agents and race != self.agents[(x-1, y-1)]) + \
                              ((x-1, y) in self.agents and race != self.agents[(x-1, y)])
        else:
            test = 8
            count_different = ((x-1, y) in self.agents and race != self.agents[(x-1, y)]) + \
                              ((x-1, y-1) in self.agents and race != self.agents[(x-1, y-1)]) + \
                              ((x, y-1) in self.agents and race != self.agents[(x, y-1)]) + \
                              ((x+1, y-1) in self.agents and race != self.agents[(x+1, y-1)]) + \
                              ((x+1, y) in self.agents and race != self.agents[(x+1, y)]) + \
                              ((x+1, y+1) in self.agents and race != self.agents[(x+1, y+1)]) + \
                              ((x, y+1) in self.agents and race != self.agents[(x, y+1)]) + \
                              ((x-1, y+1) in self.agents and race != self.agents[(x-1, y+1)])
        if count_different / test > self.tolerance:
            return False
        else:
            return True

    # Method for checking and changing agent place if he is unhappy
    def update(self):
        for i in range(self.steps):
            self.old_agents = copy.deepcopy(self.agents)
            n_changes = 0
            for agent in self.old_agents:
                if not self.is_happy(agent[0], agent[1]):
                    agent_race = self.agents[agent]
                    empty_house = random.choice(self.empty_houses)
                    self.agents[empty_house] = agent_race
                    del self.agents[agent]
                    self.empty_houses.remove(empty_house)
                    self.empty_houses.append(agent)
                    n_changes += 1
            # If there is nothing to change then it means that everybody is satisfied and other iterations doesn't need
            print(n_changes)
            if n_changes == 0:
                break

    # Method for showing the plot
    def show_plot(self):
        fig, ax = plt.subplots()
        agent_colors = {1: 'b', 2: 'g'}
        for agent in self.agents:
            ax.scatter(agent[0] + 0.5, agent[1] + 0.5, color=agent_colors[self.agents[agent]], marker='s')

        ax.set_title("Shelling model", fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.size_of_grid])
        ax.set_ylim([0, self.size_of_grid])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.show()


# Example of 1_000 agents living in 35x35 grid and first is 1_000 * 0.3 = 300 and second is 1_000 - 300 = 700
# There are 100 iterations by default and 0.25 is tolerance level of people
first = Shelling(1_000, 35, 0.3, 0.25, 100)
first.show_plot()
first.update()
first.show_plot()
