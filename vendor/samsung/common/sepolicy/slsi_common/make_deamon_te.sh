#!/bin/bash

for filename in $@
do
	echo "# $filename
type $filename, domain;
type "$filename"_exec, exec_type, file_type;
init_daemon_domain($filename)" > $filename.te
done;
