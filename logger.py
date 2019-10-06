import os
import re


class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''

    def __init__(self, file_name, formatting_name):
        self.file_name = file_name
        self.formatting_name = formatting_name

    def clear_file_text(self, file_name):
        open(file_name, 'w').close()

    def text_formatting(self, file_name, message):
        '''The logger uses this method to make doc strings flush with text document'''

        with open(self.formatting_name, "w") as logs_f:
            logs_f.writelines(message)
        with open(self.formatting_name, "r") as logs_f:
            list_lines = []
            lines = logs_f.readlines()
            for line in lines:
                if len(line.strip()) > 0:
                    list_lines.append(re.sub(' +', ' ', line).strip())

        with open(file_name, "a") as logs:
            for _ in range(2): list_lines.append('')
            logs.writelines('\n'.join(list_lines))

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
        repro_num, initial_infected):
        '''The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        metadata = (f"""
            Population Size: {pop_size}\nVaccine Percentage: {vacc_percentage}\n
            Virus Name = {virus_name}\nMortality Rate = {mortality_rate}\n
            Reproduction Rate = {repro_num}\nPeople Initially Infected: {initial_infected}\n
            """)
        #Removes indentation from the string, and reformats it to allign with text file.
        self.text_formatting(self.file_name, metadata)
        with open(self.file_name, "a") as logs_f:
            logs_f.write("Beginning step 1\n\n")

    def log_interaction(self, person, random_person, random_person_sick,
        random_person_vacc, did_infect):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects {random_person.ID} \n"

        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        #Different Case responses
        is_infected = f"{person._id} infected {random_person._id}. \n"
        is_not_infected = f"{person._id} didn't infect {random_person._id} because they got lucky!\n"
        is_vaccinated = f"{person._id} didn't infect {random_person._id} because they were vaccinated.\n"
        is_already_sick = f"{person._id} didn't infect {random_person._id} because they were already sick.\n"

        #Booleans Declared by interaction in Simulation
        with open(self.file_name, "a") as logs:
            if random_person_vacc:
                logs.write(is_vaccinated)
            elif random_person_sick:
                logs.write(is_already_sick)
            elif did_infect:
                logs.write(is_infected)
            elif not did_infect:
                logs.write(is_not_infected)

    def log_infection_survival(self, person):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        is_dead = f"{person._id} died from the infection.\n"
        is_not_dead = f"{person._id} survived the infection!\n"

        #Booleans Declared by interaction person's did_survive_infection function
        with open(self.file_name, "a") as logs:
                if person.is_alive:
                    logs.write(is_not_dead)
                else:
                    logs.write(is_dead)

    def log_time_step(self, time_step_number, total_dead, current_infected,
        total_infected, newly_infected, dead_this_step):
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
        time_step_summary = (f"""\
            {'-'*50}\nTime step {time_step_number} ended\nInfected this time step: {current_infected}\n
            Died this time step: {dead_this_step}\nTotal Population that has been infected = {total_infected}\n
            Total Deaths = {total_dead}\n{'-'*50}\n
            """)
        #Removes indentation from the string, and reformats it to allign with text file.
        self.text_formatting(self.file_name, time_step_summary)
        #If it's the last step, function will not write to file
        if current_infected != 0:
            with open(self.file_name, "a") as logs_f:
                logs_f.write(f"Beginning step {time_step_number + 1}\n\n")

    def log_answers(self, total_dead, total_infected, virus, pop_size, vacc_percentage,
        initial_infected, saved_from_vac):
        ''' The Simulation object uses this method to log the answers of the ReadMe '''

        infected_percentage  = f"{float(total_infected / pop_size)}%"
        dead_percentage = f"{float(total_dead / pop_size)}%"

        answers = (f"""\
            1. Inputs I gave for the simulation were: {pop_size}  {vacc_percentage}\
            {virus.name} {virus.mortality_rate} {virus.repro_rate}{initial_infected}\n
            2. {infected_percentage} of the population became infected at some point.\n
            3. {dead_percentage} of the population died.\n4. The amount of times someone\
            was saved because they were vaccinated was {saved_from_vac}\n
            """)

        self.clear_file_text('answers.txt')
        self.text_formatting('answers.txt', answers)
