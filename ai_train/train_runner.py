# train_snake.py
from stable_baselines3 import PPO
from ai_train.environment import RunnerEnv
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.monitor import Monitor

def make_env():
    return Monitor(RunnerEnv(render_mode=False))

def train_runner(timesteps=100000, render=False, continue_from=None):

    print("Training Runner with PPO")
    print(f"Total timesteps: {timesteps}")
    if continue_from:
        print(f"Continuing from: {continue_from}")
    print("-" * 40)

    env = SubprocVecEnv([make_env for _ in range(8)])

    if continue_from:
        model = PPO.load(continue_from, env=env)
        print(f"Model loaded from '{continue_from}'")
    else:
        model = PPO(
            "MlpPolicy",
            env,
            verbose=1,
            learning_rate=3e-4,
            n_steps=2048,
            batch_size=64,
            n_epochs=10,
            gamma=0.99,
            ent_coef=0.01
        )

    print("Starting training...")
    model.learn(
        total_timesteps=timesteps,
        reset_num_timesteps=continue_from is None
    )

    model.save("runner_model")
    print("Model saved as 'runner_model'")

    env.close()
    return model

def play_trained_model(model_path="snake_model", episodes=1, render=True):
    """Watch the trained model play"""

    print(f"Loading model: {model_path}")

    # Create environment with rendering
    env = RunnerEnv(render_mode=render)

    # Load model
    model = PPO.load(model_path, env=env)

    print(f"Watching trained agent play {episodes} episodes...")
    print("Close the window to stop early")

    scores = []
    for episode in range(episodes):
        obs, info = env.reset()
        done = False

        print(f"Episode {episode + 1}:")

        while not done:
            # Get action from model
            action, _ = model.predict(obs, deterministic=True)

            # Take step
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

        score = info.get('score', 0)
        scores.append(score)
        print(f"Score: {score}")

    env.close()

    print(f"\nResults:")
    print(f"Average Score: {sum(scores)/len(scores):.2f}")
    print(f"Best Score: {max(scores)}")

    return scores
