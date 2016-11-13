# OpenAI Gym [![CircleCI](https://circleci.com/gh/kengz/openai_gym.svg?style=shield)](https://circleci.com/gh/kengz/openai_gym) [![Code Climate](https://codeclimate.com/github/kengz/openai_gym/badges/gpa.svg)](https://codeclimate.com/github/kengz/openai_gym)

[OpenAI Gym Doc](https://gym.openai.com/docs) | [OpenAI Gym Github](https://github.com/openai/gym) | [RL intro](https://gym.openai.com/docs/rl)

Working out at the (OpenAI) gym. **Note this is still under development, but will be ready before Nov 5**


## Installation

### Basic

```shell
git clone https://github.com/kengz/openai_gym.git
cd openai_gym
python setup.py install
```

*Note that by default it installs Tensorflow for Python3 on MacOS. [Choose the correct binary to install from TF.](https://www.tensorflow.org/versions/r0.11/get_started/os_setup.html#pip-installation)*

```shell
# for example, TF for Python2, MacOS
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.11.0rc1-py2-none-any.whl
# or Linux CPU-only, Python3.5
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.11.0rc1-cp35-cp35m-linux_x86_64.whl
sudo pip install --upgrade $TF_BINARY_URL
```

### Complete

To run more than just the classic control gym env, we need to install the OpenAI gym fully. We refer to the [Install Everything](https://github.com/openai/gym#installing-everything) of the repo (which is still broken at the time of writing).

```shell
brew install cmake boost boost-python sdl2 swig wget
git clone https://github.com/openai/gym.git
cd gym
pip install -e '.[all]'
```

Try to run a Lunar Lander env, it will break (unless they fix it):
```python
import gym
env = gym.make('LunarLander-v2')
env.reset()
env.render()
```

If it fails, debug as follow (and repeat once more if it fails again, glorious python):

```shell
pip3 uninstall Box2D box2d-py
git clone https://github.com/pybox2d/pybox2d
cd pybox2d/
python setup.py clean
python setup.py build
python setup.py install
```


## Usage

The main scripts are inside the `rl/` folder. Configure your `Agent`, `problem` and `param` in `rl/main.py`, and run

```shell
python rl/main.py # run in normal mode
python rl/main.py -d # print debug log
python rl/main.py -b # blind, i.e. don't render graphics
python rl/main.py 2>&1 | tee run.log # write to log file
```

See `rl/runner.py` for the main Runner class. It takes the 3 arguments `Agent, problem, param`.

You should implement your `Agent` class in the `rl/agent/` folder. By polymorphism, your `Agent` should implement the methods:

```python
def __init__(self, env_spec, ...<etc.>):
def select_action(self, state):
def train(self, sys_vars, replay_memory):
```

Refer to the following Agents in `rl/agent/` for building your own:
- `dummy.py`: dummy agent used for a gym tour. Does random actions.
- `q_table.py`: a tabular q-learner
- `dqn.py`: agent with a simple Deep Q-Network, forms the base `DQN` class for others to inherit
- `double_dqn.py`: agent with Double Deep Q-Network, inherits `DQN`
- `lunar_dqn.py`: agent with deeper network for the Lunar-Lander game, inherits `DQN`
- `lunar_double_dqn.py`: agent with deeper network for the Lunar-Lander game, inherits `DoubleDQN`


## Roadmap

- [x] major refactoring for more efficient development; standardization of the `Agent` class, and methods it shall implement.
- [x] logging of crucial data points, for plotting after runs
- [ ] better parameter selection, to tune for a problem (can use the parallelization in util.py)
- [ ] improve memory selection policy
- [ ] smarter exploration policy, use the idea of learning activation and strange attractors of dynamical system
- [ ] visualization of NN with tensorboard?
- [ ] parametrize epsilon anneal steps by MAX_EPISODES etc, so parameter selection can be more automatic across different problems. Use sine x exp decay graph?
- [ ] solve the stability problem - some runs start out bad and end up bad too
- [ ] do policy iteration (ch 4 from text)
- [ ] other more advanced algos


## Authors

- Wah Loon Keng
- Laura Graesser
