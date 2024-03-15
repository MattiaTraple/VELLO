import simpy
from Test_E_Varie.request_resource_fun import car

#riferimento ad enviroment e setto la capacità
env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2)

#creo le 4 car che partiranno quando le creo
for i in range(4):
    env.process(car(env, 'Car %d' % i, bcs, i*2, 5))

#posso avviare al simulaizone che si fermerà quando non ci saranno più eventi restanti da smaltire
env.run()*