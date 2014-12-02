#!/bin/bash

# Bash script containing options to run sample data sets

run_txt()
{

    echo
    python waterapputils/waterapputils.py -watertxt data/watertxt-datafiles/WATER-basin-01413500.txt 
    python waterapputils/waterapputils.py -watertxt data/watertxt-datafiles/WATER-basin-01420500.txt
    python waterapputils/waterapputils.py -watertxtcmp data/watertxt-datafiles/WATER-basin-01413500.txt data/watertxt-datafiles/WATER-basin-01420500.txt 	
    echo
}

run_xml()
{

    echo
	python waterapputils/waterapputils.py -waterxml data/waterxml-datafiles/WATERSimulation-basin-01413500.xml 
	python waterapputils/waterapputils.py -waterxml data/waterxml-datafiles/WATERSimulation-basin-01420500.xml
	python waterapputils/waterapputils.py -waterxmlcmp data/waterxml-datafiles/WATERSimulation-basin-01413500.xml data/waterxml-datafiles/WATERSimulation-basin-01420500.xml
    echo
}

run_wateruse()
{
    echo
    python waterapputils/waterapputils.py -applywateruse
    echo 
}

run_all()
{

    echo 
    run_txt
    run_xml
    run_wateruse
    echo
}

usage()
{

	echo "Usage:"
	echo "    run_sample_datasets [[[-txt] [-xml] [-all]] | [-h]]"
}

# if no arguments, then run everything
if [ "$1" = "" ]; then
	echo "$0 is running ALL sample datasets"
	run_all
fi

# if there are options, then processing accordingly
while [ "$1" != "" ]; do
	case $1 in
		-txt )           echo "$0 is running TEXT sample datasets"
		                 run_txt
                         ;;
		-xml )           echo "$0 is running XML sample datasets"
                         run_xml
                         ;;
        -wateruse )      echo "$0 is running water use sample datasets as specified in user_settings.py"
                         run_wateruse
                         ;;
        -all )           echo "$0 is running ALL sample datasets"
                         run_all
                         ;;
        -h | --help )    usage
                         exit
                         ;;
        * )              usage
                         exit
                         ;;
    esac
    shift
done

