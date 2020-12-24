import logging
import os
import progressbar as pgb
import yaml

class Logger:
    def __init__(self, filename=None, colors=True, verbosity=0):
        self.filename = filename
        self.colors = colors
        self.verbosity = verbosity

        if self.filename:
            with open(self.filename, 'w') as f: 
                f.write("")

    def info(self, msg):
        self._log(f"[*] {msg}")

    def success(self, msg):
        _msg = f"[+] {msg}"
        if self.colors:
            _msg = _msg.join(["\033[32m", "\033[0m"])
        self._log(_msg)

    def partial(self, msg):
        if self.verbosity >= 1:
            _msg = f"[-] {msg}"
            if self.colors:
                _msg = _msg.join(["\033[36m", "\033[0m"])
            self._log(_msg)

    def fail(self, msg):
        if self.verbosity >= 2:
            _msg = f"[.] {msg}"
            if self.colors:
                _msg = _msg.join(["\033[34m", "\033[0m"])
            self._log(_msg)

    def debug(self, msg):
        if self.verbosity >= 3:
            _msg = f"[=] {msg}"
            if self.colors:
                _msg = _msg.join(["\033[2;37m", "\033[0m"])
            self._log(_msg)

    def warning(self, msg):
        _msg = f"[Warning] {msg}"
        if self.colors:
            _msg = _msg.join(["\033[33m", "\033[0m"])
        self._log(_msg)

    def error(self, msg):
        _msg = f"[Error] {msg}"
        if self.colors:
            _msg = _msg.join(["\033[31m", "\033[0m"])
        self._log(_msg)

    def _log(self, msg):
        if self.filename:
            with open(self.filename, "a") as f:
                f.write(f"{msg}{os.linesep}")
        print(msg)

pgb.streams.wrap_stderr()

def progressbar(
    max_value=0, 
    title="[=]", 
    counter=True,
    percent=False,
    timer=False, 
    eta=False
    ):
    widgets = []

    if title:
        widgets.append(f"{title} ")

    widgets.append(
        pgb.Bar(marker=f"=", left="[", right="]", fill='-')
    )

    if counter:
        widgets.append(pgb.Counter(format=" %(value)02d/%(max_value)d"))

    if percent:
        widgets.append(pgb.Percentage(format=" %(percentage)3d%%"))

    if timer:
        widgets += [" [", pgb.Timer(), "]"]

    if eta:
        widgets += [" (", pgb.ETA(), ")"]

    return pgb.ProgressBar(
        widgets=widgets, 
        max_value=max_value, 
        redirect_stdout=True,
    )