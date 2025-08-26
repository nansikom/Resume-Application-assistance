import os
from docx import Document
from PyPDF2 import PdfReader
from flask import Flask, request, render_template, session
import pdfplumber
import re
import uuid
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    # Clear session data when starting fresh
    session.pop('resume_text', None)
    session.pop('job_text', None)
    return render_template('index.html')

@app.route('/uploadform', methods=['POST'])
def uploadform():
    # Clear previous resume data
    session['resume_text'] = []
    
    files = request.files.getlist('files')
    text_contents = []
    
    for file in files:
        if file.filename == '':
            continue  # Skip empty files instead of returning error
            
        if file:
            # Create unique upload directory for this session
            upload_dir = f"uploads/form1/{session.get('_id', 'default')}"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Create unique filename to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_ext = os.path.splitext(file.filename)[1].lower()
            unique_filename = f"{timestamp}_{uuid.uuid4().hex[:8]}{file_ext}"
            savepath = os.path.join(upload_dir, unique_filename)
            
            try:
                file.save(savepath)
                text_content = extract_text_from_file(savepath, file_ext)
                
                if text_content.strip():  # Only add if content exists
                    text_contents.append(text_content)
                    
                # Clean up file after processing
                os.remove(savepath)
                
            except Exception as e:
                print(f"Error processing file {file.filename}: {str(e)}")
                continue
    
    # Store in session
    session['resume_text'] = text_contents
    session.modified = True  # Ensure session is marked as modified
    
    return render_template(
        'index.html',
        extractedText=session.get('resume_text', []),
        extracted_tt=session.get('job_text', [])
    )

@app.route('/uploadform1', methods=['POST'])
def uploadform1():
    # Clear previous job description data
    session['job_text'] = []
    
    files = request.files.getlist('files')
    text_contents = []
    
    for file in files:
        if file.filename == '':
            continue  # Skip empty files instead of returning error
            
        if file:
            # Create unique upload directory for this session
            upload_dir = f"uploads/form1/{session.get('_id', 'default')}"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Create unique filename to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_ext = os.path.splitext(file.filename)[1].lower()
            unique_filename = f"{timestamp}_{uuid.uuid4().hex[:8]}{file_ext}"
            savepath = os.path.join(upload_dir, unique_filename)
            
            try:
                file.save(savepath)
                text_content = extract_text_from_file(savepath, file_ext)
                
                if text_content.strip():  # Only add if content exists
                    text_contents.append(text_content)
                    
                # Clean up file after processing
                os.remove(savepath)
                
            except Exception as e:
                print(f"Error processing file {file.filename}: {str(e)}")
                continue
    
    # Store in session
    session['job_text'] = text_contents
    session.modified = True  # Ensure session is marked as modified
    
    return render_template(
        'index.html',
        extractedText=session.get('resume_text', []),
        extracted_tt=session.get('job_text', [])
    )

def extract_text_from_file(filepath, file_ext):
    """Extract text from file based on extension"""
    text_content = ""
    
    try:
        if file_ext == ".pdf":
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + '\n'
                        
        elif file_ext == ".docx":
            doc = Document(filepath)
            for para in doc.paragraphs:
                text_content += para.text + '\n'
                
        elif file_ext == ".txt":
            with open(filepath, 'r', encoding='utf-8') as f:
                text_content = f.read()
                
    except Exception as e:
        print(f"Error extracting text from {filepath}: {str(e)}")
        
    return text_content

@app.route('/clear_session', methods=['POST'])
def clear_session():
    """Endpoint to manually clear session data"""
    session.clear()
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze resume and job description for common words"""
    resume_text = session.get('resume_text', [])
    job_text = session.get('job_text', [])
    
    if not resume_text or not job_text:
        return render_template(
            'index.html',
            extractedText=resume_text,
            extracted_tt=job_text,
            error="Please upload both resume and job description files."
        )
    
    # Combine all resume and job texts
    combined_resume = ' '.join(resume_text)
    combined_job = ' '.join(job_text)
    
    common_words = wordextraction(combined_resume, combined_job)
    
    return render_template(
        'index.html',
        extractedText=resume_text,
        extracted_tt=job_text,
        common_words=common_words,
        match_count=len(common_words)
    )

def wordextraction(text, text2):
    """Extract common words between two texts"""
    # Remove punctuation and convert to lowercase
    pattern = r'[^\w\s]'
    cleaned_text1 = re.sub(pattern, '', text).lower()
    cleaned_text2 = re.sub(pattern, '', text2).lower()
    
    # Split into words
    tokens1 = set(cleaned_text1.split())
    tokens2 = set(cleaned_text2.split())
    
    # Find common words (excluding very short words)
    common_words = [word for word in tokens1.intersection(tokens2) if len(word) > 2]
    
    return sorted(common_words)

# Add session identifier for each user
@app.before_request
def before_request():
    if '_id' not in session:
        session['_id'] = str(uuid.uuid4())

if __name__ == '__main__':
    app.run(debug=True)