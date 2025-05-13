import gzip
import pathlib
import sys
from typing import List, Optional

from charmvz.log.logentry import LogEntry, EntryType, MessageType
from charmvz.sts.stsreader import StsReader

class LogReader:
    def __init__(self, logfiles: List[pathlib.Path], sts_reader: StsReader):
        self.logfiles = logfiles
        self.sts_reader = sts_reader

    def get_entry_from_line(self, line: str, pe: int) -> LogEntry:
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
            entry.pCreation = int(line_components[2])
            entry.pe = pe
        elif entry.type == EntryType.END_PHASE:
            entry.timestamp = int(line_components[2])
            # print(line_components)
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
            entry.sts_entry_name = self.sts_reader.get_entry_chare_name_by_id(
                entry.sts_entry
            )
            entry.timestamp = int(line_components[3])
            entry.event = int(line_components[4])
            entry.pCreation = int(line_components[5])
            entry.pe = pe 
            entry.msglen = int(line_components[6])
            entry.send_time = int(line_components[7])
        elif entry.type == EntryType.CREATION_BCAST:
            try:
                entry.message_type = MessageType(int(line_components[1]))
            except ValueError:
                entry.message_type == EntryType.INVALID
            entry.sts_entry = int(line_components[2])
            entry.sts_entry_name = self.sts_reader.get_entry_chare_name_by_id(
                entry.sts_entry
            )
            entry.timestamp = int(line_components[3])
            entry.event = int(line_components[4])
            entry.pCreation = int(line_components[5])
            entry.pe = pe 
            entry.msglen = int(line_components[6])
            entry.send_time = int(line_components[7])
            entry.num_pes = int(line_components[8])
        elif entry.type == EntryType.CREATION_MULTICAST:
            try:
                entry.message_type = MessageType(int(line_components[1]))
            except ValueError:
                entry.message_type == EntryType.INVALID
            entry.sts_entry = int(line_components[2])
            entry.sts_entry_name = self.sts_reader.get_entry_chare_name_by_id(
                entry.sts_entry
            )
            entry.timestamp = int(line_components[3])
            entry.event = int(line_components[4])
            entry.pCreation = int(line_components[5])
            entry.pe = pe 
            entry.msglen = int(line_components[6])
            entry.send_time = int(line_components[7])
            entry.num_pes = int(line_components[8])
            for i in range(entry.num_pes):
                entry.dest_pes.append(line_components[9 + i])
        elif entry.type == EntryType.BEGIN_PROCESSING:
            try:
                entry.message_type = MessageType(int(line_components[1]))
            except ValueError:
                entry.message_type == EntryType.INVALID
            entry.sts_entry = int(line_components[2])
            entry.sts_entry_name = self.sts_reader.get_entry_chare_name_by_id(
                entry.sts_entry
            )
            entry.timestamp = int(line_components[3])
            entry.event = int(line_components[4])
            entry.pCreation = int(line_components[5])
            entry.pe = pe 
            entry.msglen = int(line_components[6])
            entry.recv_time = int(line_components[7])
            dimensions = self.sts_reader.get_entry_chare_dimensions_by_id(
                entry.sts_entry
            )
            for dim in range(dimensions):
                entry.thread_id[dim] = int(line_components[8 + dim])
            entry.cpu_start_time = int(line_components[8 + dimensions])
            if len(line_components) > 15:
                entry.num_perf_counts = int(line_components[8 + dimensions + 1])
                for perf_count in range(entry.num_perf_counts):
                    entry.perf_counts.append(
                        int(line_components[8 + dimensions + 2 + perf_count])
                    )
        elif entry.type == EntryType.END_PROCESSING:
            try:
                entry.message_type = MessageType(int(line_components[1]))
            except ValueError:
                entry.message_type == EntryType.INVALID
            entry.sts_entry = int(line_components[2])
            entry.sts_entry_name = self.sts_reader.get_entry_chare_name_by_id(
                entry.sts_entry
            )
            entry.timestamp = int(line_components[3])
            entry.event = int(line_components[4])
            entry.pCreation = int(line_components[5])
            entry.pe = pe 
            entry.msglen = int(line_components[6])
            entry.cpu_end_time = int(line_components[7])
            if len(line_components) > 8:
                entry.num_perf_counts = int(line_components[8])
                for perf_count in range(entry.num_perf_counts):
                    entry.perf_counts.append(
                        int(line_components[8 + perf_count])
                    )
        elif (
            entry.type == EntryType.BEGIN_TRACE
            or entry.type == EntryType.END_TRACE
        ):
            entry.timestamp = int(line_components[1])
        elif entry.type == EntryType.MESSAGE_RECV:
            try:
                entry.message_type = MessageType(int(line_components[1]))
            except ValueError:
                entry.message_type == EntryType.INVALID
            entry.timestamp = int(line_components[2])
            entry.event = int(line_components[3])
            entry.pCreation = int(line_components[4])
            entry.pe = pe 
            entry.msglen = int(line_components[5])
        elif entry.type == EntryType.ENQUEUE or entry.type == EntryType.DEQUEUE:
            try:
                entry.message_type = MessageType(int(line_components[1]))
            except ValueError:
                entry.message_type == EntryType.INVALID
            entry.timestamp = int(line_components[2])
            entry.event = int(line_components[3])
            entry.pCreation = int(line_components[4])
            entry.pe = pe 
        elif (
            entry.type == EntryType.BEGIN_INTERRUPT
            or entry.type == EntryType.END_INTERRUPT
        ):
            entry.timestamp = int(line_components[1])
            entry.event = int(line_components[2])
            entry.pCreation = int(line_components[3])
            entry.pe = pe 
        elif (
            entry.type == EntryType.BEGIN_COMPUTING
            or entry.type == EntryType.END_COMPUTING
        ):
            entry.timestamp = int(line_components[1])
        elif (
            entry.type == EntryType.USER_EVENT
            or entry.type == EntryType.BEGIN_USER_EVENT_PAIR
            or entry.type == EntryType.END_USER_EVENT_PAIR
        ):
            raise NotImplementedError
        elif entry.type == EntryType.USER_STAT:
            entry.timestamp = int(line_components[1])
            entry.user_time = float(line_components[2])
            entry.stat = float(line_components[3])
            entry.pCreation = int(line_components[4])
            entry.pe = pe 
            entry.user_event_id = int(line_components[5])
        return entry

    def print_entries(
        self,
        print_header: bool = True,
        filename: Optional[str] = None,
    ):
        if filename:
            out_file = open(filename, "w")
        else:
            out_file = sys.stdout

        if print_header:
            out_file.write(
                "entry type,entry type name,message type,message type name,message time,sts entry,sts entry name,event,pe,creation pe\n"
            )

        for logfile in self.logfiles:
            open_func = None
            if logfile.suffix == ".gz":
                open_func = gzip.open
                pe = int(logfile.name.split(".")[-3])
            else:
                open_func = open
                pe = int(logfile.name.split(".")[-2])

            with open_func(logfile, "rt") as f:
                f.readline()
                for line in f:
                    entry = self.get_entry_from_line(line, pe)
                    out_file.write(f"{entry}\n")

        if filename:
            out_file.close()
