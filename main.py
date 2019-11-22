from threading import Thread, Lock, Event
import time, random

mutex = Lock()

# List of names to use for customers
names = ['João', 'Mario', 'Isabela', 'Kalinka', 'Kamila', 'Paçoca', 'Tiburcio', 'Araújo', 'Zeca', 'Orestes', 'Marcio',
         'Cloderval', 'Milena', 'Ana', 'Vinicius', 'Criolo', 'Luis', 'Bragi', 'Auja', 'Iris', 'Axel', 'Sarah',
         'Sora', 'Riku', 'Andrea', 'Agnar', 'Mamma', 'Solla', 'Olla', 'Berglind', 'Bergdis', 'Margret', 'Ana Luiza',
         'Mil Grau', 'Rastelo', 'Boiadeiro', 'Raj', 'Papai', 'Linga', 'Guaxa', 'Sumido', 'Maome', 'GPS', 'Marina',
         'Kristrun', 'Bakugou', 'Todoroki', 'PeidaFogo', 'Naruto', 'Paloma', 'Giulia', 'Laura', 'Mavis', 'Jessica']

# Format = Name, Prepare time, Coins Awarded, Beverage Level, Cost to Upgrade
beverages = [ ['Caju', 10, 5, 1, 20],
              ['Corote', 15, 10, 1, 60],
              ['Suco de Bagre', 30, 20, 1, 120], 
              ['Margarita', 60, 35, 1, 240], 
              ['Piña Colada', 100, 60, 1, 400] ]


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
        print('Beverage preparation min duration {0}'.format(preparoBebidaMin))
        print('Beverage preparation max duration {0}'.format(preparoBebidaMax))
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

class Beverage:
    def __init__(self, beverageIndex):
        self.beverageName = beverages[beverageIndex][0]
        self.beveragePrepareTime = beverages[beverageIndex][1]
        self.beverageCost = beverages[beverageIndex][2]

class Customer:
    def __init__(self, beveragesLevel):
        self.name = names[(random.randrange(0, len(names)))]
        self.beverage = Beverage(random.randrange(0, beveragesLevel+1))

class BarTender:
    bartenderWorkingEvent = Event()

    def sleep(self):
        self.bartenderWorkingEvent.wait()

    def wakeUp(self):
        self.bartenderWorkingEvent.set()

    def serveDrink(self, customer):
        #Set bartender as busy 
        self.bartenderWorkingEvent.clear()

        print('{0} is getting a {1}'.format(customer.name, customer.beverage.beverageName))
        beveragePreparationTime = customer.beverage.beveragePrepareTime
        time.sleep(beveragePreparationTime)
        print('{0} is done'.format(customer.name))
        print('Just gained ${0} .'.format(customer.beverage.beverageCost))

def printInterface(beveragesLevel, cash):
    print("Available drinks:")
    if (beveragesLevel == 0):
        print("{0}.{1}\t Prepare Time: {2} Price: {3} Level: {4} Upgrade Cost: {5}".format(beveragesLevel+1, beverages[0][0], beverages[0][1], beverages[0][2], beverages[0][3],  beverages[0][4]))
    else:
        print("{0}.{1}\t\t Prepare Time: {2} Price:  {3} Level: {4} Upgrade Cost: {5}".format(1, beverages[0][0], beverages[0][1], beverages[0][2], beverages[0][3], beverages[0][4]))        
        for i in range(1 , beveragesLevel+1):
            print("{0}.{1}\t Prepare Time: {2} Price: {3} Level: {4} Upgrade Cost: {5}".format(i+1, beverages[i][0], beverages[i][1], beverages[i][2], beverages[i][3], beverages[i][4]))

    print("Cash gained until now: $ {0}.00".format(cash))

if __name__ == '__main__':

    beveragesLevel = 0  # Variable to track level of bevarages of bar and know which ones are available
    cash = 0

    customerIntervalMin = 3     # 3 seconds
    customerIntervalMax = 15    # 15 seconds
    # Time between arrival of customers will differ between 3 and 15 seconds

    customers = []
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))

    bartender = BarTender()

    bar = Bar(bartender, customerIntervalMin, customerIntervalMax, numberOfSeats=3)
    printInterface(beveragesLevel, cash)
    bar.openShop()

    while len(customers) > 0:

        c = customers.pop()
        cash += c.beverage.beverageCost	
        # New customer enters the bar
        bar.enterBar(c)
        customerInterval = random.randrange(customerIntervalMin, customerIntervalMax+1)
        time.sleep(customerInterval)
        printInterface(beveragesLevel, cash)
        
        # Test lines
        # print("*" * 40)
        # print("Number of waiting customers/Number of seats")
        # print("{0}/{1}".format(len(barberShop.waitingCustomers), barberShop.numberOfSeats))
        # print("*" * 40)