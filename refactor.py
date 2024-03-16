import argparse
import os
import logging  # AI-GEN - CursorAI with GPT4
from datetime import datetime
from openai import OpenAI
from assistant_manager import AssistantManager
from refactoring_agent import RefactoringAgent

def parse_arguments():
    parser = argparse.ArgumentParser(description="Automated Code Refactoring Tool")
    parser.add_argument(
        "--source-list",
        required=True,
        help="Path to the text file containing the list of source files to refactor"
    )
    parser.add_argument(
        "--rules",
        default="rules.json",
        help="Path to the JSON file containing the refactoring rules (default: rules.json in the current working directory)"
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OPENAI_API_KEY"),
        help="OpenAI API key (default: OPENAI_API_KEY environment variable)"
    )
    parser.add_argument(
        "--assistant-id",
        default="asst_TujGUhdg9wg448fc9HpNJrNd",
        help="OpenAI Assistant ID (default: asst_TujGUhdg9wg448fc9HpNJrNd)"
    )
    parser.add_argument(
        "--organization-id",
        default="org-OSdfkiKEtRAYM4FrIpVfXLLC",
        help="OpenAI Organization ID (default: org-OSdfkiKEtRAYM4FrIpVfXLLC)"
    )
    parser.add_argument(
        "--base-path",
        default="",
        help="Optional base path to prefix to each source file path (default: empty, using current working directory)"
    )
    parser.add_argument(
        "--debug",
        action='store_true',
        help="Enable debug mode for more verbose logging"
    )

    return parser.parse_args()

def main():
    try:
        args = parse_arguments()

        # Set up file logging
        log_filename = f"refactor_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_filename)])

        # Set up console logging based on --debug flag
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        if args.debug:
            console_handler.setLevel(logging.INFO)
        else:
            console_handler.setLevel(logging.WARN)
        logging.getLogger().addHandler(console_handler)

        # Ensure the root logger level is set to the lowest level among all handlers if needed
        logging.getLogger().setLevel(min(logging.getLogger().level, console_handler.level))

        # Prevent double logging in the console
        logging.getLogger().propagate = False

        print("Refactor: Initializing AssistantManager and RefactoringAgent.")
        assistant_manager = AssistantManager(set_api_key=args.api_key, assistant_id=args.assistant_id, organization_id=args.organization_id)
        refactoring_agent = RefactoringAgent(files_list_path=args.source_list, rules_path=args.rules, assistant_manager=assistant_manager, base_path=args.base_path)
        
        print("Refactor: Starting the refactoring process.")
        refactoring_agent.start_refactoring_process()
    except Exception as e:
        logging.error(f"Refactor: An error occurred: {e}")
    finally:
        assistant_manager.final_cleanup()
        print("Refactor: Cleanup complete.")
        refactoring_agent.print_results()


if __name__ == "__main__":
    main()
