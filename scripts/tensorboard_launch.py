from tensorboard import program
import time

tracking_address = "./gym_linefollower/ppo_logs"

if __name__ == "__main__":
    tb = program.TensorBoard()
    tb.configure(argv=[None, '--logdir', tracking_address])
    url = tb.launch()
    print(f"Tensorflow listening on {url}")
    time.sleep(1000)