from repositories.budget import BudgetRepository

class BudgetService:
    def __init__(self, repository):
        self.repository: BudgetRepository = repository
        self.budgets = []
    
    def get_all_budget(self, user_id, category, start_date, end_date):
        return self.repository.get_all_budget(user_id, category, start_date, end_date)
    
    def get_budget_by_id(self, id):
        return self.repository.get_budget_by_id(id)
    
    def create_budget(self, user_id, category_id, amount, start_date, end_date, description):
        return self.repository.create_budget(user_id, category_id, amount, start_date, end_date, description)
    
    def update_budget(self, id, user_id, category_id, amount, start_date, end_date, description):
        return self.repository.update_budget(id, user_id, category_id, amount, start_date, end_date, description)
    
    def delete_budget(self, id, user_id):
        return self.repository.delete_budget(id, user_id)
