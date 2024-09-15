import os
import argparse
from dotenv import dotenv_values
from gepetto.assistant import Assistant
from gepetto.word_document import WordDocument

def get_default_prompt():
    if os.path.exists('prompt.txt'):
        with open('prompt.txt', 'r') as file:
            return file.read()
    else:
        return "You are an AI assistant that provides feedback on essays."

def find_processed_essays(output_dir: str):
    filenames = [filename for filename in os.listdir(output_dir) if filename.endswith('.docx')]
    return filenames

def find_unprocessed_essays(essays_dir: str, output_dir: str):
    processed_essays = find_processed_essays(output_dir)
    essays = [filename for filename in os.listdir(essays_dir) if filename.endswith('.docx') and not filename.startswith('~$')]
    return [essay for essay in essays if essay not in processed_essays]

def process_essay(essay_path: str, output_dir: str, assistant: Assistant) -> str:
    doc = WordDocument()
    text = doc.read(essay_path)
    feedback = assistant.process_text(text)
    filename = os.path.basename(essay_path)
    output_path = os.path.join(output_dir, filename)
    doc.write(output_path, feedback)
    return output_path

def main(essays_dir, output_dir, config_file):
    config = dotenv_values(config_file)
    if not 'APIKey' in config:
        config['APIKey'] = os.getenv('OPENAI_API_KEY')
    if not 'AssistantID' in config:
        config['AssistantID'] = os.getenv('ASSISTANT_ID')
    assistant = Assistant(id=config['AssistantID'], name="Assistant", instructions=get_default_prompt(), api_key=config['APIKey'])
    essays = find_unprocessed_essays(essays_dir, output_dir)
    if len(essays) == 0:
        print("No unprocessed essays found.")
        return
    for essay in essays:
        print(f"Processing {essay}...")
        essay_path = os.path.join(essays_dir, essay)
        feedback_filename = process_essay(essay_path, output_dir, assistant)
        print(f"Saved feedback to {feedback_filename}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process essays in a directory and save feedback.")
    parser.add_argument('--essays-dir', required=True, type=str, help='Directory containing essays')
    parser.add_argument('--output-dir', type=str, default="",help='Directory to save feedback (default is {--essays-dir}/feedback)')
    parser.add_argument('--config-file', type=str, default=".env", help='Path to the config file (default is .env)')
    args = parser.parse_args()
    if not args.output_dir:
        args.output_dir = os.path.join(args.essays_dir, 'feedback')
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    if not os.path.exists(args.config_file):
        raise FileNotFoundError(f"Config file not found: {args.config_file}")
    main(args.essays_dir, args.output_dir, args.config_file)
