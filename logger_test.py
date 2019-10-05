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
    # assert logger.file_name.readlines() == logger.formatting_name.readlines()
    with open(logger.file_name, "r") as logs:
        file_grid = []
        file_lines = logs.readlines()
    with open(logger.formatting_name, "r") as logs_f:
        formatting_grid = []
        form_lines = logs_f.readlines()
    assert file_lines == form_lines
