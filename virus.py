class Virus(object):
    '''Properties and attributes of the virus used in Simulation.'''

    def __init__(self, name, repro_rate, mortality_rate):
        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate


def test_virus_instantiation():
    '''Check to make sure that the virus instantiator is working.'''
    virus = Virus("Smallpox", 0.06, 0.15)
    assert virus.name == "Smallpox"
    assert virus.repro_rate == 0.06
    assert virus.mortality_rate == 0.15

def test_not_virus_instantiation():
    '''Check to make sure that the virus instantiator is not working.'''
    virus = Virus("Applebees", 0.42, 0.98)
    assert virus.name != "Smallpox"
    assert virus.repro_rate != 0.06
    assert virus.mortality_rate != 0.15
