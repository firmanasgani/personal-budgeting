from repositories.category import CategoryRepository
import enum

class typeEnum(enum.Enum):
    EXPENSES = "expenses"
    INCOME = "income"

class CategoryService:
    def __init__(self, repository):
        self.repository: CategoryRepository = repository

    def create_category(self, name, code, type, user):
        if type not in [item.value for item in typeEnum]:
            raise ValueError('Invalid type')

        return self.repository.create_category(name, code, type, user)
    
    def get_all_categories(self):
        return self.repository.get_all_categories()
    
    def get_category_by_id(self, id):
        return self.repository.get_category_by_id(id)
    
    def update_category(self, id, name, code, type, user):
        if type not in [item.value for item in typeEnum]:
            raise ValueError('Invalid type')

        return self.repository.update_category(id, name, code, type, user)

    def delete_category(self, id):
        return self.repository.delete_category(id)