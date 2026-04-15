from http.server import BaseHTTPRequestHandler
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            payload = json.loads(body)
            
            try:
                api_request = json.dumps({
                    'model': 'claude-opus-4-1-20250805',
                    'max_tokens': 1000,
                    'system': payload.get('system'),
                    'messages': payload.get('messages')
                }).encode('utf-8')
                
                req = urllib.request.Request(
                    'https://api.anthropic.com/v1/messages',
                    data=api_request,
                    headers={
                        'Content-Type': 'application/json',
                        'x-api-key': 'f0fce6bd-9129-448e-99c4-13118be34554'
                    }
                )
                
                with urllib.request.urlopen(req) as response:
                    api_response = response.read()
                    
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(api_response)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
