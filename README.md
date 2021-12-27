# chia-ping

A clone of our old friend `ping` using small transactions over the [Chia](https://www.chia.net/) blockchain instead of ICMP packets to show the round-trip latency of on-chain transactions.

This is a toy program I wrote for getting more familiar with the Chia RPC APIs.

Here's how it looks:

```console
$ ./chia-ping.py xch12j86vecwyzks3ntkmp8ztzg06s3hmntju27zw0ganyjpjms6cchqn8nnv0 -c 3
1 mojos from xch1gp0m20ygdcyd08asp3qd63my5la7eg58j46k3fkumtq0kw2jekjsr7924v: seq=0 height=1330406 time=114.345 s
1 mojos from xch1gp0m20ygdcyd08asp3qd63my5la7eg58j46k3fkumtq0kw2jekjsr7924v: seq=1 height=1330410 time=82.524 s
1 mojos from xch1gp0m20ygdcyd08asp3qd63my5la7eg58j46k3fkumtq0kw2jekjsr7924v: seq=2 height=1330419 time=128.271 s
--- xch12j86vecwyzks3ntkmp8ztzg06s3hmntju27zw0ganyjpjms6cchqn8nnv0 ping statistics ---
3 transactions transmitted, 3 transactions confirmed, 3 transactions received, 0% packet loss
round-trip min/avg/max/stddev = 82.524/108.380/128.271/23.449 s
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
