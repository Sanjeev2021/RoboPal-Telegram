import os
import telebot
import openai
from dotenv import load_dotenv

load_dotenv()

print("Starting bot")

API_KEY = os.getenv("ROBOPAL_TOKEN")
bot = telebot.TeleBot(API_KEY)

def get_api(message, text):
    exit = False
    msg = bot.send_message(message.chat.id, ".")
    try:
        openai.api_key = os.getenv("OPENAIAPI")
        prompt1 = text
    except:
        bot.edit_message_text("Something went wrong", message.chat.id, msg.message_id)
        exit = True
    if not exit:
        bot.edit_message_text("..", message.chat.id, msg.message_id)
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt1,
                temperature=0.5,
                max_tokens=3000,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0,
            )
        except:
            exit = True
            bot.edit_message_text("Something went wrong", message.chat.id, msg.message_id)
    if not exit:
        bot.edit_message_text("...", message.chat.id, msg.message_id)
        bot.edit_message_text(response.choices[0].text.strip(), message.chat.id, msg.message_id) 

@bot.message_handler(commands=['start'])
def greet(message):
    bot.send_message(message.chat.id, '''
Welcome, we are happy to see that you are intrested in using your chatbot.
Here are some list of commands :
/help -> get all the commands and guidance
/inaccurate -> use this command in case the bot is showing inaccurate results
/creator -> get the names of the creators

Start by typing something that you need answers to
If using in a group start the message by mentioning robopal
    ''')

@bot.message_handler(commands=['help'])
def greet(message):
    bot.send_message(message.chat.id, '''
    Commands:
/inaccurate -> use this command in case the bot is showing inaccurate results
/creator -> get the names of the creators

If the results are inaccurate try providing more information such as instead of saying hi say hi bot or hi robopal

Start by typing something that you need answers to
If using in a group start the message by mentioning robopal
    ''')

@bot.message_handler(commands=['inaccurate'])
def greet(message):
    bot.send_message(message.chat.id, '''
We are very sorry for the inconvenience. Please try providing more information to the bot
such as instead of saying hi say hi bot or hi robopal. 
    ''')

@bot.message_handler(commands=['creator'])
def greet(message):
    bot.send_message(message.chat.id, '''
This AI chatbot is created by Sahil Yadav and Sanjeev Yadav.
    ''')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.chat.type == 'private':
        get_api(message=message, text=message.text.strip())
    else:
        if '@robopal_bot' in message.text.lower():
            new_message = message.text.lower()
            refined_message = new_message.replace("@robopal_bot", "")
            get_api(message=message, text=refined_message.strip())
                

bot.polling(1.0)
bot.idle()