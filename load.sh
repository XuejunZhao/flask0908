cd ~/workspaces
export WORKON_HOME=~/workspaces
cd
source //anaconda/bin/virtualenvwrapper.sh
workon env1
cd /Users/xuejun/Downloads/traffic-spark-extension-master-152ea962cc1748a7a7e24ed06de5bd28099a2caa/assembly/bin && echo $PWD
TRAFFIC_HOME=/Users/xuejun/Downloads/traffic-spark-extension-master-152ea962cc1748a7a7e24ed06de5bd28099a2caa/dist ./pysubmit-traffic generate_range "20170728" 7 $1 $2 "test" 0 >>test09.txt
echo $2
echo $1


