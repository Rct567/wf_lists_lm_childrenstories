"""
This type stub file was generated by pyright.
"""

log_console = ...
default_logger = ...
def setLogLevel(log_level): # -> None:
    ...

check_paddle_install = ...
get_module_res = ...
def enable_paddle(): # -> None:
    ...

PY2 = ...
default_encoding = ...
if PY2:
    text_type = ...
    string_types = ...
    iterkeys = ...
    itervalues = ...
    iteritems = ...
else:
    text_type = ...
    string_types = ...
    xrange = range
    iterkeys = ...
    itervalues = ...
    iteritems = ...
def strdecode(sentence):
    ...

def resolve_filename(f): # -> str:
    ...

