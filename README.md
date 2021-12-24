# chia-ping

A clone of our old friend `ping` using small transactions over the [Chia](https://www.chia.net/) blockchain instead of ICMP packets to show the round-trip latency of on-chain transactions.

This is a toy program I wrote for getting more familiar with the Chia RPC APIs.

Here's how it looks:

```console
$ ./chia-ping.py -c 3 xch12j86vecwyzks3ntkmp8ztzg06s3hmntju27zw0ganyjpjms6cchqn8nnv0
1 mojos from ?: seq=0 height=1325814 time=148.966 s
1 mojos from ?: seq=1 height=1325831 time=196.025 s
1 mojos from ?: seq=2 height=1325840 time=99.994 s
--- xch12j86vecwyzks3ntkmp8ztzg06s3hmntju27zw0ganyjpjms6cchqn8nnv0 ping statistics ---
3 transactions transmitted, 3 transactions confirmed, 3 transactions received, 0.0 packet loss
round-trip min/avg/max/stddev = 99.994/148.328/196.025/48.018 s
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

Get some mojos on address_A from the [faucet](https://faucet.chia.net/) and then, start pinging.

```console
machineB $ chia-ping.py address_A
```

---
« C'est totalement inutile et donc rigoureusement indispensable ! »

-- [Jérôme Bonaldi](https://fr.wikipedia.org/wiki/J%C3%A9r%C3%B4me_Bonaldi)
