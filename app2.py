from flask import Flask, render_template, request, jsonify
import re
from collections import Counter
import math

app = Flask(__name__)

class SimpleAIResumeAnalyzer:
    """
    Portfolio-ready resume analyzer using TF-IDF similarity
    Shows ML concepts without heavy dependencies
    """
    
    def __init__(self):
        # Common tech skills and their synonyms for semantic matching
        self.skill_synonyms = {
            'python': ['python', 'py', 'django', 'flask', 'fastapi'],
            'javascript': ['javascript', 'js', 'node', 'react', 'vue', 'angular'],
            'data_science': ['data science', 'machine learning', 'ml', 'ai', 'analytics', 'pandas', 'numpy'],
            'cloud': ['aws', 'azure', 'gcp', 'cloud', 'docker', 'kubernetes'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'database', 'db'],
            'frontend': ['html', 'css', 'react', 'vue', 'angular', 'frontend', 'ui', 'ux']
        }
        
    def preprocess_text(self, text):
        """Clean and tokenize text"""
        text = text.lower()
        # Remove special characters but keep important ones like + # 
        text = re.sub(r'[^\w\s#+]', ' ', text)
        words = text.split()
        return words
    
    def get_tf_idf_vector(self, words):
        """Calculate TF-IDF vector (simplified version for portfolio)"""
        word_count = Counter(words)
        total_words = len(words)
        
        # Term Frequency
        tf = {word: count/total_words for word, count in word_count.items()}
        
        # Simple IDF (would normally use document corpus)
        # For portfolio demo, using word frequency as inverse document frequency
        idf = {word: math.log(total_words / count) for word, count in word_count.items()}
        
        # TF-IDF
        tfidf = {word: tf[word] * idf[word] for word in tf}
        return tfidf
    
    def semantic_similarity(self, resume_words, job_words):
        """Enhanced similarity using skill synonyms"""
        resume_expanded = set(resume_words)
        job_expanded = set(job_words)
        
        # Expand with synonyms
        for category, synonyms in self.skill_synonyms.items():
            if any(synonym in resume_words for synonym in synonyms):
                resume_expanded.update(synonyms)
            if any(synonym in job_words for synonym in synonyms):
                job_expanded.update(synonyms)
        
        intersection = len(resume_expanded.intersection(job_expanded))
        union = len(resume_expanded.union(job_expanded))
        
        return intersection / union if union > 0 else 0
    
    def extract_skills(self, text):
        """Extract technical skills from text"""
        words = self.preprocess_text(text)
        found_skills = []
        
        for category, synonyms in self.skill_synonyms.items():
            for synonym in synonyms:
                if synonym in words:
                    found_skills.append(synonym)
        
        return list(set(found_skills))
    
    def analyze_match(self, resume_text, job_text):
        """Main analysis function - returns detailed match results"""
        resume_words = self.preprocess_text(resume_text)
        job_words = self.preprocess_text(job_text)
        
        # Calculate different similarity scores
        basic_similarity = len(set(resume_words).intersection(set(job_words))) / len(set(resume_words + job_words))
        semantic_similarity = self.semantic_similarity(resume_words, job_words)
        
        # Extract skills
        resume_skills = self.extract_skills(resume_text)
        job_skills = self.extract_skills(job_text)
        
        # Matching skills
        matching_skills = list(set(resume_skills).intersection(set(job_skills)))
        missing_skills = list(set(job_skills) - set(resume_skills))
        
        # Final score (weighted)
        final_score = (basic_similarity * 0.3 + semantic_similarity * 0.7) * 100
        
        return {
            'overall_score': round(final_score, 1),
            'basic_similarity': round(basic_similarity * 100, 1),
            'semantic_similarity': round(semantic_similarity * 100, 1),
            'resume_skills': resume_skills,
            'job_skills': job_skills,
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'recommendations': self.get_recommendations(missing_skills, final_score)
        }
    
    def get_recommendations(self, missing_skills, score):
        """Generate improvement recommendations"""
        recommendations = []
        
        if score < 30:
            recommendations.append("Consider tailoring your resume more closely to this job")
        if score < 50:
            recommendations.append("Highlight relevant projects and experience")
        
        if missing_skills:
            recommendations.append(f"Consider learning: {', '.join(missing_skills[:3])}")
        
        if not recommendations:
            recommendations.append("Great match! Your resume aligns well with this position")
            
        return recommendations

# Initialize the analyzer
analyzer = SimpleAIResumeAnalyzer()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        resume_text = data.get('resume', '')
        job_text = data.get('job_description', '')
        
        if not resume_text or not job_text:
            return jsonify({'error': 'Please provide both resume and job description'}), 400
        
        # Perform AI analysis
        results = analyzer.analyze_match(resume_text, job_text)
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)



'''
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
'''