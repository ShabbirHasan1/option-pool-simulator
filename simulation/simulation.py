import random
from typing import List

from simulation.liquidity_provider import LiquidityProvider
from simulation.option_pool import OptionPool
from data_classes.transaction import Transaction
from simulation.purchaser import Purchaser

class Simulation:
    def __init__(self, num_liquidity_providers: int, num_purchasers: int, underlying_asset: str, epoch_dates: List[str], size_of_pool: int) -> None:
        self.actors = []
        self.option_pool = OptionPool(underlying_asset)
        self.epoch_dates = epoch_dates
        self.size_of_pool = size_of_pool

        # Create liquidity providers
        for i in range(num_liquidity_providers):
            self.actors.append(LiquidityProvider(self.option_pool))

        # Create purchasers
        for i in range(num_purchasers):
            self.actors.append(Purchaser(i, self.option_pool))

    def run(self) -> List[Transaction]:
        transactions: List[Transaction] = []

        # Run simulation
        for date in self.epoch_dates:
            random.shuffle(self.actors)
            for actor in self.actors:
                transactions.append(actor.start_epoch(date))

            random.shuffle(self.actors)
            for actor in self.actors:
                transactions.append(actor.end_epoch(date))

        return transactions
