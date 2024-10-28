from json import JSONEncoder


class GroupPrincipal:
    """GroupPrincipal class represents a group in the system"""
    def __init__(self, group_id: str, display_name: str, permissions_id: str) -> None:
        self.group_id = group_id
        self.display_name = display_name
        self.permissions_id = permissions_id

    def __eq__(self, other) -> bool:
        """Check if the group is equal to another group"""
        return self.group_id == other.group_id
    
    def __hash__(self):
        """Return the hash of the group id"""
        return hash(self.group_id)
    
    def __repr__(self) -> str:
        """Return the string representation of the group"""
        return f"GroupPrincipal(group_id={self.group_id}, display_name={self.display_name}, permissions_id={self.permissions_id})"
    
    def __str__(self) -> str:
        """Return the string representation of the group"""
        return f"GroupPrincipal(group_id={self.group_id}, display_name={self.display_name}, permissions_id={self.permissions_id})"
        
        
    def json(self) -> dict:
        """Return the JSON representation of the group."""
        return JSONEncoder().encode(self.__dict__)
