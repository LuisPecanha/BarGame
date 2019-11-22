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
customerIntervalMin = 5
customerIntervalMax = 15
haircutDurationMin = 3
haircutDurationMax = 15

class BarberShop:
    waitingCustomers = []

    def __init__(self, barber, numberOfSeats):
        self.barber = barber
        self.numberOfSeats = numberOfSeats
        print('BarberShop initilized with {0} seats'.format(numberOfSeats))
        print('Customer min interval {0}'.format(customerIntervalMin))
        print('Customer max interval {0}'.format(customerIntervalMax))
        print('Haircut min duration {0}'.format(haircutDurationMin))
        print('Haircut max duration {0}'.format(customerIntervalMax))
        print('---------------------------------------')

    def openShop(self):
        print('Barber shop is opening')
        workingThread = Thread(target = self.barberGoToWork)
        workingThread.start()

    def barberGoToWork(self):
        while True:
            mutex.acquire()

            if len(self.waitingCustomers) > 0:
                c = self.waitingCustomers[0]
                del self.waitingCustomers[0]
                mutex.release()
                self.barber.cutHair(c)
            else:
                mutex.release()
                print('Aaah, all done, going to sleep')
                barber.sleep()
                print('Barber woke up')

    def enterBarberShop(self, customer):
        mutex.acquire()
        print('>> {0} entered the shop and is looking for a seat'.format(customer.name))

        if len(self.waitingCustomers) == self.numberOfSeats:
            print('Waiting room is full, {0} is leaving.'.format(customer.name))
            mutex.release()
        
        else:
            print('{0} sat down in the waiting room'.format(customer.name))
            self.waitingCustomers.append(c)	
            mutex.release()
            barber.wakeUp()

class Customer:
    def __init__(self):
        self.name = names[(random.randrange(0, len(names)+1))]

class Barber:
    barberWorkingEvent = Event()

    def sleep(self):
        self.barberWorkingEvent.wait()

    def wakeUp(self):
        self.barberWorkingEvent.set()

    def cutHair(self, customer):
        #Set barber as busy 
        self.barberWorkingEvent.clear()

        print('{0} is having a haircut'.format(customer.name))

        #randomHairCuttingTime = random.randrange(haircutDurationMin, haircutDurationMax+1)
        randomHairCuttingTime = 6
        # print("Haircut Time = {0}".format(randomHairCuttingTime))
        time.sleep(randomHairCuttingTime)
        print('{0} is done'.format(customer.name))


if __name__ == '__main__':
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

    barber = Barber()

    barberShop = BarberShop(barber, numberOfSeats=3)
    barberShop.openShop()

    while len(customers) > 0:
        c = customers.pop()	
        # New customer enters the barbershop
        barberShop.enterBarberShop(c)
        customerInterval = random.randrange(customerIntervalMin, customerIntervalMax+1)
        time.sleep(customerInterval)
        
        # Test lines
        # print("*" * 40)
        # print("Number of waiting customers/Number of seats")
        # print("{0}/{1}".format(len(barberShop.waitingCustomers), barberShop.numberOfSeats))
        # print("*" * 40)