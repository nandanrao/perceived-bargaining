data {
  /* int<lower=2> N; // fails */
  int<lower=2> M; // participants
  real cost_alpha;
  real cost_beta;
  int N[M]; // rolls
  real roll_cost[M];
}

parameters {
  /* real<lower=0, upper=1> p; */
  real<lower=0, upper=1> p[M];
  real<lower=0> cost[M];
  /* real<lower=0, upper=1> epsilon[M]; */
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
    /* real p_distorted; */

    cost[m] ~ gamma(cost_alpha, cost_beta);

    /* epsilon[m] ~ beta(2,2); */

    p[m] ~ beta(2, 2);

    /* p_distorted = p[m] * epsilon[m]; */

    0 ~ binomial(N[m], p[m]);

    dif = roll_cost[m] - (p[m] / cost[m]);
    target += log(dif * dif);
  }
}
