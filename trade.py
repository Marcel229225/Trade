#!/usr/bin/python

##
## EPITECH PROJECT, 2022
## B-CNA-410-COT-4-1-trade-marcel.yobo
## File description:
## trade
##

import sys
import statistics
import math
import numpy as np

class trade:
    player = ""
    bot = ""
    command = {}
    inputs = ""
    BTC_stack = 0
    ETH_stack = 0
    USDT_stack = 0
    BTC_ETH_array = list()
    USDT_ETH_array = list()
    USDT_BTC_array = list()
    transaction_Fee_Percent = 0
    candles_interval = 0
    candles_total = 0
    candles_given = 0
    candles_format = ""
    time_Bank = 0
    time_Per_Move = 0
    initial_stack = 0
    format = dict()
    last_buy = dict()
    order = ""
    nb_haut = list()
    nb_bas = list()

    def manage_settings(self):
        for i in range(0, 10):
            self.inputs = input()
            arr = self.inputs.split(" ")
            if (arr[0] != "settings" or len(arr) < 3):
                print("Bad setting format: " + self.inputs, file=sys.stderr)
                exit(84)
            self.command[arr[1]] = arr[2] 
        self.time_Bank = int(self.command["timebank"])
        self.time_per_move = int(self.command["time_per_move"])
        self.player = self.command["player_names"]
        self.bot = self.command["your_bot"]
        self.candles_interval = int(self.command["candle_interval"])
        self.candles_total = int(self.command["candles_total"])
        self.candles_given = int(self.command["candles_given"])
        self.initial_stack = int(self.command["initial_stack"])
        self.candles_format = self.command["candle_format"]
        self.transaction_Fee_Percent = float(self.command["transaction_fee_percent"])
        candle = ["pair", "date", "high", "low", "open", "close", "volume"]
        self.candles_format = self.candles_format.split(",")
        nb = 0
        for j in range(len(self.candles_format)):
            for i in range(len(candle)):
                if j == i:
                    self.format[j] = nb
                    nb += 1
                    #candle.remove(i)
        if(nb != 7):
            print ("error nb\n")
            exit(84)

    def parse_next_candle(self, str):
        tmp = str.split(";")
        for i in range(len(tmp)):
            tmp1 = tmp[i].split(',')
            tmpD = dict()
            for x in range (len(tmp1)):
                if (self.candles_format[x] == "pair"):
                    tmpD[self.candles_format[x]] = tmp1[x]
                else:
                    tmpD[self.candles_format[x]] = float(tmp1[x])
            #if (tmp1[0] == "BTC_ETH"):
            #    self.BTC_ETH_array.append(tmpD)
            #if (tmp1[0] == "USDT_ETH"):
            #    self.USDT_ETH_array.append(tmpD)
            if (tmp1[0] == "USDT_BTC"):
                self.USDT_BTC_array.append(tmpD)
        return 0

    def parse_new_stack(self, str):
        tmp = str.split(",")
        for i in range(len(tmp)):
            tmp1 = tmp[i].split(":")
            if(tmp1[0] == "BTC"):
                self.BTC_stack = float(tmp1[1])
            elif(tmp1[0] == "USDT"):
                self.USDT_stack = float(tmp1[1])
        return 0

    def update_candle(self, str):
        if(str[1] == "game" and str[2] == "next_candles"):
            self.parse_next_candle(str[3])
        if(str[1] == "game" and str[2] == "stacks"):
            self.parse_new_stack(str[3])
        return 0

    def calc_deviation_standard(self, li, prd):
        tmpli = li[-prd:]
        myn = statistics.mean(tmpli)
        sum = float(0)
        i = 0
        while (i < len(tmpli)):
            sum += abs(i - myn) **2
        return (math.sqrt(sum/prd))
    
    def calc_mobile_myn(self, li, prd):
        tmpli = li[-prd:]
        total = float(0)
        for val in tmpli:
            total += val
        myn_mobile = total/prd
        return myn_mobile

    def bollinger_band(self, li, prd, devise, stack_money, stack):
        tmpli = li[-prd:]
        std = np.std(tmpli)
        mynmbl = self.calc_mobile_myn(li, prd)
        sup = mynmbl +(2* std)
        inf = mynmbl - (2*std)
        buy = ((inf - tmpli[-1])/10) * stack_money
        sell = ((tmpli[-1] - sup)/10) * stack
        curr_price = tmpli[-1]
        if(stack_money > buy and curr_price < inf and buy > 0.0001):
            print("buy " + devise + " " + str(buy))
        elif(stack > sell and curr_price > sup and sell > 0.5):
            print("sell " + devise + " " + str(sell))
        else :
            #print("pass")
            return 1
        return


    def get_close_value(self):
        liUB = list()
        for i in self.USDT_BTC_array:
            liUB.append(i["close"])
        return liUB

    def update_act(self):
        liUB = self.get_close_value()
        #self.rsi_calculator(20, liUB)
        #self.bollinger_band(liUE, 20,"USDT_ETH", self.USDT_stack /self.USDT_ETH_array[-2]["close"], self.ETH_stack)
        b = self.bollinger_band(liUB, len(liUB), "USDT_BTC", self.USDT_stack /self.USDT_BTC_array[-1]["close"],self.BTC_stack)
        if(b == 1):
            self.rsi_calculator(len(liUB), liUB)
        #self.bollinger_band(liBE, 20,"BTC_ETH",self.BTC_stack /self.BTC_ETH_array[-2]["close"],self.ETH_stack)
        return
    def is_rsi(self, prd, li):
        tmpli = li[-prd:]
        i = 1
        for val in tmpli:
            if(i == len(tmpli)-1):
                break
            if(val > tmpli[i]):
                self.nb_bas.append(val)
            if(val < tmpli[i]):
                self.nb_haut.append(val)
            i +=1
        return

    def rsi_calculator(self, prd, li):
        self.is_rsi(prd, li)
        h = self.calc_mobile_myn(self.nb_haut, prd)
        b = self.calc_mobile_myn(self.nb_bas, prd)
        rsi = 100 - (100 /(1+(h/abs(b))))
        if(rsi > 70 and self.BTC_stack > 0):
            print("sell USDT_BTC "+ str(abs(((li[-1]-li[-2])*self.BTC_stack)*0.1)))
        elif(rsi < 30 or self.USDT_stack > 100 ):
            print("buy USDT_BTC "+ str((self.USDT_stack/li[-1])*0.5))
        else :
            print("pass")
        return

    def do_action(self):
        d = self.USDT_stack
        price = self.USDT_BTC_array[-1]["close"]
        a = d /price
        if d < 100:
            print("no_moves", flush=True)
        else:
            print(f'buy USDT_BTC {0.5 * a}', flush=True)
        return 0

    def mannage_Command(self):
        while(1):
            self.inputs = input()
            parse = self.inputs.split()
            if (parse[0] == "end"):
                break
            elif(parse[0] == "update"):
                self.update_candle(parse)
            elif(parse[0] == "action"):
                self.update_act()
                
    
    def run(self):
        self.manage_settings()
        self.mannage_Command()
    

def main():
    newTrade = trade()
    newTrade.run()


if __name__ == "__main__":
    main()
    sys.exit(0)

