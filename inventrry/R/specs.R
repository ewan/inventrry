#'@export
specs <- function(feat, max_cost=Inf, seed=NULL) {
  PythonInR::pySet("feat", feat)
  PythonInR::pySet("max_cost", max_cost)
  PythonInR::pySet("seed", seed)
  PythonInR::pyExec("l = specs.specs(feat, max_cost, seed)")
  l <- PythonInR::pyGet("l", simplify=F)
  if (length(l) > 0) {
    l <- PythonInR::pyGet("l", simplify=T)
  }
  fnames <- colnames(feat)
  result <- lapply(l, function(x) fnames[x+1])
  return(result)
}

#'@export
spec_list <- function(m, fnames) {
  result <- apply(m, 1, function(x) fnames[x])
  if (is.matrix(result)) {
    # R has simplified because all specifications had same number of features
    result <- split(result, col(result))
    names(result) <- c()
  }
  if (is.vector(result)) {
    # R has simplified even further because all specifications had 1 feature
    result <- as.list(result)
  }
  return(result)
}

#'@export
spec_matrix <- function(l, fnames) {
  result <- t(vapply(l, function(x) fnames %in% x, fnames %in% fnames))
  colnames(result) <- fnames
  return(result)
}