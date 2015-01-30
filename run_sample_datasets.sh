#!/bin/bash

# Description: Bash script to run sample data sets and tests
#
# Usage: run_sample_datasets.sh [option]
#        run_sample_datasets.sh [[[-txt] [-xml] [-wateruse] [-oasis] [-ecoflowstationid] [ecoflowdaxml] [-ecoflowdashp] [-gcmdelta] [-mapsim] [-all] [tests]] | [-h]]

run_txt()
{

    echo "--- $0 is running TEXT sample datasets ---"
    echo
    python waterapputils/waterapputils.py -watertxt data/watertxt-datafiles/WATER-basin-01413500.txt 
    python waterapputils/waterapputils.py -watertxt data/watertxt-datafiles/WATER-basin-01420500.txt
    python waterapputils/waterapputils.py -watertxtcmp data/watertxt-datafiles/WATER-basin-01413500.txt data/watertxt-datafiles/WATER-basin-01420500.txt 	
    echo
}

run_xml()
{

    echo "--- $0 is running XML sample datasets ---"
    echo
	python waterapputils/waterapputils.py -waterxml data/waterxml-datafiles/WATERSimulation-basin-01413500.xml 
	python waterapputils/waterapputils.py -waterxml data/waterxml-datafiles/WATERSimulation-basin-01420500.xml
	python waterapputils/waterapputils.py -waterxmlcmp data/waterxml-datafiles/WATERSimulation-basin-01413500.xml data/waterxml-datafiles/WATERSimulation-basin-01420500.xml
    echo
}

run_wateruse()
{
    # applying wateruse requires many inputs, and those inputs are specified in the user_settings.py file which contain relative paths from the directory containing the python code
    # this requires changing directories into the waterapputils directory in order to run the sample datasets

    cd waterapputils/
    echo "--- $0 is running water use with sample datasets; single and batch ---"
    echo
    # echo "single simulation"
    # python waterapputils.py -applywateruse -samplesingle
    # echo
    echo "batch simulation"
    python waterapputils.py -applywateruse -samplebatch
    echo
    # echo "user supplied batch simulation"
    # python waterapputils.py -applywateruse -simdir ../data/sample-water-simulations/sample-batch-simulation/
    # echo 
}

run_subwateruse()
{
    echo "--- $0 is running sub water use with sample datasets ---"
    echo
    file=data/sample-water-simulations/sample-batch-simulation/waterapputils-info/wateruse_non_intersecting_centroids.txt
    if [ -f $file ]; then 
        echo "substitiuting basin id 262 for 000 in sub water use file"
        sed -i.bak 's/000/262/g' $file
        
        cd waterapputils/
        python waterapputils.py -applysubwateruse -samplebatch
    else
       echo "ERROR - file does not exist - $file" >&2
       exit 1 
    fi
}

run_oasis()
{

    echo "--- $0 is running oasis output ---"
    echo
    python waterapputils/waterapputils.py -oasis data/sample-water-simulations/sample-datafiles/WATERUSE-WATER-basin0.txt 
    echo     
}

run_ecoflowstationid()
{

    echo "--- $0 is running ecoflowstationid output ---"
    echo
    python waterapputils/waterapputils.py -ecoflowstationid data/sample-water-simulations/sample-datafiles/WATERUSE-WATER-basin0.txt
    echo     
    python waterapputils/waterapputils.py -ecoflowstationid data/sample-water-simulations/sample-datafiles/WATERUSE-WATER-basin0.txt -parameter Discharge -outfilename basin0-orig-discharge.csv
}

run_ecoflowdaxml()
{
    
    echo "--- $0 is running ecoflow drainage area using xml file ---"
    echo
    python waterapputils/waterapputils.py -ecoflowdaxml data/sample-water-simulations/sample-datafiles/WATERSimulation-basin0.xml -outfilename drainagearea-from-xml.csv
    echo
}

run_ecoflowdashp()
{
    
    echo "--- $0 is running ecoflow drainage area using shapefiles ---"
    echo
    python waterapputils/waterapputils.py -ecoflowdashp data/sample-water-simulations/sample-datafiles/Watersheds.shp -outfilename drainagearea-Watersheds.csv -labelfield STAID -areafield da_sqmi
    python waterapputils/waterapputils.py -ecoflowdashp data/sample-water-simulations/sample-datafiles/basin0.shp -outfilename drainagearea-basin0-sqmi.csv -areafield area_sqmi
    python waterapputils/waterapputils.py -ecoflowdashp data/sample-water-simulations/sample-datafiles/basin0.shp -outfilename drainagearea-basin0-sqkm.csv -areafield area_sqkm
    python waterapputils/waterapputils.py -ecoflowdashp data/sample-water-simulations/sample-datafiles/basin0.shp -outfilename drainagearea-basin0-sqm.csv -areafield area_sqm
    python waterapputils/waterapputils.py -ecoflowdashp data/sample-water-simulations/sample-datafiles/basin0.shp -outfilename drainagearea-basin0-calculated-sqmi.csv 
    echo     

}

run_gcmdelta()
{
    # applying gcmdelta requires many inputs, and those inputs are specified in the user_settings.py file which can relative paths from the directory containing the python code
    # this requires changing directories into the waterapputils directory in order to run the sample datasets

    cd waterapputils/
    echo "--- $0 is running gcm delta with sample datasets; single and batch ---"
    echo
    echo "single simulation"
    python waterapputils.py -applygcmdelta -samplesingle
    echo
    echo "batch simulation"
    python waterapputils.py -applygcmdelta -samplebatch
    echo 
}

run_subgcmdelta()
{
    echo "--- $0 is running sub gcm delta with sample datasets ---"
    echo
    file=data/sample-water-simulations/sample-batch-simulation/waterapputils-info/wateruse_non_intersecting_tiles.txt
    if [ -f $file ]; then 
        echo "substitiuting tile id 12 for 000 in sub gcm delta factor file"
        sed -i.bak 's/000/12/g' $file
        
        cd waterapputils/
        python waterapputils.py -applysubgcmdelta -samplebatch
    else
       echo "ERROR - file does not exist - $file" >&2
       exit 1 
    fi
}

run_mapsim()
{
    # applying wateruse requires many inputs, and those inputs are specified in the user_settings.py file which contain relative paths from the directory containing the python code
    # this requires changing directories into the waterapputils directory in order to run the sample datasets

    cd waterapputils/
    echo "--- $0 is creating maps with sample datasets; single and batch ---"
    echo
    echo "single simulation"
    python waterapputils.py -mapsim -samplesingle
    echo
    echo "batch simulation"
    python waterapputils.py -mapsim -samplebatch
    echo 
}


run_all()
{

    echo "--- $0 is running ALL sample datasets ... This may take a while ... Please wait ... ---"
    echo
    run_tests
    run_txt
    run_xml
    run_oasis
    run_ecoflowstationid
    run_ecoflowdaxml
    run_ecoflowdashp
    run_wateruse
    run_gcmdelta
    run_mapsim
    echo
}

run_tests()
{
    echo "--- $0 is running tests ---"
    echo
    nosetests
    echo
}

makeclean()
{

    rm -f waterapputils/*.txt
    rm -f waterapputils/*.xml
    rm -f tests/*.txt
    rm -r tests/test-dir
    rm -f tests/*.csv
    rm -r data/watertxt-datafiles/waterapputils*
    rm -r data/waterxml-datafiles/waterapputils*
    rm -r data/sample-water-simulations/sample-datafiles/waterapputils*
    rm -r data/sample-water-simulations/sample-single-simulation/waterapputils*
    rm -r data/sample-water-simulations/sample-batch-simulation/waterapputils*
    rm -r data/sample-water-simulations/sample-batch-simulation/014*/waterapputils*

}

usage()
{

	echo "Usage:"
	echo "    run_sample_datasets.sh [[[-txt] [-xml] [-wateruse] [-oasis] [-ecoflowstationid] [ecoflowdaxml] [-ecoflowdashp] [-gcmdelta] [-mapsim] [-all] [tests]] | [-h]]"
}

# main program

# if no arguments, then run everything
if [ "$1" = "" ]; then
	echo "$0 is running ALL sample datasets"
	run_all
fi

# if there are options, then processing accordingly
while [ "$1" != "" ]; do
	case $1 in
		-txt )                       run_txt
                                     ;;
		-xml )                       run_xml
                                     ;;
        -wateruse )                  run_wateruse
                                     ;;
        -subwateruse )               run_subwateruse
                                     ;;
        -oasis )                     run_oasis
                                     ;;
        -ecoflowstationid )          run_ecoflowstationid
                                     ;;
        -ecoflowdaxml )              run_ecoflowdaxml
                                     ;;
        -ecoflowdashp )              run_ecoflowdashp
                                     ;;
        -gcmdelta )                  run_gcmdelta
                                     ;;
        -subgcmdelta )               run_subgcmdelta
                                     ;;
        -all )                       run_all
                                     ;;
        -tests )                     run_tests
                                     ;;
        -mapsim )                    run_mapsim
                                     ;;
        -makeclean )                 makeclean
                                     ;;                                     
        -h | --help )                usage
                                     exit
                                     ;;
        * )                          usage
                                     exit
                                     ;;
    esac
    shift 
done

