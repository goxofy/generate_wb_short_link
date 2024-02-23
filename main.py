from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SUB = ''  # Your SUB from your WB cookies
UID = '2028810631'  # sender's uid
program_version = '1.0.0'

@app.route('/generate_sh0rt_link', methods=['POST'])
def generate_short_link():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'No URL'}), 400

        message = {
            'text': url,
            'uid': UID,
            'extensions': '{"clientid": "3dsmt6xbjdfbulag51gjd8ia91npxk"}',
            'is_encoded': 0,
            'decodetime': 1,
            'source': 209678993
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.514.1919.810 Safari/537.36',
            'Cookie': f'SUB={SUB};',
            'Referer': 'https://api.weibo.com/chat/',
            'Host': 'api.weibo.com',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post("https://api.weibo.com/webim/2/direct_messages/new.json", data=message, headers=headers)
        return handle_response(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def handle_response(response):
    try:
        response_data = response.json()
        is_succeed = response_data['url_objects'][0]['info']['result']
        if is_succeed:
            short_link = response_data['url_objects'][0]['info']['url_short']
            return jsonify({'short_link': short_link})
        else:
            error_code = response_data['error_code']
            if error_code == 21301:
                return jsonify({'error': 'SUB out of date'}), 400
            return jsonify({'error': 'Unknow error'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=50000)
