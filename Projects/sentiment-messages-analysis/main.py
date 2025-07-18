import os
from flask import Flask, render_template, request, jsonify, Markup
from werkzeug.utils import secure_filename
from text_analysis_core import TextAnalyzer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            analyzer = TextAnalyzer()
            messages = analyzer.load_messages(filepath)
            if not messages:
                return jsonify({'error': 'No messages found in file'}), 400
            
            patterns = analyzer.analyze_patterns(messages)
            colored_messages = []
            
            for msg in messages:
                colored_messages.append({
                    'sender': msg.get('sender', 'Unknown'),
                    'text': Markup(analyzer.color_code_text(msg.get('text', ''))),
                })
            
            os.remove(filepath)
            
            return jsonify({
                'patterns': {
                    'avg_message_length': f"{patterns['avg_message_length']:.2f}",
                    'question_count': patterns['question_count'],
                    'emphasis_count': patterns['emphasis_count'],
                    'unique_senders': len(patterns['unique_senders']),
                    'top_words': [
                        {'word': word, 'count': count}
                        for word, count in patterns['word_frequency'].most_common(10)
                        if word.lower() not in analyzer.stop_words and word.isalnum()
                    ],
                    'sentiment': {
                        'positive': sum(s['pos'] for s in patterns['sentiment_trends']) / len(patterns['sentiment_trends']),
                        'negative': sum(s['neg'] for s in patterns['sentiment_trends']) / len(patterns['sentiment_trends']),
                        'neutral': sum(s['neu'] for s in patterns['sentiment_trends']) / len(patterns['sentiment_trends'])
                    }
                },
                'messages': colored_messages
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)