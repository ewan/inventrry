.onLoad <- function(libname, pkgname) {
  python_dir <- file.path(libname, pkgname, "python")
  PythonInR::pyCall("sys.path.append", python_dir)
  PythonInR::pyImport("pandas", as="pd")
  PythonInR::pyImport("numpy", as="np")
  PythonInR::pyOptions("useNumpy", TRUE)
  PythonInR::pyOptions("numpyAlias", "np")
  PythonInR::pyOptions("usePandas", TRUE)
  PythonInR::pyOptions("pandasAlias", "pd")
  tryCatch(
    PythonInR::pyImport("specs"),
    error=function(e) warning("Error loading Python module: nothing will work", call.=F)
  )
}