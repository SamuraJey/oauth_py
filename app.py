from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    words = []
    if request.method == 'POST':
        words_str = request.form['words']
        words = [word.strip() for word in words_str.split(',') if word.strip()]
        if len(words) < 1:
            return render_template('index.html', error="Введите хотя бы одно слово")
        rows = int(len(words)**0.5) + 1
        cols = (len(words) + rows - 1) // rows
        words_grid = [words[i:i+cols] for i in range(0, len(words), cols)]
    else:
        words_grid = []

    return render_template('index.html', words_grid=words_grid)


@app.route('/mark_word', methods=['POST'])
def mark_word():
    word = request.form['word']
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)