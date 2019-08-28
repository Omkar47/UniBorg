from telethon import events
import asyncio
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="dump ?(.*)"))
async def _(message):
    from stdplugins.trashguy import TrashGuy
    obj = message.pattern_match.group(1)
    if not obj:
        obj = "💻 💻 💻"
