# COVID Chat Bot
This is an example of hyper local, crowd sourced and data driven chat bot for Covid. Let's call this bot - DISCO (***D***istributed ***I***nformation ***S***entinel for ***CO***vid) chat bot.

For more details on the idea and inspiration behind this bot is at my [**blog**](https://www.rajansview.com/2020/07/a-hyper-local-crowd-sourced-data-driven.html).
<br/>
<br/>

# Installation Instructions
1. Install python 3.6.4 or above. The installers can be downloaded from the [python website](https://www.python.org/downloads/).
<br/>

2. Download the code from this Github repository. Run "pip3 install -r requirements.txt" to install all the required packages.

3. Create a google spreadsheet using this [file](https://github.com/rajanm/covid-chat-bot/blob/master/covid-data-sample-google-sheet.csv) as a sample.
<br/>

4. Follow instructions from [here](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html) to
setup a google service account and give access to the above google spreadsheet. Download the google service account credentials as a JSON file.
<br/>

5. Configure and run the spreadsheet.sh (for Linux) or spreadsheet.bat (for Windows) file from [here](https://github.com/rajanm/covid-chat-bot/tree/master/scripts).
<br/>

6. This will download and store a file called **covid.csv** locally.
<br/>

7. Modify the [chat_trainer](https://github.com/rajanm/covid-chat-bot/blob/master/chat_query_trainer.py) and run this program. This will create a 
**db.sqllite3** database locally that contains all the trained respnses for the Covid FAQ.
<br/>

8. Follow the steps [here](https://core.telegram.org/bots) to create a bot in Telegram.
<br/>

9. Finally, configure and run the covidbot.sh (for Linux) or covid.bat (for Windows) from [here](https://github.com/rajanm/covid-chat-bot/tree/master/scripts).
Refer the demo below on how to interact with the bot.
<br/>
<br/>

# Bot Demo
This is a demo of the a local DISCO chat bot in Telegram (on iPhone). The bot backend itself is running on a Raspberry Pi 3.
<br/>
<br/>

<p align="center">
  <img width="300" height="600" src="https://github.com/rajanm/covid-chat-bot/blob/master/Mobile-Telegram-Covid-Chat-Bot.gif">
</p>
