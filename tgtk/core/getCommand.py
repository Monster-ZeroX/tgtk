# -*- coding: utf-8 -*-


from ..consts.DefaultCommands import Commands
from ..core.getVars import get_val 
import os,logging

torlog = logging.getLogger(__name__)

def get_command(command):
    cmd = None

    #Get the command from the constants supplied
    try:
        cmd = getattr(Commands,command)
        torlog.debug(f"getting the command {command} from file: {cmd}")
    except AttributeError:pass

    #Get the commands form the env [overlap]
    #try:
    envcmd = os.environ.get(command)
    torlog.debug(f"hetting the command {command} from file: {envcmd}")
    cmd =  envcmd if envcmd is not None else cmd

    #Get the commands form the DB [overlap]
    #TODO database

    if cmd is None:
        torlog.debug(f"None Command Error occured for command {command}")
        raise Exception("the command was not found in either the constants, environment or database. command is: {}".format(command))
    
    cmd = cmd.strip("/")
    cmd += get_val("BOT_CMD_POSTFIX")

    torlog.debug(f"final resolver for {command} is {cmd}")
    return f"/{cmd}"