# Dominoes RL Project

## In this project, I build on top of [Alan Wagner's](https://dominoes.readthedocs.io/en/latest/#board) Dominoes python library to create reinforecement learning agents that improve through self-play

# How to Run

- 1. Install repo and requirements
- 2. `run train_agent.py`

---

# Project organization

The project is currently organized as follows:

- `/dominoes_lib` includes the most important files in Wagner's library, getting rid of everything I considered unnecessary and therefore distracting.
- `play.py` is basically the original CLI in the library. I included it as a normal python script, which can be ran by typing `python play.py` in the command line.
- `/notebooks` contains jupyter notebooks that experiment with the library. For the moment, its not really working (I can't import the local library)
- `q_agent.py` is what I'm currently working on. I based the function structure on **CS50's Nim exercise**. I have yet to implement several of the functions. The biggest challenge is to ensure correct functionining with the original dominoes library.
- `play.py` is an adaptation of the original code, which allows CLI interaction. q_agent not currently supported.

---

# notes

My handling of the `dominoes` library and modifications is currently a mess.

How to modify it, integrate it, and use it in my project in real time and without breaking it is unclear to me. I should see more examples (why does open_spiel work with a similar structure but not mine?!)

---

## TO-DOs

- [ ] Eventually, rewrite the entire original library by myself so that I can understand what is happening.

- [ ] Write the training and playing functions for my algorithm.
- [ ] integrate to Github
