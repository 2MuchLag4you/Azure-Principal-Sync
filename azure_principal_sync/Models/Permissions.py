from typing import Optional
from json import JSONEncoder

class PrincipalPermissions:
    """Azure Role Permissions assigned to a Service Principal."""
    
    def __init__(self, permission_id: str, description: Optional[str], display_name: str, is_enabled: bool, permissions_value: str) -> None:
        self.id = permission_id
        self.description = description
        self.display_name = display_name
        self.permissions_value = permissions_value
        self.is_enabled = is_enabled
    
    def enable(self) -> None:
        """Enable the permission."""
        self.is_enabled = True
    
    def disable(self) -> None:
        """Disable the permission."""
        self.is_enabled = False
        
    def __repr__(self) -> str:
        """Return the string representation of the permission."""
        return f"PrincipalPermissions(id={self.id}, display_name={self.display_name}, is_enabled={self.is_enabled}, permissions_value={self.permissions_value})"
        
    def __str__(self) -> str:
        """Return the string representation of the permission."""
        return f"PrincipalPermissions(id={self.id}, display_name={self.display_name}, is_enabled={self.is_enabled}, permissions_value={self.permissions_value})"

    def __hash__(self) -> int:
        """Return the hash of the permission id."""
        return hash(self.id)
    
    def json(self) -> dict:
        """Return the JSON representation of the permission."""
        return JSONEncoder().encode(self.__dict__)