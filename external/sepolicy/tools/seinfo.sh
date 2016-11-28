#!/bin/bash


err() {
	echo -e "ERROR $@" 1>&2
	exit 1
}

while getopts "xa:" opt; do
  case $opt in
    x)
      NOOP=0
      ;;
    a)
      ATTR=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done


shift $(($OPTIND - 1))

if [[ ! -f "$@" ]]; then
	err "Usage: seinfo.sh -a ATTRIBUTE POLICY.CONF"
fi

POLICY="$@"


real_type_name() {
	ALIAS=$(egrep -e "^ *typealias .* alias.* $@[ ;]" "$POLICY")
	if [[ $ALIAS == "" ]]; then 
		echo $@
	else
		echo $ALIAS | awk '{print $2}'
	fi
}

ATTR=$(real_type_name $ATTR)
## see if there is an attribute declaration for ATTR, if not,
## check if ATTR is a type, if so, return, if not, err out
IS_ATTR=$(grep "^ *attribute $ATTR[,;]" "$POLICY"|wc -l)
if [[ $IS_ATTR -eq 0 ]]; then
	#not an attribute
	IS_TYPE=$(grep "^ *type $ATTR[,;]" "$POLICY"|wc -l)
	if [[ $IS_TYPE -eq 0 ]]; then
		err "$ATTR is not a type or attribute!"
	else
		echo $ATTR
	fi
else
	#is an attribute
	TMP=$(tempfile)
	egrep -e "^ *type [a-Z0-9_-]+ *,.* $ATTR[,; ]" -e "^ *type [a-Z0-9_-]+ *, *$ATTR[,; ]" -e "^ *type [a-Z0-9_-]+ *,.*,$ATTR[,; ]" -e "^ *typeattribute [a-Z0-9_-]+.* $ATTR[ ;]"  "$POLICY" |awk '{print $2}'|cut -d"," -f1 > "$TMP"

	while read line
	do
		real_type_name $line
	done < "$TMP"
	rm "$TMP"

fi






