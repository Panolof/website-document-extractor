import argparse
import logging
import logging.config
import yaml
import re
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.corpus import stopwords
import os 
# Download NLTK stopwords (if not already downloaded)
nltk.download('stopwords')

def setup_logging(default_path='logging_config_condenser.yaml', default_level=logging.INFO):
    if os.path.exists(default_path):
        with open(default_path, 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def clean_text(text):
    logging.info("Cleaning the text by removing links, special characters, and extra whitespace.")
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    return text

def remove_stopwords(text):
    logging.info("Removing stopwords from the text.")
    stop_words = set(stopwords.words('english'))
    return ' '.join([word for word in text.split() if word.lower() not in stop_words])

def get_embeddings(text, model_name="all-MiniLM-L6-v2"):
    logging.info(f"Generating embeddings using model: {model_name}")
    model = SentenceTransformer(model_name)
    sentences = text.split('. ')  # Split text into sentences
    sentence_embeddings = model.encode(sentences, convert_to_tensor=True)
    logging.info(f"Generated embeddings for {len(sentences)} sentences.")
    return sentences, sentence_embeddings

def condense_content(sentences, embeddings, max_sentences=5):
    logging.info(f"Condensing content to the top {max_sentences} most relevant sentences.")
    content_embedding = embeddings.mean(dim=0)  # Average embedding
    similarity_scores = util.pytorch_cos_sim(content_embedding, embeddings)[0]
    top_sentence_indices = similarity_scores.argsort(descending=True)[:max_sentences]

    condensed_content = ' '.join([sentences[i] for i in top_sentence_indices])
    return condensed_content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Condense documentation using sentence embeddings.")
    parser.add_argument('file_path', type=str, help="The path to the documentation file to condense")
    parser.add_argument('--max_sentences', type=int, default=5, help="The maximum number of sentences to retain in the condensed content")
    parser.add_argument('--model_name', type=str, default="all-MiniLM-L6-v2", help="The embedding model to use (default: all-MiniLM-L6-v2)")

    args = parser.parse_args()

    # Setup logging using the YAML configuration
    setup_logging()

    # Read the documentation file
    with open(args.file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    logging.info(f"Loaded text file with {len(text.split())} words.")

    # Clean and preprocess the text
    cleaned_text = clean_text(text)
    cleaned_text = remove_stopwords(cleaned_text)

    # Get sentence embeddings
    sentences, embeddings = get_embeddings(cleaned_text, model_name=args.model_name)

    # Condense the content based on semantic similarity
    condensed_content = condense_content(sentences, embeddings, max_sentences=args.max_sentences)

    # Output the condensed content
    logging.info("Condensed content generated successfully:")
    print(condensed_content)
