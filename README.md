# PDF-text-preprocessing
This is a Python rule based pdf preprocessing where it removes Stopwords Removal (Custom Stopwords), performs Tokenization, Lowercasing, Punctuation Removal, Whitespace Removal. Also the pdf contained sentences in Hindi and other Indian Devanagri Languages. 
So, this code identifies unicode for the devanagri script, from \u0900 to \u097F and removes it. 
<br>
This was done for an internship project. At places where you find department_folder feel free to modify it according to respective preoject demands. 
<br>
<h1>Output:</h1>
This code produces output in json format. This code can produce json files for multiple folder (over 500 files too) within a root folder. Make sure to correctly name the folder and add the correct path of the root folder in the mentioned place
