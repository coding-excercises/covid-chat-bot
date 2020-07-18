from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

'''
This is to train the responses for queries regarding 
covid using the ChatterBot ListTrainer.
'''

# All the trained data is stored in the below default database.
# The same database is used by the covid chatbot program
# in read only mode, so that training is retained and not 
# overwritten based on user chat sessions.
QUERY_RESPONSE_DB = 'db.sqlite3'

if os.path.isfile(QUERY_RESPONSE_DB):
    os.remove(QUERY_RESPONSE_DB)

bot = ChatBot(
    'Covid Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I did not understand.',
            'minimum_similarity_threshold': 0.8
        }
    ]
)

# Start by training our bot with the ChatterBot corpus data
trainer = ListTrainer(bot)

trainer.train([
    'What are symptoms of covid?',
    'Cough, fever, fatigue, breathing difficulties, breathlessness.',
])

trainer.train([
    'What are symptoms of corona?',
    'Cough, fever, fatigue, breathing difficulties, breathlessness.',
])

trainer.train([
    'Symptoms of corona?',
    'Cough, fever, fatigue, breathing difficulties, breathlessness.',
])

trainer.train([
    'Symptoms of covid?',
    'Cough, fever, fatigue, breathing difficulties, breathlessness.',
])

trainer.train([
    'what are covid symptoms?',
    'Cough, fever, fatigue, breathing difficulties, breathlessness.',
])

trainer.train([
    'Helpline number for covid in Karnataka',
    'Call 104 or 1075.',
])

trainer.train([
    'Helpline phone number for covid in Karnataka',
    'Call 104 or 1075.',
])

trainer.train([
    'Karnataka covid helpline',
    'Call 104 or 1075.',
])

trainer.train([
    'Karnataka covid helpline number',
    'Call 104 or 1075.',
])

trainer.train([
    'Helpline number for corona in Karnataka',
    'Call 104 or 1075.',
])

trainer.train([
    'Helpline phone number for corona in Karnataka',
    'Call 104 or 1075.',
])

trainer.train([
    'Karnataka corona helpline',
    'Call 104 or 1075.',
])

trainer.train([
    'Karnataka corona helpline number',
    'Call 104 or 1075.',
])
