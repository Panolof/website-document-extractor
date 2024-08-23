# Website Documentation Extractor

This project is a template for extracting hierarchical documentation from a website and saving it to a local folder as text files.

## Project Structure

```bash
git clone https://github.com/Panolof/website-document-extractor.git


```bash
.
├── README.md
├── LICENSE
├── output
│   └── .gitkeep
├── requirements.txt
├── setup.py
├── src
│   ├── __init__.py
│   └── extractor.py
├── token_estimator.py
├── content_condenser.py
├── logs
│   ├── extractor.log
│   └── content_condenser.log
├── logging_config_extractor.yaml
├── logging_config_condenser.yaml
├── .gitignore

```

## Setup Instructions

### 1. Clone the Repository

First, clone the repository:

```bash
git clone https://github.com/Panolof/website-document-extractor.git
cd website-doc-extractor
```

### 2. Create and Activate a Virtual Environment

It’s recommended to use a virtual environment to manage your project’s dependencies. You can set this up using venv:

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:

```bsah
python3 -m venv venv
source venv/bin/activate
```

After activating the virtual environment, your terminal prompt should show ```(venv)```.

### 3. Install Dependencies

Once the virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```


### 4. Running the Extractor Script

You can now run the script to extract the documentation:

```bash
python src/extractor.py <base_url> <output_folder> <index_file>
```

Replace ```<base_url>``` with the URL of the documentation you want to start crawling from, ```<output_folder>``` with the directory where the extracted text files should be saved, and ```<index_file>``` with the path to the file where the list of visited links should be saved.

### 5. Running the Content Condenser Script

After extraction, you can condense the documentation content:
```bash
python content_condenser.py <file_path> --max_sentences 5 --model_name "all-MiniLM-L6-v2"
```
Replace ```<file_path>``` with the path to the concatenated text file. Adjust ```--max_sentences``` and ```--model_name``` as needed.

### 6. Logging Configuration

The logging configuration is managed using separate YAML files for the extractor and condenser scripts:
* For the extractor script: ```logging_config_extractor.yaml```
    * Logs are written to ```logs/extractor.log```.
* For the condenser script: ```logging_config_condenser.yaml```
    * Logs are written to ```logs/content_condenser.log```.
The logging format is defined in the YAML file for both console output and file logging.

### 7. Using the Token Estimator Utility

Once you have concatenated the extracted files, you can estimate the token count:

```bash
python token_estimator.py output/how_to/concatenated.txt
```

By default, the token estimator uses the ```"gpt-3.5-turbo"``` model for estimation. You can specify a different model using the ```--model``` option:
```bash
python token_estimator.py output/how_to/concatenated.txt --model gpt-4
```

### 8. Deactivating the Virtual Environment

Once you’re done working on the project, you can deactivate the virtual environment:

```bash
deactivate
```

### Additional Information

* ```.gitignore``` is set up to ignore the venv/ folder, so your virtual environment is not tracked by Git.
* The ```output/``` folder is also ignored, as it’s meant to store extracted files.

## Future Enhancements

This is a basic template. Feel free to expand the project by adding more features like better link filtering, handling pagination, or improving the output file structure.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.






