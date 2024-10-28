from azure_principal_sync import ServicePrincipal
from azure_principal_sync.Models import UserPrincipal, GroupPrincipal, PrincipalPermissions
from msal import ConfidentialClientApplication

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

APP_ID = os.getenv('AZURE_CLIENT_APP_ID')
TENANT_ID = os.getenv('AZURE_OWN_TENANT_ID')
CLIENT_SECRET = os.getenv('AZURE_CLIENT_APP_SECRET')


# Create a ConfidentialClientApplication
app = ConfidentialClientApplication(
    client_id=APP_ID,
    client_credential=CLIENT_SECRET,
    authority=f'https://login.microsoftonline.com/{TENANT_ID}'
)

# Create a Service Principal
sp = ServicePrincipal(
    client_application=app,
    tenant_id=TENANT_ID,
    log_dir=None
)

def print_users_callback(users: list[UserPrincipal]) -> None:
    """Callback function to print each UserPrincipal in the users list."""
    for user in users:
        print(user.json())
        
def print_groups_callback(groups: list[GroupPrincipal]) -> None:
    """Callback function to print each GroupPrincipal in the groups list."""
    for group in groups:
        print(group.json())
        
def print_permissions_callback(permissions: list[PrincipalPermissions]) -> None:
    """Callback function to print each PrincipalPermissions in the permissions list."""
    for permission in permissions:
        print(permission.json())

# Test sync every 2 minutes
sp.auto_sync_service_principal(interval=3600, user_callback=print_users_callback, group_callback=print_groups_callback, permission_callback=print_permissions_callback)