#'@export
norm_rank <- function(x, rev=F) {
  if (rev) {
    r <- findInterval(-x, sort(unique(-x)))
  } else {
    r <- findInterval(x, sort(unique(x)))
  }
  if (length(r) == 1) {
    return(NA)
  }
  return((r-min(r, na.rm=T))/(max(r, na.rm=T)-min(r, na.rm=T)))
}

