from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from rembg import remove
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'

# Biar foldernya otomatis dibuat kalau belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Hapus background
            with open(filepath, 'rb') as input_file:
                input_data = input_file.read()
                output_data = remove(input_data)

            # Simpen hasil
            result_path = os.path.join(RESULT_FOLDER, file.filename)
            with open(result_path, 'wb') as output_file:
                output_file.write(output_data)

            return redirect(url_for('result', filename=file.filename))
    return render_template('index.html')

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

# Ini penting kalau mau deploy ke hosting
if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))  # Biar kalau di Railway/Render auto ambil port
    app.run(host="0.0.0.0", port=port)
