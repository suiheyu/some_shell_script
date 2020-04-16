#!bin/bash
# 指定多个git目录，批量pull
profile=""
for profile in $@
do
   true
done

i=0
for fileName in $@
do
    i=$((i+1))
    if [ $i -eq $#  ]
    then
        break
    fi
    cd $fileName
    git checkout $profile
    echo "**********更新$fileName*******"
    branch_current=`git branch | awk -F' ' '$1=="*"{print $2}'`
    echo "当前分支$branch_current"
    git reset --hard
    git pull
    cd ..
    echo "******************************"
    echo ""
done
