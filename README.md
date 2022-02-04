# chia-ping

Here's what happens when a Network Engineer starts playing with blockchains.

A clone of our old friend `ping` using small transactions over the [Chia](https://www.chia.net/) blockchain instead of ICMP packets to show the round-trip latency of on-chain transactions.

This is a toy program I wrote for getting more familiar with the Chia RPC APIs.

Here's how it looks:

```console
$ ./chia-ping.py -c 5
PING txch1a95eaxlg67k9u4d8eakavgrk3gkprsjaxwdhgxqztcmeqc7huhjs5nypjm 1 mojos of chia with 0 fees.
1 mojos to e9699e9be8d7ac5e55a7cf6dd620768a2c11c25d339b7418025e379063d7e5e5: seq=0 time=55.24 s
1 mojos to e9699e9be8d7ac5e55a7cf6dd620768a2c11c25d339b7418025e379063d7e5e5: seq=1 time=46.72 s
1 mojos to e9699e9be8d7ac5e55a7cf6dd620768a2c11c25d339b7418025e379063d7e5e5: seq=2 time=86.36 s
1 mojos to e9699e9be8d7ac5e55a7cf6dd620768a2c11c25d339b7418025e379063d7e5e5: seq=3 time=75.51 s
1 mojos to e9699e9be8d7ac5e55a7cf6dd620768a2c11c25d339b7418025e379063d7e5e5: seq=4 time=91.16 s
--- txch1a95eaxlg67k9u4d8eakavgrk3gkprsjaxwdhgxqztcmeqc7huhjs5nypjm ping statistics ---
5 transactions confirmed
round-trip min/avg/max/stddev = 46.717/70.996/91.159/19.370 s
```

## Installation

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -U pip
$ pip3 install -r requirements.txt
```

---
« C'est totalement inutile et donc rigoureusement indispensable ! »

-- [Jérôme Bonaldi](https://fr.wikipedia.org/wiki/J%C3%A9r%C3%B4me_Bonaldi)
