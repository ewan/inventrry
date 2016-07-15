#'@export
imbalance <- function(feature_values) {
  PythonInR::pySet("feature_values_pr", feature_values)
  PythonInR::pyExec("feature_values = np.array(feature_values_pr.x)")
  m <- PythonInR::pyExecg("m = imbalance.imbalance(feature_values)")[["m"]]
  return(m)
}

#'@export
nimbalance <- function(inventory, spec) {
  spec_i <- match(spec, colnames(inventory))
  return(sum(unlist(lapply(
    spec_i,
    function(i) imbalance(inventory[,i])
  ))))
}
