# Job Search The Impacts of Labor Market Congestion on Job Search

## Abstract

The internet is often considered a great reducer of frictions, and a reduction of frictions is often expected to lead to more efficient market outcomes. In the labor market, a clear implication of internet-based job applications is the ability for every worker to apply to more jobs without a corresponding increase in the firms' ability to interview more workers. In this paper I consider the interaction between this increased congestion and the search behavior of workers.

I frame job-search as a multi-armed bandit problem in which workers attempt to discover their own value in the job market at the same time as they attempt to successfully secure a job that maximizes their earnings. Following the literature from reinforcement learning and cognitive psychology, I create an experiment that measures the human biases that arise as participants are given an increased number of "pulls" without a corresponding increase in expected winnings. Furthermore, I create a treatment that measures additional changes in behavior when the expected value of the bandits is correlated with one's own self-worth.

Using results from the experiment, I train a reinforcement-learning algorithm to predict the behavior of job-seekers. I then build an agent-based model of the labor market where agents use this same algorithm to search for jobs. Finally, simulations from the model are used to show how interaction between an exogenous increase in the maximum number of applications sent per period and agents' behavioral biases lead to potential distributional implications for wages in the economy on a macro level.

## Thoughts on Equilibrium

Economics

## what ratios do you need?

* Not including behavioral adjustment.
* Then, what is threshold? And where is search directed?
* ditch threshold...


## Random High

* People apply to jobs. What happens when you increase the number of jobs they apply for?

* Macro-level congestion effects, behavioral-level psychological effects.

* Appling for jobs can be thought of as a multi-armed bandit problem where the prize is linked to one's own worth in the jobs market. This framework allows us to consider that users might apply to a job either because they intend to take it, or because they are learning their own worth. Given this framework, we test how well users approximate proper bayesian learning of the problem, and how thier biases can be altered, suboptimally, through the allowance of a larger number of attempts despite the payoff structure of the game remaining unchanged.

## Game Theory + Reinforcement Learning

Fictitious Play - this is the algorithm you have in your head when you try and imagine the simplest way to encode strategy learning in a simulation environment. There is a long history of examing whether or not this will converge to an equilibrium. The way in which it leads to "cyclical" play in the matching pennies game is an example of how it goes wrong.

MAB in Metric Space - you'll need some MAB function if you want to consider the space of jobs as a continuous metric space, which is more-or-less what you're doing. -- Gaussian Processes with UCB for continuous-space bandit problems??

Much of the literature around multi-player reinforcement learning focuses on creating "superintelligence", namely, strategies that beat humans, as opposed to predicting average human behavior.

Behavioral Game Theory is more closely aligned with what you're interested in. That being said, I don't really know if, in the end, this is really very game theoretic. The real question is: do recruiters often get applicants from people who are overqualified, that they in the end don't interview.


## LeMens

* People are bad at correcting for sampling biases -- self-generated or externally-generated biases the same general effect

* denomenator neglect --> numerocity hueristic

* Interaction with rumors!!! Is there an interaction effect???

* Test sequentially?? Test

Additional randomness and term that you are learning about and updating -- your own skill?? --> Can we frame this as a one-armed bandit...

## Why a McCall-style model is no good.

One might propose trading a directed-search framework for a stopping-time problem in which the offers to jobs come in exogenously from a distribution. This distribution can vary based on the individuals skill, of which they have a noisy prior, and the individual can update their prior on every round. The problem with this formulation is not just that, in reality, the job-search process is characterized by sparsity and lack of information. But also because, based on the fact that the value of a job-offer is left-truncated at 0, the beliefs of the agents must be updated in an inherently different fashion than in the paradigm of stopping-time problems. Specifically, in a stopping time problem of unkown distribution, one immediately has an unbiased estimator of the distribution which would cause the seeker to continue looking (given that reservation wage > expected wage), whereas in the sparse case of seeking for jobs, ones estimate is 0, and if taken as an unbiased estimate of the value of that job-type, one would necessarily stop searching immediately!

## Hrvoje Recs

* John Hey -- https://sites.google.com/a/york.ac.uk/john-hey/home/publications
* Michael Lee -- http://faculty.sites.uci.edu/mdlee/publications/

# Random

* Prelec 2010 --> difference in judgement before they place bets and after.
* Bastardi, Ulmann and Ross 2011 --> same priors, different experiences, change their belief based on choices.
* Hansen and Sargent Robustness -- 
* Thaler "overconfidence" DeBondt, W.F., Thaler, R., 1995. Financial decision-making in markets and firms: a behavioral perspective
* Kahneman, D., & Tversky, A. (2000). Choices, values, and frames
* Pearl, J. (1988). Probabilistic reasoning in intelligent systems: Networks of plausible inference

# Athey's stuff
https://arxiv.org/abs/1711.07077
https://drive.google.com/drive/folders/1dSUBEwyTONk7UB3svwBfJ48GkbMr_0Gi
https://arxiv.org/abs/1702.02896
https://drive.google.com/file/d/16-_6ziZnwBOnBKX6A-jtO08O-5mwZb7Y/view
https://github.com/gsbDBI/ExperimentData

# Writing

* Inequality - erosion of wages for the middle class
* Narratives and perceptions of the market -- globalized, competetive, cutthroat place >> political/popular discourse analysis? 
* Can one's perceived bargaining power influence this? 
* Rejections as source of erosion of power. 
* Statistical quirks with 0.
* The self and rejections. 






