import os
import datetime


class WrongFileExtensionError(Exception):
    """Raised when the filetype is wrong

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class StsReader:
    class _chare:
        def __init__(self, name: str, dimensions: int):
            self.name = name
            self.dimensions = dimensions

        def __str__(self) -> str:
            return f"[{self.name}:{self.dimensions}]"

    def __init__(self):
        self.chares = dict()
        self.entry_names = dict()
        self.entry_chares = dict()
        self.messages = dict()
        self.user_events = dict()
        self.user_stats = dict()

        self.smpmode = False

    def read_sts(self, fullpath: os.PathLike):
        extension = os.path.splitext(fullpath)[-1][1:]
        if extension != "sts":
            raise WrongFileExtensionError(f"Wrong file type: {extension}")
        with open(fullpath, "r") as f:
            for line in f:
                tokens = line.strip().split()
                if "VERSION" == tokens[0]:
                    self.version = tokens[1]
                elif "MACHINE" == tokens[0]:
                    self.machine = tokens[1]
                elif "PROCESSORS" == tokens[0]:
                    self.numpe = tokens[1]
                elif "SMPMODE" == tokens[0]:
                    print(f"ATTENTION: {tokens[0]}")
                elif "TIMESTAMP" == tokens[0]:
                    self.timestamp = datetime.datetime.fromisoformat(tokens[1])
                elif "COMMANDLINE" == tokens[0]:
                    self.commandline = tokens[1]
                elif "CHARMVERSION" == tokens[0]:
                    self.charm_version = tokens[1]
                elif "USERNAME" == tokens[0]:
                    self.username = tokens[1]
                elif "HOSTNAME" == tokens[0]:
                    self.hostname = tokens[1]
                elif "TOTAL_CHARES" == tokens[0]:
                    self.total_chares = int(tokens[1])
                elif "TOTAL_EPS" == tokens[0]:
                    self.total_events = int(tokens[1])
                elif "TOTAL_MSGS" == tokens[0]:
                    self.total_messages = int(tokens[1])
                elif "CHARE" == tokens[0]:
                    chare_id = int(tokens[1])
                    chare_name = tokens[2].strip('"')
                    chare_dims = int(tokens[3])
                    chare = self._chare(chare_name, chare_dims)
                    self.chares[chare_id] = chare
                elif "ENTRY" == tokens[0]:
                    entry_id = int(tokens[2])
                    chare_id = int(tokens[-2])
                    start = line.index('"')
                    end = line.index('"', start + 1)
                    entry_chare_name = line[start + 1 : end]
                    self.entry_names[entry_id] = entry_chare_name
                    self.entry_chares[entry_id] = self.chares[chare_id]
                elif "MESSAGE" == tokens[0]:
                    message_id = int(tokens[1])
                    message_size = int(tokens[2])
                    self.messages[message_id] = message_size
                elif "EVENT" == tokens[0]:
                    key = int(tokens[1])
                    if key not in self.user_events.keys():
                        event_name = "".join(tokens[2:-1])
                        self.user_events[key] = event_name
                elif "TOTAL_EVENTS" == tokens[0]:
                    self.total_events = int(tokens[1])
                elif "STAT" == tokens[0]:
                    key = int(tokens[1])
                    if key not in self.user_stats.keys():
                        stat_name = "".join(tokens[2:-1])
                        self.user_stats[key] = stat_name
                elif "TOTAL_STATS" == tokens[0]:
                    self.total_stats = int(tokens[1])
                elif "TOTAL_PAPI_EVENTS" == tokens[0]:
                    self.has_papi = True
                    self.total_papi_events = int(tokens[1])
                elif "PAPI_EVENT" == tokens[0]:
                    self.has_papi = True
                    key = int(tokens[1])
                    self.papi_events[key] = tokens[2]
                elif "END" == tokens[0]:
                    break
