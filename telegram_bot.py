#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram.ext import CommandHandler
from soundcloud import download

TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
HELLO = 'I can download files from soundcloud.com to this chat.'
HELP = '`\soundcloud https://soundcloud.com/<artist>/<track>`\n\n*max 50Mb*'


def start(bot, update):
  update.message.reply_text(HELLO, parse_mode='Markdown')

def help(bot, update):
  update.message.reply_text(HELP, parse_mode='Markdown')

def soundcloud(bot, update):
  sound_url = update.message.text.split()[1]
  sound_data = download(sound_url)
  caption = '*{artist} - {title}*\n\n_{genre}_'.format(**sound_data)
  bot.send_photo(chat_id=update.message.chat.id,
                 photo=sound_data['image_url'],
                 caption=caption,
                 parse_mode='Markdown')
  bot.send_audio(chat_id=update.message.chat.id,
                 audio=open(sound_data['filename'], 'rb'),
                 title=sound_data['filename'].split('.')[0],
                 parse_mode='Markdown')

updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('soundcloud', soundcloud))

updater.start_polling()
