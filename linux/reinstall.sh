#!bin/bash
#  批量卸载安装chart包
#  语法reinstall.sh <chart-dir [chart-dir1] [chart-dir2] ...> <envrionment-key>
#  例子sh reinstall.sh vod-service vod-front vod-openapi staging
#      sh reinstall.sh vod-service vod-front vod-openapi mps-dispatcher test
#      sh reinstall.sh vod-service dev
#
profile=""
for profile in $@
do
  true
done
testV=`echo $profile | grep -E "^(dev|test|staging)$"`
n=$#
echo "test value $testV"
if [ -n "$testV" ]
then
    profile=-$profile
else
    profile=""
    n=$(( n+1 ))

fi
i=0
echo "*********start**********************"
for f in $@
do
    i=$(( i+1 ))
    if [ $i -eq $n ]
    then
      break
    fi
    echo "---------卸载$f---------"
    shellName=$f/uninstall.sh
    echo "uninstall shell name $shellName"
    sh $shellName
    echo "---------卸载完成---------"
    echo ""
done

i=0
for f in $@
do
    i=$(( i+1 ))
    if [ $i -eq $n ]
    then
      break
    fi
    echo "---------安装$f---------"
    shellName=$f/install.sh
    valuesName=$f/values${profile}.yaml
    echo "install shell name $shellName"
    echo "install values name $valuesName"
    sh $shellName $valuesName
    echo "---------安装完成---------"
    echo ""
done

echo "*********end**********************"
echo ""

echo "任意键继续"
read
i=0
watchCmd="watch -n 1 -d \" kubectl -nfusionproduct get po | egrep '"
for f in $@
do
    i=$((i+1))
    if [ $i -eq $n ]
    then
      break
    fi
    watchCmd=$watchCmd'('$f')|'
done
watchCmd=${watchCmd%|}
watchCmd=$watchCmd"'\""
eval $watchCmd