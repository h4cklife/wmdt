# WMDT


## Requirements

1. Python3.6

2. Aircrack-ng suite



## Install

```
$ git clone https://github.com/h4cklife/wmdt.git
$ cd wmdt/
$ chmod +x wmdt.py
```


## Usage

```
$ airmon-ng start wlan0
$ airodump-ng wlan0mon
```

Note the channel and bssid you want to attack

```
$ ./wmdt.py
```

