from repositories.transactions import TransactionRepository

class TransactionService:
    def __init__(self, repository):
        self.repository: TransactionRepository = repository

    def create_transaction(self, user_id, category_id, amount, description, date_transaction):
        return self.repository.create_transactions(user_id, category_id, amount, description, date_transaction)
    
    def update_transaction(self, id, user_id, category_id, amount, description, date_transaction):
        return self.repository.update_transaction(id, user_id, category_id, amount, description, date_transaction)

    def delete_transaction(self, id, user_id):
        return self.repository.delete_transaction(id, user_id)
    
    def get_all_transaction(self, user_id):
        return self.repository.get_all_transaction(user_id)
    
    def get_transaction_by_id(self, transaction_id: int) -> dict:
        """
        Get a transaction by its ID.

        Args:
            transaction_id (int): The ID of the transaction to retrieve.

        Returns:
            dict: The transaction as a dictionary.
        """
        return self.repository.get_transaction_by_id(transaction_id)
