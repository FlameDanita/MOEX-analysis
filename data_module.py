import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker

from mpl_finance import candlestick2_ohlc, volume_overlay2, plot_day_summary_oclh

class data_class:
    def __init__(self):
        self.files = []
        for file in os.listdir():
            if file[-4:] == '.csv':
                self.files.append(file)
        print('Доступные файлы:', self.files)

    def read_csv(self, file_num=0):
        self.file_name = self.files[file_num]

        split_datas = self.file_name.split('_')
        self.ticker = split_datas[0]
        self.interval = split_datas[1]
        self.start_data = split_datas[2]
        self.end_data = split_datas[3].split('.')[0]

        self.table = pd.read_csv(self.file_name)

    def get_info(self):
        print("Тикер: ", self.ticker)
        print("Интервал: ", self.interval)
        print("Дата начала:", self.start_data)
        print("Дата конца:", self.end_data)

    def plot_table(self, start=0, end=60):
        fig, ax = plt.subplots(2, sharex=True, figsize=(20, 12))

        candlestick2_ohlc(
            ax[0], self.table['open'][start:end],
            self.table['high'][start:end],
            self.table['low'][start:end],
            self.table['close'][start:end],
            width=0.6, colorup='#77d879', colordown='#db3f3f')
        
        ax[0].set_xticks(range(start, end, 5)) 
        ax[0].set_xticklabels(self.table['begin'][start:end:5]) 
        ax[0].grid()

        # ax[0].xaxis.set_major_locator(ticker.MaxNLocator(5))
        # ax[0].xaxis.set_minor_locator(ticker.MaxNLocator(1))
        # ax[0].yaxis.set_major_locator(ticker.MaxNLocator(1))
        # ax[1].yaxis.set_major_locator(ticker.MaxNLocator(5))
        
        ax[1].plot(self.table['macd'][start:end], color="y", label='macd')
        ax[1].plot(self.table['signal'][start:end], label='signal')
        ax[1].plot(self.table['hist'][start:end], label='hist')
        ax[1].legend()
        ax[1].hlines(0, 0, end - start, color = 'black')
        
        ax[1].set_xticks(range(start, end, 5)) 
        ax[1].set_xticklabels(self.table['begin'][start:end:5]) 
        ax[1].grid()

        fig.autofmt_xdate(rotation=90)
        fig.tight_layout()

        plt.xlim(start, end)
        plt.show()

    def get_macd(self, price, slow, fast, smooth):
        exp1 = price.ewm(span = fast, adjust = False).mean()
        exp2 = price.ewm(span = slow, adjust = False).mean()

        macd = pd.DataFrame(exp1 - exp2).rename(columns = {'close':'macd'})
        signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
        hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
        
        frames =  [self.table, macd, signal, hist]
        self.table = pd.concat(frames, join = 'inner', axis = 1)