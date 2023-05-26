import requests
import time
import os
from module.DocumentProcessor import DocumentProcessor
import PyPDF2

LOCAL_API_GENERATE_URL = "http://127.0.0.1:5000/generate"
LOCAL_API_NEW_CHAT_URL = "http://127.0.0.1:5000/new_chat" #None if not applicable for yours API
OPENAI_KEY = None

TEMPLATE_DIR = 'task_template/'
DOCUMENT_DIR = 'documents/'
OUTPUT_DIR = 'outputs/'
SHORT_SUMMARY = True

if __name__ == "__main__":
	DocumentProcessor(
		TEMPLATE_DIR,
		DOCUMENT_DIR,
		OUTPUT_DIR,
		LOCAL_API_GENERATE_URL,
		LOCAL_API_NEW_CHAT_URL,
		OPENAI_KEY,
		SHORT_SUMMARY
	)