import requests
import os

# Configuration
ollama_endpoint = "http://localhost:11434/api/generate"  # Update with the actual endpoint
source_directory = "./java"          # Directory containing the .java files to refactor
output_directory = "./java/out"          # Directory to save the refactored .java files
refactoring_prompt = "Read the input, then refactor the code to update deprecated org.springframework.jdbc.core.simple.ParameterizedRowMapper to Spring 5.x. This is the ONLY refactoring you need to do. Please return an updated version of the original code with the refactoring. It needs to be a complete java file ready to compile."  # Your refactoring prompt

def refactor_file(file_path):
    # Construct the name for the output file
    output_file_path = os.path.join(output_directory, os.path.basename(file_path))
    
    # Read the source code
    with open(file_path, 'r') as file:
        source_code = file.read()
    
    # Prepare the data for the POST request
    data = {
        'model': 'codellama',
        'prompt': refactoring_prompt,
        'code': source_code,
        'stream': False  # AI-GEN - CursorAI with GPT4
    }
    
    # Make the POST request
    response = requests.post(ollama_endpoint, json=data)
    
    # Check if the request was successful
    if response.status_code == 200:

        refactored_code = response.json().get("response")  # AI-GEN - CursorAI with GPT4

        # Write the refactored code to the output directory
        with open(output_file_path, 'w') as file:
            file.write(refactored_code)
        print(f"Refactored file saved to: {output_file_path}")
    else:
        print(f"Failed to refactor {file_path}. Status code: {response.status_code}")

def main():
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Iterate over all .java files in the source directory
    for filename in os.listdir(source_directory):
        if filename.endswith(".java"):
            file_path = os.path.join(source_directory, filename)
            refactor_file(file_path)

if __name__ == "__main__":
    main()
