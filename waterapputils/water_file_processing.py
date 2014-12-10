def process_water_files(file_list, arguments):
    """    
    Process a list of WATER xml files according to options contained in arguments parameter.

    Parameters
    ----------
    file_list : list 
        List of files to parse, process, and plot.        
    arguments : argparse object
        An argparse object containing user options.                    
    """ 

    for f in file_list:
        
        ext = os.path.splitext(f)[1]       
        assert ext == ".txt" or ext == ".xml", "Can not process file {}. File extension {} is not .txt or .xml".format(f, ext)
        
        filedir, filename = helpers.get_file_info(f)       
 
        print("Processing: \n    {}\n".format(f))

        if ext == ".txt":
            outputdirpath = helpers.make_directory(path = filedir, directory_name = WATERTXT_DIRNAME)
            waterapputils_logging.initialize_loggers(output_dir = outputdirpath) 
            data = watertxt.read_file(f)                           
            watertxt_viewer.plot_watertxt_data(data, is_visible = arguments.showplot, save_path = outputdirpath)
            if arguments.verbose: 
                watertxt_viewer.print_watertxt_data(data) 
            print("Output: \n    {}\n\n".format(outputdirpath))
                
        elif ext == ".xml":
            outputdirpath = helpers.make_directory(path = filedir, directory_name = WATERXML_DIRNAME)
            waterapputils_logging.initialize_loggers(output_dir = outputdirpath) 
            data = waterxml.read_file(f)                           
            waterxml_viewer.plot_waterxml_timeseries_data(data, is_visible = arguments.showplot, save_path = outputdirpath)             
            waterxml_viewer.plot_waterxml_topographic_wetness_index_data(data, is_visible = arguments.showplot, save_path = outputdirpath) 
            if arguments.verbose: 
                waterxml_viewer.print_waterxml_data(data)  
            print("Output: \n    {}\n\n".format(outputdirpath))

        waterapputils_logging.remove_loggers()

def process_cmp(file_list, arguments):
    """
    Compare two WATER text files according to options contained in arguments parameter.

    Parameters
    ----------
    file_list : list 
        List of files to parse, process, and plot.        
    arguments : argparse object
        An argparse object containing user options.    
    """

    water_file1 = file_list[0]
    water_file2 = file_list[1]

    filedir1, filename1 = helpers.get_file_info(water_file1)
    filedir2, filename2 = helpers.get_file_info(water_file2)

    ext1 = os.path.splitext(filename1)[1]
    ext2 = os.path.splitext(filename2)[1]

    assert ext1 == ".txt" or ext1 == ".xml", "Can not process file {}. File extension {} is not .txt or .xml".format(filename1, ext1)
    assert ext2 == ".txt" or ext2 == ".xml", "Can not process file {}. File extension {} is not .txt or .xml".format(filename2, ext2)

    print("Processing: \n    {}\n    {}".format(water_file1, water_file2))

    if ext1 == ".txt" and ext2 == ".txt":
        outputdirpath = helpers.make_directory(path = filedir1, directory_name = WATERTXT_DIRNAME)
        waterapputils_logging.initialize_loggers(output_dir = outputdirpath) 
        watertxt_data1 = watertxt.read_file(water_file1)  
        watertxt_data2 = watertxt.read_file(water_file2)         
        watertxt_viewer.plot_watertxt_comparison(watertxt_data1, watertxt_data2, is_visible = arguments.showplot, save_path = outputdirpath)         
        
        if arguments.verbose: 
            watertxt_viewer.print_watertxt_data(watertxt_data1)  
            watertxt_viewer.print_watertxt_data(watertxt_data2)   
        
        print("Output: \n    {}".format(outputdirpath))

    elif ext1 == ".xml" and ext2 == ".xml":
        outputdirpath = helpers.make_directory(path = filedir1, directory_name = WATERXML_DIRNAME)
        waterapputils_logging.initialize_loggers(output_dir = outputdirpath) 
        waterxml_data1 = waterxml.read_file(water_file1)  
        waterxml_data2 = waterxml.read_file(water_file2)         
        waterxml_viewer.plot_waterxml_timeseries_comparison(waterxml_data1, waterxml_data2, is_visible = arguments.showplot, save_path = outputdirpath)         
        
        if arguments.verbose: 
            waterxml_viewer.print_watertxt_data(waterxml_data1)  
            waterxml_viewer.print_watertxt_data(waterxml_data2)   
        
        print("Output: \n    {}".format(outputdirpath))

    else:
        print("Can not process files {} and {}. File extensions {} and {} are not .txt or .xml".format(filename1, filename2, ext1, ext2))

    waterapputils_logging.remove_loggers()
