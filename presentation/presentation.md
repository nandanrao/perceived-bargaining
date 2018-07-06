slidenumbers: true
autoscale: true

# Numerocity Biases and the Perceived Chances of Getting a Job: Experimental Evidence and Implications for Directed Search

---

## Outline

* Background Idea
* Biases
* Experiment
* Equilibrium Model
* Conclusions

---

## Context

With the Internet:

* People apply to jobs faster.
* People apply to more jobs.
* The average person gets more rejections.
* More rejections, but more applications - chances of getting a job could be the same.
* How do job seekers handle this change?

---

## Research Question


Does an in the velocity of applications imply a corresponding increase in the bias of a job seeker's probability-of-success estimation?


---


## Ratio Bias

* Cookie Jar experiment (Miller et al 1989).
* Numerocity of numerator <> numerocity of rejections!

---

## Numerocity Heuristic

* Chickens and then humans, specifically under cognitive load (Pelham et al 1994).
* Numerocity works as estimation tool for quantity.

* Probability of getting each job vs. chances of getting a job.

---

## Learning by Experience

* Opposite effect from "learning by description" ala Prospect Theory (Hertwig et al 2004)
* Hertwig points out _undersampling_ in practice rounds.
* Does that imply a "snapping to zero" of low probability events?

---

# Turkeriment
---

## Turkeriment

MTurk:

* Task creators can specify the characteristics of those who perform their task.
* Turkers with similar qualifications have access to the same pool of jobs => same opportunity costs!
* They think about opportunity costs explicitly on a daily basis.
* [Websites with hourly equivalents](https://turkerview.com)

---

![](turkerview.png)

---

## Experimental Design


* Participants play a one-armed bandit.
* The game ends when they win or quit.
* 50% chance that their bandit pays out with probability 0.
* 50% chance that their bandit pays out with probability ???
* Group A: 3 seconds/play
* Group B: 12 seconds/play
* Participants who got lucky and won are excluded from the results.
* The question is: "how many losses do you experience before you quit trying?"

---

## Rational Response

True model:

$$
k_{n+1} \thicksim Bernouli( p )
$$

$$
p \equiv P(\gamma | n, a_H) P(a_H | n)
$$

Where $$a_H$$ denotes being in the "high skill" group, and $$\gamma$$ denotes the Bernouli payout probability of the bandit.

---

## Rational Response

* True model requires concurrent estimation of two different probabilities, not identifiable without further assumptions.

Simplify to the estimation of the posterior mean of $$p$$ directly:

$$
\hat{P}_n
$$

---

## Rational Response

Finite-horizon stopping time problem.

* No discounting.

* Think of it like the payment for one-days work.

$$
V(n) = \max \left\{ \mathbb{E}V_p(n), V_q(n)  \right\}
$$

---

## Rational Response

Where the value of quitting it given by:

$$
V_q(n) = u\left( \sum_n^T ct \right)
$$

With $$c$$ is the per-second wage of the outside option and $$t$$ is the number of seconds per round of play. The expected value of playing:

$$
\mathbb{E}V_p(n) = \hat{P}_n u(W + \sum_{n+1}^T ct) + (1 - \hat{P}_n) \mathbb{E}V(n+1)
$$

---

## Rational Response

Assume that in some $$n+1$$, $$V(n+1) = V_q(n+1)$$:

$$
\mathbb{E}V_p(n) = \hat{P}_n u(W + \sum_{n+1}^T ct) + (1 - \hat{P}_n)u\left( \sum_{n+1}^T ct \right)
$$

$$
\hat{P}_n \left[   u(W + \sum_{n+1}^T ct) - u\left( \sum_{n+1}^T ct \right) \right] = u\left( \sum_n^T ct \right) - u\left( \sum_{n+1}^T ct \right)
$$

---

## Rational Response

Letting $$u^m_{n}$$ denote the marginal utility of some consumption above and beyond $$\sum_{n}^T ct$$, we can write the stopping time conditions as follows:

$$
\hat{P}_{n} u^m_{n+1}(W) = u^m_{n+1}(ct)
$$

Use this for inference!

---

## Results


| | Group | N | t |  Time played | c | c | c |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | $$\rho = 2$$ | $$\rho = 1$$ | $$\rho = 0$$ |
| Median |         a | 29 |          4 |     240 |        0.0204 |                 0.0209 |                    2.1368  |
      |         b | 28 |         15 |     311 |               0.0138 |                 0.0141 |                    1.4448  |
      Mean |         a | 29 |          5 |  374 |          0.0348 |                 0.0356 |                    3.6450  |
       |         b | 28 |         17 |    400 |              0.0200 |                 0.0204 |                    2.0875  |
MW p | | | | | 0.084 | 0.084 | 0.078 |

Where t is roll time and c is opportunity cost in cents per second

---

## Equilibrium Model

---

## Equilibrium Model

How can biases of probability judgement affect the labor force on an aggregate level?

What effects can they have on unemployment and wage distributions across the labor market?

---

## Equilibrium Model

Searching for a model with:

* Agent(s) that direct their search towards specific "submarkets" of jobs with different wage characteristics.
* Agent(s) that do not know the objective probabilities of getting a job in any particular submarket, and must estimate these probabilities through a process of learning by experience.
* Agent(s) that can experience both rejection and success in searching for jobs, and update their beliefs accordingly.

---

## Equilibrium Model

"An equilibrium theory of learning, search, and wages" Gonzalez, Francisco M and Shi, Shouyong. Econometric 2010.

---

## Equilibrium Model

Ax-ante heterogeneity in skill:

$$
a_i \in \{ a_L, a_H \}
$$

Ax-ante homogeneity in beliefs about skill:

$$
\mu_0 = p a_H + (1-p) a_L
$$

Apply to submarket, $$x$$, by maximizing continuation value given beliefs:

$$
g(\mu)
$$

---

## Equilibrium Model

Posterior Updates:

$$
\phi(\mu) \equiv  a_H + a_L - a_Ha_L/\mu
$$

$$
H(x, \mu) \equiv a_H - (a_H - \mu)(1 - xa_L)/(1 - x\mu)
$$

Yields posterior mean after $$n = 2$$ failures:

$$
\hat{P}_2 \equiv H(g(H(g(\mu_0), \mu_0)), H(g(\mu_0),\mu_o))
$$

---

## Equilibrium Model



---

## Calibration

---

## Calibration

Opportunity cost of worker i is estimated with a prior:

$$
c_i \sim \text{DoubleExponential}(\mu^c, \sigma^c)
$$

Where $$\mu^c$$ and $$\sigma^c$$ are estimated by:

* Scraping the wages from the top 50 reviews of each worker who reviewed these experiments on Turkerview.
* Estimating the parameters by minimizing KL-divergence.

---

## Calibration

![inline](../experiments/turker-wages.pdf)

---
## Calibration

Updating is assumed to take the form:

$$
    p_{i} = \frac{1}{1 + N_i(1 + \epsilon_i)}
$$

The bias of worker i in treatment group g is assumed to come from a treatment-group specific distribution:

$$
    \epsilon_i \sim \text{Normal}(\mu^{\epsilon}_g, \sigma^{\epsilon}_g)
$$

---

## Calibration

The condition:

$$
u\left( \frac{p_{i,g}}{c_i} \right) = u\left( \frac{t_i}{W} \right)
$$

Is enforced via log difference equation with penalty $$\delta$$:

$$
    log \left( u\left( \frac{p_{i,g}}{c_i} \right) \right) - log \left( u\left( \frac{t_i}{W} \right) \right) \sim \text{Normal}(0, \frac{1}{\delta})
$$

---


## Calibration


Utility is assumed to be linear

* TODO: estimate per-person risk aversion!

---

## Estimated Posterior of Mean Bias

![inline](../experiments/mean-bias-dark.pdf)


---

## Results

Model outputs an "equilibrium belief tree".

* Binary tree, every node contains a belief, every split a fail/success updating.
* Equilibrium flow maintained by exogenous exit from market (death?) and corresponding newborns.

---

## Results

```
|--m: 0.53, u: 0.1000, e: 0.0000
   |--m: 0.24, u: 0.0541, e: 0.0000
      |--m: 0.09, u: 0.0388, e: 0.0000
      |--m: 0.84, u: 0.0006, e: 0.0933
   |--m: 0.95, u: 0.0021, e: 0.3378
      |--m: 0.88, u: 0.0007, e: 0.0000
      |--m: 1.00, u: 0.0001, e: 0.0117
```

---

## Wage Results

![inline](../equilibrium/wage-distributions.pdf)


---

## Future Research

> One of the best established findings in social psychology is that people perceive themselves readily as the origin of good effects and reluctantly as the origin of ill effects...
-- Anthony Greenwald (1980)

---

## Future Research

* Role of the ego and self-worth.

* Role of prior formation vs learning-by-experience.

* Effects for collective bargaining.

* Empirical evidence via platform data.
