.onLoad <- function(libname, pkgname) {
  python_dir <- file.path(libname, pkgname, "python")
  PythonInR::pyCall("sys.path.append", python_dir)
  PythonInR::pyImport("numpy", as="np")
  PythonInR::pyOptions("useNumpy", TRUE)
  PythonInR::pyOptions("numpyAlias", "np")
  tryCatch(
    {
      PythonInR::pyImport("specs")
      PythonInR::pyImport("mpairs")
      PythonInR::pyImport("imbalance")
    },
    error=function(e) warning("Error loading Python module: nothing will work", call.=F)
  )
}