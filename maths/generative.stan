data {
  int<lower=2> N;
  /* real t; */
  real<lower=0> alpha_t;
  real<lower=0> alpha_p;
  real<lower=0> beta_t;
  real<lower=0> beta_p;
  int k[N];
}

parameters {
  real<lower=0, upper=1> t;
  real<lower=0, upper=1> p;
}

model {
  /* alpha_1 ~ gamma(10,10); */
  /* beta_1 ~ gamma(10,10); */
  /* alpha_2 ~ gamma(10,10); */
  /* beta_2 ~ gamma(10,10); */
  t ~ beta(alpha_t, beta_t);
  /* t ~ beta(2,10); */
  p ~ beta(alpha_p, beta_p);
  p ~ beta(2,2);
  k ~ binomial(N, t*p);
}
