import sys
import psutil 
import cpuinfo
from datetime import datetime, timedelta
from telethon import events, functions, __version__
from uniborg.util import admin_cmd
from telethon.utils import get_input_location


@borg.on(admin_cmd(pattern="help ?(.*)", allow_sudo=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    splugin_name = event.pattern_match.group(1)
    if splugin_name in borg._plugins:
        s_help_string = borg._plugins[splugin_name].__doc__
    else:
        s_help_string = ""
    help_string = """@UniBorg
Python {}
Telethon {}

|─────────▄▄───▐█
|───▄██▄──█▀───█─▄
|    ─██▄▄──▐█▀▄─▐█▀
|──▄▀▌─▌─█─▌──▌─▌
|─▀▄─▐▄─▐▄▐▄─▐▄─▐▄

Evolution Of Userbots

UserBot Forked from https://github.com/udf/uniborg""".format(
        sys.version,
        __version__
    )
    tgbotusername = Config.TG_BOT_USER_NAME_BF_HER  # pylint:disable=E0602
    if tgbotusername is not None:
        results = await borg.inline_query(  # pylint:disable=E0602
            tgbotusername,
            help_string + "\n\n" + s_help_string
        )
        await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
        await event.delete()
    else:
        await event.reply(help_string + "\n\n" + s_help_string)
        await event.delete()


@borg.on(admin_cmd(pattern="dc"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetNearestDcRequest())  # pylint:disable=E0602
    await event.edit(result.stringify())


@borg.on(admin_cmd(pattern="config"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetConfigRequest())  # pylint:disable=E0602
    result = result.stringify()
    logger.info(result)  # pylint:disable=E0602
    await event.edit("""A Telethon UserBot powered by @UniBorg""")
    
    
    
@borg.on(admin_cmd(pattern="start")) 

async def _(event):

    if event.fwd_from:

        return 

    start = datetime.now()

    await event.edit("```Collecting info....!```")

    end = datetime.now()

    ms = (end - start).microseconds / 1000

    with open('/proc/uptime', 'r') as f: 

        uptime_seconds = float(f.readline().split()[0]) 

        uptime_string = str(timedelta(seconds = uptime_seconds))

        cpu = cpuinfo.get_cpu_info()['brand'] #psutil.cpu_freq(percpu=False)

        d = psutil.disk_usage('/')

    start_string = """

 ```Status :``` **ONLINE**
**Ping** :  ```{}```ms
 ```Dc : 4 NL``` 
 ```Python : {}
Telethon : {}``` 
 ```Plugins :``` {}
 ```Uptime :``` {} 
 ```Cpuinfo :``` {}
 ```Disk_usage :``` {}/100
[“When You Walk Up To Opportunity’s Door: Don’t Knock It. Kick That Bitch In, Smile and Introduce Yourself”](https://telegra.ph//file/b650b3127a801a470662a.mp4)""".format(ms,

        sys.version,

        __version__,len(borg._plugins),uptime_string,cpu,d.percent)

    await event.edit(start_string,link_preview=True)


@borg.on(admin_cmd(pattern="syntax (.*)"))
async def _(event):
    if event.fwd_from:
        return
    plugin_name = event.pattern_match.group(1)
    if plugin_name in borg._plugins:
        help_string = borg._plugins[plugin_name].__doc__
        unload_string = f"Use `.unload {plugin_name}` to remove this plugin.\n           © @UniBorg"
        if help_string:
            plugin_syntax = f"Syntax for plugin **{plugin_name}**:\n\n{help_string}\n{unload_string}"
        else:
            plugin_syntax = f"No DOCSTRING has been setup for {plugin_name} plugin."
    else:
        plugin_syntax = "Enter valid **Plugin** name.\nDo `.exec ls stdplugins` or `.helpme` to get list of valid plugin names."
    await event.edit(plugin_syntax)
