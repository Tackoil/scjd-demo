#!/bin/bash
# 1. 生成数据库可执行文件，
# 2. 根据数据库可执行文件来修改数据库
# 3. 在指定端口启动 django 服务

#echo $1 ip
#echo $2 端口号


 ret1=${1:-'0.0.0.0'}
 ret2=${2:-'14144'}
 DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/scjd_django"
 MANAGE="${DIR}/manage.py"
 if [ ! -d "${DIR}/uploads/" ]; then
  mkdir ${DIR}/uploads/
 fi
 cp -f ${DIR}/initial_chart_json/*_*.json ${DIR}/uploads/

 python ${MANAGE} makemigrations
 python ${MANAGE} migrate
 python ${MANAGE} loaddata ${DIR}/initial_chart_json/initial.json
 cd scjd_django
 python ${MANAGE} runserver ${ret1}:${ret2}
