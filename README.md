# Resume Job Application Assistance Tool 📄💼

An intelligent tool designed to help you optimize your resume for specific job applications by analyzing keyword matches and providing tailored recommendations.

## 🎯 Overview

This project provides a comprehensive solution for resume customization and job application assistance. It compares your master resume against job descriptions to identify common keywords, highlight optimization opportunities, and help you tailor your resume for maximum impact.

## ✨ Key Features

### 🔍 **Keyword Matching & Analysis**
- Extracts text from both resume and job description documents
- Identifies and highlights common keywords between documents
- Generates detailed reports for resume optimization insights

### 📁 **Multi-Format File Support**
- **PDF Documents**: Complete text extraction support
- **DOCX Files**: Microsoft Word document compatibility
- **Seamless Processing**: Handles both formats effortlessly

### 🌐 **User-Friendly Web Interface**
- Simple Flask-based web application
- Drag-and-drop file upload functionality
- Real-time analysis and results display

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7+
- pip package manager

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd resume-assistant
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Application**
   ```bash
   python app.py
   python input.py
   ```

4. **Access the Web Interface**
   Navigate to: `http://127.0.0.1:5000`

## 📦 Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **Flask** | 3.0.3 | Web framework and server |
| **pdfminer.six** | 20231228 | PDF text extraction |
| **pdfplumber** | 0.11.4 | Advanced PDF processing |
| **PyPDF2** | 3.0.1 | PDF document handling |
| **pypdfium2** | 4.30.0 | Enhanced PDF processing |
| **python-docx** | 1.1.2 | Word document processing |
| **lxml** | 5.3.0 | XML/DOCX file handling |
| **pillow** | 11.0.0 | Image processing support |

## 🚀 How to Use

### Step-by-Step Guide

1. **Start the Application**
   - Run both `python app.py` and `python input.py`
   - The server will start on port 5000

2. **Upload Documents**
   - Navigate to `http://127.0.0.1:5000`
   - Upload your master resume (PDF or DOCX)
   - Upload the target job description (PDF or DOCX)

3. **Get Results**
   - The tool will analyze both documents
   - Receive keyword matching insights
   - Get optimization recommendations

4. **Refine Your Resume**
   - Use the generated insights to update your resume
   - Focus on highlighted keywords and missing terms
   - Tailor your content for maximum relevance

## 🔧 Technical Architecture

```
resume-assistant/
├── app.py                 # Main Flask application
├── input.py              # Input processing module
├── requirements.txt      # Python dependencies
├── templates/           # HTML templates
├── static/             # CSS, JS, images
└── uploads/           # Temporary file storage
```

## 🌟 Future Enhancements

### Planned Features
- **AI-Powered Suggestions**: Automatic resume improvement recommendations
- **Smart Formatting**: Auto-generate optimized resume layouts
- **Relevance Scoring**: Keyword importance and relevance metrics
- **Industry-Specific Analysis**: Tailored insights for different job sectors
- **ATS Compatibility**: Ensure resumes pass Applicant Tracking Systems

## 📊 Sample Workflow

1. **Input**: Master resume + Job description
2. **Processing**: Text extraction → Keyword analysis → Comparison
3. **Output**: Matched keywords + Missing opportunities + Recommendations
4. **Action**: Update resume based on insights

## 📄 License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute as needed.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests to help improve this tool.

---

**Ready to optimize your job applications?** 🚀 Start using the Resume Job Application Assistance Tool today!
