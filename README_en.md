# Chinese University Obituary Data Analyze

## Introduction

Provide standardized data analysis and visualization codes for obituary data published by Chinese universities, which can save you from writing some basic data visualization related codes. Below take the real obituary data published by a real university in North China(_See file [university_1.csv](university_1.csv) for data, sensitive information has been wiped_) as an example to show usage of our code as well as analysis results.

## Data format
The standardized data file must be in .csv format, and the data table is divided into four columns: Name, Time, Age, Place; respectively representing: name, date of death, age at death, place of death.

For details, please refer to the sample data file [university_1.csv](university_1.csv) we provided. This sample data comes from all obituary information publicly released by a university in North China from 2019 to 2022. To show respect to dead and protect privacy, the sample data only shows Date of death(Time) and age at death(Age), while name (Name) and place of death (Place) are wiped.

When applying codes in this repository to your data, you should first collect relevant obituary data by yourself, and ensure that the format of your data is exactly the same as that of the sample data file [university_1.csv](university_1.csv) we provided, otherwise the code will not work properly.

The format of the date of death(Time) is: 2022/12/31, which represents December 31, 2022.

The age at death(Age) format should be a positive integer greater than 0.

## Additional explanation for _place of death_ from 2019 to 2022 in [university_1.csv](university_1.csv) data
Some may have doubts about the place of death(Place) in [university_1.csv](university_1.csv), take this into consideration, although place of death(Place) is wiped, we give the overall ratio of the place of death(Place) as follows:

**There are 351 total records from 2019 to 2022, among which 309 records (88.03%) died in the city where this university is located**, 10 records (2.85%) died in other cities in China (including Hong Kong, Macao and Taiwan regions), 15 records (4.27%) died in countries out of China, and 17 records (4.84%) did not disclose the place of death in the obituary.

**There are 39 total records in December 2022, among which 38 records (97.44%) died in the citywhere this university is located**, 1 record (2.56%) died in other cities in China (including Hong Kong, Macao and Taiwan regions), no records died in countries out of China, there is no record of which place of death is undisclosed.

## Usage
### 1. data initialization
```python
from analyze import Analyzer

analyzer = Analyzer(csv_file_path='university_1.csv', language='en')
```

**csv_file_path**: file path to your csv data file

**language**: Language setting, default is 'zh-hans' which represents simplified Chinese, choose 'en' for English. Language mainly affects the language of text in charts, such as image titles, axis text, labels, etc.

Language translation related content is in [language_translation.py](language_translation.py).

### 2. plot obituary number of a certain Chinese university in different years group by month
```python 
analyzer.plot_obituary_number_data_group_by_month(year_list=['2019', '2020', '2021', '2022'])
```
**year_list**: Specify the years covered by the obituary data file, this must match your data.

According to sample data in file [university_1.csv](university_1.csv), the result graph is shown as follows:
![](group_by_month_en.png?raw=true "obituary number of a certain Chinese university in different years group by month")

### 3. plot obituary number of a certain Chinese university in different years cumulates by month
```python
analyzer.plot_cumulative_obituary_number_by_month(year_list=['2019', '2020', '2021', '2022'])
```
**year_list**: Specify the years covered by the obituary data file, this must match your data.

According to sample data in file [university_1.csv](university_1.csv), the result graph is shown as follows:
![](cum_by_month_en.png?raw=true "obituary number of a certain Chinese university in different years cumulates by month")

### 4. plot cumulative obituary number curve by day
```python
analyzer.plot_cumulative_obituary_number_by_date(start_date='2019-01-01', end_date='2022-12-31')
```
**start_date**: Specify the start date. The date format is '2019-01-01', indicating that the start date is January 1, 2019. The start date must not be earlier than the earliest date of all records in your data file, and must be earlier than the end date end_date, otherwise an AssertionError is thrown.

**end_date**: Specify the end date. The date format is '2022-12-31', indicating that the end date is December 31, 2022. The end date must be no later than the latest date of all records in your data file, and later than the start date start_date, otherwise an AssertionError is thrown.

According to sample data in file [university_1.csv](university_1.csv), the result graph is shown as follows(two different time ranges were selected):

**Time range of the first graph: January 1, 2019 to December 31, 2022**
![](cum_by_day_en_1.png?raw=true "obituary number of a certain Chinese university cumulates by day")

**Time range of the second graph: June 1, 2022 to December 31, 2022**
![](cum_by_day_en_2.png?raw=true "obituary number of a certain Chinese university cumulates by day")


### 5. plot histogram of age at death for a specific time range
```python
compare_group_date_range = [['2019-01-01', '2019-01-31'], ['2019-11-01', '2019-12-31'], ['2020-01-01', '2020-01-31'], ['2020-11-01', '2020-12-31'], ['2021-01-01', '2021-01-31'], ['2021-11-01', '2021-12-31'], ['2022-11-01', '2022-11-30']]
analyzer.plot_age_histogram(start_date='2022-12-01', end_date='2022-12-31', show_avg=True, compare_group_date_range=compare_group_date_range)
```
**start_date**: Specify the start date of time interval that is to be analyzed. The date format is '2019-01-01', indicating that the start date is January 1, 2019. The start date must not be earlier than the earliest date of all records in your data file, and must be earlier than the end date end_date, otherwise an AssertionError is thrown.

**end_date**: Specify the end date of time interval that is to be analyzed. The date format is '2022-12-31', indicating that the end date is December 31, 2022. The end date must be no later than the latest date of all records in your data file, and later than the start date start_date, otherwise an AssertionError is thrown.

**compare_group_date_range**: Specify the time range of the comparison group. The comparison group is optional, not required. If you do not need the comparison group, you can directly delete compare_group_date_range in parameters of the plot_age_histogram function or set the value of compare_group_date_range to None. The default value of compare_group_date_range is None. compare_group_date_range is a list, each element in it is also a list (hereinafter referred to as sub-list), each sub-list specifies a sub-time interval of the comparison group, and multiple sub-time intervals can be specified. These sub-time intervals do not require to be consecutive. An example format of compare_group_date_range is: [[start_1, end_1], [start_2, end_2]]. Note that each sub-interval needs to satisfy the chronological relationship, that is, each time in a sub-list cannot exceed the time range of your data file, and the start time of each sub-interval must be earlier than the end time, otherwise an AssertionError is thrown.

**show_avg**: Display mean of target group and comparison group(if comparison group is specified) in graph if show_avg is True. show_avg can only be True or False, default value is True.

**Explanation of sample code**: In the sample code, the data whose date is between 2022-12-01 to 2022-12-31 is selected as the data to be analyzed, which is called target group. And January, November, and December of the three years of 2019, 2020, and 2021, as well as January and November of 2022 are selected as comparison group. These months of comparison group belong to Winter in North China, which is the same as target group December 2022, thus the comparison group is of comparative significance. The histogram of age at death between target group and comparison group are drawn in the same graph.

According to sample data in file [university_1.csv](university_1.csv), the result graph is shown as follows:
![](age_histogram_with_avg_en.png?raw=true "Histogram of age at death for a specific time range")

**[!] Be wary of the phenomenon that the average age at death does not decrease but increase after China changes its epidemic prevention and control policy in December 2022**

As shown in the figure above, the average age at death in December 2022 is 87.49, nearly 3 years higher than that of the comparison group, which is 84.57. Without 
rigorous analysis, one may draw a wrong conclusion that the COVID-19 pandemic is increasing life expectancy instead of decreasing it, which is quite ridiculous. The reason for this phenomenon is likely to be that in December 2022, the COVID-19 pandemic after the change of China's epidemic prevention and control policy led to a concentrated death of elderly people who normally would not have died in that month. For example, an elderly who would have lived to 96 years old ended up at 86 years old in December 2022. The result of this phenomenon is likely to be that in the next few years in China, the number of very old and super-old people will drop sharply compared with previous years.

## Suggestion and Contribution
We welcome any feedback and suggestion in Issues, such as what analysis and visualization of obituary data you want, and we will try our best to realize it as soon as possible.

## Disclaimer
The entire content of this repository is aimed at learning and exploring Python data analysis and data visualization, which is for learning and educational purpose only. Does not contain any confidential and sensitive information. All codes are open source codes related to data analysis and data visualization, do not contain any malicious programs and malicious codes. Does not provide any data collection related codes and tools. We are not responsible for any consequences of using this project.
