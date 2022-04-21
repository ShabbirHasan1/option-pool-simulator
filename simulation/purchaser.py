from scipy.stats import skewnorm, norm


import numpy as np
from data_classes.distribution import PurchaserDistribution
from processors.csv_processor import CSVProcessor

from simulation.option_pool import OptionPool


class Purchaser:
    def __init__(
        self,
        id: int,
        csv_processor: CSVProcessor,
        option_pool: OptionPool,
        distribution: PurchaserDistribution
    ) -> None:
        self.id = id
        self.csv_processor = csv_processor
        self.option_pool = option_pool
        self.distribution = distribution

        # Statistics
        self.profit = 0

    def start_epoch(self, date: str) -> None:
        premium = self.option_pool.purchase_call_option(
            date,
            self.id,
            self.generate_random_strike_range_value()
        )
        if premium != -1:
            self.profit -= premium

    def end_epoch(self, date: str) -> None:
        strike = self.option_pool.exercise_call_option(
            date,
            self.id
        )
        if strike != -1:
            self.profit -= strike
            self.profit += self.csv_processor.get_eth_price(date)

    def generate_random_strike_range_value(self) -> float:
        '''
        Use self.distribution to randomly pick a float in the range [0, 1] where
        0 represents the most in-the-money strike price and 1 represents the
        most out-of-the-money strike price.
        '''

        # uniform distribution
        if self.distribution == PurchaserDistribution.UNIFORM:
            s = np.random.uniform(low=0, high=1)

        # normal distribution centered at the money
        elif self.distribution == PurchaserDistribution.NORMAL:
            s = norm(loc=0.5, scale=0.2).rvs()

        # normal distribution centered in the money
        elif self.distribution == PurchaserDistribution.SKEWIN:
            s = skewnorm(3, loc=0.2, scale=0.2).rvs()

        # normal distribution centered out the money
        elif self.distribution == PurchaserDistribution.SKEWOUT:
            s = skewnorm(-3, loc=0.8, scale=0.2).rvs()

        # fix out of range values
        if s < 0:
            s = 0
        elif s > 1:
            s = 1

        return s
