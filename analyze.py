import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from language_translation import *


class Analyzer():
    def __init__(self, csv_file_path, language='zh-hans'):
        # csv_file_path: file path of the csv file to be analyzed, required
        # language: language of data visualization result, default language is 'zh-hans'

        # read csv file to pandas dataframe
        self.df = pd.read_csv(csv_file_path)
        # verify df is not null
        assert len(self.df) > 0

        # set language for data visualization result
        assert language in ['zh-hans', 'en']
        self.language = language
        if self.language == 'zh-hans':
            # for Chinese characters
            plt.rcParams['font.sans-serif'] = ['SimHei']

        # some pre-processing steps
        self.df['Time'] =  pd.to_datetime(self.df['Time'], format='%Y/%m/%d')
        self.df['year_month'] = self.df['Time'].apply(lambda x: x.strftime('%Y-%m')) 
        self.groups = self.df.groupby('year_month')

        # get earliest and latest date of self.df, format: datetime object
        self.earliest_date = min(self.df['Time'])
        self.latest_date = max(self.df['Time'])


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
        ax.set_ylabel(plot_group_by_month_y_label[self.language], fontsize=15)
        ax.set_xlabel(plot_group_by_month_x_label[self.language], fontsize=15)
        ax.set_title(plot_group_by_month_title[self.language], fontsize=17)
        ax.set_xticks(x, labels)
        ax.legend()
        fig.tight_layout()
        plt.show()


    def plot_cumulative_obituary_number_by_month(self, year_list):
        # year_list: a list of years that is designated, elements are str or int format, max year number is set to 5, required
        # year_list example: ['2019', '2020', '2021', '2022'], which limits year range to 2019 to 2022
        # If you want to change year_list length, you may also need to change width of bars in this function by yourself
        assert isinstance(year_list, list)
        assert len(year_list) > 0 and len(year_list) <=5
        data_list = self.obituary_number_data_group_by_month(year_list)
        labels = month_label[self.language]

        # cumulate data in data_list, save cumulative result to new_data_list
        new_data_list = []
        for list_of_one_year in data_list:
            new_data_list.append(np.cumsum(list_of_one_year))
        
        # plot
        fig, ax = plt.subplots()
        for i in range(0, len(new_data_list)):
            ax.plot(labels, new_data_list[i], label=year_list[i], marker='x')
        ax.set_ylabel(plot_cum_by_month_y_label[self.language], fontsize=15)
        ax.set_xlabel(plot_cum_by_month_x_label[self.language], fontsize=15)
        ax.set_title(plot_cum_by_month_title[self.language], fontsize=17)
        ax.grid()
        ax.legend()
        fig.tight_layout()
        plt.show()


    def obituary_number_data_group_by_date(self, start_date, end_date):
        # To analyze obituary number group by date
        # start_date: set start date, start_date must be before end_date, ex: '2019-01-01'
        # end_date: set end date, end_date must be after start_date, ex: '2022-12-31'
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        
        # check if start_date and end_date is valid
        assert start_date < end_date
        assert start_date >= self.earliest_date
        assert end_date <= self.latest_date

        # group by date
        groups_by_date = self.df.groupby('Time')
        # target_date_list: all dates between start_date and end_date, format ex: '2019-01-01', str
        target_date_list = pd.date_range(start_date, end_date - timedelta(days=1), freq='d').strftime('%Y-%m-%d').tolist()
        
        # calc obituary numbers group by date and save results to data_list for further visualization
        data_list = []
        for date_temp in target_date_list:
            try:
                data_list.append(len(groups_by_date.get_group(date_temp)))
            except KeyError:
                # current date has no data
                data_list.append(0)
        return (target_date_list, data_list)


    def plot_cumulative_obituary_number_by_date(self, start_date, end_date):
        # plot with results from self.obituary_number_data_group_by_date(self, start_date, end_date)
        # start_date: set start date, start_date must be before end_date, ex: '2019-01-01'
        # end_date: set end date, end_date must be after start_date, ex: '2022-12-31'
        target_date_list, data_list = self.obituary_number_data_group_by_date(start_date, end_date)
        # calc cumulative data_list
        data_list = np.cumsum(data_list)
        # convert target_date_list to datetime
        plot_target_date_list = [datetime.strptime(date, '%Y-%m-%d').date() for date in target_date_list]
        
        # plot
        fig, ax = plt.subplots()
        ax.plot(plot_target_date_list, data_list, label=plot_cum_by_date_label[self.language])
        ax.set_ylabel(plot_cum_by_date_y_label[self.language], fontsize=15)
        ax.set_xlabel(plot_cum_by_date_x_label[self.language], fontsize=15)
        ax.set_title(plot_cum_by_date_title[self.language]+', '+start_date+' to '+end_date, fontsize=17)
        ax.grid()
        ax.legend(loc='upper left')
        fig.tight_layout()
        plt.show()


    def plot_age_histogram(self, start_date, end_date, compare_group_date_range=None, show_avg=True):
        # plot histogram of age between start_date and end_date(include start_date and end_date)
        # start_date: set start date, start_date must be before end_date, ex: '2019-01-01'
        # end_date: set end date, end_date must be after start_date, ex: '2022-12-31'
        # compare_group_date_range, set some date ranges as comparison group(as second histogram in the same chart)
        # compare_group_date_range is a list of lists, each list in it represents a date range, these date range does not need to be consecutive
        # compare_group_date_range format example: [[start_1, end_1], [start_2, end_2]]

        # check if start_date and end_date is valid
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        assert start_date < end_date
        assert start_date >= self.earliest_date
        assert end_date <= self.latest_date

        assert show_avg == True or show_avg == False

        # check legality if compare_group_date_range is not None
        if compare_group_date_range != None:
            assert isinstance(compare_group_date_range, list)
            assert len(compare_group_date_range) > 0
            for i in range(0, len(compare_group_date_range)):
                assert isinstance(compare_group_date_range[i], list)
                assert len(compare_group_date_range[i]) == 2
                # convert to datetime object
                compare_group_date_range[i][0] = datetime.strptime(compare_group_date_range[i][0], "%Y-%m-%d")
                compare_group_date_range[i][1] = datetime.strptime(compare_group_date_range[i][1], "%Y-%m-%d")
                assert compare_group_date_range[i][0] < compare_group_date_range[i][1]
                assert compare_group_date_range[i][0] >= self.earliest_date
                assert compare_group_date_range[i][1] <= self.latest_date
        
        if compare_group_date_range != None:
             # get df_compare if compare_group_date_range is given
            df_compare = self.df[self.df.Time.between(compare_group_date_range[0][0], compare_group_date_range[0][1])]
            if len(compare_group_date_range) >= 2:
                for i in range(1, len(compare_group_date_range)):
                    df_temp = self.df[self.df.Time.between(compare_group_date_range[i][0], compare_group_date_range[i][1])]
                    df_compare = pd.concat([df_compare, df_temp], axis=0, ignore_index=True)

        df_target = self.df[self.df.Time.between(start_date, end_date)]
        

        # plot
        # two histograms overlap each other
        #if compare_group_date_range != None:
            #bins = np.linspace(30, 110, 100)
            #plt.hist(df_target['Age'], bins=bins, edgecolor='black', weights=np.zeros_like(df_target['Age']) + 1. / df_target['Age'].size, alpha=0.5, label=plot_age_histogram_target_label[self.language])
            #plt.hist(df_compare['Age'], bins=bins, edgecolor='black', weights=np.zeros_like(df_compare['Age']) + 1. / df_compare['Age'].size, alpha=0.5, label=plot_age_histogram_compare_label[self.language])
        
        # two histograms side-by-side
        if compare_group_date_range != None:
            plt.hist([df_target['Age'], df_compare['Age']], weights=[np.zeros_like(df_target['Age'])+1./df_target['Age'].size, np.zeros_like(df_compare['Age'])+1./df_compare['Age'].size], bins=50, density=True, label=[plot_age_histogram_target_label[self.language], plot_age_histogram_compare_label[self.language]])   
            if show_avg == True:
                df_compare_avg_age = round(df_compare['Age'].mean(), 2)
                plt.axvline(x=df_compare_avg_age, color='green', linestyle='--', label=plot_age_histogram_avg_compare_label[self.language]+': '+str(df_compare_avg_age))
        else:
            plt.hist(df_target['Age'], bins=50, edgecolor='black', weights=np.zeros_like(df_target['Age'])+1./df_target['Age'].size, alpha=0.5, label=plot_age_histogram_target_label[self.language])

        if show_avg == True:
            df_target_avg_age = round(df_target['Age'].mean(), 2)
            plt.axvline(x=df_target_avg_age, color='red', linestyle='--', label=plot_age_histogram_avg_target_label[self.language]+': '+str(df_target_avg_age))
        plt.xlabel(plot_age_histogram_x_label[self.language], fontsize=15)
        plt.ylabel(plot_age_histogram_y_label[self.language], fontsize=15)
        plt.title(plot_age_histogram_title[self.language], fontsize=17)
        plt.legend(loc='upper left')
        plt.tight_layout()
        plt.show()




#analyzer = Analyzer('university_1.csv', language='en')
#analyzer.plot_obituary_number_data_group_by_month(year_list=['2019', '2020', '2021', '2022'])
#analyzer.plot_cumulative_obituary_number_by_month(year_list=['2019', '2020', '2021', '2022'])
#analyzer.plot_cumulative_obituary_number_by_date(start_date='2019-01-01', end_date='2022-12-31')

#compare_group_date_range = [['2019-01-01', '2019-01-31'], ['2019-11-01', '2019-12-31'], ['2020-01-01', '2020-01-31'], ['2020-11-01', '2020-12-31'], ['2021-01-01', '2021-01-31'], ['2021-11-01', '2021-12-31'], ['2022-11-01', '2022-11-30']]
#analyzer.plot_age_histogram(start_date='2022-12-01', end_date='2022-12-31', show_avg=True, compare_group_date_range=compare_group_date_range)