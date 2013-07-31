#!/bin/bash

SCRIPTDIR="$1"
NAME="${2}.txt"
SCRIPT="$SCRIPTDIR/$NAME"
URL="$3"
shift 3
PATTERN="$*"

TMPDIR=/tmp/lynx-check

source /etc/profile

if [ ! -d $TMPDIR ]; then
  if ! mkdir $TMPDIR ; then
    echo "Lynxcheck: UNKNOWN (unable to create $TMPDIR)"
    exit 3
  fi
fi

# start lynx session
cd $TMPDIR

# remove old "screenshot"
test -e $NAME && rm -f $NAME

if ! test -r $SCRIPT ; then
	echo "Lynxcheck: UNKNOWN (Script file $SCRIPT unreadable/does not exist)"
	exit 3
fi


start_time=$(/bin/date +%s%N)

#if ! /usr/bin/strace -f -o /tmp/lynx.trace /usr/bin/lynx -nocolor -nopause -cmd_script "$SCRIPT" "$URL" > /dev/null 2>&1 ; then
#if ! /usr/bin/lynx -nocolor -nopause -cmd_script "$SCRIPT" "$URL" > /dev/null 2>&1 ; then


if ! lynx -term=linux -nocolor -nomargins -nopause -nounderline -nobold -cmd_script "$SCRIPT" "$URL" > $NAME 2> /dev/null ; then
	echo "Lynxcheck: CRITICAL (lynx failed)"
	exit 2
fi
end_time=$(/bin/date +%s%N)
time=$((end_time-start_time))
time=$(echo "scale=3;$time/ 1000000000" | /usr/bin/bc)
if grep -q "^\." <<<$time ; then
	time="0${time}"
fi

# verify file
if [ -e $NAME ]; then
	
	GREP_RESULT=""
	GREP_RESULT=$(grep "$PATTERN" $NAME)
	
	if [ ! -z "$GREP_RESULT" ]; then
	
		echo "Lynxcheck: OK | time=$time"
		exit 0
		
	else
		
		echo "Lynxcheck: CRITICAL (pattern not found) | time=$time"
		exit 2
	
	fi
	
else

	#echo "Lynxcheck: UNKNOWN (Plugin Error)"
	echo "Lynxcheck: Critical (Result file not found)| time=$time"
	#exit 3
	exit 2
	
fi
