#!/bin/bash

# Description: Bash script to automate the process of running/processing many WATER simulations
#
# Usage: run_simulations.bash [option]
#        run_simulations.bash [[[-txt] [-xml] [-wateruse] [-oasis] [-ecoflowstationid] [ecoflowdaxml] [-ecoflowdashp] [-gcmdelta] [-mapsim] [-all] [tests]] | [-h]]

run()
{
	echo "Running option:" $1

    # Applying wateruse requires many inputs, and some of those inputs are specified 
    # in the user_settings.py file which may contain relative paths from the 
    # waterapputils/waterapputils directory which requires changing directories.
	cd waterapputils/

	for dir in $2/* 
	do
	    echo $dir
	    python waterapputils.py $1 -simdir $dir
	done	
}

usage()
{
	echo "Usage:"
	echo "    run_simulations.bash [option] path-to-simulations-directory"
	echo ""
	echo "    run_simulations.bash [[[-applywateruse] [-applysubwateruse] [-applygcmdelta] [-applysubgcmdelta]] path-to-simulations-directory | [-h]]"
}

# main program

# if no arguments, then print usage
if [ "$1" = "" ]; then
	usage
fi

# while there are options/arguments, process accordingly
while [ "$1" != "" ] ; do

	OPTION=$1
	SIMDIR=$2

	case $OPTION in
		-applywateruse )		run $OPTION $SIMDIR
								;;
		-applysubwateruse )		run $OPTION $SIMDIR
								;;								
		-applygcmdelta )		run $OPTION $SIMDIR
								;;
		-applysubgcmdelta )		run $OPTION $SIMDIR
								;;
		-h | --help ) 			usage
								exit
								;;
		* )			 			exit
								;;
	esac
	shift
done
