from repositories.users import UserRepository

class UserService:
    def __init__(self, repository):
        self.repository: UserRepository = repository

    def validate_password(self, password):
        
        if not password:
            raise ValueError("Password is not define")
        if len(password) <= 8:
            raise ValueError("Password must contains more than 8 characters")
        
        
    def create_user(self, username: str, password: str, fullname: str) -> dict:
        """
        Create a new user in the database.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            fullname (str): The full name of the user.

        Returns:
            dict: The created user.
        """
        self.validate_password(password)
        return self.repository.insert_user(username, fullname, password)

    def get_all_users(self):
        return self.repository.get_users()
    
    def get_users_by_id(self, id):
        return self.repository.get_user_by_id(id)
    
    def update_user(self, id: str, username: str, fullname: str, password: str) -> dict:
        """Update an existing user in the database.

        Args:
            id (str): The id of the user to update.
            username (str): The new username of the user.
            fullname (str): The new full name of the user.
            password (str): The new password of the user.

        Returns:
            dict: The updated user.
        """
        if password is not None:
            self.validate_password(password)
        return self.repository.update_user(id, username, fullname, password)
    
    def delete_user(self, id):
        return self.repository.delete_user(id)
    

    