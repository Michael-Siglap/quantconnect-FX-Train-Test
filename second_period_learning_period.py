# region imports
from AlgorithmImports import *
# endregion

class QuantconnectGroupA(QCAlgorithm):

 
    def Initialize(self):
        self.SetStartDate(2019, 1, 1)  # Set Start Date
        #self.SetEndDate(2018,12,31) # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        
        # Dictionaries to store values
        self.curr = ["EURUSD","USDJPY","GBPUSD","AUDUSD","USDCAD"]
        self.rsi = {}
        self.macd = {}
        self.back_1 = {}
        self.back_2 = {}
        self.current = {}
        self.entry_price = {}
        
        for i in self.curr:
            self.AddForex(i, Resolution.Daily, Market.Oanda)
            self.rsi[i] = self.RSI(i, 14)
            self.macd[i] = self.MACD(i, 50, 200, 9, MovingAverageType.Exponential, Resolution.Daily)
            self.back_1[i]= None
            self.back_2[i] = None
            self.current[i] = None
            self.entry_price[i] = None
            

    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. 
           Each new data point will be pumped in here.
           Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''
        for currency in self.curr:
            
            self.back_2[currency] = self.back_1[currency]
            self.back_1[currency] = self.current[currency]
            self.current[currency] = data[currency].Close
            
            if self.rsi[currency].IsReady and self.macd[currency].IsReady:
                self.Debug("RSI/MACD Ready")
            
                if self.back_2[currency] == None or self.back_1[currency] == None or self.current[currency] == None: return
                
                # trading conditions, only when we are not invested in EURUSD
                if self.back_1[currency] > self.back_2[currency] and self.current[currency] > self.back_1[currency] and \
                self.rsi[currency].Current.Value < 80 and  ( self.macd[currency].Current.Value > self.macd[currency].Signal.Current.Value) : 
                    self.Debug("conditions met")
                    if not self.Securities[currency].Invested:
                        self.SetHoldings(currency, .3) # invest 10% of our capital
                        self.entry_price[currency] = self.current[currency]
                        
                
                # exit conditions, only if we are invested in EURUSD
                if self.Securities[currency].Invested:
                    if self.current[currency] <= self.entry_price[currency] - 0.01:
                        self.Liquidate(currency, "stop-loss")
                    elif self.current[currency] >= self.entry_price[currency] + 0.0600:
                        self.Liquidate(currency, "take-profit")
