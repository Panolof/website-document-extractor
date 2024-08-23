# Website Documentation Extractor

This project is a template for extracting hierarchical documentation from a website and saving it to a local folder as text files.

## Project Structure

```bash
git clone https://github.com/Panolof/website-document-extractor.git


```bash
.
├── README.md
├── output
│   └── .gitkeep
├── requirements.txt
├── setup.py
├── src
│   ├── __init__.py
│   └── extractor.py
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
python src/extractor.py <base_url> <output_folder>
```

Replace ```<base_url>``` with the URL of the documentation you want to start crawling from and ```<output_folder>``` with the directory where the extracted text files should be saved.

### 5. Logging Configuration

The logging configuration is managed using a YAML file (```logging_config.yaml```). The script logs detailed information, including requests, response status codes, and errors:
* Logs are written to ```logs/extractor.log```.
* The logging format is defined in the YAML file for both console output and file logging.

### 6. Deactivating the Virtual Environment

Once you’re done working on the project, you can deactivate the virtual environment:

```bash
deactivate
```

### Additional Information

* ```.gitignore``` is set up to ignore the venv/ folder, so your virtual environment is not tracked by Git.
* The ```output/``` folder is also ignored, as it’s meant to store extracted files.

## Future Enhancements

This is a basic template. Feel free to expand the project by adding more features like better link filtering, handling pagination, or improving the output file structure.







