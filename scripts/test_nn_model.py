from linefollower_env import LineFollowerEnv
from tensorflow.keras.optimizers import Adam
from nn_model import build_model, build_agent

if __name__ == "__main__":
    env = LineFollowerEnv()
    actions = env.action_space.n
    model = build_model(actions)
    dqn = build_agent(model, actions)
    dqn.compile(Adam(learning_rate=1e-3), metrics=['mae'])
    dqn.load_weights("./gym_linefollower/nn_weights/weights_best.h5")
    dqn.test(env, nb_episodes=100, visualize=True)
    