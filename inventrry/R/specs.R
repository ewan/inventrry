#'@export
specs <- function(feat, max_cost=Inf, seed=NULL) {
  PythonInR::pySet("feat", feat)
  PythonInR::pySet("max_cost", max_cost)
  PythonInR::pySet("seed", seed)
  result <- PythonInR::pyExecg("result = specs.specs(feat, max_cost, seed)")
  return(result)
}
