#'@export
feature_matrix <- function(feat, contains_weird_things=F) {
  feat_v <- unlist(feat)
  if (contains_weird_things) {
    feat_chr <- sort(c("-", "0", "+", sort(unique(feat_v))))
    feat_chr_to_num <- 1:length(feat_chr) - 2    
  } else {
    feat_chr <- c("-", "0", "+")
    feat_chr_to_num <- c(-1, 0, 1)
  }
  names(feat_chr_to_num) <- feat_chr
  result <- feat_chr_to_num[feat_v]
  dim(result) <- c(nrow(feat), ncol(feat))
  colnames(result) <- colnames(feat)
  return(result)
}