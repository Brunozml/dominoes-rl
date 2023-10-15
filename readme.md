# Dominoes RL Project

In this project, I build on top of [Alan Wagner's](https://dominoes.readthedocs.io/en/latest/#board) Dominoes python library to create reinforecement learning agents that improve through self-play

The project is currently organized as follows:

- `/dominoes_lib` includes the most important files in Wagner's library, getting rid of everything I considered unnecessary and therefore distracting.
- `play.py` is basically the original CLI in the library. I included it as a normal python script, which can be ran by typing `python play.py` in the command line.
- `/notebooks` contains jupyter notebooks that experiment with the library. For the moment, its not really working (I can't import the local library)
- `q_agent.py` is what I'm currently working on. I based the function structure on **CS50's Nim exercise**. I have yet to implement several of the functions. The biggest challenge is to ensure correct functionining with the original dominoes library.

---

## TO-DOs

- [ ] Eventually, rewrite the entire original library by myself so that I can understand what is happening.

- [ ] Write the training and playing functions for my algorithm.
- [ ] integrate to Github
