# -*- coding: utf-8 -*-


from ..consts.ExecVarsSample import ExecVars
#from ..core.database_handle import tkdb
from tgtk import SessionVars
import os

def get_val(variable):
    return SessionVars.get_var(variable)

