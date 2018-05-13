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
