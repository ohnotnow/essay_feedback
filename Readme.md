# Essay Feedback Processor

This project provides a script that processes essays in `.docx` format, generates feedback using an AI assistant, and saves the results in a specified output directory.

## Features

- Scans a directory for `.docx` essays.
- Identifies unprocessed essays and generates feedback using the provided AI assistant.
- Saves the feedback in the output directory.
- Will automatically generate an assistant if one is not provided (you can specify the prompt in a file called `prompt.txt`).

## Requirements

- Python 3.7+

## Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/ohnotnow/essay_feedback
cd essay_feedback
python3 -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following environment variables:

```
APIKey=<your_openai_api_key>
AssistantID=<your_assistant_id>
```

Alternatively, you can export the `OPENAI_API_KEY` and `ASSISTANT_ID` as environment variables, and they will be used if not set in the `.env` file.

## Usage

Run the script by providing the essays directory and output directory:

```bash
python main.py --essays-dir /path/to/essays --output-dir /path/to/output
```

Options:
- `--essays-dir`: Directory containing the `.docx` essays (required).
- `--output-dir`: Directory where feedback will be saved (default: `feedback` subdirectory inside `essays-dir`).
- `--config-file`: Path to the configuration file (default: `.env`).

### Example

```bash
python process_essays.py --essays-dir ./essays --output-dir ./feedback --config-file .env
```

This will process all unprocessed `.docx` files in the `./essays` directory and save the feedback in the `./feedback` directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
