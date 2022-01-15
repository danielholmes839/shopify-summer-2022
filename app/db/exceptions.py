class ItemNotFound(Exception):
    def __init__(self, item_id: str):
        self.message = f'item with id:{item_id} not found'
        super().__init__(self.message)

    def __repr__(self) -> str:
        return self.message


class ItemAttributeException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __repr__(self) -> str:
        return self.message
