from linefollower_env import LineFollowerEnv
from stable_baselines3 import PPO
from datetime import datetime

if __name__ == "__main__":
    now = datetime.now()
    current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
    env = LineFollowerEnv()
    model = PPO('MlpPolicy', env, verbose = 1,tensorboard_log = "./gym_linefollower/ppo_logs/")
    model.learn(total_timesteps=100000)
    model.save(path=f"./gym_linefollower/ppo_models/ppo_model_{current_time}")
    