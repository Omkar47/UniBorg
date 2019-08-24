from telethon import events
import asyncio
import zipfile
from pySmartDL import SmartDL
import time
import os
from uniborg.util import admin_cmd, humanbytes, progress, time_formatter


@borg.on(admin_cmd("compress"))
async def _(event):
    if event.fwd_from:
        return
    if not event.is_reply:
        await event.edit("Reply to a file to compress it.")
        return
    mone = await event.reply("Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
            directory_name = "{}".format(downloaded_file_name.replace("`", ""))
            await event.edit("Download to local finished")
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    zipf = zipfile.ZipFile(directory_name + ".zip", "w", zipfile.ZIP_DEFLATED)
    zipdir(directory_name, zipf)
    zipf.close()
    await borg.send_file(
        event.chat_id,
        directory_name + ".zip",
        caption="Zipped By SnapDragon",
        force_document=True,
        allow_cache=False,
        reply_to=event.message.id,
        progress_callback=progress
    )
    try:
        os.remove(directory_name + ".zip")
        os.remove(directory_name)
    except:
        pass
    await event.edit("DONE!!!")
    await asyncio.sleep(3)
    await event.delete()


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
            os.remove(os.path.join(root, file))


def progress(current, total):
    logger.info("Uploaded: {} of {}\nCompleted {}".format(current, total, (current / total) * 100))
