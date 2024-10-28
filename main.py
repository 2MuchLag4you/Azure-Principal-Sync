from Azure import ServicePrincipal
from Azure.Models import UserPrincipal
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

sp.auto_sync_service_principal(interval=3600, callback=print_users_callback)
permissions = sp.get_assigned_permissions()