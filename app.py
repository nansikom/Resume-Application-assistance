import os
from docx import Document
from PyPDF2 import PdfReader
from flask import Flask,request,render_template
import pdfplumber
import re
from flask import session
app = Flask(__name__,template_folder='templates')
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')
'''
@app.route('/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    text_contents = []
    for file in files:
        if file.filename  =='':
            return "No selected file",400
        #more like saving the uploaded file into the file storage object file       
        if file:
            upload_dir= "uploads"
            os.makedirs(upload_dir, exist_ok=True)
        if not os.path.exists(upload_dir):
            return "Upload directory not created.", 500  # Server Error

        savepath=os.path.join("uploads", file.filename)
        file.save(savepath)
        file_ext=os.path.splitext(file.filename)[1].lower()
        text_content = ""
        if file_ext == ".pdf":
            with pdfplumber.open(savepath) as pdf:
                #reader= PdfReader(f)
                for page in pdf.pages:
                    page_text = page.extract_text() 
                    print(page_text)
                    if page_text:
                        text_content += page_text + '\n'
                        print(text_content)
        elif file_ext == ".docx":
            doc = Document(savepath)
            for para in doc.paragraphs:
                    text_content += para.text + '\n'
                    print(text_content)
        text_contents.append(text_content)
    return render_template('index.html',extracted_texts=text_contents)
'''  



@app.route('/uploadform1',methods=['POST'])
def uploadform1():
    files = request.files.getlist('files')
    text_contents = []
    common_words=[]
   # if 'text_contents' not in session:
    #    session['text_contents']=[]
    session['text_contents'] = []

    for file in files:
        if file.filename  =='':
            return "No selected file",400
        #more like saving the uploaded file into the file storage object file       
        if file:
            upload_dir= "uploads/form1"
            os.makedirs(upload_dir, exist_ok=True)
        if not os.path.exists(upload_dir):
            return "Upload directory not created.", 500  # Server Error

        savepath=os.path.join("uploads/form1", file.filename)
        file.save(savepath)
        file_ext=os.path.splitext(file.filename)[1].lower()
        text_content = ""
        if file_ext == ".pdf":
            with pdfplumber.open(savepath) as pdf:
                #reader= PdfReader(f)
                for page in pdf.pages:
                    page_text = page.extract_text() 
                    #print(page_text)
                    if page_text:
                        text_content += page_text + '\n'
            #print(text_content)
        elif file_ext == ".docx":
            doc = Document(savepath)
            for para in doc.paragraphs:
                    text_content += para.text + '\n'
        session['text_contents'].append(text_content)
        num_uploaded_files= len(session['text_contents'])
        print(f"Uploaded text contents:  {session['text_contents']}")
        print(f"Number of uploaded files:,{num_uploaded_files}")
    texts1=""
    texts=""
    if len(session.get('text_contents', [])) > 1:

    #if len(session[text_contents]) > 1:
        texts= session['text_contents'][0]
        print(texts)
        texts1=session['text_contents'][1]
        print(texts1)
        common_words=wordextraction(texts,texts1)
        print(common_words)
    elif len(session['text_contents']) == 1:
        texts = session['text_contents'][0]
        #print(texts)
        # Only set texts1 if there's more than one document uploaded
        print("Only one document uploaded. No comparison possible.")
    else:
        print("No documents uploaded.")
    print(f"Extracted text 1: {texts}")
    print(f"Extracted text 2: {texts1}")
    #print(f"Common words: {common_words}")
    

    
    return render_template('index.html',extracted_texts1=session['text_contents'],extracted_tt= session['text_contents'],common_words=common_words)

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
if __name__== '__main__':
  app.run(debug=True)
  '''
  Find a  way of inputting the documents and searching thru them 
  '''