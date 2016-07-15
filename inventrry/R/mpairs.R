#'@export
mpairs <- function(inventory, spec, feature) {
  PythonInR::pySet("inventory", inventory)
  if (is.character(spec) | is.character(feature)) {
    PythonInR::pySet("fnames", colnames(inventory))
  }
  if (is.character(spec)) {
    PythonInR::pySet("spec_c", spec)
    PythonInR::pySet("k", length(colnames(inventory)))
    PythonInR::pyExec("spec = [i for i in range(k) if fnames.x[i] in spec_c.x]")
  } else {
    PythonInR::pySet("spec", spec)
  }
  if (is.character(feature)) {
    PythonInR::pySet("feature_c", feature)
    PythonInR::pyExec("feature = fnames.x.index(feature_c)")
  } else {
    PythonInR::pySet("feature", feature)
  }
  m <- PythonInR::pyExecg("m = mpairs.mpairs(inventory, spec, feature)")[["m"]]
  return(m)
}

#'@export
nmpairs <- function(inventory, spec) {
  spec_i <- as.list(match(spec, colnames(inventory)) - 1)
  return(sum(unlist(lapply(
    spec_i,
    function(i) mpairs(inventory, spec_i, i)
  ))))
}
