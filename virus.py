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

def test_compare_names():
    '''Checks to see if multiple Virus Objects can be made'''
    virus1 = Virus("Flu", 0.4, 0.3)
    virus2 = Virus("Plague", 0.9, 0.3)
    assert virus1.name != virus2.name
    assert virus1.repro_rate != virus2.repro_rate
    assert virus1.mortality_rate == virus2.mortality_rate
