import gzip
import pathlib
import sys
from typing import List

from charmvz.log.logentry import LogEntry, EntryType, MessageType
from charmvz.sts.stsreader import StsReader


class LogReader:
    def __init__(self, logfiles: List[pathlib.Path], sts_reader: StsReader):
        self.logfiles = logfiles
        self.sts_reader = sts_reader
        self.entries = list()

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
            entry.pe = int(line_components[5])
            entry.msglen = line_components[6]
            entry.send_time = line_components[7]
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
            entry.pe = int(line_components[5])
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
            entry.pe = int(line_components[5])
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
            entry.pe = int(line_components[5])
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
            entry.pe = int(line_components[5])
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
            entry.pe = int(line_components[4])
            entry.msglen = int(line_components[5])
        elif entry.type == EntryType.ENQUEUE or entry.type == EntryType.DEQUEUE:
            try:
                entry.message_type = MessageType(int(line_components[1]))
            except ValueError:
                entry.message_type == EntryType.INVALID
            entry.timestamp = int(line_components[2])
            entry.event = int(line_components[3])
            entry.pe = int(line_components[4])
        elif (
            entry.type == EntryType.BEGIN_INTERRUPT
            or entry.type == EntryType.END_INTERRUPT
        ):
            entry.timestamp = int(line_components[1])
            entry.event = int(line_components[2])
            entry.pe = int(line_components[3])
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
            entry.pe = float(line_components[4])
            entry.user_event_id = float(line_components[5])
        return entry

    def read_logs(self, progress=False):
        for logfile in self.logfiles:
            self._read_log(logfile, progress)

    def clear(self):
        self.entries.clear()

    def _read_log(self, logfile, progress=False):
        open_func = None
        if logfile.suffix == ".gz":
            open_func = gzip.open
        else:
            open_func = open

        with open_func(logfile, "rt") as f:
            f.readline()
            phases = 0
            for idx, line in enumerate(f):
                if progress and idx % 100 == 0:
                    print(f"Reading entry {idx}")
                entry = self.get_entry_from_line(line)
                # https://github.com/charmplusplus/charm/blob/main/src/ck-perf/trace-projections.C#L584
                if (
                    entry.type == EntryType.END_PHASE
                    or entry.type == EntryType.END_COMPUTING
                ):
                    phases += 1
                    entry.num_phases = phases
                self.entries.append(entry)

    def print_entries(self, filename: str = None):
        print()
        if filename:
            file = open(filename, "w")
        else:
            file = sys.stdout
        file.write(
            "entry type,entry type name,message type,message type name,message time,sts entry,sts entry name,event,pe\n"
        )
        for entry in self.entries:
            file.write(f"{entry}\n")
        if filename:
            file.close()
