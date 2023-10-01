# region imports
from AlgorithmImports import *
# endregion

class CasualApricotKitten(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015,12,24)
        self.SetEndDate(2015,12,28)

        # self.SetCash(100000)
        # self.AddEquity("SPY", Resolution.Minute)
        # self.AddEquity("BND", Resolution.Minute)
        # self.AddEquity("AAPL", Resolution.Minute)
        # self.SetStartDate(2020, 1, 28)
        # self.SetEndDate(2020, 6, 1)
        self.SetCash(100000)

        future = self.AddFuture(Futures.Metals.Gold, Resolution.Minute)
        future.SetFilter(0, 90)
        self.option = self.AddFutureOption(future.Symbol, lambda universe: universe.Strikes(-5, +5))

    def OnData(self, slice: Slice):
        if not self.Portfolio.Invested:
            for kvp in slice.OptionChains:
                chain = kvp.Value
                # find the call options expiring today
                contracts = filter(lambda x:
                                x.Expiry.date() == self.Time.date() and
                                x.Strike < chain.Underlying.Price and
                                x.Right == OptionRight.Call, chain)
                
                # sorted the contracts by their strikes, find the second strike under market price 
                sorted_contracts = sorted(contracts, key = lambda x: x.Strike, reverse = True)[:2]

                if sorted_contracts:
                    self.MarketOrder(sorted_contracts[0].Symbol, 1)
                    self.MarketOrder(sorted_contracts[1].Symbol, -1)

            for kvp in slice.FutureChains:
                chain = kvp.Value

                print(chain)

            # self.SetHoldings("SPY", 0.33)
            # self.SetHoldings("BND", 0.33)
