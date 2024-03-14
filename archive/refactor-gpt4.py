import requests
import os

# Configuration
assistant_id = "asst_TujGUhdg9wg448fc9HpNJrNd"  # GPT Assistant ID
source_directory = "./java"          # Directory containing the .java files to refactor
output_directory = "./java/out"          # Directory to save the refactored .java files
refactoring_prompt = "Read the input, then refactor the code to update deprecated org.springframework.jdbc.core.simple.ParameterizedRowMapper to Spring 5.x. This is the ONLY refactoring you need to do. Please return an updated version of the original code with the refactoring. It needs to be a complete java file ready to compile."  # Your refactoring prompt
api_key = ""

def refactor_file(file_path):
    # Construct the name for the output file
    output_file_path = os.path.join(output_directory, os.path.basename(file_path))  # AI-GEN - CursorAI with GPT4
    
    # Prepare the data for the POST request
    headers = {
        "Authorization": f"Bearer {api_key}",  # AI-GEN - CursorAI with GPT4
        "Content-Type": "multipart/form-data"  # AI-GEN - CursorAI with GPT4
    }
    data = {
        "inputs": {
            "prompt": refactoring_prompt,  # AI-GEN - CursorAI with GPT4
            "temperature": 0.5,
            "max_tokens": 2048,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
    }  # AI-GEN - CursorAI with GPT4
    files = {'file': open(file_path, 'rb')}  # AI-GEN - CursorAI with GPT4
    
    # Make the POST request to the assistant endpoint
    assistant_endpoint = f"https://api.openai.com/v1/assistants/{assistant_id}/completions"  # AI-GEN - CursorAI with GPT4
    response = requests.post(assistant_endpoint, headers=headers, data=data, files=files)  # AI-GEN - CursorAI with GPT4
    
    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        refactored_code = response_data.get("choices")[0].get("text")  # AI-GEN - CursorAI with GPT4
        file_url = response_data.get("choices")[0].get("file", None)  # AI-GEN - CursorAI with GPT4

        # Write the refactored code to the output directory
        with open(output_file_path, 'w') as file:
            file.write(refactored_code)  # AI-GEN - CursorAI with GPT4
        print(f"Refactored file saved to: {output_file_path}")  # AI-GEN - CursorAI with GPT4

        # Download the file if a URL is provided
        if file_url:
            download_response = requests.get(file_url)  # AI-GEN - CursorAI with GPT4
            with open(output_file_path, 'wb') as file:
                file.write(download_response.content)  # AI-GEN - CursorAI with GPT4
            print(f"Downloaded refactored file from {file_url} to: {output_file_path}")  # AI-GEN - CursorAI with GPT4
    else:
        print(f"Failed to refactor {file_path}. Status code: {response.status_code}")  # AI-GEN - CursorAI with GPT4

def main():
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)  # AI-GEN - CursorAI with GPT4
    
    # Iterate over all .java files in the source directory
    for filename in os.listdir(source_directory):
        if filename.endswith(".java"):
            file_path = os.path.join(source_directory, filename)  # AI-GEN - CursorAI with GPT4
            refactor_file(file_path)  # AI-GEN - CursorAI with GPT4

if __name__ == "__main__":
    main()  # AI-GEN - CursorAI with GPT4

