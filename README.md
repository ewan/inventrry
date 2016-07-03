#inventrry

install.packages("PythonInR", type="source")
install_name_tool -change "/System/Library/Frameworks/Python.framework/Versions/2.7/Python" "/Users/emd/anaconda/lib/libpython2.7.dylib" /Library/Frameworks/R.framework/Versions/3.2/Resources/library/PythonInR/libs/PythonInR.so
Sys.setenv(PYTHONHOME="/Users/emd/anaconda")