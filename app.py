from flask import Flask, request, send_file, render_template, jsonify
from gtts import gTTS
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_tts():
    data = request.json
    text = data.get('text', '').strip()
    lang = data.get('lang', 'id')

    if not text:
        return jsonify({"error": "Teks tidak boleh kosong!"}), 400

    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang=lang)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        return send_file(
            mp3_fp, 
            mimetype="audio/mpeg", 
            as_attachment=True, 
            download_name=f"voice-{lang}.mp3"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
