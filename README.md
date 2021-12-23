# chia-ping

A clone of our old friend `ping` using small transactions over the [Chia](https://www.chia.net/) blockchain instead of ICMP packets.

This is a toy program I wrote for getting more familiar with the Chia RPC APIs.

Here's how it looks:

```console
% ./chia-ping.py xch12j86vecwyzks3ntkmp8ztzg06s3hmntju27zw0ganyjpjms6cchqn8nnv0
1 mojos from 127.0.0.1: height=1321474 time=38.326266000000004 s
--- xch12j86vecwyzks3ntkmp8ztzg06s3hmntju27zw0ganyjpjms6cchqn8nnv0 ping statistics ---
1 transactions transmitted, 0 transactions confirmed, 1 transactions received, 0 packet loss
round-trip min/avg/max/stddev = 0/0/0/0 s
```

## Installation

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -U pip
$ pip3 install -r requirements.txt
```

## Usage

You need two computers with the [Chia Light Wallet Beta](https://www.chia.net/download/) running, each its own address.

First, start the responder on one machine with the address of the other wallet.

```console
machineA $ chia-ping.py -r address_B
```

And then, start pinging.

```console
machineB $ chia-ping.py address_A
```

---
« C'est totalement inutile et donc rigoureusement indispensable ! »

-- [Jérôme Bonaldi](https://fr.wikipedia.org/wiki/J%C3%A9r%C3%B4me_Bonaldi)
