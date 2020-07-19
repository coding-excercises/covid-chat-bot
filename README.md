# COVID Chat Bot
This is an example of hyper local, crowd sourced and data driven chat bot for Covid. Let's call this bot - DISCO (***D***istributed ***I***nformation ***S***entinel for ***CO***vid) chat bot.

For more details on the idea and inspiration behind this bot is at my [**blog**](https://www.rajansview.com/2020/07/a-hyper-local-crowd-sourced-data-driven.html).
<br/>
<br/>

# Technology
## Software
1. Python - as the programming language and runtime.
2. Chatterbot - as the dialog engine for the FAQ. While other dialog engines are available, this has been used  as it can run in a low-spec machine such as a Raspberry Pi.
3. Pandas - to process the data.
4. Matplotlib - to generate the charts.
5. Google Spreadsheets - to capture the data. Formulae are created in spreadsheet so that the calculations are done 'at data source' rather than in the bot.
6. Google Drive API - to download the spreadsheet to a local file cache.
7. Telegram - to create the bot.

## Hardware
1. Raspberry Pi 3 - to run the Telegram bot 'server'. Alternatively, it could be run on a desktop or laptop or server or cloud.
<br/>
<br/>

# Installation Instructions
1. Install python 3.6.4 or above. The installers can be downloaded from the [python website](https://www.python.org/downloads/).
2. Download the code from this Github repository. Run "pip3 install -r requirements.txt" to install all the required packages.
3. Create a google spreadsheet using this [file](https://github.com/rajanm/covid-chat-bot/blob/master/covid-data-sample-google-sheet.csv) as a sample.
4. Follow instructions from [here](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html) to
setup a google service account and give access to the above google spreadsheet. Download the google service account credentials as a JSON file.
5. Configure and run the spreadsheet.sh (for Linux) or spreadsheet.bat (for Windows) file from [here](https://github.com/rajanm/covid-chat-bot/tree/master/scripts).
6. This will download and store a file called **covid.csv** locally.
7. Modify the [chat_trainer](https://github.com/rajanm/covid-chat-bot/blob/master/chat_query_trainer.py) and run this program. This will create a 
**db.sqllite3** database locally that contains all the trained respnses for the Covid FAQ.
8. Follow the steps [here](https://core.telegram.org/bots) to create a bot in Telegram.
9. Finally, configure and run the covidbot.sh (for Linux) or covid.bat (for Windows) from [here](https://github.com/rajanm/covid-chat-bot/tree/master/scripts).
Refer the demo below on how to interact with the bot.

# Bot Demo
This is a demo of the a local DISCO chat bot in Telegram (on iPhone). The bot backend itself is running on a Raspberry Pi 3.
<br/>
<br/>

<p align="center">
  <img width="300" height="600" src="https://github.com/rajanm/covid-chat-bot/blob/master/Mobile-Telegram-Covid-Chat-Bot.gif">
</p>
