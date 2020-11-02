#!/bin/bash

# 判断参数个数
if [ $# != 2 ]; then
    echo "there are two args, one is user name, the other is user mail"
    echo "for example: $0 bibo bib019842003@163.com"
    exit 1
fi

# 清空 ~/.gitconfig 文件
echo "" > ~/.gitconfig

username=$1
useremail=$2

# 配置用户名和邮箱
git config --global user.name ${username}
git config --global user.email ${useremail}

# 配置默认编辑器
git config --global core.editor vi 

# url 地址转换
git config --global url."ssh://${username}@127.0.0.1:29415".insteadOf http://127.0.0.1
git config --global url."ssh://${username}@127.0.0.1:29415".insteadOf http://127.0.0.1:8087
