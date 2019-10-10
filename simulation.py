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
        self._create_population(self.initial_infected)
        dead_this_step = 0
        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        plot_y = [self.current_infected]
        plot_y2 = [self.total_dead]
        #Runs until there are no more infected people. Only vaccinated or dead.
        while should_continue:
            self.time_step()
            time_step_counter += 1
            #Graph values
            plot_y.append(self.current_infected)
            plot_y2.append(self.total_dead)
            current_dead = self.total_dead
            dead_this_step = self.total_dead - current_dead
            #Logs and checks if to repeat
            self.logger.log_time_step(time_step_counter, self.total_dead,
            self.current_infected, self.total_infected, len(self.newly_infected),
            dead_this_step)
            should_continue = self._simulation_should_continue()

        print(f'The simulation has ended after {time_step_counter} turns.')
        self.logger.log_answers(self.total_dead, self.total_infected,self.virus,
        self.pop_size, self.vacc_percentage, self.initial_infected, self.saved_from_vac)
        #Creates a graph about logs and answers
        self.plot_graph(time_step_counter, plot_y, plot_y2)

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
                # person_id = person.id
                while total_interactions < 100:
                    random_person = random.choice(self.population)
                    if random_person.is_alive and random_person._id != person._id:
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
        #Checks if if they are vaccinated, or are already sick. If not they have
        #a chance to get infected
        if random_person.is_vaccinated:
            self.saved_from_vac += 1
            interacted = 'is_vaccinated'
        elif random_person.infection != None:
            interacted = 'is_not_sick'
        else:
            infect = random.random()
            if infect <= self.virus.repro_rate:
                self.newly_infected.append(random_person._id)
                interacted = 'did_infect'
            else:
                interacted = 'did_not_infect'

        self.logger.log_interaction(person, random_person, interacted)
        return interacted

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

    def plot_graph(self, time_step, plot_y, plot_y2):
        '''Makes a graph using matplotlib. Takes in final step counter as x
        element, and the y value is the total amount of deaths or currently infected.
        '''
        #For X and Y Values of Points, als smoothing points
        x = range(time_step + 1)
        y = np.array(plot_y)
        y2 = np.array(plot_y2)
        spline = UnivariateSpline(x, y, s=3)
        spline2 = UnivariateSpline(x, y2, s=3)
        xsmooth = np.linspace(0, time_step, 500)
        #Creates different sublots for variable output to logs.
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        #Draws the lines and applys smoothing
        ax1.plot(x, y, 'o', color='blue')#Dots
        ax2.plot(x, y2, 'o', color='red')
        l1, = ax1.plot(xsmooth, spline(xsmooth), 'b--', label='People Currently Infected')#Lines
        l2, = ax2.plot(xsmooth, spline2(xsmooth), 'r--', label='Total Deaths')
        ax1.fill_between(xsmooth, spline(xsmooth), color='blue', alpha=0.5)
        t1, = ax1.plot([],[], marker='s', color='blue', alpha=0.5, ls="none")#Fake plot line for Total Infected.
        #Graph Labels
        ax1.set_title(f'Population Size: {self.pop_size}', fontsize=8)
        fig.suptitle(f'{self.virus.name} Infection', fontsize=14)
        ax1.set_xlabel('Time Steps')
        ax1.set_ylabel('People Currently Infected', color='blue')
        ax2.set_ylabel('Total Deaths', color='red')
        #X ticker amount and plot limits
        ax1.locator_params(integer=True) #Sets X ticker values to int numbers.
        ax1.set_xlim([0, time_step])
        ax1.set_ylim(bottom=0)
        plt.legend([l1, t1, l2],['People Currently Infected', f'Total Infected: {self.total_infected}',
          'Total Deaths'], loc ='lower center', fontsize ='x-small')
        #Saves and shows graph made
        fig.savefig("Graph_Infected_and_Dead.png")
        plt.show()

if __name__ == "__main__":
    #python3 simulation.py 5000 0.80 Smallpox 0.15 0.06 10
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    repro_num = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, virus, initial_infected)

    sim.run()
