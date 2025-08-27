import os
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

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploadform',methods=['POST'])
def uploadform():
    session['resume_text'] = []
    files = request.files.getlist('files')
    text_contents = []
    common_words=[]
   # if 'text_contents' not in session:
    #    session['text_contents']=[]
    session['text_contents'] = []

    for file in files:
        if file.filename  =='':
            continue
        #more like saving the uploaded file into the file storage object file       
        if file:
            upload_dir= "uploads/form1"
            os.makedirs(upload_dir, exist_ok=True)
            # Create unique filename to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_ext = os.path.splitext(file.filename)[1].lower()
            unique_filename = f"{timestamp}_{uuid.uuid4().hex[:8]}{file_ext}"
            savepath = os.path.join(upload_dir, unique_filename)

            try:
                file.save(savepath)
                text_content= extract_text_from_file(savepath, file_ext)
                if text_content.strip():  # Only add if content exists
                    text_contents.append(text_content)
                os.remove(savepath)  # Clean up file after processing
            except Exception as e:
                print(f"Error processing file {file.filename}: {str(e)}")
                continue

    # store in session as resume
    session['resume_text'] = text_contents
    session.modified = True

    return render_template(
            'index.html',
            extractedText=session.get('resume_text'),
            extracted_tt=session.get('job_text')
        )
    
    
@app.route('/uploadform1',methods=['POST'])
def uploadform1():
    session['job_text'] = []
    files = request.files.getlist('files')
    text_contents = []
    common_words=[]
   # if 'text_contents' not in session:
    #    session['text_contents']=[]
    session['text_contents1'] = []

    for file in files:
        if file.filename  =='':
            continue
        #more like saving the uploaded file into the file storage object file       
        
        if file:
            upload_dir= "uploads/form1"
            os.makedirs(upload_dir, exist_ok=True)
            # Create unique filename to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_ext = os.path.splitext(file.filename)[1].lower()
            unique_filename = f"{timestamp}_{uuid.uuid4().hex[:8]}{file_ext}"
            savepath = os.path.join(upload_dir, unique_filename)

            try:
                file.save(savepath)
                text_content= extract_text_from_file(savepath, file_ext)
                if text_content.strip():  # Only add if content exists
                    text_contents.append(text_content)
                os.remove(savepath)  # Clean up file after processing
            except Exception as e:
                print(f"Error processing file {file.filename}: {str(e)}")
                continue

    # store in session as resume
        session['job_text'] = text_contents
        session.modified = True

    return render_template(
            'index.html',
            extractedText=session.get('resume_text'),
            extracted_tt=session.get('job_text')
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
    stop_words ={'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
    
    # Get text and clean it
    #This combines all the text
    full_resume =' '.join(resume_texts).lower()
    full_job = ' '.join(job_texts).lower()
    resume_words = set([word for word in full_resume.split() if word not in stop_words and len(word) > 2])  
    job_words = set([word for word in full_job.split() if word not in stop_words and len(word) > 2]) 
    common_words = resume_words.intersection(job_words)    
    # Calculate 
    # unique words comes from 
    #total_unique_words = len(resume_words.union(job_words))  
    match_percentage = (len(common_words)/ len(job_words))* 100 if len(job_words) > 0 else 0
    return{
        'common_words': list(common_words)[:20],
        'total_common': len(common_words),
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










