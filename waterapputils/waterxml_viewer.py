# -*- coding: utf-8 -*-
"""
:Module: waterxml_viewer.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/ 

:Synopsis: Handles views of the data, such as printing and plotting.
"""

__author__   = "Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center."
__copyright__ = "http://www.usgs.gov/visual-id/credit_usgs.html#copyright"
__license__   = __copyright__
__contact__   = __author__

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from textwrap import wrap
from StringIO import StringIO
import datetime
import numpy as np
import os

# my modules
import waterxml

def print_waterxml_data(waterxml_tree):
    """   
    Print information and data contained in the water xml tree. 
    
    Parameters
    ----------
    waterxml_tree : dictionary 
        A dictionary containing data found in WATER output text file.
    
    """  
    # print relevant information
    print("")
    print("--- WATER XML FILE INFORMATION ---")
    
    project, study, simulation = waterxml.get_xml_data(waterxml_tree = waterxml_tree)

    print("Project Information:")
    print("    {}\n".format(project))

    print("Study Information:")
    print("    {}\n".format(study))
       
    print("Simulation Information:\n")
    for key, value in simulation.iteritems():
        if key == "SimulID":
            print("    SimulID:")
            print("        {}\n".format(value))
        elif key == "StudyID":
            print("    StudyID:")
            print("        {}\n".format(value))        
        elif key == "RegionType":
            print("    RegionType:")
            print("        {}\n".format(value))     
        elif key in ["SimulationFeatures", "SimulationTopographicWetnessIndex", "StudyUnitDischargeSeries", "ClimaticPrecipitationSeries", "ClimaticTemperatureSeries"]:
            print("    {}".format(key))
            for i in range(len(value)):
                for j in range(len(value[i])):
                    print("")
                    for k, v in value[i][j].iteritems():
                        print("        {} : {}".format(k, v))
                print("")    


def plot_waterxml_topographic_wetness_index_data(waterxml_tree, is_visible = True, save_path = None):
    """   
    Plot histogram of topographic_wetness_index data from the WATER \*.xml file.
    
    Parameters
    ----------
    waterxml_data : dictionary 
        A dictionary containing data found in WATER \*.xml data file.
    is_visible : bool
        Boolean value to show plots         
    save_path : string 
        String path to save plot(s)      
    """
    twi_str = "Topographic Wetness Index"     
    
    project, study, simulation = waterxml.get_xml_data(waterxml_tree = waterxml_tree)       

    for i in range(len(simulation["SimulID"])):
 
        region_type = simulation["RegionType"][i]
        sim_id = simulation["SimulID"][i]

        # get the bin_ids, bin_value_means, and bin_value_fractions - these are lists each of which contain arrays corresponding to each SimulID 
        bin_ids, bin_value_means, bin_value_fractions = waterxml.get_topographic_wetness_index_data(simulation_dict = simulation)

        fig = plt.figure(figsize=(12,10))
        ax1 = fig.add_subplot(211)
        ax1.grid(True)
        ax1.set_title("{}\nRegion Type: {}\nSimulation ID: {}".format(twi_str, region_type, sim_id))
        ax1.set_xlabel("Bin Ids")
        ax1.set_ylabel("Bin Value Means")   
       
        width = 0.7 * (bin_ids[i][1] - bin_ids[i][0])
        ax1.bar(bin_ids[i], bin_value_means[i], width = width, align = "center", label = "Bin Value Means") 
    
        ax2 = fig.add_subplot(212)
        ax2.grid(True)
        ax2.set_xlabel("Bin Ids")
        ax2.set_ylabel("Bin Value Fractions")   
       
        ax2.bar(bin_ids[i], bin_value_fractions[i], width = width, align = "center", label = "Bin Value Fractions") 
                
        # save plots
        if save_path:        
            # set the size of the figure to be saved
            curr_fig = plt.gcf()
            curr_fig.set_size_inches(12, 10)
            
            # split the parameter name to not include units because some units contain / character which Python interprets as an escape character
            filename = "-".join([project["UserName"], project["ProjName"], twi_str, region_type, sim_id])  + ".png"           
            filepath = os.path.join(save_path, filename)
            plt.savefig(filepath, dpi = 100)                        
          
        # show plots
        if is_visible:
            plt.show()
        else:
            plt.close()
            
def plot_waterxml_timeseries_data(waterxml_tree, is_visible = True, save_path = None):
    """   
    Plot timeseries data from the WATER \*.xml file.  The timeseries data are contained 
    in the study simulation dictionary. The following timeseries data are plotted:
    discharge - from xml element called "StudyUnitDischargeSeries", 
    precipitation - from xml element called "ClimaticPrecipitationSeries",
    temperature = from xml element called "ClimaticTemperatureSeries"
    
    Parameters
    ----------
    waterxml_data : dictionary 
        A dictionary containing data found in WATER \*.xml data file.
    is_visible : bool
        Boolean value to show plots         
    save_path : string 
        String path to save plot(s)      
    """
    project, study, simulation = waterxml.get_xml_data(waterxml_tree = waterxml_tree)       

    for i in range(len(simulation["SimulID"])):
        for timeseries_str in ["StudyUnitDischargeSeries", "ClimaticPrecipitationSeries", "ClimaticTemperatureSeries"]:         

            region_type = simulation["RegionType"][i]
            sim_id = simulation["SimulID"][i]

            # get the dates, values, and units - these are lists each of which contain arrays corresponding to each SimulID 
            dates, values, units = waterxml.get_timeseries_data(simulation_dict = simulation, timeseries_key = timeseries_str)

            fig = plt.figure(figsize=(12,10))
            ax = fig.add_subplot(111)
            ax.grid(True)

            if timeseries_str == "StudyUnitDischargeSeries":
                ylabel = "Discharge ({})".format(units[i])
                color_str = "b"
                
            elif timeseries_str == "ClimaticPrecipitationSeries":
                ylabel = "Precipitation ({})".format(units[i])
                color_str = "SkyBlue"      
                
            elif timeseries_str == "ClimaticTemperatureSeries":
                ylabel = "Temperature ({})".format(units[i])
                color_str = "orange"  
                
            else:
                ylabel = "Some other parameter"
                color_str = "k" 
            
            ax.set_title("{}\nRegion Type: {}\nSimulation ID: {}".format(timeseries_str, region_type, sim_id))
            ax.set_xlabel("Date")
            ax.set_ylabel(ylabel)   
            
            plt.plot(dates[i], values[i], color = color_str, label = ylabel) 
        
            # rotate and align the tick labels so they look better
            fig.autofmt_xdate()
            
            # use a more precise date string for the x axis locations in the
            # toolbar
            ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
         
            # legend; make it transparent    
            handles, labels = ax.get_legend_handles_labels()
            legend = ax.legend(handles, labels, fancybox = True)
            legend.get_frame().set_alpha(0.5)
            legend.draggable(state=True)
            
            # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
            text = "mean = %.2f\nmax = %.2f\nmin = %.2f" % (np.nanmean(values[i]), np.nanmax(values[i]), min(values[i]))
            patch_properties = {"boxstyle": "round", "facecolor": "wheat", "alpha": 0.5}
                           
            ax.text(0.05, 0.95, text, transform = ax.transAxes, fontsize = 14, 
                    verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)
            
            # save plots
            if save_path:        
                # set the size of the figure to be saved
                curr_fig = plt.gcf()
                curr_fig.set_size_inches(12, 10)
                
                # split the parameter name to not include units because some units contain / character which Python interprets as an escape character
                filename = "-".join([project["UserName"], project["ProjName"], timeseries_str, region_type, sim_id])  + ".png"           
                filepath = os.path.join(save_path, filename)
                plt.savefig(filepath, dpi = 100)                        
              
            # show plots
            if is_visible:
                plt.show()
            else:
                plt.close()

def plot_waterxml_timeseries_comparison(waterxml_tree1, waterxml_tree2, is_visible = True, save_path = None):
    """   
    Compare each timeseries for 2 WATER \*.xml files.
    
    Parameters
    ----------
    waterxml_data1 : dictionary 
        A dictionary containing data found in WATER \*.xml data file.
    waterxml_data2 : dictionary 
        A dictionary containing data found in WATER \*.xml data file.
    is_visible : bool
        Boolean value to show plots         
    save_path : string 
        String path to save plot(s)      
    """
    project1, study1, simulation1 = waterxml.get_xml_data(waterxml_tree = waterxml_tree1)       
    project2, study2, simulation2 = waterxml.get_xml_data(waterxml_tree = waterxml_tree2)

    assert len(simulation1["SimulID"]) == len(simulation2["SimulID"]), "The lengths of the number of SimulID's between the 2 xml files are not equal."

    for i in range(len(simulation1["SimulID"])):
        for timeseries_str in ["StudyUnitDischargeSeries", "ClimaticPrecipitationSeries", "ClimaticTemperatureSeries"]:         

            region_type1 = simulation1["RegionType"][i]
            sim_id1 = simulation1["SimulID"][i]

            region_type2 = simulation2["RegionType"][i]
            sim_id2 = simulation2["SimulID"][i]

            # get the dates, values, and units - these are lists each of which contain arrays corresponding to each SimulID 
            dates1, values1, units1 = waterxml.get_timeseries_data(simulation_dict = simulation1, timeseries_key = timeseries_str)
            dates2, values2, units2 = waterxml.get_timeseries_data(simulation_dict = simulation2, timeseries_key = timeseries_str)

            assert region_type1 == region_type2, "Region Types {} and {} are not equal".format(region_type1, region_type2)
            assert sim_id1 == sim_id2, "Simulation Id's {} and {} are not equal".format(sim_id1, sim_id2)
            assert units1[i] == units2[i], "Units {} and {} are not equal".format(units1[i], units2[i])            
            assert len(dates1[i]) == len(dates2[i]), "Length of dates {} and {} are not equal".format(dates1[i], dates2[i]) 
            assert len(values1[i]) == len(values2[i]), "Length of values {} and {} are not equal".format(values1[i], values2[i]) 
               
            fig = plt.figure(figsize=(12,10))
            ax1 = fig.add_subplot(211)
            ax1.grid(True)

            if timeseries_str == "StudyUnitDischargeSeries":
                ylabel = "Discharge ({})".format(units1[i])
                color_str1 = "b"
                color_str2 = "r"  
                
            elif timeseries_str == "ClimaticPrecipitationSeries":
                ylabel = "Precipitation ({})".format(units1[i])
                color_str1 = "SkyBlue"      
                color_str2 = "r"  
                
            elif timeseries_str == "ClimaticTemperatureSeries":
                ylabel = "Temperature ({})".format(units1[i])
                color_str1 = "orange"  
                color_str2 = "r"                 
            else:
                ylabel = "Some other parameter"
                color_str1 = "k" 
                color_str2 = "r" 
                
            ax1.set_title("{}\nRegion Type: {}\nSimulation ID: {}".format(timeseries_str, region_type1, sim_id1))
            ax1.set_xlabel("Date")
            ax1.set_ylabel(ylabel)   
            
            ax1.plot(dates1[i], values1[i], color = color_str1, label = ylabel + " xml-file-1", linewidth = 2) 
            ax1.hold(True)
            ax1.plot(dates2[i], values2[i], color = color_str2, label = ylabel + " xml-file-2", linewidth = 2, alpha = 0.6)
            
            # increase y axis to have text and legend show up better
            curr_ylim = ax1.get_ylim()
            ax1.set_ylim((curr_ylim[0], curr_ylim[1] * 1.5))
    
            # rotate and align the tick labels so they look better
            fig.autofmt_xdate()
            
            # use a more precise date string for the x axis locations in the
            # toolbar
            ax1.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
         
            # legend; make it transparent    
            handles1, labels1 = ax1.get_legend_handles_labels()
            legend1 = ax1.legend(handles1, labels1, fancybox = True)
            legend1.get_frame().set_alpha(0.5)
            legend1.draggable(state=True)
            
            # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
            text1 = "mean = %.2f\nmax = %.2f\nmin = %.2f\n---\nmean = %.2f\nmax = %.2f\nmin = %.2f" % (np.nanmean(values1[i]), np.nanmax(values1[i]), np.nanmin(values1[i]), np.nanmean(values2[i]), np.nanmax(values2[i]), np.nanmin(values2[i]))
            patch_properties = {"boxstyle": "round", "facecolor": "wheat", "alpha": 0.5}
                           
            ax1.text(0.05, 0.95, text1, transform = ax1.transAxes, fontsize = 14, 
                    verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)
 
            # plot difference = values_b - values_a
            ax2 = fig.add_subplot(212, sharex = ax1)
            ax2.grid(True)
            ax2.set_title('Difference: ' + timeseries_str)
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Difference' + ' (' + units1[i] + ')')
            diff = values2[i] - values1[i]
            ax2.plot(dates1[i], diff, color = 'k', linewidth = 2)  

            # increase y axis to have text and legend show up better
            curr_ylim2 = ax2.get_ylim()
            ax2.set_ylim((curr_ylim2[0], curr_ylim2[1] * 1.5))
            
            # use a more precise date string for the x axis locations in the toolbar
            ax2.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

            # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
            text2 = "mean = %.2f\nmax = %.2f\nmin = %.2f\n" % (np.nanmean(diff), np.nanmax(diff), np.nanmin(diff))
                           
            ax2.text(0.05, 0.95, text2, transform = ax2.transAxes, fontsize = 14, 
                    verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)
           
            # rotate and align the tick labels so they look better; note that ax2 will 
            # have the dates, but ax1 will not. do not need to rotate each individual axis
            # because this method does it
            fig.autofmt_xdate()
           
            # save plots
            if save_path:        
                # set the size of the figure to be saved
                curr_fig = plt.gcf()
                curr_fig.set_size_inches(12, 10)
                
                # split the parameter name to not include units because some units contain / character which Python interprets as an escape character
                filename = "-".join(["xml1", "vs", "xml2", timeseries_str, region_type1, sim_id1])  + ".png" 
         
                filepath = os.path.join(save_path, filename)
                plt.savefig(filepath, dpi = 100)                                          
                        
            # show plots
            if is_visible:
                plt.show()
            else:
                plt.close()

def _create_test_data():
    """ Create test data to use with tests """
    
    fixture = {}
    
    fixture["data_file"] = \
        """
        <Project>
            <ProjID>1</ProjID>
            <UserName>jlant</UserName>
            <DateCreated>2014-04-22T10:00:00.0000-00:00</DateCreated>
            <ProjName>my-project</ProjName>
            <Study>
                <StudyID>1</StudyID>
                <ProjID>1</ProjID>
                <StudyLocDecDeg>40.5, -75.9</StudyLocDecDeg>
                <StudyXLocation>1600000.0</StudyXLocation>
                <StudyYLocation>2100000.0</StudyYLocation>
                <StudyDescription>Test simulation</StudyDescription>
                <IsPointApproved>true</IsPointApproved>
                <IsDelineated>true</IsDelineated>
                <IsStudyApproved>true</IsStudyApproved>
                <StudySimulation>
                    <SimulID>1</SimulID>
                    <StudyID>1</StudyID>
                    <RegionType>4</RegionType>
                    <isInitialized>true</isInitialized>
                    <isLoaded>true</isLoaded>
                    <isCompleted>false</isCompleted>
                    <SimulationFeatures>
                        <AttID>1</AttID>
                        <SimulID>1</SimulID>
                        <AttName>Study Unit Total Area</AttName>
                        <AttCode>1</AttCode>
                        <AttMeanVal>100.0</AttMeanVal>
                        <AttMinVal>90.0</AttMinVal>
                        <AttMaxVal>110.0</AttMaxVal>
                        <AttstdDev>0</AttstdDev>
                        <AttDescription> Study unit total area</AttDescription>
                        <AttUnitsCode>303</AttUnitsCode>
                        <AttUnits>(sq Km)</AttUnits>
                    </SimulationFeatures>
                    <SimulationFeatures>
                        <AttID>2</AttID>
                        <SimulID>1</SimulID>
                        <AttName>Total Estimated Stream Area</AttName>
                        <AttCode>37</AttCode>
                        <AttMeanVal>5</AttMeanVal>
                        <AttMinVal>4</AttMinVal>
                        <AttMaxVal>6</AttMaxVal>
                        <AttstdDev>0</AttstdDev>
                        <AttDescription>Estimated area of stream coverage</AttDescription>
                        <AttUnitsCode>303</AttUnitsCode>
                        <AttUnits>(sq Km)</AttUnits>
                    </SimulationFeatures>
                    <SimulationTopographicWetnessIndex>                        
                        <BinID>1</BinID>
                        <SimulID>1</SimulID>
                        <BinValueMean>3.1</BinValueMean>
                        <BinValueFraction>0.002</BinValueFraction>                    
                    </SimulationTopographicWetnessIndex>
                    <SimulationTopographicWetnessIndex>                        
                        <BinID>2</BinID>
                        <SimulID>1</SimulID>
                        <BinValueMean>4.2</BinValueMean>
                        <BinValueFraction>0.005</BinValueFraction>                    
                    </SimulationTopographicWetnessIndex>
                    <StudyUnitDischargeSeries>                        
                        <SeriesID>1</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-01T00:00:00-05:00</SeriesDate>
                        <SeriesValue>100.0</SeriesValue>
                        <SeriesUnitsCode>54</SeriesUnitsCode>
                        <SeriesUnit>mm per day</SeriesUnit>                    
                    </StudyUnitDischargeSeries>
                    <StudyUnitDischargeSeries>                        
                        <SeriesID>2</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-02T00:00:00-05:00</SeriesDate>
                        <SeriesValue>110.0</SeriesValue>
                        <SeriesUnitsCode>54</SeriesUnitsCode>
                        <SeriesUnit>mm per day</SeriesUnit>                    
                    </StudyUnitDischargeSeries>
                    <ClimaticPrecipitationSeries>                        
                        <SeriesID>1</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-01T00:00:00-05:00</SeriesDate>
                        <SeriesValue>3.0</SeriesValue>
                        <SeriesUnitsCode>4</SeriesUnitsCode>
                        <SeriesUnit>mm</SeriesUnit>                    
                    </ClimaticPrecipitationSeries>
                    <ClimaticPrecipitationSeries>                        
                        <SeriesID>2</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-02T00:00:00-05:00</SeriesDate>
                        <SeriesValue>4.5</SeriesValue>
                        <SeriesUnitsCode>4</SeriesUnitsCode>
                        <SeriesUnit>mm</SeriesUnit>                    
                    </ClimaticPrecipitationSeries>
                    <ClimaticTemperatureSeries>                        
                        <SeriesID>1</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-01T00:00:00-05:00</SeriesDate>
                        <SeriesValue>11.1</SeriesValue>
                        <SeriesUnitsCode>31</SeriesUnitsCode>
                        <SeriesUnit>Celsius</SeriesUnit>                    
                    </ClimaticTemperatureSeries>
                    <ClimaticTemperatureSeries>                        
                        <SeriesID>2</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-02T00:00:00-05:00</SeriesDate>
                        <SeriesValue>12.2</SeriesValue>
                        <SeriesUnitsCode>31</SeriesUnitsCode>
                        <SeriesUnit>Celsius</SeriesUnit>                    
                    </ClimaticTemperatureSeries>
                </StudySimulation>             
            </Study>
        </Project>
        """
       
    fileobj = StringIO(fixture["data_file"])
    
    xml_tree = waterxml.read_file(fileobj)  

    return xml_tree    

def _create_test_data2():
    """ Create test data to use with tests """
    
    fixture = {}
    
    fixture["data_file"] = \
        """
        <Project>
            <ProjID>1</ProjID>
            <UserName>jlant</UserName>
            <DateCreated>2014-04-22T10:00:00.0000-00:00</DateCreated>
            <ProjName>my-project2</ProjName>
            <Study>
                <StudyID>1</StudyID>
                <ProjID>1</ProjID>
                <StudyLocDecDeg>40.5, -75.9</StudyLocDecDeg>
                <StudyXLocation>1600000.0</StudyXLocation>
                <StudyYLocation>2100000.0</StudyYLocation>
                <StudyDescription>Test simulation</StudyDescription>
                <IsPointApproved>true</IsPointApproved>
                <IsDelineated>true</IsDelineated>
                <IsStudyApproved>true</IsStudyApproved>
                <StudySimulation>
                    <SimulID>1</SimulID>
                    <StudyID>1</StudyID>
                    <RegionType>4</RegionType>
                    <isInitialized>true</isInitialized>
                    <isLoaded>true</isLoaded>
                    <isCompleted>false</isCompleted>
                    <SimulationFeatures>
                        <AttID>1</AttID>
                        <SimulID>1</SimulID>
                        <AttName>Study Unit Total Area</AttName>
                        <AttCode>1</AttCode>
                        <AttMeanVal>100.0</AttMeanVal>
                        <AttMinVal>90.0</AttMinVal>
                        <AttMaxVal>110.0</AttMaxVal>
                        <AttstdDev>0</AttstdDev>
                        <AttDescription> Study unit total area</AttDescription>
                        <AttUnitsCode>303</AttUnitsCode>
                        <AttUnits>(sq Km)</AttUnits>
                    </SimulationFeatures>
                    <SimulationFeatures>
                        <AttID>2</AttID>
                        <SimulID>1</SimulID>
                        <AttName>Total Estimated Stream Area</AttName>
                        <AttCode>37</AttCode>
                        <AttMeanVal>5</AttMeanVal>
                        <AttMinVal>4</AttMinVal>
                        <AttMaxVal>6</AttMaxVal>
                        <AttstdDev>0</AttstdDev>
                        <AttDescription>Estimated area of stream coverage</AttDescription>
                        <AttUnitsCode>303</AttUnitsCode>
                        <AttUnits>(sq Km)</AttUnits>
                    </SimulationFeatures>
                    <SimulationTopographicWetnessIndex>                        
                        <BinID>1</BinID>
                        <SimulID>1</SimulID>
                        <BinValueMean>3.1</BinValueMean>
                        <BinValueFraction>0.002</BinValueFraction>                    
                    </SimulationTopographicWetnessIndex>
                    <SimulationTopographicWetnessIndex>                        
                        <BinID>2</BinID>
                        <SimulID>1</SimulID>
                        <BinValueMean>4.2</BinValueMean>
                        <BinValueFraction>0.005</BinValueFraction>                    
                    </SimulationTopographicWetnessIndex>
                    <StudyUnitDischargeSeries>                        
                        <SeriesID>1</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-01T00:00:00-05:00</SeriesDate>
                        <SeriesValue>200.0</SeriesValue>
                        <SeriesUnitsCode>54</SeriesUnitsCode>
                        <SeriesUnit>mm per day</SeriesUnit>                    
                    </StudyUnitDischargeSeries>
                    <StudyUnitDischargeSeries>                        
                        <SeriesID>2</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-02T00:00:00-05:00</SeriesDate>
                        <SeriesValue>210.0</SeriesValue>
                        <SeriesUnitsCode>54</SeriesUnitsCode>
                        <SeriesUnit>mm per day</SeriesUnit>                    
                    </StudyUnitDischargeSeries>
                    <ClimaticPrecipitationSeries>                        
                        <SeriesID>1</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-01T00:00:00-05:00</SeriesDate>
                        <SeriesValue>6.0</SeriesValue>
                        <SeriesUnitsCode>4</SeriesUnitsCode>
                        <SeriesUnit>mm</SeriesUnit>                    
                    </ClimaticPrecipitationSeries>
                    <ClimaticPrecipitationSeries>                        
                        <SeriesID>2</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-02T00:00:00-05:00</SeriesDate>
                        <SeriesValue>9</SeriesValue>
                        <SeriesUnitsCode>4</SeriesUnitsCode>
                        <SeriesUnit>mm</SeriesUnit>                    
                    </ClimaticPrecipitationSeries>
                    <ClimaticTemperatureSeries>                        
                        <SeriesID>1</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-01T00:00:00-05:00</SeriesDate>
                        <SeriesValue>22.2</SeriesValue>
                        <SeriesUnitsCode>31</SeriesUnitsCode>
                        <SeriesUnit>Celsius</SeriesUnit>                    
                    </ClimaticTemperatureSeries>
                    <ClimaticTemperatureSeries>                        
                        <SeriesID>2</SeriesID>
                        <SimulID>1</SimulID>
                        <SeriesDate>2014-01-02T00:00:00-05:00</SeriesDate>
                        <SeriesValue>24.4</SeriesValue>
                        <SeriesUnitsCode>31</SeriesUnitsCode>
                        <SeriesUnit>Celsius</SeriesUnit>                    
                    </ClimaticTemperatureSeries>
                </StudySimulation>             
            </Study>
        </Project>
        """
       
    fileobj = StringIO(fixture["data_file"])
    
    xml_tree = waterxml.read_file(fileobj)  

    return xml_tree  


def test_print_waterxml_data():
    """ Test print_waterxml_data() """
    
    print("--- print_waterxml_data() ---")     

    xml_tree = _create_test_data()
    print_waterxml_data(waterxml_tree = xml_tree)

def test_plot_waterxml_timeseries_data():
    """ Test plot_waterxml_timeseries_data """
    
    print("--- plot_waterxml_timeseries_data() ---")     

    xml_tree = _create_test_data()
    plot_waterxml_timeseries_data(waterxml_tree = xml_tree, is_visible = True, save_path = None)    

def test_plot_waterxml_topographic_wetness_index_data():
    """ Test plot_waterxml_topographic_wetness_index_data() """
    
    print("--- plot_waterxml_topographic_wetness_index_data() ---")     

    xml_tree = _create_test_data()
    plot_waterxml_topographic_wetness_index_data(waterxml_tree = xml_tree, is_visible = True, save_path = None) 

def test_plot_waterxml_timeseries_comparison():
    """ Test plot_waterxml_timeseries_comparison functionality() """
    
    print("--- Testing plot_waterxml_timeseries_comparison_comprison() ---")    
    
    waterxml_tree1 = _create_test_data()
    waterxml_tree2 = _create_test_data2()
    plot_waterxml_timeseries_comparison(waterxml_tree1, waterxml_tree2, is_visible = True, save_path = None)
    
    print("Plotting completed")
    print("")


def main():
    """ Test functionality of waterxml_viewer() """

    print("")
    print("RUNNING TESTS ...")
    print("")

    test_print_waterxml_data()

    test_plot_waterxml_timeseries_data()
    
    test_plot_waterxml_topographic_wetness_index_data()    

    test_plot_waterxml_timeseries_comparison()

    
if __name__ == "__main__":
    main() 