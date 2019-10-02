import textwrap
from textwrap import dedent

class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''
    # TODO: Write a test suite for this class to make sure each method is working
    # as expected.

    # PROTIP: Write your tests before you solve each function, that way you can
    # test them one by one as you write your class.

    def __init__(self, file_name, formatting_name):
        # TODO:  Finish this initialization method. The file_name passed should be the
        # full file name of the file that the logs will be written to.
        self.file_name = file_name
        self.formatting_name = formatting_name

    def clear_file_text(self, log_name):
        open(log_name, 'w').close()

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       repro_num, initial_infected):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!

        metadata = dedent(f"""\
            Population Size: {pop_size}\nVaccine Percentage: {vacc_percentage}\n
            Virus Name = {virus_name}\nMortality Rate = {mortality_rate}\n
            Reproduction Rate = {repro_num}\nPeople Initially Infected: {initial_infected}\n
            """)

        #Removes indentation from the string, and then reformats it a few times
        #So it looks normal in the file.
        with open(self.formatting_name, "w") as logs_f:
            logs_f.writelines(metadata)
        with open(self.formatting_name, "r") as logs_f:
            list_lines = []
            lines = logs_f.readlines()
            for line in lines:
                if len(line.strip()) > 0: list_lines.append(line.strip())
        with open(self.file_name, "a") as logs:
            logs.writelines('\n'.join(list_lines))

        self.clear_file_text(self.formatting_name)

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects {random_person.ID} \n"

        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
        #Different Case responses
        is_infected = f"{person._id} infects {random_person._id} \n"
        is_not_infected = f"{person._id} didn't infect {random_person._id} because they got lucky!.\n"
        is_vaccinated = f"{person._id} didn't infect {random_person._id} because they were vaccinated.\n"
        is_already_sick = f"{person._id} didn't infect {random_person._id} because they were already sick.\n"

        #Booleans Declared by interaction in Simulation
        with open(self.file_name, "a") as logs:
            if is_vaccinated: logs.write(is_vaccinated)
            elif random_person_sick: logs.write(is_already_sick)
            elif did_infect: logs.write(is_infected)
            elif not did_infect: logs.write(is_not_infected)


    def log_infection_survival(self, person, did_die_from_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        is_dead = f"{person._id} died from the infection.\n"
        is_not_dead = f"{person._id} survived the infection!\n"

        #Booleans Declared by interaction person's did_survive_infection function
        with open(self.file_name, "a") as logs:
            if did_die_from_infection: logs.write(is_dead)
            elif not did_die_from_infectiont: logs.write(is_not_dead)

    def log_time_step(self, time_step_number, total_dead=0, current_infected=0,
    total_infected=0, newly_infected=0, dead_this_step=0):
        ''' STRETCH CHALLENGE DETAILS:

        If you choose to extend this method, the format of the summary statistics logged
        are up to you.

        At minimum, it should contain:
            The number of people that were infected during this specific time step.
            The number of people that died on this specific time step.
            The total number of people infected in the population, including the newly infected
            The total number of dead, including those that died during this time step.

        The format of this log should be:
            "Time step {time_step_number} ended, beginning {time_step_number + 1}\n"
        '''
        # TODO: Finish this method. This method should log when a time step ends, and a
        # new one begins.
        # NOTE: Here is an opportunity for a stretch challenge!
        time_step_summary = dedent(f"""\
            Infected this time step: {newly_infected}\nDied this time step: {dead_this_step}\n
            Total Population infected = {total_infected}\nTotal Deaths = {total_dead}\n
            Time step {time_step_number} ended; Beginning {time_step_number + 1}\n
            """)

        #Removes indentation from the string, and then reformats it a few times
        #So it looks normal in the file.
        with open(self.formatting_name, "w") as logs_f:
            logs_f.writelines(time_step_summary)
        with open(self.formatting_name, "r") as logs_f:
            step_summary_lines = []
            lines = logs_f.readlines()
            for line in lines:
                if len(line.strip()) > 0: step_summary_lines.append(line.strip())
        with open(self.file_name, "a") as logs:
            logs.writelines('\n'.join(step_summary_lines))

        self.clear_file_text(self.formatting_name)
