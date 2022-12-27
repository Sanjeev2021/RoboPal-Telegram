import os
import telebot
import openai
from dotenv import load_dotenv

load_dotenv()

print("Starting bot")

API_KEY = os.getenv("ROBOPAL_TOKEN")
bot = telebot.TeleBot(API_KEY)

def get_api(message):
    openai.api_key = os.getenv("OPENAIAPI")
    prompt1 = message
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt1,
        temperature=0.9,
        max_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"],
    )
    return response.choices[0].text.strip()

@bot.message_handler(commands=['start'])
def greet(message):
    bot.send_message(message.chat.id, '''
    Welcome, we are happy to see that you are intrested in using your chatbot.
    Here are some list of commands :
    /help -> get all the commands and guidance
    /inaccurate -> use this command in case the bot is showing inaccurate results
    /creator -> get the names of the creators

    Start by typing something that you need answers to
    ''')

@bot.message_handler(commands=['help'])
def greet(message):
    bot.send_message(message.chat.id, '''
    Commands:
    /inaccurate -> use this command in case the bot is showing inaccurate results
    /creator -> get the names of the creators

    If the results are inaccurate try providing more information such as
    instead of saying hi say hi bot or hi robopal

    Start by typing something that you need answers to
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
        bot.send_message(message.chat.id, get_api(message=message.text))
    else:
        if '@robopal_bot' in message.text.lower():
            new_message = message.text.lower()
            refined_message = new_message.replace("@robopal_bot", "")
            bot.send_message(message.chat.id, get_api(message=refined_message.strip()))
                

bot.polling(1.0)
bot.idle()