from typing import Optional


class Product:
    def __init__(self, id: str, name: str, description: str, category: Optional[str]):
        self.id = id
        self.name = name
        self.description = description
        self.category = category

    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category
        }
