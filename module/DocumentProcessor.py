import glob
import subprocess
import re
import requests
import time
import os
import PyPDF2

def read_paragraphs(file_path):
    paragraphs = []

    if file_path.endswith('.txt'):
        with open(file_path, 'r', errors='ignore') as file:
            paragraphs = file.read().split('\n')
    elif file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            print("Reading PDF, Might Take a While")
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                paragraphs.extend(page.extract_text().split('\n'))

    return paragraphs

def extract_taskname(input_string):
    return input_string.split("\\")[-1].split("/")[-1].split(".")[0]

def search_files(paths, extensions):
    files = []
    for path in paths:
        for extension in extensions:
            pattern = f"{path}/**/*.{extension}"
            files.extend(glob.glob(pattern, recursive=True))
    return files

class DocumentProcessor:
    def __init__(self, template_dir, document_dir, out_dir, generate_url, new_chat_url, openai_key=None, short_summary=True):
        # Search for template files
        for task in search_files([template_dir], ['txt']):
            task_name = extract_taskname(task)
            output_dir = f"{out_dir}/{task_name}"
            template = open(task, "r", encoding='utf-8', errors='ignore').read()
            print(f"Performing Task: {task_name}, {output_dir}")

            # Search for document files
            for document in search_files([f'{document_dir}/{task_name}/'], ['txt', 'pdf']):
                document_name = extract_taskname(document)
                if os.path.exists(f"{output_dir}/{document_name}.txt"):
                    continue

                # Check if a new chat window can be opened
                assert self._new_window(new_chat_url, openai_key)
                if not os.path.exists(output_dir):
                    os.mkdir(output_dir)

                paragraphs = read_paragraphs(document)

                prompt = template.strip("\n")
                index = 0
                output_list = list()

                with open(f"{output_dir}/{document_name}.txt", "a") as fp:
                    while index < len(paragraphs):
                        prompt += "\n" + paragraphs[index]
                        index += 1

                        if len(prompt) > 10000:
                            response = self._send_prompt(prompt, generate_url, openai_key)
                            if response is not None:
                                output_list.append(response['response'])
                                prompt = template.strip("\n")

                    response = self._send_prompt(prompt, generate_url, openai_key)
                    if response is not None:
                        output_list.append(response['response'])

                    for output in output_list:
                        try: fp.write(output + "\n\n")
                        except: print(f"Failed to Write {output}")

                if short_summary:
                    self._organize_summary_prompt(output_dir, document_name)
                    if response is not None:
                        output = response['response']
                        open(f"{output_dir}/{document_name}_short_summary.txt", "w").write(output)

    def _new_window(self, url, openai_key):
        if openai_key is None and url is not None:
            try:
                response = requests.get(url)
                return True
            except:
                return False
        else:
            return True

    def _send_prompt(self, prompt, url, openai_key):
        if openai_key is None:
            params = {'prompt': prompt}
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else None
        else:
            openai.api_key = openai_key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ]
            )
            return response['choices'][0]['message']['content']

    def _organize_summary_prompt(self, output_dir, document_name):
        with open(f"{output_dir}/{document_name}.txt", "r") as in_fp:
            summary_prompt = """
            Summarize the following text and format it in a numbered list so it is easier to read and understand:
            -------
            """ + in_fp.read()
            return summary_prompt