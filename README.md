# Multi-Agent Petri Net Mining

This project was developed as part of a university practical course on process mining. The goal was to implement algorithms that generate **multi-agent petri nets** from process log files.

## Approach

1. **Per-Agent Petri Net Generation** – For each agent, a petri net is constructed using either the *Inductive Miner* or *Split Miner*.
2. **Agent Connection** – Common process steps and interaction messages are identified to connect the individual agents.
3. **Interaction Pattern Detection** – Property-preserving transformations are applied to reveal the underlying interaction pattern of the multi-agent system.

## Background

In the [original research paper](https://doi.org/10.1007/s10270-022-01008-x), the authors proposed starting with a small interaction pattern and refining it. While theoretically sound, this quickly led to **combinatorial explosion** and proved impractical.

## My Contribution

To address this, I **reversed the refinement process**:

- Refinements were transformed into **reduction operations**.
- These reductions were applied to the mined multi-agent petri nets.

This reverse approach significantly improved performance and allowed detection of the underlying interaction pattern—even when it didn’t exactly match any predefined patterns.

<img width="1470" height="920" alt="Screenshot 2025-08-10 at 13 49 23" src="https://github.com/user-attachments/assets/96fb59c4-731b-44de-8768-8b7cb2c42071" />

