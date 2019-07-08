
# grap OS from os-release (ex. ID="centos")
eval $(cat /etc/os-release | grep ^ID=.*)

echo $ID



