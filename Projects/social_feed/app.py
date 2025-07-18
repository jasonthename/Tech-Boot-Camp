from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

posts = []
post_id_counter = 1

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    global post_id_counter
    name = request.form['name']
    title = request.form['title']
    body = request.form['body']
    if name and title and body:
        posts.insert(0, {
            'id': post_id_counter,
            'name': name,
            'title': title,
            'body': body,
            'likes': 0,
            'comments': []
        })
        post_id_counter += 1
    return redirect(url_for('index'))

@app.route('/like/<int:post_id>')
def like(post_id):
    for post in posts:
        if post['id'] == post_id:
            post['likes'] += 1
            break
    return redirect(url_for('index'))

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    comment_text = request.form.get('comment')
    commenter_name = request.form.get('commenter')
    for post in posts:
        if post['id'] == post_id and comment_text and commenter_name:
            post['comments'].append({
                'name': commenter_name,
                'text': comment_text
            })
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)