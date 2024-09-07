from repositories.auth import AuthRepository

class AuthService:
    def __init__(self, repository):
        self.repository: AuthRepository = repository

    def login(self, username: str, password: str) -> dict:
        print(username)
        return self.repository.login(username, password)