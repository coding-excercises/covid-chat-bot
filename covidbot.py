"""
This covid bot has been inspired by the telegram example conversationbot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:

Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import pandas as pd
import re
import os
import sys
from datetime import datetime
import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
from chatterbot import ChatBot
import logging
from logging.handlers import RotatingFileHandler

# Enable logging with rotating log files of 1 mb size with latest 5 log backups
logging.basicConfig(
        handlers=[RotatingFileHandler('covidbot.log', maxBytes=1048576, backupCount=5)],
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')

logger = logging.getLogger('covidbot')

# Assigns 0, 1, 2 to below constants
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

# Keyboard options for the main menu
reply_keyboard = [['Latest covid update within .5 km', 'Latest covid update within 01 km'],
                  ['Latest covid update within 02 km', 'Latest covid update within 05 km'],
                  ['Latest covid update within 10 km', 'More Information'],
                  ['Covid Query', 'Bye']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard = True)

# Keyboard options for the queries menu
query_keyboard = [['Ask another query', 'Main Menu']]
query_markup = ReplyKeyboardMarkup(query_keyboard, one_time_keyboard=False, resize_keyboard = True)

UNKNOWN_REQUEST = 'Apologies, I did not understand your request. Please choose an option from keyboard'

query_bot = ChatBot(
                'Covid Bot',
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                logic_adapters=[
                    {
                        'import_path': 'chatterbot.logic.BestMatch',
                        'default_response': 'I am sorry, but I did not understand.',
                        'minimum_similarity_threshold': 0.8
                    }
                ],
                read_only=True
            )    

# This value is read from sys args, it is the first arguement
bot_location = ''
# This value is read from sys args, it is the second arguement
bot_telegram_token = ''

# Bot start command handler
def start(update, context):
    if (update.message.chat.first_name == None or len(update.message.chat.first_name) == 0):
        first_name = 'User'
    else:
        first_name = update.message.chat.first_name 
    logger.info("Received a start conversation from " + first_name)

    update.message.reply_text(
        "Hi " + first_name + "! \n\nMy name is " + bot_location  
        + " Covid Bot. I will try to provide local COVID-19 updates for " 
        + bot_location + " area."  
        + "\nPlease choose an option from the keyboard options below.",
        reply_markup=markup)

    return CHOOSING

# Process and respond with analysis based on the distance (in km) input
def get_latest_covid_update(text):
    # Default message in case of unknown input. Also, telegram doesn't allow empty string 
    # to be sent as response back to user.
    covid_update = 'Apologies, no updates available at the moment. Please try again later.'
    covid_text = ''

    try:
        if os.path.isfile('covid.csv'):
            df = pd.read_csv ('covid.csv', encoding='utf-8')
            df['Date'] = pd.to_datetime(df.Date, dayfirst = True, format = '%Y-%m-%d')
            df = df.sort_values(by = 'Date' , ascending=[False])
            df = df.head(n=1)
            df = df.rename_axis(None)
            with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
                logger.info(df.to_string())
            # print(df)

            option_contains_km = re.findall("km$", text)
            distance_text = text[-5:].strip()
            logger.info('distance_text: ' + distance_text)
            # print(distance_text)

            if option_contains_km:
                date = datetime.strptime(df['Date'].to_string(index=False), '%Y-%m-%d')
                str_date = date.strftime('%d-%b-%Y')
                text1 = 'Here is update within ' + distance_text + ' of ' + bot_location + '.'
                text2 = '\n\nOn ' + str_date + ' at ' + df['Time'].to_string(index=False) + ' as per ' + df['Data Source'].to_string(index=False) + ' there are ' + df['No of people COVID positive within ' + distance_text].to_string(index=False) + ' COVID positive people out of a total of ' + df['No of people within ' + distance_text].to_string(index=False) + ' in last 28 days.'
                text3 = '\n\nCompared to previous day, COVID infection growth rate is ' + df['Percentage growth of COVID positive within ' + distance_text].to_string(index=False) + '%.'
                covid_text = text1 + text2 + text3
                logger.info(covid_text)
                if len(covid_text) > 0:
                    covid_update = covid_text
            else:
                logger.info('Unable to find distance range in input.')

    except Exception as e:
        logger.error('Error in get covid update fn ' + e.to_string())

    return covid_update

# Handle main menu queries
def regular_choice(update, context):
    bot = telegram.Bot(token = bot_telegram_token)
    user_chat_id = update.message.chat_id

    text = update.message.text

    first_name = ''
    if (update.message.chat.first_name == None or len(update.message.chat.first_name) == 0):
        first_name = 'User'
    else:
        first_name = update.message.chat.first_name 

    logger.info("Received a choice " + text + " from " + first_name)

    option_contains_km = re.findall("km$", text)
    distance_text = text[-5:].strip()

    option_contains_more_info = re.findall("More Information$", text)
    option_contains_start = re.findall("/start$", text)
    option_contains_query = re.findall("Covid Query$", text)
    option_contains_bye = re.findall("Bye$", text)

    if option_contains_km:
        response_text = get_latest_covid_update(text)
        response_text = 'Hi ' + first_name + '!\n\n' + response_text
        logger.info(response_text)
        update.message.reply_text(response_text, reply_markup=markup)

        # This has been added as sometimes the response takes time to be 
        # processed in a Raspberry Pi
        update.message.reply_text('Please wait, sending trends.', reply_markup=markup)
        if os.path.isfile(distance_text + ' positive.png'):
            bot.send_photo(chat_id = user_chat_id, photo = open (distance_text + ' positive.png','rb'))
        if os.path.isfile(distance_text + ' risk.png'):
            bot.send_photo(chat_id = user_chat_id, photo = open (distance_text + ' risk.png','rb'))        
        return CHOOSING
    elif option_contains_more_info:
        response_text = 'The data from Arogya Setu app is crowdsourced ' \
            + 'and the analysis and trends are shown by this bot for ' \
            + bot_location + ' location only.'
        update.message.reply_text(response_text, reply_markup=markup)
        return CHOOSING
    elif option_contains_start:
        response_text = 'Your chat session is already started. Please ' \
            + 'select an option from the keyboard options.'
        update.message.reply_text(response_text, reply_markup=markup)
        return CHOOSING
    elif option_contains_query:
        response_text = 'You can type your covid queries.'
        update.message.reply_text(response_text, reply_markup=query_markup)
        # custom_choice(update, context)
        return TYPING_CHOICE
    elif option_contains_bye:
        done(update, context)
        return CHOOSING
    else:
        response_text = UNKNOWN_REQUEST
        update.message.reply_text(response_text, reply_markup=markup)
        return CHOOSING

# Handle keyboard queries
def custom_choice(update, context):
    text = update.message.text

    option_contains_main_menu = re.findall("Main Menu$", text)
    option_contains_more_query = re.findall("Ask another query$", text)
    
    if option_contains_main_menu:
        response_text = 'Going back to Main Menu'
        update.message.reply_text(response_text, reply_markup=markup)
        return CHOOSING
    elif option_contains_more_query:
        response_text = 'Please type your query'
        update.message.reply_text(response_text, reply_markup=query_markup)
        return TYPING_CHOICE
    else:
        # This has been added as sometimes the response takes time to be
        # processed in a Raspberry Pi
        update.message.reply_text('Please wait, checking for answers.', reply_markup=query_markup)

        response_text = query_bot.get_response(text).text
        response_confidence = query_bot.get_response(text).confidence
        if response_confidence >= 0.8:
            update.message.reply_text(response_text, reply_markup=query_markup)
        else:
            update.message.reply_text('I am sorry, but I did not understand.', reply_markup=query_markup)
        return TYPING_CHOICE

# Handle goodbyes and end conversation
def done(update, context):
    update.message.reply_text('Hope I was able to help. Take care and stay safe.',
                            reply_markup=markup)

    return ConversationHandler.END


# The main function
def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    # updater = Updater("TOKEN", use_context=True)
    updater = Updater(bot_telegram_token, use_context=True)
    logger.info('Starting covid telegram bot')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],

        states = {
            CHOOSING: [MessageHandler(Filters.regex('[km]'),
                                      regular_choice),
                       MessageHandler(Filters.regex('[More Information]'),
                                      regular_choice),
                       MessageHandler(Filters.regex('[Bye]'),
                                      regular_choice),
                       MessageHandler(Filters.regex('[Covid Query]'),
                                      regular_choice)],    
                                      
            TYPING_CHOICE: [MessageHandler(Filters.regex('[Ask another query]'),
                                           custom_choice),
                            MessageHandler(Filters.regex('^$'),
                                           custom_choice)                                           
                            ]

        },

        fallbacks = [MessageHandler(Filters.regex('[stop]'), done)]
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    logger.info('Started covid telegram bot')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

# Program main entry point
if __name__ == '__main__':
    try:
        bot_location = sys.argv[1]
    except IndexError:
        print('Please enter a physical/geographical location for the bot.') 
        exit(1)  

    try:
        bot_telegram_token = sys.argv[2]
    except IndexError:
        print('Please enter a valid telegram token for the bot.')   
        exit(1)

    main()
