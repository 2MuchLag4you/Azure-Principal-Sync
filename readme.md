# Azure Service Principal Synchronization
This repository provides an example for setting up and managing an Azure Service Principal synchronization process using Python. The code demonstrates loading environment variables, creating an MSAL application client, and performing actions such as retrieving assigned users, groups, permissions, and synchronizing users automatically or manually.

## Requirements
- Python 3.10+
- [Azure identity](https://pypi.org/project/azure-identity/)
- [MSAL](https://pypi.org/project/msal/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Setup
1. Clone the repository and navigate to the directory:
```bash
git clone <repository_url>
cd <repository_directory>
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Configure environment variables: Create a `.env` file with the following variables:
```plaintext
AZURE_CLIENT_APP_ID=<Your Azure Application ID>
AZURE_OWN_TENANT_ID=<Your Tenant ID>
AZURE_CLIENT_APP_SECRET=<Your Application Secret>
```
## Usage
The notebook provides details on:
- Loading modules and environment variables
- Setting up a `ConfidentialClientApplication` and a `ServicePrincipal`
- Retrieving assigned users, groups, permissions, and synchronization options

For code specifics on synchronization methods and additional details, please refer to the [notebook](azure_sync.ipynb) on GitHub.