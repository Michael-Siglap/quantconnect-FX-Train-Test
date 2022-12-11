# region imports
from AlgorithmImports import *
# endregion

class MACrossover(QCAlgorithm):

    def Initialize(self):
        
        self.SetStartDate(2010,1, 1)  # Set Start Date
        self.SetEndDate(2017,12, 31)  # Set Start Date
        
        self.SetCash(100000)  # Set Strategy Cash
        #self.SetEndDate(2020,6,30)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage)
        self.long_list =[]
        self.short_list =[]
        
        self.stop =False
        
        self.currencies = ["EURUSD","GBPJPY","EURAUD","USDJPY","EURGBP"]
        self.AddForex("EURUSD", Resolution.Daily)
        self.AddForex("GBPJPY", Resolution.Daily)
        self.AddForex("EURAUD", Resolution.Daily)
        self.AddForex("USDJPY", Resolution.Daily)
        self.AddForex("EURGBP", Resolution.Daily)
     
    def OnData(self, data):

        if self.stop:
            return 
       
        currencies = self.currencies
        
        for currency in currencies:
            #self.Debug("The currency is running")
            currency_data = self.History ([currency], 30 , Resolution.Daily)
            MA21_Pre = currency_data.close[8:30].mean()
            MA5_Pre = currency_data.close [24:30].mean()
            MA21_Current = currency_data.close[9:31].mean()
            MA5_Current = currency_data.close[25:31].mean()
            
            #First Trade
            #entry 
            if currency not in self.long_list and currency not in self.short_list:
                self.Debug ("found currency" +str(currency))
                #Checking Bullish Crossover
                if MA5_Pre < MA21_Pre and MA5_Current > MA21_Current:
                    #self.Debug("checking long condition")
                    self.SetHoldings (currency, 0.2)
                    
                    self.long_list.append(currency)
                
                #Checking Bearish Crossover    
                if MA5_Pre > MA21_Pre and MA5_Current < MA21_Current:
                    #self.Debug("checking short condition")
                    self.SetHoldings (currency, -0.2)
                    self.short_list.append(currency)
            
            #exit and again entry        
            if currency in self.long_list:
                #Checking Bearish Crossover 
                if MA5_Pre > MA21_Pre and MA5_Current < MA21_Current:
                    self.SetHoldings (currency, -0.2)
                    self.long_list.remove(currency)
                    self.short_list.append(currency)
                
            if currency in self.short_list:
                #Checking Bullish Crossover
                if MA5_Pre < MA21_Pre and MA5_Current > MA21_Current:
                    self.SetHoldings (currency, 0.2)
                    self.short_list.remove(currency)
                    self.long_list.append(currency)    
                    
                    
        if self.Portfolio.Cash <85000:
            self.stop = True
            self.Liquidate()
            
            
            
