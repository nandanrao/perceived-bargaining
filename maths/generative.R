library(rstan)
rstan_options(auto_write = TRUE)
options(mc.cores = parallel::detectCores())

data <- list(
    N = 10,
    k = rep(0, 10),
    t = 0.06
)

model <- stan("generative.stan", data=data)
