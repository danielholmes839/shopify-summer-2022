class ProductNotFound(Exception):
    def __init__(self, product_id: str):
        self.message = f'product with id:{product_id} not found'
        super().__init__(self.message)

    def __repr__(self) -> str:
        return self.message


class ProductAttributeException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __repr__(self) -> str:
        return self.message
