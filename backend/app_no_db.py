"""
Simplified Flask app for frontend testing without MongoDB
Only for UI demonstration purposes
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'online',
        'message': 'Demo mode - MongoDB not required',
        'version': '1.0.0-demo'
    }), 200

@app.route('/api/auth/login', methods=['POST'])
def demo_login():
    return jsonify({
        'message': 'Demo mode - Install MongoDB for full functionality',
        'error': 'MongoDB connection required'
    }), 503

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  DEMO MODE - Frontend UI Testing Only")
    print("  Install MongoDB for full functionality")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
