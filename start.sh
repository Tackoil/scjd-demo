#!/bin/bash
# 1. 生成数据库可执行文件，
# 2. 根据数据库可执行文件来修改数据库
# 3. 在指定端口启动 django 服务

#echo $1 ip
#echo $2 端口号


 python scjd_django/manage.py makemigrations
 python scjd_django/manage.py migrate
 python scjd_django/manage.py runserver $1:$2

