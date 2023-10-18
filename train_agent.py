#%%
import dominoes_lib as dominoes
from q_agent import train
import matplotlib.pyplot as plt
import numpy as np

q_agent = train(n= 1000)

# print (q_agent.q)
# get the Q-values learned by the agent
q_values = q_agent.q
print(q_values)


# %% visualizing Q-values and learning process

# inspiration:
# https://gymnasium.farama.org/tutorials/training_agents/blackjack_tutorial/
# https://gymnasium.farama.org/tutorials/training_agents/FrozenLake_tuto/


# BUGGY!!
def plot_qvals(q_agent):
    # get the Q-values learned by the agent
    q_values = q_agent.q

    # extract the states and actions from the Q-values dictionary
    states, actions = zip(*q_values.keys())

    # get the unique states
    unique_states = np.unique(states, axis=0)

    # get the unique actions
    unique_actions = actions # np.unique(actions)

    # create a matrix of Q-values for each state-action pair
    q_matrix = np.zeros((len(unique_states), len(unique_actions)))
    for i, state in enumerate(unique_states):
        for j, action in enumerate(unique_actions):
            if (tuple(state), tuple(action)) in q_values:
                q_matrix[i, j] = q_values[(tuple(state), tuple(action))]

    # plot the Q-values as a heatmap
    fig, ax = plt.subplots()
    im = ax.imshow(q_matrix, cmap='coolwarm')

    # set the x-axis and y-axis labels
    ax.set_xticks(np.arange(len(unique_actions)))
    ax.set_yticks(np.arange(len(unique_states)))
    ax.set_xticklabels([f"{action['end1']}-{action['end2']}" for action in unique_actions])
    ax.set_yticklabels([str(state) for state in unique_states])

    # rotate the x-axis labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # set the colorbar
    cbar = ax.figure.colorbar(im, ax=ax)

    # set the title
    ax.set_title("Q-values learned by the agent")

    # show the plot
    plt.show()# get the Q-values learned by the agent

    return plt