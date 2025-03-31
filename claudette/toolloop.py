# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_toolloop.ipynb.

# %% auto 0
__all__ = []

# %% ../01_toolloop.ipynb
from .core import *
from fastcore.utils import *
from fastcore.meta import delegates

from anthropic.types import TextBlock, Message, ToolUseBlock

# %% ../01_toolloop.ipynb
#| exports
@patch
@delegates(Chat.__call__)
def toolloop(self:Chat,
             pr, # Prompt to pass to Claude
             max_steps=10, # Maximum number of tool requests to loop through
             trace_func:Optional[callable]=None, # Function to trace tool use steps (e.g `print`)
             cont_func:Optional[callable]=noop, # Function that stops loop if returns False
             first_call_prefill:str="", # Prefill for the first call
             **kwargs):
    "Add prompt `pr` to dialog and get a response from Claude, automatically following up with `tool_use` messages"
    n_msgs = len(self.h)

    # add optional prefill tool steering for the first call
    if first_call_prefill != "":
        first_kwargs = kwargs.copy()
        first_kwargs['prefill'] = first_call_prefill
    else:
        first_kwargs = kwargs

    r = self(pr, **first_kwargs)

    for i in range(max_steps):
        if r.stop_reason!='tool_use': break
        if trace_func: trace_func(self.h[n_msgs:]); n_msgs = len(self.h)
        r = self(**kwargs)
        if not (cont_func or noop)(self.h[-2]): break
    if trace_func: trace_func(self.h[n_msgs:])
    return r
