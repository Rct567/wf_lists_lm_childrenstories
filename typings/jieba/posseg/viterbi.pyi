"""
This type stub file was generated by pyright.
"""

import sys

MIN_FLOAT = ...
MIN_INF = ...
if sys.version_info[0] > 2:
    xrange = range
def get_top_states(t_state_v, K=...): # -> list[Any]:
    ...

def viterbi(obs, states, start_p, trans_p, emit_p): # -> tuple[Any, list[None]]:
    ...

