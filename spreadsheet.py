import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import sys
import matplotlib 
import matplotlib.dates as mdates
import logging
from logging.handlers import RotatingFileHandler

# Enable logging with rotating log files of 1 mb size with latest 5 log backups
logging.basicConfig(
        handlers=[RotatingFileHandler('spreadsheet.log', maxBytes=1048576, backupCount=5)],
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')

logger = logging.getLogger('spreadsheet download')

# This value is read from sys args, it is the first arguement.
# The keyfile can be generated from Google Cloud developers console
# when creating a service account.
keyfile = ''
NO_OF_HISTORICAL_DAYS = 7

# Download the google spreadsheet to a local csv file
def download_gsheet_data(keyfile):
        scope = ['https://www.googleapis.com/auth/drive']
        # use creds to create a client to interact with the Google Drive API
        creds = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        sheet = client.open("covid-data").sheet1

        # The belwo column names should be present in the google spreadsheet in as well
        df = pd.DataFrame(sheet.get_all_records(), 
                columns = [
                        'Date',
                        'Time',
                        'Data Source',
                        'Data Source Type',
                        'No of people within .5 km', 
                        'No of people self assessed within .5 km',
                        'No of people assesed as unwell within .5 km',
                        'No of people COVID positive within .5 km',
                        'No of people identified as at risk within .5 km', 
                        'Percentage of COVID positive within .5 km',
                        'Percentage growth of COVID positive within .5 km', 
                        'Percentage of people at risk within .5 km', 
                        'No of people within 01 km',
                        'No of people self assessed within 01 km',
                        'No of people assesed as unwell within 01 km',
                        'No of people COVID positive within 01 km',
                        'No of people identified as at risk within 01 km',
                        'Percentage of COVID positive within 01 km',
                        'Percentage growth of COVID positive within 01 km',
                        'Percentage of people at risk within 01 km',
                        'No of people within 02 km', 
                        'No of people self assessed within 02 km',
                        'No of people assesed as unwell within 02 km',
                        'No of people COVID positive within 02 km',
                        'No of people identified as at risk within 02 km',
                        'Percentage of COVID positive within 02 km',
                        'Percentage growth of COVID positive within 02 km',
                        'Percentage of people at risk within 02 km',
                        'No of people within 05 km',
                        'No of people self assessed within 05 km',
                        'No of people assesed as unwell within 05 km',
                        'No of people COVID positive within 05 km',
                        'No of people identified as at risk within 05 km',
                        'Percentage of COVID positive within 05 km',
                        'Percentage growth of COVID positive within 05 km',
                        'Percentage of people at risk within 05 km',
                        'No of people within 10 km',
                        'No of people self assessed within 10 km',
                        'No of people assesed as unwell within 10 km',
                        'No of people COVID positive within 10 km',
                        'No of people identified as at risk within 10 km',
                        'Percentage of COVID positive within 10 km',
                        'Percentage growth of COVID positive within 10 km',
                        'Percentage of people at risk within 10 km'
                ])

        # print(dataframe)
        # No of rows in the google spreadsheet in google drive
        # print(sheet.row_count)

        # Convert to datetime
        df['Date'] = pd.to_datetime(df.Date, format = '%d-%m-%Y')

        # Data from google spreadsheet is srted by date descending
        df = df.sort_values(by = 'Date' , ascending=[False])

        # Latest data as per NO_OF_HISTORICAL_DAYS will be saved to local file so that it
        # lookup by chatbot is faster.
        df = df.head(n=NO_OF_HISTORICAL_DAYS)

        # No of rows in the dataframe (this will not have the empty rows from google spreadsheet)
        logger.info('Refreshing local file: ' 
                + str(len(df.index)) 
                + ' rows being written to the local file.')

        # Write all columns to a local file
        df.to_csv('covid.csv', encoding='utf-8')

        logger.info('Refreshed local file: ' 
                + str(len(df.index)) 
                + ' written to the local file.')

# Generate the graph for the covid positive cases
def refresh_positive_plot(df, distance_text):
        # Create a chart - x-axis: Date, y:axis: covid positive count
        chart = df.plot(x='Date', y=['No of people COVID positive within ' + distance_text], 
                        kind='line', legend=True, colormap="winter", 
                        title='COVID update within ' + distance_text 
                        + ' for last ' + str(NO_OF_HISTORICAL_DAYS) + ' days', 
                        style='.-')
        chart_pic = chart.get_figure()

        # Save the chart as a photo for the chatbot to retrieve and send to users
        # This makes the query process light weight in chat bot
        chart_pic.savefig(distance_text + ' positive.png')

        logger.info('Refreshing local plot for No of people COVID positive within ' + distance_text)

# Generate the graph for the covid at-risk cases
def refresh_risk_plot(df, distance_text):
        # Create a chart - x-axis: Date, y:axis: covid positive count
        chart = df.plot(x='Date', y=['No of people identified as at risk within ' + distance_text], 
                        kind='line', legend=True, colormap="summer", 
                        title='COVID update within ' + distance_text 
                        + ' for last ' + str(NO_OF_HISTORICAL_DAYS) + ' days', 
                        style='.-')
        chart_pic = chart.get_figure()

        # Save the chart as a photo for the chatbot to retrieve and send to users
        # This makes the query process light weight in chat bot
        chart_pic.savefig(distance_text + ' risk.png')

        logger.info('Refreshing local plot for No of people identified as at risk within ' + distance_text)

# The main function
def main():
        # Download the google spreadsheet
        download_gsheet_data(keyfile)

        # read from local csv file in ascending order of dates
        df = pd.read_csv ('covid.csv', encoding='utf-8')
        df['Date'] = pd.to_datetime(df.Date, format = '%Y-%m-%d')
        df = df.sort_values(by = 'Date', ascending=[True])

        # generate covid positive charts for the bot to use in replies 
        # for each distance range query
        refresh_positive_plot(df, '.5 km')
        refresh_positive_plot(df, '01 km')
        refresh_positive_plot(df, '02 km')
        refresh_positive_plot(df, '05 km')
        refresh_positive_plot(df, '10 km')

        # generate covid 'at risk' charts for the bot to use in replies 
        # for each distance range query
        refresh_risk_plot(df, '.5 km')
        refresh_risk_plot(df, '01 km')
        refresh_risk_plot(df, '02 km')
        refresh_risk_plot(df, '05 km')
        refresh_risk_plot(df, '10 km')

# Program main entry point
if __name__ == '__main__':
    try:
        keyfile = sys.argv[1]
    except IndexError:
        print('Please enter keyfile of the google service account.') 
        exit(1)  

    main()