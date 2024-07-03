import simpy

#di base non temina mai percchè è una simulazione, siamo noi che gli daremo un tempo di run
def car(env):
    while True:
        print('Start parking at %d' % env.now)
        parking_duration = 5
        yield env.timeout(parking_duration)

        print('Start driving at %d' % env.now)
        trip_duration = 2
        yield env.timeout(trip_duration)
        
        
class Car(object):
    def __init__(self, env):
        self.env = env
        # Start the run process everytime an instance is created.
        self.action = env.process(self.run())

    def run(self):
        while True:
            print('Start parking and charging at %d' % self.env.now)
            charge_duration = 5
           

             # We may get interrupted while charging the battery
            try:
                # We yield the process that process() returns
                # to wait for it to finish
                yield self.env.process(self.charge(charge_duration))
            except simpy.Interrupt:
                # When we received an interrupt, we stop charging and
                # switch to the "driving" state
                print('Was interrupted. Hope, the battery is full enough ...')


            # The charge process has finished and
            # we can start driving again.
            print('Start driving at %d' % self.env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)

    def charge(self, duration):
        yield self.env.timeout(duration)

#con questa fun vado ad interrompere l'esecuzione, tipo se l'autista non vuole più aspettare la fine della ricarica
def driver(env, car):
    yield env.timeout(3)
    car.action.interrupt()