import meraki
from rich import print as rprint
from env import API_KEY, NET_ID

DASHBOARD = meraki.DashboardAPI(API_KEY)

def find_ssids(netId):
    """Used to find all the SSIDs on a particular network"""
    response = DASHBOARD.wireless.getNetworkWirelessSsids(netId)
    export_ssids(response)

def export_ssids(ssidList):
    for ssid in ssidList:
        rprint('[red]*[/red]' * 25)
        rprint(f"SSID Name: {ssid['name']}")
        rprint(f"Is Enabled: {ssid['enabled']}")
        rprint(f"Is visible to users: {ssid['visible']}")
        if ssid['authMode'] == 'open':
            rprint(f"Password: OPEN - NO PASSWORD REQUIRED")
        else:
            rprint(f"Password: {ssid['psk']}")
        rprint(f"IP Address Assignment Mode: {ssid['ipAssignmentMode']}")

if __name__ == "__main__":
    find_ssids(NET_ID)