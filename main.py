from ai_train.train_runner import train_runner, play_trained_model
from manual_game.manual_gameplay import run_game
import argparse 

def main():
    parser = argparse.ArgumentParser(description="PPO Runner Training")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Train
    train_parser = subparsers.add_parser("train", help="Train the model")
    train_parser.add_argument("--timesteps", type=int, default=100_000)
    train_parser.add_argument("--render", action="store_true")
    train_parser.add_argument("--continue_train", type=str, default=None, metavar="MODEL_PATH")

    # Play
    play_parser = subparsers.add_parser("play", help="Regarder le model jouer")
    play_parser.add_argument("--model", type=str, default="runner_model", help="Changer le nom du model à utiliser")
    play_parser.add_argument("--episodes", type=int, default=1, help="Changer le nombre d'épisode")
    play_parser.add_argument("--no-render", action="store_true", help="Désactiver le rendu (plus rapide)")
    play_parser.add_argument("--manual", action="store_true", help="Jouer manuellement")

    args = parser.parse_args()

    if args.command == "train" or args.command is None:
        train_runner(
            timesteps=args.timesteps if args.command else 100_000,
            render=args.render if args.command else False,
            continue_from=args.continue_from if args.command else None
        )
    elif args.command == "play":
        if args.manual:
            run_game()
        else:
            play_trained_model(args.model, args.episodes, render= not args.no_render)

if __name__ == "__main__":
    main()