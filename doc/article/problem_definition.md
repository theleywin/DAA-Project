# 3. Problem Definition and Modeling

In this section, we formally define the frequency assignment problem addressed in this work and introduce its graph-based modeling.

We model the cellular network as an undirected graph:

$$G = (V, E)$$

where each vertex $ v \in V $ represents a cellular base station (tower), and each edge $ (u, v) \in E $ indicates that towers $ u $ and $ v $ are geographically close enough to potentially cause radio interference. Consequently, adjacent vertices are not allowed to operate using the same radio frequency.

Let $ C = \{c_1, c_2, \dots, c_k\} $ denote the finite set of available radio frequencies.  
We define a cost function:

$$w : V \times C \rightarrow \mathbb{R}_{\ge 0}$$

where $ w(v, c) $ represents the operational cost incurred when assigning frequency $ c $ to tower $ v $.  
This cost function abstracts multiple real-world factors, such as hardware compatibility, energy consumption, and regulatory constraints.

A **frequency assignment** is defined as a function:

$$f : V \rightarrow C$$

An assignment $ f $ is said to be **valid** if it satisfies the interference constraint:

$$f(u) \neq f(v) \quad \forall (u, v) \in E$$

The total cost associated with a frequency assignment $ f $ is given by:

$$\text{Cost}(f) = \sum_{v \in V} w(v, f(v))$$

The **Cost-Aware Frequency Assignment Problem (CA-FAP)** consists of finding a valid assignment $ f $ that minimizes the total cost $ \text{Cost}(f) $.

This formulation generalizes the classical graph coloring problem by associating a cost with each vertex–color pair, thereby significantly increasing both the expressive power of the model and its practical relevance for real-world cellular networks.
