from threading import Thread, Lock, Event
import time, random

mutex = Lock()

# List of names to use for customers
names = ['João', 'Mario', 'Isabela', 'Kalinka', 'Kamila', 'Paçoca', 'Tiburcio', 'Araújo', 'Zeca', 'Orestes', 'Marcio',
         'Cloderval', 'Milena', 'Ana', 'Vinicius', 'Criolo', 'Luis', 'Bragi', 'Auja', 'Iris', 'Axel', 'Sarah',
         'Sora', 'Riku', 'Andrea', 'Agnar', 'Mamma', 'Solla', 'Olla', 'Berglind', 'Bergdis', 'Margret', 'Ana Luiza'
         'Mil Grau', 'Rastelo', 'Boiadeiro', 'Raj', 'Papai', 'Linga', 'Guaxa', 'Sumido', 'Maome', 'GPS', 'Marina',
         'Kristrun', 'Bakugou', 'Todoroki', 'PeidaFogo', 'Naruto', 'Paloma', 'Giulia', 'Laura', 'Mavis', 'Jessica']

# Interval in seconds
preparoBebidaMin = 3
preparoBebidaMax = 15

class Bar:
    waitingCustomers = []

    def __init__(self, bartender, customerIntervalMin, customerIntervalMax, numberOfSeats):
        self.bartender = bartender
        self.numberOfSeats = numberOfSeats
        self.customerIntervalMin = customerIntervalMin
        self.customerIntervalMax = customerIntervalMax
        print('Bar initilized with {0} seats'.format(numberOfSeats))
        print('Customer min interval {0}'.format(customerIntervalMin))
        print('Customer max interval {0}'.format(customerIntervalMax))
        print('Haircut min duration {0}'.format(preparoBebidaMin))
        print('Haircut max duration {0}'.format(preparoBebidaMax))
        print('---------------------------------------')

    def openShop(self):
        print('Bar is opening')
        workingThread = Thread(target = self.bartenderGoToWork)
        workingThread.start()

    def bartenderGoToWork(self):
        while True:
            mutex.acquire()

            if len(self.waitingCustomers) > 0:
                c = self.waitingCustomers[0]
                del self.waitingCustomers[0]
                mutex.release()
                self.bartender.serveDrink(c)
            else:
                mutex.release()
                print('Aaah, nothing to do, going to sleep')
                bartender.sleep()
                print('Bartender woke up')

    def enterBar(self, customer):
        mutex.acquire()
        print('>> {0} entered the bar and is looking for a seat'.format(customer.name))

        if len(self.waitingCustomers) == self.numberOfSeats:
            print('Waiting room is full, {0} is leaving.'.format(customer.name))
            mutex.release()
        
        else:
            print('{0} sat down in the waiting room'.format(customer.name))
            self.waitingCustomers.append(c)	
            mutex.release()
            bartender.wakeUp()

class Customer:
    def __init__(self):
        self.name = names[(random.randrange(0, len(names)))]

class BarTender:
    bartenderWorkingEvent = Event()

    def sleep(self):
        self.bartenderWorkingEvent.wait()

    def wakeUp(self):
        self.bartenderWorkingEvent.set()

    def serveDrink(self, customer):
        #Set bartender as busy 
        self.bartenderWorkingEvent.clear()

        print('{0} is having a haircut'.format(customer.name))

        #randomHairCuttingTime = random.randrange(preparoBebidaMin, preparoBebidaMax+1)
        randomHairCuttingTime = 6
        # print("Haircut Time = {0}".format(randomHairCuttingTime))
        time.sleep(randomHairCuttingTime)
        print('{0} is done'.format(customer.name))


if __name__ == '__main__':

    customerIntervalMin = 3     # 3 seconds
    customerIntervalMax = 15    # 15 seconds
    # Time between arrival of customers will differ between 3 and 15 seconds

    customers = []
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())
    customers.append(Customer())

    bartender = BarTender()

    bar = Bar(bartender, customerIntervalMin, customerIntervalMax, numberOfSeats=3)
    bar.openShop()

    while len(customers) > 0:
        c = customers.pop()	
        # New customer enters the bar
        bar.enterBar(c)
        customerInterval = random.randrange(customerIntervalMin, customerIntervalMax+1)
        time.sleep(customerInterval)
        
        # Test lines
        # print("*" * 40)
        # print("Number of waiting customers/Number of seats")
        # print("{0}/{1}".format(len(barberShop.waitingCustomers), barberShop.numberOfSeats))
        # print("*" * 40)