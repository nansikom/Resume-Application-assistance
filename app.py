import os
import json
from docx import Document
from PyPDF2 import PdfReader
from flask import Flask,request,render_template
import pdfplumber
import re
from flask import session
import uuid
from datetime import datetime

app = Flask(__name__,template_folder='templates')
app.secret_key = 'your_secret_key_here'

# Try to use Flask-Session for server-side storage, fallback to default if not available
try:
    from flask_session import Session
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'flask_sessions')
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    Session(app)
    print("Using Flask-Session with filesystem storage")
except ImportError:
    print("Flask-Session not available, using default cookie-based sessions")
    # For large documents, we'll need to be careful about cookie size limits
    # The app will still work but may hit cookie size limits with very large documents

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploadform',methods=['POST'])
def uploadform():
    # Clear only resume text, keep job description
    Resumedisplay= request.form.get('Resumedisplay', '').strip()

    # Clear and reset resume text
    text_contents = []

    if Resumedisplay:
        text_contents.append(Resumedisplay)
        print(f"New resume text uploaded: {len(Resumedisplay)} characters")
    else:
        print("No resume text provided.")

    # Completely replace the resume_text in session
    session['resume_text'] = text_contents
    session.modified = True

    print(f"Session updated - Resume docs: {len(session.get('resume_text', []))}, Job docs: {len(session.get('job_text', []))}")

    # Always return JSON for AJAX requests
    if request.is_json or request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        response = {'status': 'success', 'message': 'Resume uploaded successfully'}
        return app.response_class(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )

    return render_template(
            'index.html',
            extractedText=session.get('resume_text'),
            extracted_tt=session.get('job_text'),
            upload_success='resume'
        )


@app.route('/uploadform1',methods=['POST'])
def uploadform1():
    # Clear only job description, keep resume text
    jobdesc= request.form.get('jobdesc', '').strip()

    # Clear and reset job text
    text_contents = []

    if jobdesc:
        text_contents.append(jobdesc)
        print(f"New job description uploaded: {len(jobdesc)} characters")
    else:
        print("No job description provided.")

    # Completely replace the job_text in session
    session['job_text'] = text_contents
    session.modified = True

    print(f"Session updated - Resume docs: {len(session.get('resume_text', []))}, Job docs: {len(session.get('job_text', []))}")

    # Always return JSON for AJAX requests
    if request.is_json or request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        response = {'status': 'success', 'message': 'Job description uploaded successfully'}
        return app.response_class(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )

    return render_template(
            'index.html',
            extractedText=session.get('resume_text'),
            extracted_tt=session.get('job_text'),
            upload_success='job'
        )
    

@app.route('/clear_session', methods=['POST'])
def clear_session():
    """Endpoint to manually clear session data"""
    session.clear()
    return render_template('index.html')
@app.route('/debug')
def debug_session():
    """Simple route to see what is happening in your session"""
    return {
        # if there isjob text yes if nothing return an empty list.
        'return_text': session.get('resume_text', []),
        'job_text': session.get('job_text', []),
        'session_id': session.get('_id', 'No ID'),
        'total_resume_docs':len(session.get('resume_text', [])),
        'total_job_docs': len(session.get('resume_text', [])),
        'total_job_docs': len(session.get('job_text', [])),

    }
@app.route('/stats')
def document_stats():
    """Show basic stats about the uploaded documents"""
    resume_texts = session.get('resume_text', [])
    job_texts = session.get('job_text', [])

    #Combine all resume texts and job texts 
    full_resume =' '.join(resume_texts) if resume_texts else ''
    full_job = ' '.join(job_texts) if job_texts else ''
    return {
        'resume_stats':{
            'total_words': len(full_resume.split()) if full_resume else 0,
            'total_characters': len(full_resume),
            'documents_uploaded': len(resume_texts)
        },
        'job_stats':{
            'total_words': len(full_job.split()) if full_job else 0,
            'total_characters': len(full_job),
            'documents_uploaded': len(job_texts)
        }
    }

@app.route('/simple_match')
def simple_match():
    """Find common words between resume and job description"""   
    resume_texts = session.get('resume_text', [] )
    print("this resume",resume_texts)
    job_texts = session.get('job_text', []) 
    print("this job_texts", job_texts) 
    if not resume_texts or not job_texts:
        return {'error': 'Need both the resume and job description uploaded'}  
    
    # Expanded stop words to filter out generic terms
    stop_words ={'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'from', 'as', 'this', 'that', 'these', 'those', 'it', 'its', 'who', 'what', 'where', 'when', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'just', 'may', 'must', 'shall', 'about', 'above', 'across', 'after', 'against', 'along', 'among', 'around', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'during', 'except', 'inside', 'into', 'near', 'off', 'out', 'over', 'through', 'toward', 'under', 'until', 'upon', 'within', 'without', 'least', 'less', 'much', 'many', 'several', 'any', 'either', 'neither', 'one', 'two', 'three', 'first', 'second', 'last', 'next', 'previous', 'new', 'old', 'good', 'great', 'best', 'better', 'well', 'also', 'even', 'still', 'yet', 'already', 'always', 'never', 'often', 'sometimes', 'usually', 'here', 'there', 'now', 'then', 'today', 'tomorrow', 'yesterday', 'ago', 'later', 'soon', 'early', 'late', 'long', 'short', 'high', 'low', 'large', 'small', 'big', 'little', 'full', 'empty', 'strong', 'weak', 'able', 'unable', 'make', 'made', 'making', 'get', 'got', 'getting', 'give', 'given', 'giving', 'take', 'taken', 'taking', 'come', 'came', 'coming', 'go', 'went', 'going', 'see', 'saw', 'seen', 'seeing', 'know', 'knew', 'known', 'knowing', 'think', 'thought', 'thinking', 'find', 'found', 'finding', 'use', 'used', 'using', 'work', 'worked', 'working', 'call', 'called', 'calling', 'try', 'tried', 'trying', 'ask', 'asked', 'asking', 'need', 'needed', 'needing', 'feel', 'felt', 'feeling', 'become', 'became', 'becoming', 'leave', 'left', 'leaving', 'put', 'putting'}
    
    # Get text and clean it
    full_resume =' '.join(resume_texts).lower()
    full_job = ' '.join(job_texts).lower()
    
    # Filter for meaningful keywords (longer words, likely skills/technical terms)
    resume_words = set([word for word in full_resume.split() if word not in stop_words and len(word) > 3])  
    job_words = set([word for word in full_job.split() if word not in stop_words and len(word) > 3]) 
    
    common_words = resume_words.intersection(job_words)
    missing_words_raw = job_words - resume_words
    
    # Further filter missing words to focus on likely skills (4+ chars, not too common)
    missing_words = set([word for word in missing_words_raw if len(word) >= 4])
    
    match_percentage = (len(common_words)/ len(job_words))* 100 if len(job_words) > 0 else 0
    return{
        'common_words': sorted(list(common_words)),
        'missing_words': sorted(list(missing_words)),
        'total_common': len(common_words),
        'total_missing': len(missing_words),
        'match_percentage':round(match_percentage, 1),
        'resume_word_count': len(resume_words),
        'job_word_count': len(job_words)
    }
def wordextraction(text, text2):
        print("j")
        pattern= r'[^\w\s]'
        cleanedsentencestp1= re.sub(pattern,'',text) 
        lowerletters=cleanedsentencestp1.lower()
        tokens=[]
        tokens= lowerletters.split()
        cleanedsentencestp2= re.sub(pattern,'',text2) 
        lowerletter=cleanedsentencestp2.lower()
        token=[]
        token= lowerletter.split()
        cats=[]
        print(f"Tokens from text 1: {tokens}")
        print(f"Token from text 2: {token}")

        for word in tokens:
            if word in token:
                cats.append(word)
        return cats
def extract_text_from_file(filepath, file_ext):
        text_content = ""
        if file_ext == ".pdf":
            with pdfplumber.open(filepath) as pdf:
                #reader= PdfReader(f)
                for page in pdf.pages:
                    page_text = page.extract_text() 
                    #print(page_text)
                    if page_text:
                        text_content += page_text + '\n'
            #print(text_content)
        elif file_ext == ".docx":
            doc = Document(filepath)
            for para in doc.paragraphs:
                    text_content += para.text + '\n'
        return text_content

@app.before_request
def before_request():
    # create a new session ID if the ID doesnt exist.
    if '_id' not in session:
        session['_id'] = str(uuid.uuid4())
if __name__== '__main__':
  app.run(debug=True)
  '''
  Find a  way of inputting the documents and searching thru them 
  '''










