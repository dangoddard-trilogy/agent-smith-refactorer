import argparse
import os
import logging  # AI-GEN - CursorAI with GPT4
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

        # Configure logging based on the debug mode argument
        if args.debug:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        else:
            logging.basicConfig(level=logging.WARN)

        print("Refactor: Initializing AssistantManager and RefactoringAgent.")  # AI-GEN - CursorAI with GPT4
        # Instantiate the AssistantManager with API key, Assistant ID, and Organization ID
        assistant_manager = AssistantManager(set_api_key=args.api_key, assistant_id=args.assistant_id, organization_id=args.organization_id)
        
        # Instantiate the RefactoringAgent with the path to the source list, the rules file, and the AssistantManager
        refactoring_agent = RefactoringAgent(files_list_path=args.source_list, rules_path=args.rules, assistant_manager=assistant_manager, base_path=args.base_path)
        
        print("Refactor: Starting the refactoring process.")  # AI-GEN - CursorAI with GPT4
        # Start the refactoring process
        refactoring_agent.start_refactoring_process()
    except Exception as e:
        logging.error(f"Refactor: An error occurred: {e}")
    finally:
        # Ensure cleanup_files is called regardless of success or failure
        assistant_manager.final_cleanup()  # AI-GEN - CursorAI with GPT4
        print("Refactor: Cleanup complete.")  # AI-GEN - CursorAI with GPT4
        refactoring_agent.print_results()


if __name__ == "__main__":
    main()
