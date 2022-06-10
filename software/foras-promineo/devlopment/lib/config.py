"""
config.py

modifications to pycubed beepsat-advanced-2 code to imlement satellite and task-level config loading
original code by Max Holliday

configs are stpred in msgpak .bak files, 
TODO implement a command that allows changinging config settings on the fly in db_cdh and cdh

modified by C. Hillis

Ideally we would use the /lib/cfg.bak, since it has a lower likelihood of failure...
"""

import msgpack

def load_cfg(cfg, name, log, sd=False):
    try:
        if sd:
            path = "/sd/cfg/{}.bak".format(name)
            with open(path,'rb') as f:
                cfg.update(msgpack.unpack(f))
        else:
            path = "/lib/cfg/{}.bak".format(name)
            with open('/lib/config.bak','rb') as f:
                cfg.update(msgpack.unpack(f))
    except Exception as e:
        log("[ERROR][LOAD CONFIG FOR {} FAIL]".format(name))
    
def save_cfg(cfg, name, log, sd=False):
        # binary pack config and save it
        try:
            if sd:
                path = "/sd/cfg/{}.bak".format(name)
                with open(path,'wb') as f:
                    msgpack.pack(cfg,f)
            else:
                path = "/lib/cfg/{}.bak".format(name)
                with open(path,'wb') as f:
                    msgpack.pack(cfg,f)
        except Exception as e:
            log("[ERROR][LOAD CONFIG FOR {} FAIL]".format(name))
