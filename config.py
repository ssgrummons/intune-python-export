from dotenv import load_dotenv
load_dotenv()
import os

# MS Graph
CLIENT_ID = os.environ.get("client_id") # Value should be kept in .env file
CLIENT_SECRET = os.environ.get("client_secret") # Value should be kept in .env file
TENANT_ID = os.environ.get("tenant_id")
RESOURCE = 'https://graph.microsoft.com/'

version = 'v1.0'

# "((ManagementAgents eq '2') or (ManagementAgents eq '64')) selects only Intune Managed Devices
# ((DeviceType eq '0') or (DeviceType eq '1') or (DeviceType eq '7') or (DeviceType eq '16')) selects only Windows devicess
report_template = {
    "reportName": "Devices",
    "filter": "((ManagementAgents eq '2') or (ManagementAgents eq '64')) and ((DeviceType eq '0') or (DeviceType eq '1') or (DeviceType eq '7') or (DeviceType eq '16'))",
    "select": [
        "DeviceName",
        "deviceType",
        "OSVersion",
        "LastContact",
        "CreatedDate",
        "UPN",
        "Model",
        "Manufacturer",
        "SerialNumber",
        "WifiMacAddress",
        "DeviceId"
        ]
    }

# If set to Audit Only, the data will be pulled from Graph but no groups will be changed
# No report will be sent to New Relic
audit_only = os.environ.get("audit_only")

if None != os.environ.get("debug"):
    debug = os.environ.get("debug")
else:
    debug = False
