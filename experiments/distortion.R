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
    penalty = 100,
    mean_cost = 4.,
    sd_cost = 3.,
    sd_epsilon_shape = 2,
    sd_epsilon_scale = 2,
    lower_rho = 1,
    upper_rho = 4,
    sd_rho_shape = 6,
    sd_rho_scale = 1,
    mean_rho_nu = 1,
    mean_epsilon_nu = 5,
    fraction = 10,
    M = nrow(d),
    N = d$rolls,
    G = d$group,
    roll_time = d$roll_time,
    prize = d$prize
)

vb(model.grouped, data, elbo_samples = 1000)


s <- sampling(model.grouped, data, iter = 2000, control = list(adapt_delta = .8, max_treedepth = 10))

s <- sampling(model.grouped, data, iter = 4000, control = list(adapt_delta = .85, max_treedepth = 20))

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
