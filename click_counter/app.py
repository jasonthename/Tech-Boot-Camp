from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'super-secret-key'

# Use filesystem-based session (so it's not just in memory)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    # Initialize click count in session
    if 'clicks' not in session:
        session['clicks'] = 0
    return render_template('index.html', clicks=session['clicks'])

@app.route('/click')
def click():
    # Increment the click counter
    session['clicks'] = session.get('clicks', 0) + 1
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session['clicks'] = 0
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)