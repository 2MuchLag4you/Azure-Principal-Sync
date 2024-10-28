class UserPrincipal:
    """UserPrincipal class represents a user in the system"""
    def __init__(self, user_id: str, email: str, name: str, source: str = "Directly") -> None:
        self.user_id = user_id
        self.email = email
        self.name = name
        self.enabled = True
        self.source = source

    def set_email(self, email: str) -> None:
        """Set the email of the user"""
        self.email = email

    def enable(self) -> None:
        """Enable the user"""	
        self.enabled = True

    def disable(self) -> None:
        """Disable the user"""
        self.enabled = False

    def is_enabled(self) -> bool:
        """Check if the user is enabled"""
        return self.enabled

    def __eq__(self, other) -> bool:
        return self.user_id == other.user_id
    
    def __hash__(self):
        return hash(self.user_id)
    
    def __repr__(self) -> str:
        return f"UserPrincipal(user_id={self.user_id}, email={self.email}, name={self.name})"

    def __str__(self) -> str:
        return f"UserPrincipal(user_id={self.user_id}, email={self.email}, name={self.name})"