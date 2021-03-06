functions {
  real posterior(real pH, real t, real eps) {
    return (pH - t*pH) / (1 - t*pH) * (1 - eps);
  }
}

data {
  int<lower=2> M; // participants
  real scale_eps;
  real cost_sd;
  real mean_cost_nu;
  real t_beta;
  int fraction;
  int N[M]; // rolls
  int G[M]; // group assignment
  real roll_cost[M];
}

parameters {
  /* int<lower=0, upper=1> a[M]; */
  real<lower=0, upper=1> t[M];
  real<lower=0> cost[M];
  real<lower=0> mean_cost;
  real<lower=0, upper=1> epsilon[2];
}

model {
  for (m in 1:M) {
    real dif;
    real cost_fractions;
    real pH;
    int a;
    // COST
    mean_cost ~ cauchy(0, mean_cost_nu);
    cost[m] ~ normal(mean_cost, cost_sd);
    cost_fractions = cost[m] / fraction;

    epsilon[G[m]] ~ cauchy(0, scale_eps);

    t[m] ~ beta(1,t_beta);

    pH = 0.5;
    for (n in 1:N[m]) {
      pH = posterior(pH, t[m], epsilon[G[m]]);
    }
    print(pH)
    // pH iteration...
    a[m] ~ bernoulli(pH);
    0 ~ binomial(N[m], t[m]*a);

    dif = roll_cost[m] - ( pH*t[m] / cost_fractions );
    target += -(dif * dif);
  }
}
