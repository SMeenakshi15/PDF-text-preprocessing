import os
import json
import re
import fitz  # PyMuPDF

# Define custom stopwords
custom_stopwords = [
    'a', 'an', 'are', 'as', 'at', 'by', 'for', 'from', 'in', 'into', 
    'on', 'onto', 'that', 'to', 'with', 'was', 'were', 'has', 'have', 
    'it', 'its', 'of', 'the', 'this', 'those', 'these', 'and', 'or', 
    'but', 'not', 'so', 'than', 'then', 'over', 'under', 'such', 'do', 
    'does', 'did', 'be', 'been', 'being', 'if', 'else', 'no', 'nor'
]

# Convert custom stopwords to a set for faster lookup
stop_words_set = set(custom_stopwords)

def remove_hindi_characters(text):
    """Remove Hindi (Devanagari) and non-ASCII characters from the text."""
    # Filter out characters in the Devanagari Unicode block (\u0900-\u097F)
    # Also remove any other non-ASCII characters
    return re.sub(r'[^\x00-\x7F]+', '', text)

def preprocess_text(text):
    """Preprocess the text: lowercasing, punctuation removal, stopwords removal, and whitespace normalization."""
    # Remove Hindi and other non-ASCII characters
    text = remove_hindi_characters(text)
    
    # Lowercasing
    text = text.lower()
    
    # Tokenization and punctuation removal (keep only words)
    tokens = re.findall(r'\b\w+\b', text)
    
    # Stopwords removal
    tokens = [token for token in tokens if token not in stop_words_set]
    
    # Reconstruct the text
    processed_text = ' '.join(tokens)
    
    # Whitespace normalization
    processed_text = re.sub(r'\s+', ' ', processed_text).strip()
    
    return processed_text

def extract_pdf_content(pdf_path):
    """Extract and preprocess text content from a PDF file."""
    content = ""
    try:
        doc = fitz.open(pdf_path)
        print(f"Processing PDF: {pdf_path}")  # Debugging line
        for page in doc:
            text = page.get_text()
            print(f"Extracted text from page: {text[:200]}")  # Print a snippet for debugging
            content += preprocess_text(text) + "\n\n"
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
    return content

def parse_pdf_folders(root_folder):
    """Parse the folder structure and generate a JSON file."""
    result = []
    
    # Iterate over each department folder
    for department_folder in os.listdir(root_folder):
        department_path = os.path.join(root_folder, department_folder)
        if os.path.isdir(department_path):
            # Iterate over each PDF in the department folder
            for pdf_file in os.listdir(department_path):
                if pdf_file.endswith('.pdf'):
                    pdf_path = os.path.join(department_path, pdf_file)
                    pdf_content = extract_pdf_content(pdf_path)
                    if pdf_content:  # Only add if content is not empty
                        department_data = {
                            "title": pdf_file.replace('.pdf', ''),
                            "content": pdf_content.strip()
                        }
                        result.append(department_data)
                        print(f"Added to JSON: {department_data['title']}")  # Debugging line
    
    return result

def save_json(data, output_file):
    """Save the generated JSON data to a file."""
    try:
        # Set ensure_ascii=False to avoid escaping non-ASCII characters
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"JSON file saved successfully to {output_file}")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")

# Example usage
root_folder = 'path_to_your_root_folder'  # Replace with the actual path to your PDF folders
output_file = 'output.json'  # Output JSON file name

parsed_data = parse_pdf_folders(root_folder)
save_json(parsed_data, output_file)
