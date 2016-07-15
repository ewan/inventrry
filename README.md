#inventrry

R package for calculating geometry statistics of sound inventories (or in fact any set that comes with a binary encoding.

###Setup

This package calls Python code using the PythonInR package. On Unix systems, PythonInR will by default be linked to whatever libpython it finds first (i.e., the default Python installation). If you're not using your default Python installation, you may have to recompile PythonInR from source, so that the shared object file that's generated won't link to the wrong version of libpython.

If you're on a Mac, even that isn't enough, because (as far as I can see) the linker will stubbornly refuse to include absolute paths, and `dyn.load` in R (which does the loading of the PythonInR shared object) will ignore all the ordinary environment variables to set the dynamic library paths. You'll need to modify the contents of the shared object file after it's linked. For example, on my system:

    install.packages("PythonInR", type="source")
    install_name_tool -change "/System/Library/Frameworks/Python.framework/Versions/2.7/Python" "/Users/emd/anaconda/lib/libpython2.7.dylib" /Library/Frameworks/R.framework/Versions/3.2/Resources/library/PythonInR/libs/PythonInR.so 
Where the first argument is the original reference spit out by the linker (which you can see using `otool -g`), the second argument is what I need to change it to, and the third argument is the location of the installed shared object file.

It is then *absolutely essential* that, before running anything with PythonInR, you set the PYTHONHOME environment variable to the folder containing the version of Python you're using.

    Sys.setenv(PYTHONHOME="/Users/emd/anaconda")

Otherwise, R will crash.