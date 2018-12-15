# WMDT


## Requirements

1. Python3.6

2. Aircrack-ng suite



## Install

```
$ git clone https://github.com/dbe-5/wmdt.git
$ cd wifimassdeauth
$ chmod +x wifimassdeauth.py
```


## Usage

```
$ airmon-ng start wlan0
$ airodump-ng wlan0mon
```

Note the channel and bssid you want to attack

```
$ ./wifimassdeauth.py
```

