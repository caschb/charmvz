from enum import Flag


class EntryType(Flag):
    # https://github.com/charmplusplus/charm/blob/main/src/ck-perf/trace-common.h#L26
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
    MEMORY_MALLOC = 24
    MEMORY_FREE = 25
    USER_SUPPLIED = 26
    MEMORY_USAGE = 27
    USER_SUPPLIED_NOTE = 28
    USER_SUPPLIED_BRACKETED_NOTE = 29
    END_PHASE = 30
    SURROGATE_BLOCK = 31
    USER_STAT = 32

    BEGIN_USER_EVENT_PAIR = 98
    END_USER_EVENT_PAIR = 99
    USER_EVENT_PAIR = 100


class MessageType(Flag):
    # https://github.com/charmplusplus/charm/blob/33d4d3b783301f39d6ee41542098441a2ee34256/src/ck-core/charm.h#L339
    INVALID = 0
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
        self.sts_entry_name = ""
        self.event = -1
        self.pe = -1
        self.cast_pes = -1
        self.msglen = -1  # <-> CREATION
        self.user_event_id = -1  # <-> USER_EVENT_PAIR
        self.send_time = -1
        self.recv_time = -1
        self.thread_id = [-1, -1, -1, -1, -1, -1]
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
        self.num_phases = 0

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
        message = f"{self.type.value},{self.type.name},{self.message_type.value},{self.message_type.name},{self.timestamp},{self.sts_entry},{self.sts_entry_name},{self.event},{self.pe}"
        return message

    def per_type_repr(self) -> str:
        if (
            self.type == EntryType.BEGIN_IDLE
            or self.type == EntryType.END_IDLE
            or self.type == EntryType.BEGIN_PACK
            or self.type == EntryType.END_PACK
            or self.type == EntryType.BEGIN_UNPACK
            or self.type == EntryType.END_UNPACK
        ):
            return (
                f"{self.type.value},{self.type.name},{self.timestamp},{self.pe}"
            )
        elif self.type == EntryType.END_PHASE:
            return f"{self.type.value},{self.type.name},{self.num_phases},{self.timestamp}"
        elif self.type == EntryType.USER_SUPPLIED:
            raise NotImplementedError
        elif self.type == EntryType.USER_SUPPLIED_NOTE:
            raise NotImplementedError
        elif self.type == EntryType.USER_SUPPLIED_BRACKETED_NOTE:
            raise NotImplementedError
        elif self.type == EntryType.MEMORY_USAGE:
            return f"{self.type.value},{self.type.name},{self.memory_usage},{self.timestamp}"
        elif self.type == EntryType.CREATION:
            return f"{self.type.value},{self.type.name},{self.message_type.value},{self.message_type.name},{self.sts_entry},{self.timestamp},{self.event},{self.pe},{self.msglen},{self.send_time}"
        elif self.type == EntryType.CREATION_BCAST:
            return f"{self.type.value},{self.type.name},{self.message_type.value},{self.message_type.name},{self.sts_entry},{self.timestamp},{self.event},{self.pe},{self.msglen},{self.send_time},{self.num_pes}"
        elif self.type == EntryType.CREATION_MULTICAST:
            return f"{self.type.value},{self.type.name},{self.message_type.value},{self.message_type.name},{self.sts_entry},{self.timestamp},{self.event},{self.pe},{self.msglen},{self.send_time},{self.num_pes},{','.join([str(i) for i in self.dest_pes])}"
        elif self.type == EntryType.BEGIN_PROCESSING:
            return f"{self.type.value},{self.type.name},{self.message_type.value},{self.message_type.name},{self.sts_entry},{self.timestamp},{self.event},{self.pe},{self.msglen},{self.recv_time},{','.join([str(i) for i in self.thread_id])}"
        elif self.type == EntryType.END_PROCESSING:
            return f"{self.type.value},{self.type.name},{self.message_type.value},{self.message_type.name},{self.sts_entry},{self.timestamp},{self.event},{self.pe},{self.msglen},{self.recv_time},{','.join([str(i) for i in self.thread_id])}"
        elif (
            self.type == EntryType.BEGIN_TRACE
            or self.type == EntryType.END_TRACE
        ):
            return f"{self.type.value},{self.type.name},{self.timestamp}"
        elif self.type == EntryType.MESSAGE_RECV:
            return f"{self.type.value},{self.type.name},{self.message_type.value},{self.message_type.name},{self.timestamp},{self.event},{self.pe},{self.msglen}"
        elif self.type == EntryType.ENQUEUE or self.type == EntryType.DEQUEUE:
            return f"{self.type.value},{self.type.name},{self.message_type.value},{self.message_type.name},{self.timestamp},{self.event},{self.pe}"
        elif (
            self.type == EntryType.BEGIN_INTERRUPT
            or self.type == EntryType.END_INTERRUPT
        ):
            return f"{self.type.value},{self.type.name},{self.timestamp},{self.event},{self.pe}"
        elif (
            self.type == EntryType.BEGIN_COMPUTING
            or self.type == EntryType.END_COMPUTING
        ):
            return f"{self.type.value},{self.type.name},{self.timestamp},{self.num_phases}"
        elif (
            self.type == EntryType.USER_EVENT
            or self.type == EntryType.BEGIN_USER_EVENT_PAIR
            or self.type == EntryType.END_USER_EVENT_PAIR
        ):
            raise NotImplementedError
        elif self.type == EntryType.USER_STAT:
            return f"{self.type.value},{self.type.name},{self.timestamp},{self.user_time},{self.stat},{self.pe},{self.user_event_id}"
