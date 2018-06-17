library(rstan)
rstan_options(auto_write = TRUE)
options(mc.cores = parallel::detectCores())

d <- read.csv('distortion.csv')

model <- stan_model("distortion.stan")

model.grouped <- stan_model("distortion-grouped.stan")

model.linear <- stan_model("distortion-linear.stan")

data <- list(
    scale_eps = 5,
    cost_sd = 1,
    t = d$t,
    mean_cost_nu= 5,
    fraction = 1000,
    M = nrow(d),
    N = d$rolls,
    G = d$group,
    roll_cost = d$roll_cost
)

m <- vb(model.linear, data)

s <- sampling(model.linear, data)


data <- list(
    scale_eps = 5,
    cost_sd = 1,
    mean_cost_nu = 5,
    fraction = 1000,
    M = nrow(d),
    N = d$rolls,
    G = d$group,
    roll_cost = d$roll_cost
)

s <- sampling(model.grouped, data)

vb(model.grouped, data)

model.joint <- stan_model("distortion-joint.stan")

data <- list(
    scale_eps = 5,
    cost_sd = 1,
    mean_cost_nu = 5,
    t_beta = 3,
    fraction = 1000,
    M = nrow(d),
    N = d$rolls,
    G = d$group,
    roll_cost = d$roll_cost
)

m <- vb(model.joint, data)

## model.nodistortion <- stan_model("distortion.stan")
## vb(model.nodistortion, data)in
