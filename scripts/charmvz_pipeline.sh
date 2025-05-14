#!/bin/bash
declare -A pj_ids

generate_event_def() {
    local event_name="$1"
    local id="$2"
    pj_ids[$event_name]=$id
    echo "%EventDef $event_name $id"
    "define_$event_name"
    generate_event_closure
}

generate_event_closure() {
    echo "%EndEventDef"
}

field_time()         { echo "%       Time date"; }
field_container()    { echo "%       Container string"; }
field_type()         { echo "%       Type string"; }
field_value_string() { echo "%       Value string"; }
field_value_double() { echo "%       Value double"; }
field_name()         { echo "%       Name string"; }
field_color()        { echo "%       Color color"; }
field_start_container() { echo "%       StartContainer string"; }
field_end_container()   { echo "%       EndContainer string"; }
field_start_container_type() { echo "%       StartContainerType string"; }
field_end_container_type()   { echo "%       EndContainerType string"; }
field_key()          { echo "%       Key string"; }

define_PajePushState() {
    field_time
    field_container
    field_type
    field_value_string
}

define_PajePopState() {
    field_time
    field_container
    field_type
}

define_PajeDefineContainerType() {
    field_name
    field_type
}

define_PajeDefineStateType() {
    field_name
    field_type
}

define_PajeCreateContainer() {
    field_time
    field_type
    field_name
    field_container
}

define_PajeDestroyContainer() {
    field_time
    field_type
    field_name
}

generate_event_def PajeCreateContainer 0
generate_event_def PajeDestroyContainer 1
generate_event_def PajePushState 2
generate_event_def PajePopState 3
generate_event_def PajeDefineContainerType 4
generate_event_def PajeDefineStateType 5

pj() {
    local event_name="$1"
    echo ${pj_ids[$event_name]}
}

# PajePushState Time Container Type Value
pj_PushState() {
    local time="$1" container="$2" type="$3" value="$4"
    echo $(pj "PajePushState") "$time" "$container" "$type" "$value"
}

# PajePopState Time Container Type
pj_PopState() {
    local time="$1" container="$2" type="$3"
    echo $(pj "PajePopState") "$time" "$container" "$type"
}

# PajeDefineContainerType [Alias] Type Name
pj_DefineContainerType() {
    local type="$1" name="$2"
    echo $(pj "PajeDefineContainerType") "$type" "$name"
}

pj_DefineStateType() {
    local type="$1" name="$2"
    echo $(pj "PajeDefineStateType") "$type" "$name"
}

# PajeCreateContainer Time [Alias] Container Type Name
pj_CreateContainer() {
    local time="$1" type="$2" name="$3" container="$4"
    echo $(pj "PajeCreateContainer") "$time" "$type" "$name" "$container"
}

# PajeDestroyContainer Time Type Name
pj_DestroyContainer() {
    local time="$1" type="$2" name="$3"
    echo $(pj "PajeDestroyContainer") "$time" "$type" "$name"
}

pj_DefineContainerType PE 0
pj_DefineStateType STATE PE

TEMPFILE=/tmp/out.aux
cat | \
    grep _PROCESSING | \
    cut -d, -f1,5,7,9 > ${TEMPFILE}

PE_ELEMENTS=$(cat ${TEMPFILE} | cut -d, -f4 | sort | uniq)
for pe in ${PE_ELEMENTS}; do
    pj_CreateContainer 0.0 PE pe${pe} 0
done

PAJEFILE=/tmp/out.pj
cat ${TEMPFILE} | \
    sed 's/,/ /g' | \
    awk '{ print $1 " " $2 " pe" $4 " STATE " $3 }' | \
    sed '/^3/ s/ [^ ]*$//' | \
    sort -S 50% --parallel=4 -T . -s -V --key=2,2 > ${PAJEFILE}

#OUTPUT="output.pj"
CSV="output.csv"
~/dev/pajeng/b13/pj_dump ${PAJEFILE} | grep ^State > ${CSV}
#head ${CSV}
