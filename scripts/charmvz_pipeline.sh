#!/bin/bash
OUTPUT="output.pj"
echo '%EventDef PajePushState 2
%       Time date
%       Container string
%       Type string
%       Value string
%EndEventDef
%EventDef PajePopState 3
%       Time date
%       Container string
%       Type string
%EndEventDef
%EventDef PajeCreateContainer 10
%       Time date
%       Type string
%       Name string
%       Container string
%EndEventDef
%EventDef PajeDestroyContainer 11
%       Time date
%       Type string
%       Name string
%EndEventDef
%EventDef PajeDefineContainerType 12
%       Name string
%       Type string
%EndEventDef
%EventDef PajeDefineVariableType 13
%       Alias string
%       Type string
%       Name string
%       Color color
%EndEventDef
%EventDef PajeDefineStateType 14
%       Name string
%       Type string
%EndEventDef
%EventDef PajeDefineEventType 15
%       Alias string
%       Type string
%       Name string
%EndEventDef
%EventDef PajeDefineLinkType 16
%       Alias string
%       Type string
%       StartContainerType string
%       EndContainerType string
%       Name string
%EndEventDef
%EventDef PajeDefineEntityValue 17
%       Alias string
%       Type string
%       Name string
%       Color color
%EndEventDef
#
# This is the type hierarchy
#
12 PE 0
14 STATE PE
#
# These are the events
#' > $OUTPUT

INPUTFILE=${HOME}/Devel/charmvz/results.csv
TEMPFILE=/tmp/mytempfile.aux
cat ${INPUTFILE} | \
    grep _PROCESSING | \
    cut -d, -f1,5,2,9 > ${TEMPFILE}

OUTPUT="output.pj"
TEMPFILE=/tmp/mytempfile.aux
PE_ELEMENTS=$(cat ${TEMPFILE} | cut -d, -f4 | sort | uniq)
echo ${PE_ELEMENTS}
for pe in ${PE_ELEMENTS}; do
    echo "10 0.0 PE pe${pe} 0"
done >> $OUTPUT

OUTPUT="output.pj"
TEMPFILE=/tmp/mytempfile.aux
cat ${TEMPFILE} | \
    sed 's/,/ /g' | \
    awk '{ print $1 " " $2 " pe" $4 " STATE " $3 }' | \
    sed '/^3/ s/ [^ ]*$//' >> $OUTPUT

#OUTPUT="output.pj"
#CSV="output.csv"
#~/dev/pajeng/b13/pj_dump ${OUTPUT} | grep ^State > ${CSV}
#head ${CSV}
