class pillinfo:
    def __init__(self, id: int) -> None:
        self.id = id
        self.name = None
        self.quantity = None
        self.dosage = None
        self.expiration = None
        self.direction = None
    
    def setname(self, name):
        self.name = name
    
    def setquantity(self, quantity):
        self.quantity = quantity
    
    def setdosage(self, dosage):
        self.dosage = dosage

    def setexpiration(self, expiration):
        self.expiration = expiration

    def setdirection(self, direction):
        self.direction = direction

    def getname(self):
        return self.name
    
    def getquantity(self):
        return self.quantity
    
    def getdosage(self):
        return self.dosage
    
    def getexpiration(self):
        return self.expiration
    
    def getdirection(self):
        return self.direction
    
    def getid(self):
        return self.id
    
    def __str__(self) -> str:
        return "Pill ID: " + str(self.id) + \
                ", Name: " + str(self.name) + \
                ", Quantity: " + str(self.quantity) + \
                ", Dosage: " + str(self.dosage) + \
                ", Expiration: " + str(self.expiration) + \
                ", Direction: " + str(self.direction)
    