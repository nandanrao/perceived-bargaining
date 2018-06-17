data {
  /* int<lower=2> N; // fails */
  int<lower=2> M; // participants
  real scale_eps;
  real cost_sd;
  real mean_cost_nu;
  int fraction;
  int N[M]; // rolls
  real roll_cost[M];
}

parameters {
  /* real<lower=0, upper=1> p; */
  real<lower=0, upper=1> p[M];
  real<lower=0> cost[M];
  real<lower=0> mean_cost;
  /* real<lower=0> sd_cost; */
  /* real<lower=0> scale_cost; */
  real<lower=0> epsilon[M];
}

model {
  /* alpha_1 ~ gamma(10,10); */
  /* beta_1 ~ gamma(10,10); */
  /* alpha_2 ~ gamma(10,10); */
  /* beta_2 ~ gamma(10,10); */
  /* t ~ beta(2,10); */
  /* sigma_e ~ invgamma(10, 10) */

  for (m in 1:M) {
    real dif;
    real p_distorted;
    real cost_fractions;

    mean_cost ~ cauchy(0, mean_cost_nu);
    cost[m] ~ normal(mean_cost, cost_sd);
    cost_fractions = cost[m] / fraction;

    // learn two epsilons: one for each group!

    epsilon[m] ~ cauchy(0, scale_eps);


    p[m] ~ beta(1, 1 + (N[m] * (1 + epsilon[m])));

    dif = roll_cost[m] - ( p[m] / cost_fractions );
    target += -(dif * dif);
  }
}
