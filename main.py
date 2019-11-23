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

cash = 0

class Bar:
    """Class to represent the bar functioning correctly

    Attributes:
        bartender (Bartender): The bartender responsible for taking requests and serving them.
        customerIntervalMin (int): Mininum time possible for another client to arrive
        customerIntervalMax (int): Maximum time possible for another client to arrive
        numberOfSeats (int): Number of maximum possible customers that can wait to be attended

    Methods:
        openShop: Used to start the thread responsible for bartender
        bartenderGoToWork: See if there are customers waiting to be attended and free's the bartender to serve them
        if there are, else sends the bartender to sleep.
        enterBar: Adds a customer to the bar
    """
    waitingCustomers = []

    def __init__(self, bartender, customerIntervalMin, customerIntervalMax, numberOfSeats):
        self.bartender = bartender
        self.numberOfSeats = numberOfSeats
        self.customerIntervalMin = customerIntervalMin
        self.customerIntervalMax = customerIntervalMax
        # print('Bar initilized with {0} seats'.format(numberOfSeats))
        # print('Customer min interval {0}'.format(customerIntervalMin))
        # print('Customer max interval {0}'.format(customerIntervalMax))
        print('----------------------------------------')

    def openShop(self):
        """Starts thread responsible for handling bartenders work
        """
        print('Bar is opening')
        workingThread = Thread(target = self.bartenderGoToWork)
        workingThread.start()

    def bartenderGoToWork(self):
        """Checks the semaphore to see if bartender is occupied and if there are available clients to be attended.
        If waiting clients and unoccupied bartender, next waiting customer is served.
        If no waiting clients and barber is not serving, he goes to sleep.
        When customer arrives, the barber is awoken.
        """
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
        """Responsible for handling customers that arrive in bar. 
        If bar is full, makes customer leave the bar.
        If bar is not full, the customer will wait to be served.

        Args:
            customer (Customer): Customer object that will enter the bar.
        """
        mutex.acquire()
        print('>> {0} entered the bar and is looking for a seat'.format(customer.name))

        if len(self.waitingCustomers) == self.numberOfSeats:
            print('Waiting room is full, {0} is leaving.'.format(customer.name))
            mutex.release()
        
        else:
            print('{0} sat down on the balcony.'.format(customer.name))
            self.waitingCustomers.append(c)	
            mutex.release()
            bartender.wakeUp()

class Beverage:
    """Class to represent a beverage.

    Attributes:
        beverageIndex (int): Used to know which beverage to identify in the list beverages.
    """
    def __init__(self, beverageIndex):
        self.beverageName = beverages[beverageIndex][0]
        self.beveragePrepareTime = beverages[beverageIndex][1]
        self.beverageCost = beverages[beverageIndex][2]

class Customer:
    """Class to represent a customer.

    Attributes:
        beveragesLevel (int): Used to hold the level of beverages that the bar holds and know how many options can be served.
    """
    def __init__(self, beveragesLevel):
        self.name = names[(random.randrange(0, len(names)))]
        self.beverage = Beverage(random.randrange(0, beveragesLevel+1))

class BarTender:
    """Class to represent the bartender responsible for serving beverages.

    Attributes:
        customer (Customer): A Customer object that holds the necassary information such as name and beverage to be served.
    """
    bartenderWorkingEvent = Event()

    def sleep(self):
        """Puts the bartender thread to sleep.
        """
        self.bartenderWorkingEvent.wait()

    def wakeUp(self):
        """Wakes up the bartender thread.
        """
        self.bartenderWorkingEvent.set()

    def serveDrink(self, customer):
        """Makes the bartender serve the beverage to the customer and sets him busy. Also notifies when serving is done
        and how much cash was gained.

        Args:
            customer (Customer): Customer object with information such as name and the beverage that will
            be served.
            cash (int): Global variable to store the cash that bar has available. Updated here
            when client gets beverage.
        """
        global cash
        #Set bartender as busy 
        self.bartenderWorkingEvent.clear()

        print('{0} is getting a {1}'.format(customer.name, customer.beverage.beverageName))
        beveragePreparationTime = customer.beverage.beveragePrepareTime
        time.sleep(beveragePreparationTime)
        print('{0} is done'.format(customer.name))
        cash += customer.beverage.beverageCost
        print('Just gained ${0} .'.format(customer.beverage.beverageCost))

def printInterface(bar ,beveragesLevel, beverageUnlockCost, numberOfVisits, barReputation):
    """Function to print the user interface showing him the available beverages that can be served at the bar
    at the current moment and the cost to upgrade them or unlock new ones. Will also show cost and the upgrades available for the number of seats.

    Args:
        bar (Bar): Bar object used to show number of waiting customers and available seats.
        beveragesLevel (int): Index to know which beverages are available and their info.
        beverageUnlockCost (int): Amount of cash necessary to aquire new beverage to be served.
        barReputation (int): Keeps track of the bar reputation that makes more customers appear.
        cash (int): amount of cash the bar has to make upgrades.
    """
    global cash

    print("-" * 40)
    print("Seats occupied: {0}/{1} | Number Of Visits: {2} | Bar Reputation: {3}".format(len(bar.waitingCustomers), bar.numberOfSeats, numberOfVisits, barReputation))
    print("Available drinks:")
    if (beveragesLevel == 0):
        print("{0}.{1}\t Prepare Time: {2} Price: {3} Level: {4} Upgrade Cost: {5}".format(beveragesLevel+1, beverages[0][0], beverages[0][1], beverages[0][2], beverages[0][3],  beverages[0][4]))
    else:
        print("{0}.{1}\t\t Prepare Time: {2} Price:  {3} Level: {4} Upgrade Cost: {5}".format(1, beverages[0][0], beverages[0][1], beverages[0][2], beverages[0][3], beverages[0][4]))        
        for i in range(1 , beveragesLevel+1):
            print("{0}.{1}\t Prepare Time: {2} Price: {3} Level: {4} Upgrade Cost: {5}".format(i+1, beverages[i][0], beverages[i][1], beverages[i][2], beverages[i][3], beverages[i][4]))

    print("Cash gained until now: $ {0}".format(cash))
    print("Cost to unlock new beverage - {0}: $ {1}".format(beverages[beveragesLevel+1][0], beverageUnlockCost))
    print("Options available: 1 -> Unlock new drink | 2 -> Upgrade Caju | 9 -> Continue")
    print("-" * 40)

def inputHandler(userInput, beveragesLevel, beverageUnlockCost):
    """Function to handle the input that player chooses and do the acordding actions

    Args:
        userInput (int): The option that player chose.
        cash (int): Money that bar has to make upgrades.
        beveragesLevel (int): Number of beverages that bar can currently serve.
        beverageUnlockCost (int): Money necessary to aquire new beverage to serve.
        cash (int): Here cash is modified when an upgrade happens
    """
    global cash

    # User chose to continue as usual
    if userInput == 9:
        print("Continue on my friend.")
        print("-" * 40)
        return cash, beveragesLevel, beverageUnlockCost
    
    # User chose to aquire new beverage.
    elif userInput == 1:
        if cash >= beverageUnlockCost:
            cash -= beverageUnlockCost  # Subtracts new beverage cost from cash
            beveragesLevel += 1         # Beverages levels up
            beverageUnlockCost *= 10    # Cost to unlock next beverage is previous cost * 10
            print("Unclocked {0}".format(beverages[beveragesLevel][0]))
            print("*" * 40)

            return cash, beveragesLevel, beverageUnlockCost

        else:
            print("Not enough cash, stranger!")
            print("-" * 40)

    # User chose to upgrade Caju
    elif userInput == 2:
        if cash >= beverages[0][4]:
            cash -= beverages[0][4]                             # Subtracts Caju upgrade cost from cash
            beverages[0][3] += 1                                # Upgrades Caju level
            beverages[0][4] * 2                                 # Increases next Caju upgrade cost by twice its previous cost
            beverages[0][1] /= beverages[0][3]                  # Decreases caju preparation time by half
            print("Upgraded {0} skills!".format(beverages[0][0]))   # Prints out upgrade message

            return cash, beveragesLevel, beverageUnlockCost
        
        else:
            print("Not enough cash, stranger!")
            print("-" * 40)

    return cash, beveragesLevel, beverageUnlockCost

def checkReputation(barReputation, numberOfVisits):
    """Checks number of visits of bar and updates the reputation when necessary

    Args:
        barReputation (int): The higher, more frequently customers will appear at bar
        numberOfVisits (int): Is the number of customers that have been to the bar
    """
    if barReputation >= 5:
        return 5
    else:
        if numberOfVisits == 0:
            return 0
        elif (numberOfVisits % 100) == 0:
            barReputation += 1
            print("\nReputation went up by 1!!!\n")
            return barReputation

    return barReputation
    

if __name__ == '__main__':

    beveragesLevel = 0      # Variable to track level of bevarages of bar and know which ones are available
    beverageUnlockCost = 50 # Variable to register the cash necessary to unlock new beverage
    barReputation = 0       # The higher this gets, higher the chances of more customers coming in
    numberOfVisits = 0      # Tracks how much clients were served. Is used to calculate the bar reputation

    customerIntervalMin = 3     # 3 seconds
    customerIntervalMax = 10    # 15 seconds, will decrease based on reputation
    # Initial time between arrival of customers will differ between 3 and 15 seconds

    customers = []
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))
    customers.append(Customer(beveragesLevel))

    bartender = BarTender()

    bar = Bar(bartender, customerIntervalMin, customerIntervalMax, numberOfSeats=3)
    bar.openShop()

    while len(customers) > 0:

        printInterface(bar, beveragesLevel, beverageUnlockCost, numberOfVisits, barReputation)
        
        # Handling user input
        """If you want to show all beverages and thread and semaphore working correctly, remove
        2 lines below and modify beverages level above.
        """
        userInput = int(input("Choose an option: "))
        cash, beveragesLevel, beverageUnlockCost = inputHandler(userInput, beveragesLevel, beverageUnlockCost)

        c = customers.pop()                                                     # Gets a customer from customer list
        numberOfVisits += 1                                                     # +1 visitor
        barReputation = checkReputation(barReputation, numberOfVisits)          # Updates bar reputation if necessary
        customers.append(Customer(beveragesLevel))                              # Appends a new customer to list
        # New customer enters the bar
        bar.enterBar(c)
        
        customerIntervalMax -= barReputation     
        customerInterval = random.randrange(customerIntervalMin, (customerIntervalMax+1))
        time.sleep(customerInterval)                
        
        # Test lines
        # print("*" * 40)
        # print("Number of waiting customers/Number of seats")
        # print("{0}/{1}".format(len(barberShop.waitingCustomers), barberShop.numberOfSeats))
        # print("*" * 40)