# -*- coding: utf-8 -*-


from telethon import TelegramClient,events 
from telethon import __version__ as telever
from pyrogram import __version__ as pyrover
from telethon.tl.types import KeyboardButtonCallback
from ..consts.ExecVarsSample import ExecVars
from ..core.getCommand import get_command
from ..core.getVars import get_val
from ..functions.Leech_Module import check_link,cancel_torrent,pause_all,resume_all,purge_all,get_status,print_files, get_transfer
from ..functions.tele_upload import upload_a_file,upload_handel
from ..functions import Human_Format
from .database_handle import tkupload,tktorrents, tkdb
from .settings import handle_settings,handle_setting_callback
from .user_settings import handle_user_settings, handle_user_setting_callback
from functools import partial
from ..functions.rclone_upload import get_config,rclone_driver
from ..functions.admin_check import is_admin
from .. import upload_db, var_db, tor_db, user_db, uptime
import asyncio as aio
import re,logging,time,os,psutil,shutil
from tgtk import __version__
from .ttk_ytdl import handle_ytdl_command,handle_ytdl_callbacks,handle_ytdl_file_download,handle_ytdl_playlist,handle_ytdl_playlist_down
from ..functions.instadl import _insta_post_downloader
torlog = logging.getLogger(__name__)
from .status.status import Status
from .status.menu import create_status_menu, create_status_user_menu
import signal
from PIL import Image

def add_handlers(bot: TelegramClient):
    #bot.add_event_handler(handle_leech_command,events.NewMessage(func=lambda e : command_process(e,get_command("LEECH")),chats=ExecVars.ALD_USR))
    
    bot.add_event_handler(
        handle_leech_command,
        events.NewMessage(pattern=command_process(get_command("LEECH")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        handle_purge_command,
        events.NewMessage(pattern=command_process(get_command("PURGE")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        handle_pauseall_command,
        events.NewMessage(pattern=command_process(get_command("PAUSEALL")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        handle_resumeall_command,
        events.NewMessage(pattern=command_process(get_command("RESUMEALL")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_status_command,
        events.NewMessage(pattern=command_process(get_command("STATUS")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_u_status_command,
        events.NewMessage(pattern=command_process(get_command("USTATUS")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_settings_command,
        events.NewMessage(pattern=command_process(get_command("SETTINGS")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_exec_message_f,
        events.NewMessage(pattern=command_process(get_command("EXEC")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        upload_document_f,
        events.NewMessage(pattern=command_process(get_command("UPLOAD")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_ytdl_command,
        events.NewMessage(pattern=command_process(get_command("YTDL")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_ytdl_playlist,
        events.NewMessage(pattern=command_process(get_command("PYTDL")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        about_me,
        events.NewMessage(pattern=command_process(get_command("ABOUT")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        get_logs_f,
        events.NewMessage(pattern=command_process(get_command("GETLOGS")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        handle_test_command,
        events.NewMessage(pattern="/test",
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_server_command,
        events.NewMessage(pattern=command_process(get_command("SERVER")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        set_password_zip,
        events.NewMessage(pattern=command_process("/setpass"),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_user_settings_,
        events.NewMessage(pattern=command_process(get_command("USERSETTINGS")))
    )

    bot.add_event_handler(
        _insta_post_downloader,
        events.NewMessage(pattern=command_process(get_command("INSTADL")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        start_handler,
        events.NewMessage(pattern=command_process(get_command("START")))
    )

    bot.add_event_handler(
        clear_thumb_cmd,
        events.NewMessage(pattern=command_process(get_command("CLRTHUMB")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        set_thumb_cmd,
        events.NewMessage(pattern=command_process(get_command("SETTHUMB")),
        chats=get_val("ALD_USR"))
    )


    signal.signal(signal.SIGINT, partial(term_handler,client=bot))
    signal.signal(signal.SIGTERM, partial(term_handler,client=bot))

    #*********** Callback Handlers *********** 
    
    bot.add_event_handler(
        callback_handler_canc,
        events.CallbackQuery(pattern="torcancel")
    )

    bot.add_event_handler(
        handle_settings_cb,
        events.CallbackQuery(pattern="setting")
    )

    bot.add_event_handler(
        handle_upcancel_cb,
        events.CallbackQuery(pattern="upcancel")
    )

    bot.add_event_handler(
        handle_pincode_cb,
        events.CallbackQuery(pattern="getpin")
    )

    bot.add_event_handler(
        handle_ytdl_callbacks,
        events.CallbackQuery(pattern="ytdlsmenu")
    )

    bot.add_event_handler(
        handle_ytdl_callbacks,
        events.CallbackQuery(pattern="ytdlmmenu")
    )
    
    bot.add_event_handler(
        handle_ytdl_file_download,
        events.CallbackQuery(pattern="ytdldfile")
    )
    
    bot.add_event_handler(
        handle_ytdl_playlist_down,
        events.CallbackQuery(pattern="ytdlplaylist")
    )

    bot.add_event_handler(
        handle_user_setting_callback,
        events.CallbackQuery(pattern="usetting")
    )
    bot.add_event_handler(
        handle_server_command,
        events.CallbackQuery(pattern="fullserver")
    )
#*********** Handlers Below ***********

async def handle_leech_command(e):
    if not e.is_reply:
        await e.reply("reply to a link or magnet.")
    else:
        rclone = False
        tsp = time.time()
        buts = [[KeyboardButtonCallback("to telegram",data=f"leechselect tg {tsp}")]]
        if await get_config() is not None:
            buts.append(
                [KeyboardButtonCallback("to drive",data=f"leechselect drive {tsp}")]
            )
        # tsp is used to split the callbacks so that each download has its own callback
        # cuz at any time there are 10-20 callbacks linked for leeching XD
           
        buts.append(
                [KeyboardButtonCallback("upload in a zip.[Toggle]", data=f"leechzip toggle {tsp}")]
        )
        buts.append(
                [KeyboardButtonCallback("extract from archive.[Toggle]", data=f"leechzipex toggleex {tsp}")]
        )
        
        conf_mes = await e.reply(f"<b>first click if you want to zip the contents or extract as an archive (only one will work at a time) then, </b>\n<b>choose where to upload your files: </b>\nthe files will be uploaded to default destination after {get_val('DEFAULT_TIMEOUT')} sec of no action by user.\n\n supported archives to extract are: .zip, 7z, tar, gzip2, iso, wim, rar, tar.gz,tar.bz2",parse_mode="html",buttons=buts)        
        
        # zip check in background
        ziplist = await get_zip_choice(e,tsp)
        zipext = await get_zip_choice(e,tsp,ext=True)
        
        # blocking leech choice 
        choice = await get_leech_choice(e,tsp)
        
        # zip check in backgroud end
        await get_zip_choice(e,tsp,ziplist,start=False)
        await get_zip_choice(e,tsp,zipext,start=False,ext=True)
        is_zip = ziplist[1]
        is_ext = zipext[1]
        
        
        # Set rclone based on choice
        if choice == "drive":
            rclone = True
        else:
            rclone = False
        
        await conf_mes.delete()

        if rclone:
            if get_val("RCLONE_ENABLED"):
                await check_link(e,rclone, is_zip, is_ext)
            else:
                await e.reply("<b>rclone has been disabled by the administrator.</b>",parse_mode="html")
        else:
            if get_val("LEECH_ENABLED"):
                await check_link(e,rclone, is_zip, is_ext)
            else:
                await e.reply("<b>telegram leech has been disabled by the administrator.</b>",parse_mode="html")


async def get_leech_choice(e,timestamp):
    # abstract for getting the confirm in a context

    lis = [False,None]
    cbak = partial(get_leech_choice_callback,o_sender=e.sender_id,lis=lis,ts=timestamp)
    
    gtyh = ""

    e.client.add_event_handler(
        #lambda e: test_callback(e,lis),
        cbak,
        events.CallbackQuery(pattern="leechselect")
    )

    start = time.time()
    defleech = get_val("DEFAULT_TIMEOUT")

    while not lis[0]:
        if (time.time() - start) >= 60: #TIMEOUT_SEC:
            
            if defleech == "leech":
                return "tg"
            elif defleech == "rclone":
                return "drive"
            else:
                # just in case something goes wrong
                return "tg"
            break
        await aio.sleep(1)

    val = lis[1]
    
    e.client.remove_event_handler(cbak)

    return val

async def get_zip_choice(e,timestamp, lis=None,start=True, ext=False):
    # abstract for getting the confirm in a context
    # creating this functions to reduce the clutter
    if lis is None:
        lis = [None, None, None]
    
    if start:
        cbak = partial(get_leech_choice_callback,o_sender=e.sender_id,lis=lis,ts=timestamp)
        lis[2] = cbak
        if ext:
            e.client.add_event_handler(
                cbak,
                events.CallbackQuery(pattern="leechzipex")
            )
        else:
            e.client.add_event_handler(
                cbak,
                events.CallbackQuery(pattern="leechzip")
            )
        return lis
    else:
        e.client.remove_event_handler(lis[2])


async def get_leech_choice_callback(e,o_sender,lis,ts):
    # handle the confirm callback

    if o_sender != e.sender_id:
        return
    data = e.data.decode().split(" ")
    if data [2] != str(ts):
        return
    
    lis[0] = True
    if data[1] == "toggle":
        # encompasses the None situation too
        print("data ",lis)
        if lis[1] is True:
            await e.answer("will not be zipped", alert=True)
            lis[1] = False 
        else:
            await e.answer("will be zipped", alert=True)
            lis[1] = True
    elif data[1] == "toggleex":
        print("exdata ",lis)
        # encompasses the None situation too
        if lis[1] is True:
            await e.answer("it will not be extracted.", alert=True)
            lis[1] = False 
        else:
            await e.answer("if it is a archive, it will be extracted. furthermore, you can add a password if the archive is password protected.", alert=True)
            lis[1] = True
    else:
        lis[1] = data[1]
    

#add admin checks here - done
async def handle_purge_command(e):
    if await is_admin(e.client,e.sender_id,e.chat_id):
        await purge_all(e)
    else:
        await e.delete()

async def handle_pauseall_command(e):
    if await is_admin(e.client,e.sender_id,e.chat_id):
        await pause_all(e)
    else:
        await e.delete()

async def handle_resumeall_command(e):
    if await is_admin(e.client,e.sender_id,e.chat_id):
        await resume_all(e)
    else:
        await e.delete()

async def handle_settings_command(e):
    if await is_admin(e.client,e.sender_id,e.chat_id):
        await handle_settings(e)
    else:
        await e.delete()

async def handle_status_command(e):
    cmds = e.text.split(" ")
    if len(cmds) > 1:
        if cmds[1] == "all":
            await get_status(e,True)
        else:
            await get_status(e)
    else:
        await create_status_menu(e)

async def handle_u_status_command(e):
    await create_status_user_menu(e)
        
        
async def handle_test_command(e):
    pass
    

async def handle_settings_cb(e):
    if await is_admin(e.client,e.sender_id,e.chat_id):
        await handle_setting_callback(e)
    else:
        await e.answer("you do not have the permission to touch this command.",alert=True)

async def handle_upcancel_cb(e):
    db = upload_db

    data = e.data.decode("UTF-8")
    torlog.info("data is {}".format(data))
    data = data.split(" ")

    if str(e.sender_id) == data[3]:
        db.cancel_download(data[1],data[2])
        await e.answer("the upload has been canceled.")
    else:
        await e.answer("you can't cancel other peoples uploads.",alert=True)


async def callback_handler_canc(e):
    # TODO the msg can be deleted
    #mes = await e.get_message()
    #mes = await mes.get_reply_message()
    

    torlog.debug(f"the sender id is {e.sender_id}")
    torlog.debug("list bot is authorized on: {} {}".format(get_val("ALD_USR"),type(get_val("ALD_USR"))))

    data = e.data.decode("utf-8").split(" ")
    torlog.debug("data is {}".format(data))
    is_aria = False
    if data[1] == "aria2":
        is_aria = True
        data.remove("aria2")

    if data[2] == str(e.sender_id):
        hashid = data[1]
        hashid = hashid.strip("'")
        torlog.info(f"Hashid :- {hashid}")

        await cancel_torrent(hashid, is_aria)
        await e.answer("the download has been canceled.",alert=True)
    elif e.sender_id in get_val("ALD_USR"):
        hashid = data[1]
        hashid = hashid.strip("'")
        
        torlog.info(f"Hashid: {hashid}")
        
        await cancel_torrent(hashid, is_aria)
        await e.answer("the download has been canceled by an authorized user.",alert=True)
    else:
        await e.answer("you can only cancel your own downloads.", alert=True)


async def handle_exec_message_f(e):
    if get_val("REST11"):
        return
    message = e
    client = e.client
    if await is_admin(client, message.sender_id, message.chat_id, force_owner=True):
        PROCESS_RUN_TIME = 100
        cmd = message.text.split(" ", maxsplit=1)[1]

        reply_to_id = message.id
        if message.is_reply:
            reply_to_id = message.reply_to_msg_id

        process = await aio.create_subprocess_shell(
            cmd,
            stdout=aio.subprocess.PIPE,
            stderr=aio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        e = stderr.decode()
        if not e:
            e = "No Error"
        o = stdout.decode()
        if not o:
            o = "No Output"
        else:
            _o = o.split("\n")
            o = "`\n".join(_o)
        OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"

        if len(OUTPUT) > 3900:
            with open("exec.text", "w+", encoding="utf8") as out_file:
                out_file.write(str(OUTPUT))
            await client.send_file(
                entity=message.chat_id,
                file="exec.text",
                caption=cmd,
                reply_to=reply_to_id
            )
            os.remove("exec.text")
            await message.delete()
        else:
            await message.reply(OUTPUT)
    else:
        await message.reply("only for owner.")

async def handle_pincode_cb(e):
    data = e.data.decode("UTF-8")
    data = data.split(" ")
    
    if str(e.sender_id) == data[2]:
        db = tor_db
        passw = db.get_password(data[1])
        if isinstance(passw,bool):
            await e.answer("selection is time-sensitive, the download has already started.")
        else:
            await e.answer(f"your pincode is \"{passw}\"",alert=True)

        
    else:
        await e.answer("this torrent is not yours.",alert=True)

async def upload_document_f(message):
    if get_val("REST11"):
        return
    imsegd = await message.reply(
        "processing ..."
    )
    imsegd = await message.client.get_messages(message.chat_id,ids=imsegd.id)
    if await is_admin(message.client, message.sender_id, message.chat_id, force_owner=True):
        if " " in message.text:
            recvd_command, local_file_name = message.text.split(" ", 1)
            recvd_response = await upload_a_file(
                local_file_name,
                imsegd,
                False,
                upload_db
            )
            #torlog.info(recvd_response)
    else:
        await message.reply("only for owner.")
    await imsegd.delete()

async def get_logs_f(e):
    if await is_admin(e.client,e.sender_id,e.chat_id, force_owner=True):
        e.text += " tk_logs.txt"
        await upload_document_f(e)
    else:
        await e.delete()

async def set_password_zip(message):
    #/setpass message_id password
    data = message.raw_text.split(" ")
    passdata = message.client.dl_passwords.get(int(data[1]))
    if passdata is None:
        await message.reply(f"no entry found for this job id {data[1]}")
    else:
        print(message.sender_id)
        print(passdata[0])
        if str(message.sender_id) == passdata[0]:
            message.client.dl_passwords[int(data[1])][1] = data[2]
            await message.reply(f"password updated successfully.")
        else:
            await message.reply(f"cannot update the password since this isn't your download.")

async def start_handler(event):
    msg = "TK - A Telegram Leecher Bot."
    await event.reply(msg, parse_mode="html")

def progress_bar(percentage):
    """Returns a progress bar for download
    """
    #percentage is on the scale of 0-1
    comp = get_val("COMPLETED_STR")
    ncomp = get_val("REMAINING_STR")
    pr = ""

    if isinstance(percentage, str):
        return "NaN"

    try:
        percentage=int(percentage)
    except:
        percentage = 0

    for i in range(1,11):
        if i <= int(percentage/10):
            pr += comp
        else:
            pr += ncomp
    return pr

async def handle_server_command(message):
    print(type(message))
    if isinstance(message, events.CallbackQuery.Event):
        callbk = True
    else:
        callbk = False

    try:
        # Memory
        mem = psutil.virtual_memory()
        memavailable = Human_Format.human_readable_bytes(mem.available)
        memtotal = Human_Format.human_readable_bytes(mem.total)
        mempercent = mem.percent
        memfree = Human_Format.human_readable_bytes(mem.free)
    except:
        memavailable = "N/A"
        memtotal = "N/A"
        mempercent = "N/A"
        memfree = "N/A"

    try:
        # Frequencies
        cpufreq = psutil.cpu_freq()
        freqcurrent = cpufreq.current
        freqmax = cpufreq.max
    except:
        freqcurrent = "N/A"
        freqmax = "N/A"

    try:
        # Cores
        cores = psutil.cpu_count(logical=False)
        lcores = psutil.cpu_count()
    except:
        cores = "N/A"
        lcores = "N/A"

    try:
        cpupercent = psutil.cpu_percent()
    except:
        cpupercent = "N/A"
    
    try:
        # Storage
        usage = shutil.disk_usage("/")
        totaldsk = Human_Format.human_readable_bytes(usage.total)
        useddsk = Human_Format.human_readable_bytes(usage.used)
        freedsk = Human_Format.human_readable_bytes(usage.free)
    except:
        totaldsk = "N/A"
        useddsk = "N/A"
        freedsk = "N/A"


    try:
        transfer = await get_transfer()
        dlb = Human_Format.human_readable_bytes(transfer["dl_info_data"])
        upb = Human_Format.human_readable_bytes(transfer["up_info_data"])
    except:
        dlb = "N/A"
        upb = "N/A"

    diff = time.time() - uptime
    diff = Human_Format.human_readable_timedelta(diff)

    if callbk:
        msg = (
            f"<b>bot uptime</b> {diff}\n\n"
            "<b>cpu stats:</b>\n"
            f"cores: {cores} logical: {lcores}\n"
            f"cpu frequency: {freqcurrent}  mhz max: {freqmax}\n"
            f"cpu utilization: {cpupercent}%\n"
            "\n"
            "<b>storage stats:</b>\n"
            f"total: {totaldsk}\n"
            f"used: {useddsk}\n"
            f"free: {freedsk}\n"
            "\n"
            "<b>memory stats:</b>\n"
            f"available: {memavailable}\n"
            f"total: {memtotal}\n"
            f"usage: {mempercent}%\n"
            f"free: {memfree}\n"
            "\n"
            "<b>transfer info:</b>\n"
            f"download: {dlb}\n"
            f"upload: {upb}\n"
        )
        await message.edit(msg, parse_mode="html", buttons=None)
    else:
        try:
            storage_percent = round((usage.used/usage.total)*100,2)
        except:
            storage_percent = 0

        
        msg = (
            f"<b>bot uptime:</b> {diff}\n\n"
            f"cpu utilization: {progress_bar(cpupercent)} - {cpupercent}%\n\n"
            f"storage used: {progress_bar(storage_percent)} - {storage_percent}%\n"
            f"total: {totaldsk} free: {freedsk}\n\n"
            f"memory used:- {progress_bar(mempercent)} - {mempercent}%\n"
            f"total: {memtotal} free: {memfree}\n\n"
            f"transfer download: {dlb}\n"
            f"transfer upload: {upb}\n"
        )
        await message.reply(msg, parse_mode="html", buttons=[[KeyboardButtonCallback("get detailed stats.","fullserver")]])


async def about_me(message):
    db = var_db
    _, val1 = db.get_variable("RCLONE_CONFIG")
    if val1 is None:
        rclone_cfg = "no rclone config is loaded."
    else:
        rclone_cfg = "rclone config is loaded."

    val1  = get_val("RCLONE_ENABLED")
    if val1 is not None:
        if val1:
            rclone = "rclone enabled by admin."
        else:
            rclone = "rclone disabled by admin."
    else:
        rclone = "N/A"

    val1  = get_val("LEECH_ENABLED")
    if val1 is not None:
        if val1: 
            leen = "leech command enabled by admin."
        else:
            leen = "leech command disabled by admin."
    else:
        leen = "N/A"


    diff = time.time() - uptime
    diff = Human_Format.human_readable_timedelta(diff)

    msg = (
        "<b>name</b>: <code>tgtk</code>\n"
        f"<b>version</b>: <code>{__version__}</code>\n"
        f"<b>telethon Version</b>: {telever}\n"
        f"<b>pyrogram Version</b>: {pyrover}\n"
        "<u>currents configs:</u>\n\n"
        f"<b>bot uptime:</b> {diff}\n"
        "<b>torrent download engine:</b> <code>qBittorrent [4.3.0 fix active]</code> \n"
        "<b>direct link download engine:</b> <code>aria2</code> \n"
        "<b>upload Engine:</b> <code>rclone</code> \n"
        "<b>youtube download engine:</b> <code>youtube-dl</code>\n"
        f"<b>rclone config: </b> <code>{rclone_cfg}</code>\n"
        f"<b>leech: </b> <code>{leen}</code>\n"
        f"<b>rclone: </b> <code>{rclone}</code>\n"
    )

    await message.reply(msg,parse_mode="html")


async def set_thumb_cmd(e):
    thumb_msg = await e.get_reply_message()
    if thumb_msg is None:
        await e.reply("reply to a photo or photo as a document.")
        return
    
    if thumb_msg.document is not None or thumb_msg.photo is not None:
        value = await thumb_msg.download_media()
    else:
        await e.reply("reply to a photo or photo as a document.")
        return

    try:
        im = Image.open(value)
        im.convert("RGB").save(value,"JPEG")
        im = Image.open(value)
        im.thumbnail((320,320), Image.ANTIALIAS)
        im.save(value,"JPEG")
        with open(value,"rb") as fi:
            data = fi.read()
            user_db.set_thumbnail(data, e.sender_id)
        os.remove(value)
    except Exception:
        torlog.exception("Set Thumb")
        await e.reply("an error occurred while setting the thumbnail.")
        return
    
    try:
        os.remove(value)
    except:pass

    user_db.set_var("DISABLE_THUMBNAIL",False, str(e.sender_id))
    await e.reply("thumbnail set. try using /usettings to get more control. can be used in private too.")

async def clear_thumb_cmd(e):
    user_db.set_var("DISABLE_THUMBNAIL",True, str(e.sender_id))
    await e.reply("thumbnail disabled. try using /usettings to get more control. can be used in private too.")

async def handle_user_settings_(message):
    if not message.sender_id in get_val("ALD_USR"):
        if not get_val("USETTINGS_IN_PRIVATE") and message.is_private:
            return

    await handle_user_settings(message)

def term_handler(signum, frame, client):
    torlog.info("TERM RECEIVD")
    async def term_async():
        omess = None
        st = Status().Tasks
        msg = "the bot is restarting, re-add your tasks.\n\n"
        for i in st:
            if not await i.is_active():
                continue

            omess = await i.get_original_message()
            if str(omess.chat_id).startswith("-100"):
                chat_id = str(omess.chat_id)[4:]
                chat_id = int(chat_id)
            else:
                chat_id = omess.chat_id
            
            sender = await i.get_sender_id()
            msg += f"<a href='tg://user?id={sender}'>reboot</a> - <a href='https://t.me/c/{chat_id}/{omess.id}'>task</a>\n"
        
        if omess is not None:
            await omess.respond(msg, parse_mode="html")
        exit(0)

    client.loop.create_task(term_async())
        

def command_process(command):
    return re.compile(command,re.IGNORECASE)