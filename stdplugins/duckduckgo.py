from telethon import events
import os
import requests
import json
from uniborg.util import admin_cmd


@borg.on(admin_cmd("ddg (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://duckduckgo.com/?q={}".format(input_str.replace(" ","+"))
    response_api = requests.get(sample_url).text
    if response_api:
        link = response_api.rstrip()
        await event.edit("Let me 🦆 DuckDuckGo that for you:\n🔎[{}]({})".format(input_str, link))
    else:
        await event.edit("something is wrong. please try again later.")
