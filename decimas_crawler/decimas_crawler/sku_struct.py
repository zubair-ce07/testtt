
class Skus:
    price = None
    currency = None 
    size = None
    colour = None
    sku_id = None
    
    def __init__(self, price, currency, size, colour, sku_id):
        self.price = price
        self.currency = currency
        self.size = size
        self.colour = colour
        self.sku_id = sku_id

class ColourProdcuts:
    color = None
    products = []
    def __init__(self, data):
        self.color = data['label']
        self.products = data['prodcuts']
