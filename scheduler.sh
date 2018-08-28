#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
$3 scrape.py \-con_req $1 \-con_req_dom $2 --schedule 
