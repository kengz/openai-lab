import gym
import tensorflow as tf
import numpy as np
from collections import deque
from replay_memory import ReplayMemory
from dqn import DQN

SOLVED_MEAN_REWARD = 195.0
MAX_STEPS = 200
MAX_EPISODES = 30
MAX_HISTORY = 100
MODEL_PATH = 'models/dqn.tfl'

episode_history = deque(maxlen=MAX_HISTORY)
env = gym.make('CartPole-v0')


def get_env_spec(env):
    '''
    return the env specs: dims, actions
    '''
    return {
        'state_dim': env.observation_space.shape[0],
        'state_bounds': np.transpose(
            [env.observation_space.low, env.observation_space.high]),
        'action_dim': env.action_space.n,
        'actions': list(range(env.action_space.n))
    }


# update the hisory, max len = MAX_HISTORY
# @return [bool] solved
def update_history(total_rewards, epi, total_t):
    episode_history.append(total_rewards)
    mean_rewards = np.mean(episode_history)
    logs = [
        '{:->20}'.format(''),
        'Episode {}'.format(epi),
        'Finished at t={}'.format(total_t),
        'Average reward for the last {} episodes: {}'.format(
            MAX_HISTORY, mean_rewards),
        'Reward for this episode: {}'. format(total_rewards)
    ]
    print('\n'.join(logs))
    solved = mean_rewards >= SOLVED_MEAN_REWARD
    return solved


# run an episode
# @return [bool] if the problem is solved by this episode
def run_episode(epi, env, replay_memory, dqn):
    total_rewards = 0
    state = env.reset()
    replay_memory.reset_state(state)
    for t in range(MAX_STEPS):
        env.render()
        action = dqn.select_action(state)
        next_state, reward, done, info = env.step(action)
        replay_memory.add_exp(action, reward, next_state, int(done))
        dqn.train(replay_memory)
        state = next_state
        total_rewards += reward
        if done:
            break
    solved = update_history(total_rewards, epi, t)
    return solved


# the primary method to run
# epi starts from 1 to MAX_EPISODES (inclusive)
# @return [bool] if the problem is solved
def deep_q_learn(env):
    sess = tf.Session()
    env_spec = get_env_spec(env)
    replay_memory = ReplayMemory(env_spec)
    dqn = DQN(env_spec, sess)
    sess.run(tf.initialize_all_variables())
    # dqn.restore(MODEL_PATH+'-30')
    for epi in range(MAX_EPISODES):
        solved = run_episode(epi, env, replay_memory, dqn)
        if solved:
            break
        # if epi % 10 == 0:
        #     dqn.save(MODEL_PATH, epi)
    print('Problem solved? {}'.format(solved))
    return solved


if __name__ == '__main__':
    deep_q_learn(env)
