functions {
  real u(real c, real rho) {
    return ((c+1)^(1/(1 - rho)) - 1)/(1 - rho);
  }
}

data {
  int<lower=2> M; // participants
  real penalty;
  /* real sd_cost_shape; */
  /* real sd_cost_scale; */
  real sd_epsilon_shape;
  real sd_epsilon_scale;
  real sd_rho_shape;
  real sd_rho_scale;
  real mean_rho_nu;
  real mean_epsilon_nu;
  /* real mean_cost_nu; */
  real mean_cost;
  real sd_cost;
  real lower_rho;
  real upper_rho;
  /* real mean_cost_center; */
  int fraction;
  int N[M]; // rolls
  int G[M]; // group assignment
  real prize[M];
  real roll_time[M];
}

parameters {
  /* real<lower=0> mean_cost; */
  /* real<lower=0> sd_cost; */
  real<lower=0> cost[M];
  /* real<lower=lower_rho, upper=upper_rho> mean_rho; */
  /* real<lower=0> sd_rho; */
  /* real<lower=lower_rho, upper=upper_rho> rho[M]; */
  /* real<lower=0> cost; */
  real<lower=0> sd_epsilon;
  real<lower=0> mean_epsilon[2];
  real<lower=0> epsilon[M];
}

model {
  for (m in 1:M) {
    real dif;
    real p;
    real t;
    real W;
    real c;
    t = roll_time[m];
    W = prize[m];
    c = cost[m];
    /* mean_cost ~ cauchy(mean_cost_center, mean_cost_nu); */
    /* sd_cost ~ inv_gamma(sd_cost_shape, sd_cost_scale); */
    c * fraction ~ double_exponential(mean_cost, sd_cost);
    /* cost * fraction ~ cauchy(mean_cost_center, mean_cost_nu); */

    /* mean_rho ~ normal(1, mean_rho_nu); */
    /* sd_rho ~ inv_gamma(sd_rho_shape, sd_rho_scale); */
    /* rho[m] ~ normal(mean_rho, sd_rho); */

    mean_epsilon[G[m]] ~ cauchy(0, mean_epsilon_nu);
    sd_epsilon ~ inv_gamma(sd_epsilon_shape, sd_epsilon_scale);
    epsilon[m] ~ normal(mean_epsilon[G[m]], sd_epsilon);

    p = 1/(1 + N[m] * (1 + epsilon[m]));
    p*W/(c*t) ~ lognormal(0, 1/penalty); // linear case

    /* p * u(W, rho[m]) / u(c*t, rho[m]) ~ lognormal(0, 1/penalty); */
    /* target += -penalty * (dif * dif); */

    // add log absolute derivatives of rho...
    /* target += log(fabs( */
    /*                    -log(W)*W^(1- rho[m]) / ((1-rho[m]) * (c*t)^(1-rho[m])) - */
    /*                    W^(1-rho[m]) * (1-rho[m]) / (u(c*t, rho[m]))^2 * (-log(c*t) * (c*t)^(1-rho[m])) */
    /*                     )); */

    // log absolute derivate of cost
    /* target += log(fabs( -W^(1-rho[m])/(1-rho[m]) * u(c*t, rho[m])^(-2) * (c*t)^(-rho[m]) )); */
  }
}

generated quantities {
  real dif[M];
  real p[M];
  for (m in 1:M) {
    p[m] = 1/(1 + N[m] * (1 + epsilon[m]));
    dif[m] = p[m]*prize[m]/(cost[m]*roll_time[m]);
    /* dif[m] = log(p[m] * u(prize[m], rho[m]) / u(cost[m]*roll_time[m], rho[m])); */
  }

}
