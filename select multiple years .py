from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    batch_options = [
        {"value": "None", "label": "None"},
        {"value": "I", "label": "2021-2025"},
        {"value": "II", "label": "2021-2025"},
        {"value": "III", "label": "2021-2025"},
        {"value": "IV", "label": "All"}
    ]
    
    selected_batches = []
    if request.method == 'POST':
        selected_batches = request.form.getlist('batch')
    
    return render_template('index.html', batch_options=batch_options, selected_batches=selected_batches)

if __name__ == '__main__':
    app.run(debug=True)
