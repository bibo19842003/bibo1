#!/bin/bash

cd /tmp
rm -rf bibo1
git clone https://github.com/bibo19842003/bibo1.git
cd bibo1/env/ubuntu_init


# 更换 ubuntu 22.04国内源
# https://blog.csdn.net/zynaln/article/details/124373005
sudo cp sources.list /etc/apt/

sudo apt update


# samba 
# https://blog.51cto.com/u_64214/5532988
# https://blog.51cto.com/u_64214/5532840
sudo apt install samba -y
mkdir ~/share_file
chmod 777 ~/share_file
sudo smbpasswd -a bibo
sudo cp smb.conf /etc/samba/
# sudo systemctl restart smbd
sudo service smbd restart


# sshd
sudo apt install openssh-server -y
sudo /etc/init.d/ssh stop
sudo /etc/init.d/ssh start


# miniconda
# https://mirror.tuna.tsinghua.edu.cn/help/anaconda/
# https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/
# Miniconda3-py39_4.12.0-Linux-x86_64.sh
pwd
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh
chmod a+x Miniconda3-py39_4.12.0-Linux-x86_64.sh
./Miniconda3-py39_4.12.0-Linux-x86_64.sh
cp .condarc ~/
conda clean -i

# https://www.jianshu.com/p/ca7e3d9d27a3
mkdir ~/.pip
cp pip.conf ~/.pip/












# 



