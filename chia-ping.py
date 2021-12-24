#!./.venv/bin/python

import time
import argparse
import logging
import asyncio

from timeit import default_timer as timer
from dataclasses import dataclass

from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.util.bech32m import decode_puzzle_hash
from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.ints import uint16
from chia.wallet.transaction_record import TransactionRecord

parser = argparse.ArgumentParser(description="Ping using chia transactions.")
parser.add_argument("address", type=str, help="Address to send the mojos to")
parser.add_argument(
    "-r", "--responder", action="store_true", help="respond to incoming pings"
)
parser.add_argument(
    "-c",
    "--count",
    type=int,
    default=1,
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


@dataclass
class Stats:
    sent: int = 0
    confirmed: int = 0
    received: int = 0

    loss: float = 0

    min: float = 0
    max: float = 0
    avg: float = 0
    stddev: float = 0


async def send(args, stats):
    wallet_client = await get_wallet_client()

    logging.debug(f"Sending a {args.amount} mojos transaction to {args.address}")

    transaction = await wallet_client.send_transaction_multi(
        args.wallet,
        [
            {
                "puzzle_hash": decode_puzzle_hash(args.address),
                "amount": args.amount,
            }
        ],
        fee=args.fee,
    )
    stats.sent += 1

    logging.debug(f"Waiting for transaction {transaction.name} to become confirmed")

    while not transaction.confirmed:
        time.sleep(1)
        transaction = await wallet_client.get_transaction(args.wallet, transaction.name)
        # logging.debug(transaction)

    stats.confirmed += 1
    logging.debug(f"Transaction {transaction.name} confirmed")

    wallet_client.close()
    await wallet_client.await_closed()

    return transaction


async def receive(args, stats):
    wallet_client = await get_wallet_client()

    initial_transaction_count = await wallet_client.get_transaction_count(args.wallet)

    logging.debug(
        f"Waiting for incoming transaction, count: {initial_transaction_count}"
    )

    while True:
        transaction_count = await wallet_client.get_transaction_count(args.wallet)

        # logging.debug(
        #     f"Waiting for new transaction, initial_count={initial_transaction_count} count={transaction_count}"
        # )

        if transaction_count > initial_transaction_count:
            break

        await asyncio.sleep(1)

    transactions = await wallet_client.get_transactions(args.wallet, 0, 1)
    transaction = transactions[0]
    logging.debug(f"New transaction {transaction.name} received")
    stats.received += 1

    wallet_client.close()
    await wallet_client.await_closed()

    return transaction


async def display(transaction: TransactionRecord, duration, seq):
    logging.debug(f"display({transaction})")
    print(
        f"{transaction.amount} mojos from ?: seq={seq} height={transaction.confirmed_at_height} time={duration:} s"
    )


async def summary(args, stats):
    logging.debug("summary")
    print(
        f"""--- {args.address} ping statistics ---
{stats.sent} transactions transmitted, {stats.confirmed} transactions confirmed, {stats.received} transactions received, {stats.loss} packet loss
round-trip min/avg/max/stddev = {stats.min}/{stats.avg}/{stats.max}/{stats.stddev} s"""
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


async def main():
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )

    if args.responder:
        while True:
            transaction = await receive(args)
            logging.debug(transaction)

            transaction = await send(args)
            logging.debug(transaction)

    else:
        try:
            stats = Stats()

            i = 0
            while i <= args.count:
                transaction = await send(args, stats)
                start = timer()
                transaction = await receive(args, stats)
                duration = timer() - start
                await display(transaction, duration, i)
                i += 1
        except KeyboardInterrupt:
            pass

        await summary(args, stats)


if __name__ == "__main__":
    asyncio.run(main())
