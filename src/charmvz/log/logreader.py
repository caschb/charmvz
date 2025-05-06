import gzip
import pathlib
from typing import List

from charmvz.log.logentry import LogEntry, EntryType, MessageType


class LogReader:
    def __init__(self, logfiles: List[pathlib.Path]):
        self.logfiles = logfiles

    def _find_correct_logfile(self, pe: int) -> pathlib.Path:
        for logfile in self.logfiles:
            pe_idx = -1
            if logfile.suffix == ".gz":
                pe_idx = -3
            else:
                pe_idx = -2
            log_pe = int(logfile.name.split(".")[pe_idx])

            if log_pe == pe:
                return logfile

        raise FileNotFoundError

    def get_entry_from_line(self, line: str) -> LogEntry:
        line_components = line.split()
        entry = LogEntry()
        entry_id = int(line_components[0])
        try:
            entry.type = EntryType(entry_id)
        except ValueError:
            entry.type = EntryType.INVALID

        if (
            entry.type == EntryType.BEGIN_IDLE
            or entry.type == EntryType.END_IDLE
            or entry.type == EntryType.BEGIN_PACK
            or entry.type == EntryType.END_PACK
            or entry.type == EntryType.BEGIN_UNPACK
            or entry.type == EntryType.END_UNPACK
        ):
            entry.timestamp = int(line_components[1])
            entry.pe = int(line_components[2])
        elif entry.type == EntryType.USER_SUPPLIED:
            raise NotImplementedError
        elif entry.type == EntryType.USER_SUPPLIED_NOTE:
            raise NotImplementedError
        elif entry.type == EntryType.USER_SUPPLIED_BRACKETED_NOTE:
            raise NotImplementedError
        elif entry.type == EntryType.MEMORY_USAGE:
            entry.memory_usage = int(line_components[1])
            entry.timestamp = int(line_components[1])
        elif entry.type == EntryType.CREATION:
            try:
                entry.message_type = MessageType(int(line_components[1]))
            except ValueError:
                entry.message_type == EntryType.INVALID
            entry.sts_entry = int(line_components[2])
            entry.timestamp = int(line_components[3])
            entry.event = int(line_components[4])
            entry.pe = int(line_components[5])
            entry.msglen = line_components[6]
            entry.send_time = line_components[7]
        elif entry.type == EntryType.CREATION_BCAST:
            try:
                entry.message_type = MessageType(int(line_components[1]))
            except ValueError:
                entry.message_type == EntryType.INVALID
            entry.timestamp = int(line_components[3])
            entry.event = int(line_components[4])
            entry.pe = int(line_components[5])
            entry.msglen = int(line_components[6])
            entry.send_time = int(line_components[7])
            entry.num_pes = int(line_components[8])
        elif entry.type == EntryType.CREATION_MULTICAST:
            try:
                entry.message_type = MessageType(int(line_components[1]))
            except ValueError:
                entry.message_type == EntryType.INVALID
            entry.timestamp = int(line_components[3])
            entry.event = int(line_components[4])
            entry.pe = int(line_components[5])
            entry.msglen = int(line_components[6])
            entry.send_time = int(line_components[7])
            entry.num_pes = int(line_components[8])
            for i in range(entry.num_pes):
                entry.dest_pes.append(line_components[9 + i])

        return entry

    def read_log(self, pe: int):
        logfile = self._find_correct_logfile(pe)

        open_func = None
        if logfile.suffix == ".gz":
            open_func = gzip.open
        else:
            open_func = open

        with open_func(logfile, "rt") as f:
            print(
                "entry type,entry type name,message type,message type name,message time,sts entry,event,pe"
            )
            f.readline()
            for line in f:
                self.get_entry_from_line(line)
