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










