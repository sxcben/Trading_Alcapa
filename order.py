class Order:
    next_id = 0

    def __init__(self, side, price, quantity):
        self.id = Order.next_id
        Order.next_id += 1
        self.price = price
        self.quantity = quantity
        self.side = side
    
    def check_negative_price(self):
        return self.price < 0

    def check_negative_quantity(self):
        print('function from Order')
        return self.quantity < 0
    
    def __str__(self):
        return 'ID: ' + str(self.id) + ' ; Side: ' + str(self.side) + ' ; Price: ' + str(self.price) + ' ; Quantity: ' + str(self.quantity)