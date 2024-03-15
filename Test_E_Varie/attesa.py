import simpy
from function import Car
from function import driver
env = simpy.Environment()
car = Car(env)
#decido di settare uno stop quando penso che l macchina sia abbastanza carica
env.process(driver(env, car))

env.run(until=15)