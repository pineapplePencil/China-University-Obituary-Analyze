import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from language_translation import *


class Analyzer():
    def __init__(self, csv_file_path, language='zh-hans'):
        # csv_file_path: file path of the csv file to be analyzed, required
        # language: language of data visualization result, default language is 'zh-hans'

        # read csv file to pandas dataframe
        self.df = pd.read_csv(csv_file_path)

        # set language for data visualization result
        assert language in ['zh-hans', 'en']
        self.language = language
        if self.language == 'zh-hans':
            # for Chinese characters
            plt.rcParams['font.sans-serif'] = ['SimHei']

        # some pre-processing steps
        self.df['Time'] =  pd.to_datetime(self.df['Time'], format='%Y-%m-%d')
        self.df['year_month'] = self.df['Time'].apply(lambda x: x.strftime('%Y-%m')) 
        self.groups = self.df.groupby('year_month')


    def obituary_number_data_group_by_month(self, year_list):
        # To analyze obituary number group by month
        month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

        # calc obituary numbers group by month and save results to data_list for further visualization
        data_list = []
        for i in range(0, len(year_list)):
            year_temp = str(year_list[i])
            temp_list = []
            for j in range(0, len(month_list)):
                try:
                    temp_list.append(len(self.groups.get_group(year_temp+'-'+str(month_list[j]))))
                except KeyError:
                    # current month has no data
                    temp_list.append(0)
            data_list.append(temp_list)
        return data_list


    def plot_obituary_number_data_group_by_month(self, year_list):
        # year_list: a list of years that is designated, elements are str or int format, max year number is set to 5, required
        # year_list example: ['2019', '2020', '2021', '2022'], which limits year range to 2019 to 2022
        # If you want to change year_list length, you may also need to change width of bars in this function by yourself
        # data visualization with data given by obituary_number_data_group_by_month
        # Thanks some codes provided by Matplotlib Gallery "Grouped bar chart with labels", 
        # Link: https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
        assert isinstance(year_list, list)
        assert len(year_list) > 0 and len(year_list) <=5
        data_list = self.obituary_number_data_group_by_month(year_list)
        labels = month_label[self.language]

        # col_number: number of bars of each group
        col_number = len(year_list)
        # x: label locations
        x = np.arange(len(labels))
        # width: width of each bar in one group
        width = 0.65 / col_number  

        # plot grouped bar chart
        fig, ax = plt.subplots()
        rects_list = []
        for i in range(0, col_number):
            rects_temp = ax.bar(x - width*col_number/2 + width/2 + i*width, data_list[i], width, label=year_list[i], edgecolor="black")
            ax.bar_label(rects_temp, padding=3)
        ax.set_ylabel(y_label[self.language], fontsize=15)
        ax.set_xlabel(x_label[self.language], fontsize=15)
        ax.set_title(title[self.language], fontsize=17)
        ax.set_xticks(x, labels)
        ax.legend()
        fig.tight_layout()
        plt.show()



#analyzer = Analyzer('university_1.csv', language='zh-hans')
#analyzer.plot_obituary_number_data_group_by_month(year_list=['2019', '2020', '2021', '2022'])


