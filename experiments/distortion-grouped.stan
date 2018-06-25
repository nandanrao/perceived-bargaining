data {
  /* int<lower=2> N; // fails */
  int<lower=2> M; // participants
  real penalty;
  real sd_cost_shape;
  real sd_cost_scale;
  real sd_epsilon_shape;
  real sd_epsilon_scale;
  real rho_shape;
  real rho_scale;
  real mean_epsilon_nu;
  real mean_cost_nu;
  real mean_cost_center;
  int fraction;
  int N[M]; // rolls
  int G[M]; // group assignment
  real prize[M];
  real roll_time[M];
}

parameters {
  real<lower=0> mean_cost;
  real<lower=0> sd_cost;
  real<lower=0> rho;
  real<lower=0> cost[M];
  real<lower=0> sd_epsilon[2];
  real<lower=0> mean_epsilon[2];
  real<lower=0> epsilon[M];
  /* real<lower=0, upper=1> p[M]; */
}

model {
  for (m in 1:M) {
    real dif;
    real cost_fractions;
    real p;

    mean_cost ~ cauchy(mean_cost_center, mean_cost_nu);
    sd_cost ~ inv_gamma(sd_cost_shape, sd_cost_scale);

    rho ~ gamma(rho_shape, rho_scale);

    cost[m] * fraction ~ normal(mean_cost, sd_cost);

    sd_epsilon[G[m]] ~ inv_gamma(sd_epsilon_shape, sd_epsilon_scale);
    mean_epsilon[G[m]] ~ cauchy(0, mean_epsilon_nu);
    epsilon[m] ~ normal(mean_epsilon[G[m]], sd_epsilon[G[m]]);

    /* p[m] ~ beta(1, 1 + (N[m] * (1 + epsilon[m]))); */
    p = 1/(1 + N[m] * (1 + epsilon[m]));

    dif = roll_time[m]*cost[m] - (p*prize[m]^(1-rho) - p + 1)^(1/(1 - rho));
    /* dif = prize[m]^p - roll_time[m]*cost_fractions; */
    /* dif = (roll_time[m]/prize[m]) - ( p^(1/(1-rho)) / cost[m] ); */
    /* dif = (roll_time[m]/prize[m]) - ( p / cost[m] ); */

    target += -penalty * (dif * dif);
  }
}
