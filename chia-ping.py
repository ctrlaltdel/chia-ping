#!/usr/bin/env python

import argparse
import logging
import asyncio
import statistics

from timeit import default_timer as timer
from typing import List

from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.util.bech32m import decode_puzzle_hash
from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.ints import uint16
from chia.wallet.transaction_record import TransactionRecord

from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.types.blockchain_format.coin import Coin
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.ints import uint16
from chia.wallet.transaction_record import TransactionRecord


parser = argparse.ArgumentParser(description="Ping using chia transactions.")
parser.add_argument(
    "-c",
    "--count",
    type=int,
    default=-1,
    help="Stop after sending and receiving count transactions",
)
parser.add_argument(
    "--wallet",
    type=int,
    default=1,
    help="ID of the wallet to user",
)
parser.add_argument("-d", "--debug", action="store_true")

parser.add_argument("--fee", type=float, default=0)
parser.add_argument("--amount", type=float, default=1)


class Stats:
    confirmed: int = 0

    _durations: List[float] = []

    def add_duration(self, duration: float):
        self._durations.append(duration)

    def min(self) -> float:
        if self._durations:
            return min(self._durations)
        else:
            return 0.0

    def max(self) -> float:
        if self._durations:
            return max(self._durations)
        else:
            return 0.0

    def avg(self) -> float:
        if self._durations:
            return statistics.mean(self._durations)
        else:
            return 0.0

    def stddev(self) -> float:
        if len(self._durations) > 1:
            return statistics.stdev(self._durations)
        else:
            return 0.0


async def display(coin: Coin, duration, seq):
    # coin {'amount': 1,
    #  'parent_coin_info': '0x3624c357df3af2dd194d7e2b2ce477c095fefc2f86821beaaa7f4e22cfeaf038',
    # 'puzzle_hash': '0xf4bab1ca7ffc2bad1e2d5e5adab06a7ea99924da938189fb4cad149628dff21e'}

    logging.debug(f"display({coin})")
    print(f"{coin.amount} mojos to {coin.puzzle_hash}: seq={seq} time={duration:.2f} s")


async def summary(address, stats):
    logging.debug("summary")
    print(
        f"""--- {address} ping statistics ---
{stats.confirmed} transactions confirmed
round-trip min/avg/max/stddev = {stats.min():.3f}/{stats.avg():.3f}/{stats.max():.3f}/{stats.stddev():.3f} s"""
    )


async def get_wallet_client():
    config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    wallet_client = await WalletRpcClient.create(
        config["self_hostname"],
        uint16(config["wallet"]["rpc_port"]),
        DEFAULT_ROOT_PATH,
        config,
    )
    return wallet_client


# Send from your default wallet on your machine
# Wallet has to be running, e.g., chia start wallet
async def send_money_async(args, amount, address, fee=0):
    config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    self_hostname = config["self_hostname"]  # localhost
    wallet_rpc_port = config["wallet"]["rpc_port"]  # 9256

    try:
        logging.debug(f"sending {amount} to {address}...")
        # create a wallet client
        wallet_client = await WalletRpcClient.create(
            self_hostname, uint16(wallet_rpc_port), DEFAULT_ROOT_PATH, config
        )
        # send standard transaction
        res = await wallet_client.send_transaction(args.wallet, amount, address, fee)
        tx_id = res.name
        logging.debug(f"waiting until transaction {tx_id} is confirmed...")
        # wait until transaction is confirmed
        tx: TransactionRecord = await wallet_client.get_transaction(args.wallet, tx_id)
        while not tx.confirmed:
            await asyncio.sleep(5)
            tx = await wallet_client.get_transaction(args.wallet, tx_id)

        # get coin infos including coin id of the addition with the same puzzle hash
        logging.debug(f"\ntx {tx_id} is confirmed.")
        puzzle_hash = decode_puzzle_hash(address)
        coin = next((c for c in tx.additions if c.puzzle_hash == puzzle_hash), None)
        logging.debug(coin)
        return coin
    finally:
        wallet_client.close()
        await wallet_client.await_closed()


async def main():
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )

    stats = Stats()

    wallet_client = await get_wallet_client()
    address = await wallet_client.get_next_address(args.wallet, True)

    print(f"PING {address} {args.amount} mojos of chia with {args.fee} fees.")

    try:

        i = 0
        while i <= args.count - 1:
            start = timer()

            coin = await send_money_async(args, args.amount, address, args.fee)

            stats.confirmed += 1

            duration = timer() - start
            stats.add_duration(duration)
            await display(coin, duration, i)
            i += 1
    except KeyboardInterrupt:
        pass
    finally:
        wallet_client.close()
        await wallet_client.await_closed()

    await summary(address, stats)


if __name__ == "__main__":
    asyncio.run(main())
