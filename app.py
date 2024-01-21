from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Perform some processing based on user_input to get results
        # For simplicity, let's consider a list of results
        results = ['Result 1', 'Result 2', 'Result 3']

        return render_template('index.html', user_input=user_input, results=results)

@app.route('/redirect/<result>')
def redirect_to_link(result):
    # Perform logic to get the link related to the result
    # For simplicity, let's consider a dictionary of links
    links = {
        'Result 1': 'https://chat.openai.com/c/66c19528-1da8-4a75-8233-79a75d01f63b',
        'Result 2': 'https://example.com/link2',
        'Result 3': 'https://example.com/link3',
    }

    link = links.get(result)
    if link:
        return redirect(link)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
