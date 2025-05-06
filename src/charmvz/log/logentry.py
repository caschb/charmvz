from enum import Flag


class EntryType(Flag):
    INVALID = 0
    CREATION = 1
    BEGIN_PROCESSING = 2
    END_PROCESSING = 3
    ENQUEUE = 4
    DEQUEUE = 5
    BEGIN_COMPUTING = 6
    END_COMPUTING = 7
    BEGIN_INTERRUPT = 8
    END_INTERRUPT = 9
    MESSAGE_RECV = 10
    BEGIN_TRACE = 11
    END_TRACE = 12
    USER_EVENT = 13
    BEGIN_IDLE = 14
    END_IDLE = 15
    BEGIN_PACK = 16
    END_PACK = 17
    BEGIN_UNPACK = 18
    END_UNPACK = 19
    CREATION_BCAST = 20
    CREATION_MULTICAST = 21
    MEMORY_MALLOC = 24  # From trace-common.h in Charm++'s repo
    MEMORY_FREE = 25  # From trace-common.h in Charm++'s repo
    USER_SUPPLIED = 26
    MEMORY_USAGE = 27
    USER_SUPPLIED_NOTE = 28
    USER_SUPPLIED_BRACKETED_NOTE = 29
    END_PHASE = 30  # From trace-common.h in Charm++'s repo
    SURROGATE_BLOCK = 31  # From trace-common.h in Charm++'s repo

    USER_STAT = 32

    BEGIN_USER_EVENT_PAIR = 98
    END_USER_EVENT_PAIR = 99
    USER_EVENT_PAIR = 100


class MessageType(Flag):
    # https://github.com/charmplusplus/charm/blob/33d4d3b783301f39d6ee41542098441a2ee34256/src/ck-core/charm.h#L339
    NEW_CHARE_MSG = 1
    NEW_VCHARE_MSG = 2
    BOC_INIT_MSG = 3
    FOR_CHARE_MSG = 4
    FOR_BOC_MSG = 5
    FOR_VID_MSG = 6
    FILL_VID_MSG = 7
    DELETE_VID_MSG = 8
    RODATA_MSG = 9
    ROMSG_MSG = 10

    LDB_MSG = 12
    QD_BOC_MSG = 14
    QD_BROADCAST_BOC_MSG = 15
    INVALID = -1

    START_EXIT_MSG = 13
    EXIT_MSG = 14
    REQ_STAT_MSG = 15
    STAT_MSG = 16
    STAT_DONE_MSG = 17
    NODE_BOC_INIT_MSG = 18
    FOR_NODE_BOC_MSG = 19
    ARRAY_ELT_INIT_MSG = 20
    FOR_ARRAY_ELT_MSG = 21
    FOR_IDED_OBJ_MSG = 22
    BOC_BCAST_MSG = 23
    ARRAY_BCAST_MSG = 24
    ARRAY_BCAST_FWD_MSG = 25


class LogEntry:
    def __init__(self):
        self.is_valid = True
        self.type = EntryType.INVALID
        self.message_type = MessageType.INVALID
        self.timestamp = -1
        self.sts_entry = -1
        self.event = -1
        self.pe = -1
        self.cast_pes = -1
        self.msglen = -1  # <-> CREATION
        # self.user_event_id = -1 # <-> USER_EVENT_PAIR
        self.send_time = -1
        self.recv_time = -1
        self.thread_id = (-1, -1, -1, -1, -1, -1)
        self.cpu_start_time = -1
        self.cpu_end_time = -1
        self.num_perf_counts = -1
        self.perf_counts = list()
        self.num_pes = -1
        self.dest_pes = list()
        self.user_supplied = -1
        self.memory_usage = -1
        self.note = ""
        self.nested_id = -1  # <-> AMPI
        self.stat = -1.0
        self.user_time = -1.0

    def isBeginType(self) -> bool:
        return (
            self.type == EntryType.BEGIN_IDLE
            or EntryType.BEGIN_PROCESSING
            or EntryType.BEGIN_COMPUTING
            or EntryType.BEGIN_INTERRUPT
            or EntryType.BEGIN_TRACE
            or EntryType.BEGIN_PACK
            or EntryType.BEGIN_UNPACK
            or EntryType.BEGIN_USER_EVENT_PAIR
        )

    def isEndType(self) -> bool:
        return (
            self.type == EntryType.END_IDLE
            or EntryType.END_PROCESSING
            or EntryType.END_COMPUTING
            or EntryType.END_INTERRUPT
            or EntryType.END_TRACE
            or EntryType.END_PACK
            or EntryType.END_UNPACK
            or EntryType.END_USER_EVENT_PAIR
        )

    def __repr__(self) -> str:
        message = f"{self.type.value},{self.type.name},{self.message_type.value},{self.message_type.name},{self.timestamp},{self.sts_entry},{self.event},{self.pe}"
        return message
