# bash script to automate the process of running many WATER simulations

SIMULATIONSDIR=$1

#cd waterapputils/

for dir in $SIMULATIONSDIR/* 
do
    echo $dir
#    python waterapputils.py -applysubwateruse -simdir $dir
done
