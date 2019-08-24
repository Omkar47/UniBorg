from telethon import events
import asyncio
import zipfile
from pySmartDL import SmartDL
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
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, "trying to download")
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        while not downloader.isFinished():
            total_length = downloader.filesize if downloader.filesize else None
            downloaded = downloader.get_dl_size()
            display_message = ""
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            speed = downloader.get_speed()
            elapsed_time = round(diff) * 1000
            progress_str = "[{0}{1}]\nProgress: {2}%".format(
                ''.join(["█" for i in range(math.floor(percentage / 5))]),
                ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2))
            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = f"trying to download\nURL: {url}\nFile Name: {file_name}\n{progress_str}\n{humanbytes(downloaded)} of {humanbytes(total_length)}\nETA: {estimated_total_time}"
                if round(diff % 10.00) == 0 and current_message != display_message:
                    display_message = current_message
            except Exception as e:
                logger.info(str(e))
    directory_name = "{}".format(downloaded_file_name.replace("`", ""))
    ziping = zipfile.ZipFile(directory_name + ".zip", "w", zipfile.ZIP_DEFLATED)
    zipdir(directory_name, ziping)
    ziping.close()
    await borg.send_file(
        event.chat_id,
        directory_name + ".zip",
        caption=file_caption,
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
