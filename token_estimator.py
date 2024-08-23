import os
import tiktoken
import argparse

def estimate_token_count(text, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    token_count = len(encoding.encode(text))
    return token_count

def read_concatenated_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate token count for a concatenated text file.")
    parser.add_argument('file_path', type=str, help="The path to the concatenated text file")
    parser.add_argument('--model', type=str, default="gpt-3.5-turbo", help="The model to use for token estimation (default: gpt-3.5-turbo)")

    args = parser.parse_args()

    # Read the concatenated file
    text = read_concatenated_file(args.file_path)

    # Estimate the token count
    token_count = estimate_token_count(text, model=args.model)
    
    print(f"Estimated token count for {args.file_path}: {token_count}")
