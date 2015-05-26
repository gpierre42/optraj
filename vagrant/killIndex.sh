#!/bin/bash

output=`ps aux|grep index.py`
set -- $output
pid=$2
kill $pid
