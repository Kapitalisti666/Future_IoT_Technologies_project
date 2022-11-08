import gym
from gym import error, spaces, utils
import numpy
import time
import os
import RPi.GPIO as gpio


class LineFollowerEnv(gym.Env):

    def __init__(self):
        gym.Env.__init__(self)

        gpio.setmode(gpio.BCM)
        gpio.setup(19, gpio.OUT) # Left motor
        gpio.setup(26, gpio.OUT) # Right motor

        gpio.setup(16, gpio.IN) # Left sensor
        gpio.setup(20, gpio.IN) # Middle sensor
        gpio.setup(21, gpio.IN) # Right sensor
        
        self.observation_space = spaces.MultiBinary(3)

        self.action_space = spaces.Discrete(3)

        self.actions = []  

        def right_turn():
            gpio.output(19, 1)
            time.sleep(0.4)
            gpio.output(19, 0)

        def left_turn():
            gpio.output(21, 1)
            time.sleep(0.4)
            gpio.output(21, 0)
        
        def straight():
            gpio.output(21, 1)
            gpio.output(19, 1)
            time.sleep(0.4)
            gpio.output(21, 0)
            gpio.output(19, 0)
        
        self.actions.append(left_turn()) # Right motor on
        self.actions.append(straight()) # Both motors on
        self.actions.append(right_turn()) # Left motor on

        self.reset()

    def reset(self):

        self.observation = None
        self.reward      = 0.0
        self.done        = False
        self.info        = {}

        time.sleep(10)
        self.observation = self._update_observation()
        return self.observation

    def step(self, action):
        
        self.actions[action]
        self.done   = False
        self.reward = 0.0

        self.observation = self._update_observation()

        if str(self.observation) == "[0. 1. 0.]":
            self.reward = 1
        elif str(self.observation) == "[1. 1. 1.]":
            self.reward = -0.5 
        elif str(self.observation) == "[1. 1. 0.]":
            self.reward = 0.8
        elif str(self.observation) == "[0. 1. 1.]":
            self.reward = 0.8
        elif str(self.observation) == "[1. 0. 0.]":  
            self.reward = 0.4
        elif str(self.observation) == "[0. 0. 1.]":  
            self.reward = 0.4
        else:
            self.reward = -1
            
        return self.observation, self.reward, self.done, self.info
        
    def render(self):
        pass
    
    def _update_observation(self):
            
        observation = numpy.zeros(3)
        
        if gpio.input(16) == 1:
            print("LEFT")
            observation[0] = 1 
        if gpio.input(20) == 1:
            print("MIDDLE")
            observation[1] = 1
        if gpio.input(21) == 1:
            print("RIGHT")
            observation[2] = 1
        print(observation)

        return observation
    