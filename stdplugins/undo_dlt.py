from telethon import events
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="undlt")
async def _(event):
    if event.fwd_from:
        return
    a = await borg.get_admin_log(event.chat_id,limit=1, search="", edit=False, delete=True)
    for i in a:
      await event.reply(i.original.action.message)
