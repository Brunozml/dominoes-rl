import dominoes
import numpy as np
import matplotlib.pyplot as plt

q_agent = dominoes.players.QAgent(alpha = 0.5, epsilon = 0.1)


#%% Visualizing Values learned
# train agent
q_agent.train(n = 1000, verbose = False)
print(q_agent.q)
# convert state-action values to state values
state_values = dict()
for key in q_agent.q:
    state = key[0]
    if state not in state_values:
        state_values[state] = q_agent.q[key]
    else:
        state_values[state] += q_agent.q[key]

# create the value grid for plotting
value_grid = np.zeros((7,7))
for key in state_values:
    value_grid[key[0], key[1]] = state_values[key]

# plot the value grid
plt.imshow(value_grid)
plt.colorbar()
plt.show()

# plot the value grid in 3d
ax1 = fig.add_subplot(1, 2, 1, projection="3d")
ax1.plot_surface(x, y, z, cmap="viridis", edgecolor="none")

# %%
