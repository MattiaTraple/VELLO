import simpy

from function import car

env=simpy.Environment()

#creazione dell'istanza
#posso utilizzarla per porcessare interazioni (.process)
env.process(car(env))
#scelgo per quanto runnarla
env.run(until=15)




