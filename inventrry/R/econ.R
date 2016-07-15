#'@export
econ <- function(n, k) {
  result <- rep(NA, length(n))
  result[(k >= 1) & (k > (n-1))] <- -Inf
  result[(k >= 1) & (k <= (n-1) & n > 2^k)] <- Inf
  result[(k == 1) & (n == 2)] <- 0.5
  rest <- (k != 1 | n != 2) & (k <= (n-1)) & (n <= 2^k)
  result[rest] <- (n[rest]-(k[rest]+1))/(2^k[rest]-(k[rest]+1))
  return(result)
}