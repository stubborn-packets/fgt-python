# Using Netmiko with FortiGate

As a big fan and user of FortiNet’s FortiGate products I have found myself really liking the CLI more than the GUI. Being a Network Engineer the CLI always is the safe place, where magic happens and where a few misspelled words after typing all day will make you want to throw your keyboard. Not saying that the GUI isn’t fantastic or doesn’t have it’s place, it most certainly does especially when review logs and long lines of IPv4 Policies. But for any configuration needs, the CLI is my friend.

One great thing about having a CLI is the ability to script out changes using our favorite network automation tool, Python! This is where our friend Netmiko comes in. This fantasic tool allows for us as Network Engineers to script out our CLI commands so they can be easily repeated on as many devices as needed. Netmiko supports many devices natively but Fortinet is still in experimental support so some things many not work but for most of the scripts I’ve written it has been awesome and I haven’t seen any issues. 

If you wish to know more about Netmiko please see Kirk Byers Github page for full documentation and including list of supported platforms
https://github.com/ktbyers/netmiko

***Full script: show_sys_int.py***

## Lab and Demo Information

In this demo let’s:
1. Connect to a Fortigate and get the hostname
2. Create a Loopback interface 
3. Show the interface configuration to verify. 
Let’s take a look and see what this looks like in a lab environment using EVE-NG running FortiGate v7.0.9.

*If you’re going to try this in your lab, you can download a FortiGate image from [FortiNet’s Support site](https://support.fortinet.com) with a valid account and  device registration. I unfortunately cannot provide anyone with access to the images.*

## Preparation

Firstly we need to get our client setup for connecting to our device. For this, I’m using Linux WSL running on a Windows Machine. I have Python 3.10 installed and using a virtual environment to isolate the packages.

Next we need to install Netmiko which can be installed using pip. I am also going to install rich as it making printing items on the terminal look nice and pretty.
```
pip install netmiko
pip install rich
```
I have my lab running in EVE-NG and setup a subnet which I can reach locally from my computer, 10.199.199.0/24. A good test is to make sure that you can ping/ssh into the box before coding so you don’t start spinning your head later wondering why something isn’t working when it turns out you had the wrong username/password or the device isn’t routable. 

Lastly I’m using VScode to write all my code. I’ve been a huge fan of how lightweight it is and how easily it works with Git and GitHub. But you can use any editor of your choosing. 

Once ping/SSH has been confirmed, now we can start with the fun stuff!


## print(”Hello World!”)

No we are not really going to print Hello World even though that is generally the first thing you do when learning a new programming language. We are going to start with the basics and get the hostname of the device. 

To start I’m creating a new file (show-sys-int.py) and I’m going to import a few modules
- getpass - allows for a password to be requested without it displaying the characters as it’s being typed
- ConnectHandler from netmiko - this is going to handle all the backend connection magic to the FortiGate
- print from rich - not needed but it does make printing out to the console look nice
```
import getpass
from netmiko import ConnectHandler
from rich import print as rprint
```
With the modules imported, we can start writing our first bit of code. We are going to create a dictionary for all the device variables and also ask the user to type in the IP address of the connecting device as well as the user credentials for SSH
```
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
```
Next let’s us connect to the device and let’s get the hostname of it. Something basic that tells us that Netmiko is working as expected and plus we can use the hostname later ;) For this we are going to use a connection manager with Netmiko which will automatically close the session when the code is completed. Very important to always close your connections! 

Within the ConnectHandler we are going to unpack the FGT dictionary created above and assign that to the variable conn. This allows us to store that information if we needed to make additional calls to the device we don’t need to unpack and device those variables.
```
with ConnectHandler(**FGT) as conn:
    hostname = conn.find_prompt()[:-1]
    print(hostname)
```
I’m using stripping the last character out of the hostname to remove the ‘#’ that is found when you SSH into the device. Just makes using it later in code cleaner. And we like clean code

With the above run, you should get something like this:
```
(.venv) jbuck:~/fgt-python/fgt-show-interface$ python3 show_sys_int.py 
What is the device IP address: 10.199.199.100
What is the username: admin
Password: 
LAB-FGT-1
```
If that worked, we can go ahead and remove the print(hostname) or comment it out as we know that works. I’ll comment it out so if I ever need to refer to it later or work backwards on an issue it’s still there. I do a lot of print statements in my code projects so I know things are working and then comment out the print statements when I’ve verified it’s working. 


## Show me the goods!

With basic connectivity confirmed and Netmiko working like a champ, let’s now get to the good stuff and create a loopback interface and verify it!

Netmiko supports sending CLI commands in a string format. This can be a single string, list of strings and a list of commands from a text file. For this we’re going to demo sending commands from a list as well as a single string. 

Hopefully if you’re reading this you have some familiarity with the FortiNet CLI syntax. If not, no worries, it’s pretty easy to follow if you know how to do this on other platforms. I’m first going to create a list object with each item being a string containing the commands in sequence I want to run. These are the same commands that you would run if you were SSH’d into the FortiGate.
```
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
```
If you follow the list we’re creating an interface named ‘Loopback99’, assigning it to the root vdom, setting the type as looback, giving it the IP address of 10.99.99.1/24 and allowing PING. There are so many options that you can configure but these should give us a good starting point.

Next let’s use the power of Netmiko and send these commands to the FortiGate.
```
# Create a loopback interface sending the list object and print the SSH output
rprint(f'Running commands on: [green]{hostname}[/green]')
output = conn.send_config_set(create_loopback)
rprint('[red]*[/red]' * 5 + 'CONFIG OUTPUT' + '[red]*[/red]' * 5)
rprint(output)
```
To start I’m using Rich to add some color to console output, because just looking at white text on a black console isn’t fun. I’m doing a simple print statement to say that the commands are running and specifying the hostname variable we created earlier. I like to do this so if you are connecting to multiple devices you know where you’re at. For a single device, it just looks nice. 

Next we are going to use the ConnectHandler object conn that we created earlier and also using the send_config_set() function to define our list object. I’m assigning this to a variable named output which I can use to print later.

If you run the code right now, you should see Netmiko running the CLI commands just like if you were SSH’d into the FortiGate.
```
(.venv) jbuck:~/fgt-python/fgt-show-interface$ python3 show_sys_int.py 
What is the device IP address: 10.199.199.100
What is the username: admin
Password: 
Running commands on: LAB-FGT-1 
*****CONFIG OUTPUT*****
config system interface
LAB-FGT-1 (interface) # edit Loopback99
new entry 'Loopback99' added
LAB-FGT-1 (Loopback99) # set vdom root
LAB-FGT-1 (Loopback99) # set type loopback
LAB-FGT-1 (Loopback99) # set alias Loopback99
LAB-FGT-1 (Loopback99) # set ip 10.99.99.1/24
LAB-FGT-1 (Loopback99) # set allowaccess ping
LAB-FGT-1 (Loopback99) # next
LAB-FGT-1 (interface) # end
LAB-FGT-1 #
```
Now let’s finish it up and verify that the newly created Loopback is setup correctly. Again we are going to use the ConnectHandler object conn but use the send_command() function as we are going to send one command. This function only takes one string object. I’m going to send ‘show system interface Loopback99’ and print that out as well. 
```
# Verify that the interface has been added and print the results
verify_output = conn.send_command('show system interface Loopback99')
rprint('[red]*[/red]' * 5 + 'VERIFY CONFIG' + '[red]*[/red]' * 5)
print(verify_output)
```
Now if you run the full script your output should look like mine below:
```
(.venv) jbuck:~/fgt-python/fgt-show-interface$ python3 show_sys_int.py 
What is the device IP address: 10.199.199.100
What is the username: admin
Password: 
Running commands on: LAB-FGT-1 
*****CONFIG OUTPUT*****
config system interface
LAB-FGT-1 (interface) # edit Loopback99
new entry 'Loopback99' added
LAB-FGT-1 (Loopback99) # set vdom root
LAB-FGT-1 (Loopback99) # set type loopback
LAB-FGT-1 (Loopback99) # set alias Loopback99
LAB-FGT-1 (Loopback99) # set ip 10.99.99.1/24
LAB-FGT-1 (Loopback99) # set allowaccess ping
LAB-FGT-1 (Loopback99) # next
LAB-FGT-1 (interface) # end
LAB-FGT-1 # 
*****VERIFY CONFIG*****
config system interface
    edit "Loopback99"
        set vdom "root"
        set ip 10.99.99.1 255.255.255.0
        set allowaccess ping
        set type loopback
        set alias "Loopback99"
        set snmp-index 8
    next
end
```

## Final Thoughts

That was fun! Netmiko makes sending command(s) to devices really easy and fast. You can see the power of this if you needed to make a change to 5, 10, 100 device were you can create a script and have it do all the work for you. Spend a few minutes writing the script and save hours. Well worth learning!

To see the full script: show_sys_int.py
