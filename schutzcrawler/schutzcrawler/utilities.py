class Utilities:
    def next_request_or_product(self, product):
        if product["requests"]:
            return product["requests"].pop()
        else:
            return product