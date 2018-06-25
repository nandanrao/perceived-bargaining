library(rstan)
library(dplyr)
rstan_options(auto_write = TRUE)
options(mc.cores = parallel::detectCores())

d <- read.csv('distortion.csv')

model <- stan_model("distortion.stan")


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




model.grouped <- stan_model("distortion-grouped.stan")

d <- d %>% mutate(prize = 500)

data <- list(
    penalty = 1000,
    sd_cost_shape = 10,
    sd_cost_scale = 1,
    sd_epsilon_shape = 2,
    sd_epsilon_scale = 2,
    rho_shape = 3,
    rho_scale = 1,
    mean_epsilon_nu = 5,
    mean_cost_nu = 5,
    mean_cost_center = 0,
    fraction = 10,
    M = nrow(d),
    N = d$rolls,
    G = d$group,
    roll_time = d$roll_time,
    prize = d$prize
)

vb(model.grouped, data)

s <- sampling(model.grouped, data)

o <- optimizing(model.grouped, data)

library(tidyr)
eps.sampled <- data.frame(rstan::extract(s, pars = c('mean_epsilon')))
gather(eps.sampled) %>% ggplot(aes(x = value, color = key)) + geom_density()


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
