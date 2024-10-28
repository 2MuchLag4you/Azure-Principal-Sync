

import requests



from msal import ConfidentialClientApplication
from datetime import datetime, timedelta

import time
import threading
from typing import Optional, Callable

from .Models import UserPrincipal, GroupPrincipal
from .Tools import Logger



class ServicePrincipal:
    """ServicePrincipal class to manage service principal synchronisation from Azure."""
    
    def __init__(self, client_application: ConfidentialClientApplication, tenant_id: str, log_dir: Optional[str]) -> None:
        """Initialise the ServicePrincipal object"""
        
        self.tenant_id = tenant_id
               
        self.__client_application = client_application
        self.__access_token = None
        self.__access_token_expiry = None
        self.__service_principal_id = None
        self.__log_dir = log_dir
        self.__sync_thread = None
        
        self.__scopes = [
            "https://graph.microsoft.com/.default"
        ]
        
        self.__logger = None
        self.set_logger()
        

    def set_logger(self) -> None:
        """Set the logger and log level"""
        
        if not isinstance(self.__logger, Logger):
            self.__logger = Logger(self.tenant_id, self.__log_dir)
            self.__logger.log_message("Logger set for ServicePrincipal", "debug")

    def check_access_token(self) -> bool:
        """Check if the access token is valid"""
        current_time = datetime.now()
        self.__logger.log_message(f"Access token check requested at: {current_time}", "debug")
        
        if self.__access_token is not None and self.__access_token_expiry > current_time:
            return True
        return False
                
    def __get_access_token(self) -> Optional[str]:
        """Get the access token for the service principal"""
        current_time = datetime.now()
        self.__logger.log_message(f"Access token requested at: {current_time}", "debug")
        if self.__access_token is not None and self.__access_token_expiry > current_time:
            return self.__access_token
        
        result = self.__client_application.acquire_token_for_client(scopes=self.__scopes)
        
        if "access_token" in result: 
            expire_time = current_time + timedelta(seconds=result['expires_in'])
            
            self.__access_token_expiry = expire_time
            self.__access_token = result['access_token']
            return self.__access_token
        
        self.__logger.log_message("Error getting access token", "error")
        self.__logger.log_message(result, "error")
        
        return None
            
    def get_tenant_id(self) -> str:
        """Get the tenant id for the service principal"""
        
        return self.tenant_id
    
    def get_service_principal(self) -> str:
        """Get the service principal from Azure"""
        
        # Check if the access token is still valid
        if not self.check_access_token():
            if not self.__get_access_token():
                raise Exception("Error getting access token")
        
        # Get the service principal if the script has already cached it
        if self.__service_principal_id is not None:
            return self.__service_principal_id
        
        app_id = self.__client_application.client_id
        
        
        self.__logger.log_message(f"Getting service principal for App ID: {app_id}", "info")
        url = f"https://graph.microsoft.com/v1.0/servicePrincipals?$filter=appId eq '{app_id}'"
        
        headers = {
            "Authorization": f"Bearer {self.__access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.__logger.log_message(f"Error getting service principal: {e}", "error")
            return None
        
        if response.status_code == 200:
            response_json = response.json()
            if response_json['value']:
                self.__service_principal_id = response_json['value'][0]['id']
                self.__logger.log_message(f"Service principal found: {response_json['value'][0]['displayName']} ({self.__service_principal_id})", "info")
                return self.__service_principal_id
        
        return None
    
    def get_assigned_groups(self) -> list[GroupPrincipal]:
        """Get the groups assigned to the service principal"""

        # Check if the access token is still valid
        if not self.check_access_token():
            if not self.__get_access_token():
                raise Exception("Error getting access token")
        
        # Get the service principal id
        service_principal_id = self.get_service_principal()
        if service_principal_id is None:
            return []
        
        self.__logger.log_message(f"Getting groups assigned to service principal: {service_principal_id}", "info")
        
        target_url = f"https://graph.microsoft.com/v1.0/servicePrincipals/{service_principal_id}/appRoleAssignedTo?$select=id,principalId,principalDisplayName,principalType,deletedDateTime"
        headers = {
            "Authorization": f"Bearer {self.__access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(target_url, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.__logger.log_message(f"Error getting groups assigned to service principal: {e}", "error")
            return []
        
        groups = []
        
        if response.status_code == 200:
            if response.json()['value']:
                for principal in response.json()['value']:
                    if principal['principalType'] == "Group":
                        groups.append(GroupPrincipal(
                            group_id=principal['principalId'],
                            display_name=principal['principalDisplayName'],
                        ))
            
        return groups
    
    
    def get_assigned_users(self) -> list[UserPrincipal]:
        """Get the users assigned to the service principal"""

        # Check if the access token is still valid
        if not self.check_access_token():
            if not self.__get_access_token():
                raise Exception("Error getting access token")
        
        # Get the service principal id
        service_principal_id = self.get_service_principal()
        if service_principal_id is None:
            return []
        
        self.__logger.log_message(f"Getting users assigned to service principal: {service_principal_id}", "info")
        
        target_url = f"https://graph.microsoft.com/v1.0/servicePrincipals/{service_principal_id}/appRoleAssignedTo?$select=id,principalId,principalDisplayName,principalType,deletedDateTime"
        headers = {
            "Authorization": f"Bearer {self.__access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(target_url, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.__logger.log_message(f"Error getting users assigned to service principal: {e}", "error")
            return []
        
        users = []
        
        if response.status_code == 200:
            if response.json()['value']:
                for principal in response.json()['value']:
                    if principal['principalType'] == "User":
                        users.append(UserPrincipal(
                            user_id=principal['principalId'],
                            email="",
                            name=principal['principalDisplayName'],
                            source="Directly"
                        ))
            
        return users

    def get_users_assigned_to_group(self, group: GroupPrincipal) -> list[UserPrincipal]:
        """Retrieve the users assigned to a group"""
        
        # Check if the access token is still valid
        if not self.check_access_token():
            if not self.__get_access_token():
                raise Exception("Error getting access token")
        
        # Get the service principal id
        service_principal_id = self.get_service_principal()
        if service_principal_id is None:
            return []
        
        if group.group_id is None:
            self.__logger.log_message("Group ID is None", "error")
            return []
        
        self.__logger.log_message(f"Getting users assigned to group: {group.group_id}", "info")
        
        target_url = f"https://graph.microsoft.com/v1.0/groups/{group.group_id}/members?$select=id,displayName,userPrincipalName"
        headers = {
            "Authorization": f"Bearer {self.__access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(target_url, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.__logger.log_message(f"Error getting users assigned to group: {e}", "error")
            return []
        
        users = []
        
        if response.status_code == 200:
            if response.json()['value']:
                for user in response.json()['value']:
                    users.append(UserPrincipal(
                        user_id=user['id'],
                        email=user['userPrincipalName'],
                        name=user['displayName'],
                        source=group.display_name
                    ))
        
        return users
    
    def __get_user_principal_name(self, user_id: str) -> str:
        """Get the user principal name from the user id"""
        
        # Check if the access token is still valid
        if not self.check_access_token():
            if not self.__get_access_token():
                raise Exception("Error getting access token")
            
        self.__logger.log_message(f"Getting user principal name for user: {user_id}", "info")
        
        target_url = f"https://graph.microsoft.com/v1.0/users/{user_id}?$select=id,displayName,userPrincipalName"
        headers = {
            "Authorization": f"Bearer {self.__access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(target_url, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.__logger.log_message(f"Error getting user principal name: {e}", "error")
            return ""
        
        if response.status_code == 200:
            return response.json()['userPrincipalName']
        
        return ""
    

    def sync_service_principal(self): 
        """Sync the service principal with the groups and users assigned to it"""
        
        self.__logger.log_message("Syncing service principal", "info")
        
        service_principal_id = self.get_service_principal()
        if service_principal_id is None:
            self.__logger.log_message("Service principal not found", "error")
            return
        
        groups = self.get_assigned_groups()
        users = self.get_assigned_users()
        
        for group in groups:
            users += self.get_users_assigned_to_group(group)
        
        for user in users:
            user.set_email(self.__get_user_principal_name(user.user_id))
        
        return users
    
    def auto_sync_service_principal(self, interval: int = 3600, callback: Optional[Callable[[list[UserPrincipal]], None]] = None) -> None:
        """Auto sync of the service principal with an optional callback function after each sync."""

        # Function to run the auto sync process
        def sync_thread():
            """Thread to run the auto sync process"""
            while True:
                users = self.sync_service_principal()  # Run the sync process
                if callback:
                    callback(users)  # Call the callback with the synced users
                time.sleep(interval) # Sleep for the interval

        # Start the auto-sync in a separate thread
        self.__sync_thread = threading.Thread(target=sync_thread, daemon=True)
        self.__sync_thread.start()
        self.__logger.log_message("Auto sync of service principal with callback requested", "info")
    
    
    def manual_sync_service_principal(self):
        """Manual sync of the service principal"""
        
        self.__logger.log_message("Manual sync of service principal requested", "info")
        return self.sync_service_principal()
    