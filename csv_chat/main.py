from dotenv import load_dotenv
from csv_chat.question_answerer import QuestionAnswerer
from csv_chat.analytics import Analytics
import argparse



def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--analytics",
        action="store_true",
        help="Count analytics"
    )
    parser.add_argument(
        "model",
        type=str,
        nargs="?",
        default="gpt-4o-mini",
        choices=["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4"],
        help="Select a model from the following options (default: gpt-4o-mini): gpt-4o-mini, gpt-3.5-turbo, gpt-4"
    )
    args = parser.parse_args()
        
    try:
        question_answerer = QuestionAnswerer(model=args.model, verbose=args.verbose)
    except EnvironmentError as err:
        print(err)
        return

    if args.analytics:
        analytics = Analytics(question_answerer)
        accuracy = analytics.run()
        print(f"Accuracy: {accuracy*100:.2f}%")
    else:
        question_answerer.run()


if __name__ == '__main__':
    main()
