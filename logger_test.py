import random, sys
random.seed(42)
import numpy as np
from person import Person
from logger import Logger
from virus import Virus
from simulation import Simulation
import pytest
import io
import re

def capture_console_output(function_body):
    # _io.StringIO object
    string_io = io.StringIO()
    sys.stdout = string_io
    function_body()
    sys.stdout = sys.__stdout__
    return string_io.getvalue()

def test_clear_file_text():
    logger = Logger("logs.txt", "logs_formatting.txt")
    logger.clear_file_text(logger.file_name)
    logger.clear_file_text(logger.formatting_name)
    with open(logger.file_name, "r") as logs:
        file_grid = []
        file_lines = logs.readlines()
    with open(logger.formatting_name, "r") as logs_f:
        formatting_grid = []
        form_lines = logs_f.readlines()
    assert file_lines == form_lines

def test_text_formatting():
    logger = Logger("logs.txt", "logs_formatting.txt")
    file_name = 'logs.txt'
    message = "Testing creating of\n        new lines       and     spacing"
    logger.text_formatting(file_name, message)
    with open(logger.file_name, "r") as logs:
        lines = []
        lines = logs.readlines()
    assert lines[0] == 'Testing creating of' + '\n'
    assert lines[1] == 'new lines and spacing' + '\n'

#write_metadata, log_time_step, and log_answers, all rely on just above two
#functions to work. Same tests would apply to all.

def test_log_interaction():
    logger = Logger("logs.txt", "logs_formatting.txt")
    virus = Virus("Smallpox", 0.06, 0.15)
    sim = Simulation(200, 0.90, virus)
    person = Person(1, False, infection=virus)
    random_person2 = Person(2, False, infection=virus)
    random_person3 = Person(3, True, None)
    logger.clear_file_text(logger.file_name)
    sim.interaction(person, random_person2)
    sim.interaction(person, random_person3)
    with open(logger.file_name, "r") as logs:
        lines = []
        lines = logs.readlines()
    assert lines[0] == "1 didn't infect 2 because they were already sick.\n"
    assert lines[1] == "1 didn't infect 3 because they were vaccinated.\n"

def test_log_infection_survival():
    logger = Logger("logs.txt", "logs_formatting.txt")
    virus = Virus("Smallpox", 0.06, 0.15)
    person = Person(1, False, infection=virus)
    logger.clear_file_text(logger.file_name)
    survived = person.did_survive_infection()
    logger.log_infection_survival(person)
    with open(logger.file_name, "r") as logs:
        lines = []
        lines = logs.readlines()
    if survived:
        assert lines[0] == "1 survived the infection!\n"
    else:
        assert lines[0] == "1 died from the infection.\n"
        
