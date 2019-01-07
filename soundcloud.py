#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from codecs import getdecoder
from re import findall
from requests import get
from urllib.request import urlretrieve

fields = [
  'artist',
  'title',
  'genre',
  'image_url',
  'file_url',
  'filename'
]
patterns = [
  '"username":"(.*?)"',
  '"title":"(.*?)"',
  '"genre":"(.*?)"',
  'img src="(.*?)"'
]
sound_url = 'https://api.soundcloud.com/i1/tracks/{0}/streams?client_id={1}'
client_id = 'Oa1hmXnTqqE7F2PKUpRdMZqWoguyDLV0'


def get_element(pattern, page):
	return getdecoder('unicode_escape')(findall(pattern, page)[0])[0]

def download(url):

  page = get(url).text
  sound_id = get_element('sounds:(.*?)"', page)
  response = get(sound_url.format(sound_id, client_id)).json()

  sound_data = list(map(lambda x: get_element(x, page), patterns))
  filename = '{0}_-_{1}.mp3'.format(*sound_data[:2]).replace(' ', '_')
  sound_data.extend([response['http_mp3_128_url'], filename])

  sound_data = dict(zip(fields, sound_data))
  urlretrieve(sound_data['file_url'], sound_data['filename'])

  return sound_data
