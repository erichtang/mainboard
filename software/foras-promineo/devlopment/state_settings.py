"""
safe_mode settings DNE, as all tasks there are de-init'd and it runs a very concise loop
"""

settings_lookup = {
    'adcs_task' : adcs_task,
}

adcs_task = {
    'idle' : adcs_task_idle,
    'startup' : adcs_task_safe,
    'payload' : adcs_task_payload
}

adcs_task_idle = {
    'priority'      : 2,
    'frequency'     : 1,
    'mode'          : 0
}

adcs_task_startup = {
    'priority'      : 2,
    'frequency'     : 1,
    'mode'          : 0
}

adcs_task_payload = {
    'priority'      : 2,
    'frequency'     : 1,
    'mode'          : 0
}