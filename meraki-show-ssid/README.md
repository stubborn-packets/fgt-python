# List Meraki SSID Info using the Meraki SDK

Meraki and Python, goes together like lamb and tuna fish (Big Daddy reference). With Meraki working off a central cloud controller model using Network automation with Meraki just makes sense. You have one central place to query all the data you need and build scripts around, whether that is just showing information and creating a new network. 

To make our Network Automation goals achieved easier and to increase adoption they have created the Meraki SDK. This SDK is available to us via PIP and makes doing tasks within Meraki so simple. This is partly due to the fact that the data is returned to us in Python objects so we can quickly and easily do things with the data. No more converting the responses from XML or JSON into Python! This is HUGE! 

In this example I’m going to show you how to query the all the SSID’s setup in an network and display some of the data on the console for each SSID. For this I’m going to be using the Read Only Meraki DevNet sandbox which Cisco provides to us for free. Once you see how easy it is to get this data, you can start thinking about way to import it into your environment.

Below are some links that will be helpful to you if you wish to learn more about the Meraki SDK, DevNet Sandbox and the Meraki API documentation

Meraki Github [https://github.com/meraki](https://github.com/meraki)

PyPi Meraki [https://pypi.org/project/meraki/#description](https://pypi.org/project/meraki/#description)

DevNet Sandbox [https://developer.cisco.com/site/sandbox/](https://developer.cisco.com/site/sandbox/)

Meraki API Documentation [https://developer.cisco.com/meraki/api-v1/](https://developer.cisco.com/meraki/api-v1/)

***Full script: meraki-show-ssid.py***

## Lab Overview

In this lab we are going to query all the SSIDs in a given network and display the name, if it’s enabled, if it’s visible, the PSK if there is one and the IP address assignment type. I’m only doing this for a single Network but you could easily pull all the networks attached to an organization and do the same with just a few extra lines of code.

Like I mentioned above, to accomplish this I’m going to use the Read Only account in the Meraki DevNet Sandbox. The login information and API key can be found once you login to the [Cisco Developer website]([https://developer.cisco.com/](https://developer.cisco.com/)) and registration is free. High recommended if you want to learn what you can do with Meraki and Network Automation.

As the login information could change, I’m storing the API key in a separate file called [env.py](http://env.py) and importing that into my working file. All you need to get started is an API key from the DevNet Sandbox or your own Meraki environment. Here is a link to the documentation for obtaining your Meraki API key

[https://developer.cisco.com/meraki/api-v1/#!authorization](https://developer.cisco.com/meraki/api-v1/#!authorization)

## Preparation

To start working with the Meraki SDK we need to install the module which we can do very easily using PIP.
```
pip install meraki
```
That is it. Now let’s jump into the code

## Time spent is time saved (coding)

With any modules that someone wrote and made available to us (thank you!) that we use to use in our project, we need to import them.
```
import meraki
from rich import print as rprint
from env import API_KEY, NET_ID
```
- import meraki - this is the SDK which handles all the backend connection handling so we don’t need to
- from rich import print as rprint - not needed but does make things look nicer in the console.
- from env import API_KEY and NET_ID - these are the environment variables which have been provided from the Cisco DevNet Sandbox. The API key is the most important as that is your token to be able to access the sandbox. Without that, you would receive a 401 unauthorized. And the NET_ID is the Network ID that I’m going to query. Since I’m only looking at a single network I only have 1 network ID. However if I was going to be querying multiple networks I could have a list of them and use a for loop to go through each one

Meraki has a few different API which they make available to us. In this example I’m going to be using the Dashboard API. To make our lives easier I’m going to define a variable called DASHBOARD and assigned it to the Meraki Dashboard function and include my API key. This will be used each time that we make a call into the Meraki dashboard.
```
DASHBOARD = meraki.DashboardAPI(API_KEY)
```
To make this code easier to read and increase the reusability of the code, I’m going to break the code up into two functions:

1. query the Meraki Dashboard and get all the SSIDs on that network in put that into a list
2. take the list object and iterate through it displaying the relevant data for each SSID to the console

Let’s start with the first function, the querying of data.
```
def find_ssids(netId):
    """Used to find all the SSIDs on a particular network"""
    response = DASHBOARD.wireless.getNetworkWirelessSsids(netId)
    export_ssids(response)
```
I’ve defined a function called find_ssids() which takes in the Network ID of the network we wish to query. 

Next making the call to Meraki using the DASHBOARD function which we created above. Remember this does include the API Key so our request is authorized. Within the DASHBOARD function I’m going to go into the wireless set of functions and finally the getNetworkWirelessSsids function and passing in the Network ID variable. Phew. This might sound like a lot but it is quite easy after you’ve done it a few times. If you want to see what functions are available and what is required for each function you have two options:

1. The Meraki API reference guide [https://developer.cisco.com/meraki/api-v1/#!api-reference-overview](https://developer.cisco.com/meraki/api-v1/#!api-reference-overview)
2. VScode! As you’re writing the API call VScode context sensitive help will also guide you and let you know what it can return and what is required. 

If you print the response right now you will get back a list object of dictionaries for each SSID. And this is already a Python dictionary, not just JSON data being presented. This is the power of the SDK in Python.

Finally we are going to take that list object and send it over to the export_ssids function which will take that list and break it down SSID by SSID and present the data to us. Each dictionary contains a bunch of information, some of wish we may not need to look at or need. Here is an example of what you would get back without removing anything
```
{
    'number': 14,
    'name': 'Unconfigured SSID 15',
    'enabled': False,
    'splashPage': 'None',
    'ssidAdminAccessible': False,
    'authMode': 'open',
    'radiusAccountingEnabled': None,
    'ipAssignmentMode': 'NAT mode',
    'adultContentFilteringEnabled': False,
    'dnsRewrite': {'enabled': False, 'dnsCustomNameservers': []},
    'minBitrate': 11,
    'bandSelection': 'Dual band operation',
    'perClientBandwidthLimitUp': 0,
    'perClientBandwidthLimitDown': 0,
    'perSsidBandwidthLimitUp': 0,
    'perSsidBandwidthLimitDown': 0,
    'mandatoryDhcpEnabled': False,
    'visible': True,
    'availableOnAllAps': True,
    'availabilityTags': [],
    'speedBurst': {'enabled': False}
}
```
I have defined a second function called export_ssids that takes in a variable which I’ve assigned ssidList which is going to be the list we just created. This variable can be named anything you want, my suggestion would be to name is something that is related to the data so when you look back at your code you know what is happening.

Now that we have our list in our function, we are going to create a for loop so we can iterate through that list object.
```
def export_ssids(ssidList):
    """Takes in a list of SSIDs and breaks the information down"""
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
```
I’m using Rich to print out 25 red asterisks so that way I can easy tell in the console where one SSID starts and ends. Just something nice for the console. 

Next I’m printing out specific information from the SSID dictionary and because it’s nested in a for loop we are only looking at one SSID at a time but the code will be repeated for each SSID in the list. And because this is already a dictionary, you can call it just like you would any other dictionary dictionary[’key’] and the value is printed. 

For the password you need to structure it a little different if you want to display the PSK. If the authmode is open you will not have a key for psk telling you want the password is, because why would you when there is no password. So I created a simple if statement looking if the auth mode was open then I just wrote ‘open - no password required’ however if the auth mode was psk then I looked for the value of the psk key. 

And finally since all the code is in functions they need to be called before they can be executed. To do that I have this little statement below
```
if __name__ == "__main__":
    find_ssids(NET_ID)
```
This simply just states that if this specific file is ran then the find_ssids() function can be run using the provided network ID. This makes it so if you want to re-use the function in a different script you’re not worrying about anything running. 

Now if you run the script you should get some output similar to what I have below. With the SDK you also get a log file each time you run so if you see that in your project don’t be alarmed.

```
*************************
SSID Name: DevNet Sandbox ALWAYS ON - wirel
Is Enabled: True
Is visible to users: True
Password: OPEN - NO PASSWORD REQUIRED
IP Address Assignment Mode: NAT mode
*************************
SSID Name: TEST
Is Enabled: True
Is visible to users: True
Password: DevNetMegaAPI4ever
IP Address Assignment Mode: NAT mode
*************************
SSID Name: Réseau invité
Is Enabled: True
Is visible to users: True
Password: OPEN - NO PASSWORD REQUIRED
IP Address Assignment Mode: NAT mode
*************************
```
Congrats!

## Final Thoughts

The Meraki SDK is a blast to work with. This tool really makes it easy to script out and get the data back all using Python. No more converting from one data format into another, this keeps it all within Python and makes the code easy and clean.