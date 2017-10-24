# LAN-IoT-profile-manager
A simple manager that receives a JSON formatted string(a profile), and then applies it to a local area network with IoT devices
(currently only support for Lifx bulbs)

Usage:

## For getting a json formatted overview of current state of online bulbs:

python liotpm.py state '{"devices":[{"mac":"00:00:00:00:00:00","ip":"192.168.0.1"}]}'

## For applying a 'profile' or json array to specified bulbs 

 python liotpm.py apply '{"devices":[{"mac":"00:00:00:00:00:00","ip":"192.168.0.1","power":"on","brightness":"65535","hue":"0","saturation":"0","temperature":"9000","duration":"1000"}]}'




This little script is using https://github.com/mclarkk/lifxlan, which is a great module for locally controlling lifx bulbs.
