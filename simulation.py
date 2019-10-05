import random, sys
random.seed(42)
import numpy as np
from person import Person
from logger import Logger
from virus import Virus
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=10):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        self.logger = Logger('logs.txt', 'logs_formatting.txt')
        self.population = [] # List of Person objects
        self.pop_size = pop_size # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.saved_from_vac = 0
        self.newly_infected = []

        #Clearing Text Files and Printing metadata
        self.logger.clear_file_text(self.logger.file_name)
        self.logger.write_metadata(pop_size, vacc_percentage, self.virus.name,
            self.virus.mortality_rate, self.virus.repro_rate, initial_infected)

    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        #Gets a list of random numbers in range pop_size to apply initial infections to
        amount_vaccinated = int(self.vacc_percentage * self.pop_size)
        vacc_seeding = np.random.choice(range(1, (self.pop_size) + 1), amount_vaccinated, replace=False)
        virus_seeding = np.random.choice(range(1, (self.pop_size) + 1), initial_infected, replace=False)

        #Checks if any person is in the previous lists, if assigned them corresponding variables
        for i in range(self.pop_size):
            person = Person(i+1, False, None)
            self.population.append(person)
            if person._id in vacc_seeding: person.is_vaccinated = True
            if person._id in virus_seeding:
                self.newly_infected.append(person._id)
                self.current_infected += 1
                person.infection = self.virus


    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        #Decides if there are people infected, if not end the game.
        if self.current_infected == 0:
            return False
        else:
            return True

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        self._create_population(initial_infected)
        dead_this_step = 0
        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        plot_current_infected = []

        #Runs until there are no more infected people. Only vaccinated or dead.
        while should_continue:
            plot_current_infected.append(self.current_infected)
            current_dead = self.total_dead
            self.time_step()
            time_step_counter += 1
            dead_this_step = self.total_dead - current_dead
            self.logger.log_time_step(time_step_counter, self.total_dead,
            self.current_infected, self.total_infected, len(self.newly_infected),
            dead_this_step)
            should_continue = self._simulation_should_continue()

        print(f'The simulation has ended after {time_step_counter} turns.')
        self.logger.log_answers(self.total_dead, self.total_infected,self.virus,
        self.pop_size, self.vacc_percentage, self.initial_infected, self.saved_from_vac)
        #Opens up Graph for statistic about log and answers
        plot_y = np.array(plot_current_infected)
        self.plot_graph(time_step_counter, plot_y)

    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a random person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''

        total_interactions = 0
        #If the random person isn't alive, we loop again without adding to interaction counter
        for person in self.population:
            if person.infection == self.virus and person.is_alive:
                while total_interactions < 100:
                    random_person = random.choice(self.population)
                    if random_person.is_alive:
                        total_interactions += 1
                        self.interaction(person, random_person)
                total_interactions = 0
                person.did_survive_infection()
                self.logger.log_infection_survival(person)
        self._infect_newly_infected()

        #Gets values of Person Objects and assigns Simulation values based off their properties
        died = 0
        total_vaccinated = 0
        current_infected = 0
        for person in self.population:
            if not person.is_alive:
                died += 1
            elif person.infection == self.virus:
                self.total_infected += 1
                current_infected += 1
            elif person.is_vaccinated:
                total_vaccinated += 1

        self.total_dead = died
        self.current_infected = current_infected
        self.total_vaccinated = total_vaccinated

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True
        random_person_vacc = None
        random_person_sick = None
        did_infect = None

        if random_person.is_vaccinated:
            random_person_vacc = True
            self.saved_from_vac += 1
        elif random_person.infection != None:
            random_person_sick = True
        else:
            infect = random.random()
            if infect <= virus.repro_rate:
                self.newly_infected.append(random_person._id)
                did_infect = True
            else:
                did_infect = False

        self.logger.log_interaction(person, random_person, random_person_sick,
        random_person_vacc, did_infect)


    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease.
        '''
        #Iterates through the newly_infected list, and sets their infection
        #to the virus. Resets list after.
        for person in self.population:
            for id in self.newly_infected:
                if person._id == id:
                    person.infection= self.virus
        self.newly_infected = []

    def plot_graph(self, time_step, plot_y):
        '''Makes a graph using matplotlib. Takes in final step counter as last x
        element, last element in y is based off of infect population.
        '''
        x = range(time_step)
        y = plot_y
        spline = UnivariateSpline(x, y, s=10)
        xsmooth = np.linspace(0, time_step, 300)
        #Displays for the Plot, Actual Data vs Smoothed Data
        plt.plot(x, y, 'o')
        plt.plot(xsmooth, spline(xsmooth))
        plt.title(f'{self.virus.name} Infection')
        plt.xlabel('Time Steps')
        plt.ylabel('People Currently Infected')
        plt.show()

if __name__ == "__main__":
    #python3 simulation.py 4000 0.75 Smallpox 0.15 0.06 5
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    repro_num = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 10

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, virus, initial_infected)

    sim.run()
