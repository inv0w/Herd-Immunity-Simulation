import random, sys
random.seed(42)
import numpy as np
from person import Person
from logger import Logger
from virus import Virus
from simulation import Simulation
import pytest
import io


def capture_console_output(function_body):
    # _io.StringIO object
    string_io = io.StringIO()
    sys.stdout = string_io
    function_body()
    sys.stdout = sys.__stdout__
    return string_io.getvalue()

def test_create_population():
    virus = Virus("Smallpox", 0.06, 0.15)
    sim = Simulation(100, 0.90, 20, virus)
    sim._create_population(sim.initial_infected)
    assert len(sim.population) == sim.pop_size
    assert len(sim.newly_infected) == sim.initial_infected

def test_simulation_should_continue():
    virus = Virus("Smallpox", 0.06, 0.15)
    sim = Simulation(100, 0.90, 20, virus)

def test_infect_newly_infected():
    virus = Virus("Smallpox", 0.06, 0.15)
    sim = Simulation(100, 0.90, 20, virus)
    person1 = Person(1, True)
    sim.newly_infected.append(person1._id)
    sim._infect_newly_infected()
    assert person1.infection == virus
