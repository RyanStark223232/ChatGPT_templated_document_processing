# ChatGPT_templated_document_processing

This GitHub project provides a template-based solution for mass converting documents using ChatGPT and generating output files. It utilizes a document processor module to streamline the conversion process.

![Cover Image](/public/document_processor_art.png)

## How to Use

1. Clone the repository to your local machine:

```bat
git clone https://github.com/RyanStark223232/ChatGPT_templated_document_processing
```

2. Install the required dependencies by running the following command:

```bat
pip install -r requirements.txt
```

3. Open the `main.py` file in your preferred Python IDE or text editor and set up the necessary configurations in the code:

  - LOCAL_API_GENERATE_URL: The URL for the local API endpoint used to generate responses with ChatGPT.
  - LOCAL_API_NEW_CHAT_URL (optional): The URL for the local API endpoint used to initiate a new chat conversation with ChatGPT. Leave it as None if not applicable for your API.
  - OPENAI_KEY: Your OpenAI API key. If provided, will ignore the Local API. Leave it as `None` if you wanna use Local API.
  - TEMPLATE_DIR: The directory path where your task templates are stored. You may create new ones by referencing the structure of the existing ones
  - DOCUMENT_DIR: The directory path where your input documents are located. The folder name must match the name of the template.
  - OUTPUT_DIR: The directory path where the output files will be saved.
  - SHORT_SUMMARY: Set this flag to True if you want to generate short summaries for the converted documents.

4. Customize your task templates:

In the task_template directory, create template files for each document conversion task. These templates should include specific instructions and placeholders for the AI model to fill in.

5. Prepare your input documents:

Place your input documents in the documents directory. Supported document formats include PDF and TXT

6. Run the main.py script: ```python main.py```

7. Sit back and relax while the document processor module handles the conversion process. The output files will be saved in the outputs directory, preserving the original file names.

That's it! You have successfully utilized this project to mass convert your documents using ChatGPT. Feel free to modify the code and templates to suit your specific requirements.

If you encounter any issues or have suggestions for improvements, please create an issue on the project's GitHub repository.