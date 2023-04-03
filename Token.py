from AFN import generate_afn
from newpostfix import shunting_yard
import pandas as pd

def set_list(sett):
    if isinstance(sett, set):
        return list(sett)
    else:
        return sett

def list_set(listt):
    if isinstance(listt, list):
        return set(listt)
    else:
        return listt
    
def empty(empty):
    if empty == '':
        return tuple()
    else:
        return empty
    
def Token()