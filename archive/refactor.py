from assistantManager import AssistantManager
import time  # AI-GEN - CursorAI with GPT4





def main():
    set_api_key = ''  # Replace with your actual API key
    assistant_id = 'asst_TujGUhdg9wg448fc9HpNJrNd'  # Replace with your actual Assistant ID
    organization_id = 'org-OSdfkiKEtRAYM4FrIpVfXLLC'
    manager = AssistantManager(set_api_key, assistant_id, organization_id)  # AI-GEN - CursorAI with GPT4

    thread_id = manager.create_new_thread()  # AI-GEN - CursorAI with GPT4
    message = manager.create_message(thread_id)
    run = manager.create_run(thread_id)

    while True:  # AI-GEN - CursorAI with GPT4
        run = manager.get_run_status(thread_id, run.id)  # AI-GEN - CursorAI with GPT4
        if run.status == 'completed':  # AI-GEN - CursorAI with GPT4
            break  # AI-GEN - CursorAI with GPT4
        print(f"Run status: {run.status}")
        print(f"Waiting 1 seconds...")
        time.sleep(1)  # AI-GEN - CursorAI with GPT4

    messages = manager.list_messages(thread_id)

    print(f"Thread ID: {thread_id}")  # AI-GEN - CursorAI with GPT4
    print(f"Messages: {messages}")
    print(f"Run: {run.status}")

if __name__ == "__main__":
    main()  # AI-GEN - CursorAI with GPT4