class GroupPrincipal:
    """GroupPrincipal class represents a group in the system"""
    def __init__(self, group_id: str, display_name: str):
        self.group_id = group_id
        self.display_name = display_name

    def __eq__(self, other) -> bool:
        """Check if the group is equal to another group"""
        return self.group_id == other.group_id
    
    def __hash__(self):
        """Return the hash of the group id"""
        return hash(self.group_id)
    
    def __repr__(self) -> str:
        """Return the string representation of the group"""
        return f"GroupPrincipal(group_id={self.group_id}, display_name={self.display_name})"
    
    def __str__(self) -> str:
        """Return the string representation of the group"""
        return f"GroupPrincipal(group_id={self.group_id}, display_name={self.display_name})"
        
