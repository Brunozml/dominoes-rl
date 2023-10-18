# Dominoes RL Project

In this project, I build on top of [Alan Wagner's](https://dominoes.readthedocs.io/en/latest/#board) Dominoes python library to create reinforecement learning agents that improve through self-play

The project is currently organized as follows:

- `/dominoes_lib` includes the most important files in Wagner's library, getting rid of everything I considered unnecessary and therefore distracting.
- `play.py` is basically the original CLI in the library. I included it as a normal python script, which can be ran by typing `python play.py` in the command line.
- `/notebooks` contains jupyter notebooks that experiment with the library. For the moment, its not really working (I can't import the local library unless I'm using local paths)
- `q_agent.py` is what I'm currently working on. I based the function structure on **CS50's Nim exercise**. The biggest challenge is to ensure correct functionining with my modified dominoes library.

---

## TO-DOs

- [ ] Eventually, rewrite most of the original library by myself so that I can understand what is happening and what I can change. Use open_spiel and gymnasium as inspiration for project structure.
- [X] write update_q_values and functions within
- [X] Write the training and playing functions for my algorithm.
- [ ] visualize the q-values
- [ ] setup function to play against my agent
