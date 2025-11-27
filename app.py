from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# --- KONFIGURASI API ---
API_KEY = "485187c230mshd0a33d5fe8862cfp12b74fjsn9e02ec64df70"
API_HOST = "tiktok-video-downloader-api.p.rapidapi.com"
API_URL = "https://tiktok-video-downloader-api.p.rapidapi.com/media"

def get_tiktok_video_info(tiktok_link):
    querystring = {"videoUrl": tiktok_link}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    try:
        print(f"Sedang memproses: {tiktok_link}")
        response = requests.get(API_URL, headers=headers, params=querystring)
        data = response.json()
        
        print("Hasil dari API:", data) 

        # --- PERBAIKAN LOGIKA DISINI ---
        # Berdasarkan log kamu, link download ada di key 'downloadUrl'
        if 'downloadUrl' in data:
            return {
                "status": "success",
                "title": data.get('description', 'Video TikTok'),
                "download_url": data.get('downloadUrl'), 
                "thumbnail": data.get('cover')
            }
        else:
            return {"status": "error", "message": "Gagal. API tidak memberikan link download."}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    req_data = request.json
    url_input = req_data.get('url')
    
    if not url_input:
        return jsonify({"status": "error", "message": "Link tidak boleh kosong!"})
    
    result = get_tiktok_video_info(url_input)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)