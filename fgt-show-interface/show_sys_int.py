import getpass
from netmiko import ConnectHandler
from rich import print as rprint

# Define Fortigate Connection Dictionary
FGT = {
    "device_type": 'fortinet',
    "host": "",
    "username": "",
    "password": "",
}

# Prompt user for credentials and host information
FGT["host"] = input("What is the device IP address: ")
FGT["username"] = input("What is the username: ")
FGT["password"] = getpass.getpass()

with ConnectHandler(**FGT) as conn:
    # Find the hostname of the device
    hostname = conn.find_prompt()[:-1]
    # print(hostname)

    # Commands to send to device
    create_loopback = [
    'config system interface',
    'edit Loopback99',
    'set vdom root',
    'set type loopback',
    'set alias Loopback99',
    'set ip 10.99.99.1/24',
    'set allowaccess ping',
    'next',
    'end',
    ]

    # Create a loopback interface sending the list object and print the SSH output
    rprint(f'Running commands on: [green]{hostname}[/green]')
    output = conn.send_config_set(create_loopback)
    rprint('[red]*[/red]' * 5 + 'CONFIG OUTPUT' + '[red]*[/red]' * 5)
    rprint(output)
    
    # Verify that the interface has been added and print the results
    verify_output = conn.send_command('show system interface Loopback99')
    rprint('[red]*[/red]' * 5 + 'VERIFY CONFIG' + '[red]*[/red]' * 5)
    print(verify_output)