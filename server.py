import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# 地图：0空地 1障碍 2边界
MAP = [
    [2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,1,0,0,0,0,2],
    [2,0,1,0,1,0,1,1,0,2],
    [2,0,1,0,0,0,0,1,0,2],
    [2,0,0,0,1,0,0,0,0,2],
    [2,2,2,2,2,2,2,2,2,2],
]

robot = {"x": 1, "y": 1}  # 当前格子坐标

def can_move(nx, ny):
    if 0 <= ny < len(MAP) and 0 <= nx < len(MAP[0]):
        return MAP[ny][nx] == 0
    return False

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/map":
            self._send({"map": MAP, "robot": robot})
        elif self.path == "/state":
            self._send({"robot": robot})
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/move":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            dx, dy = body.get("dx", 0), body.get("dy", 0)
            nx, ny = robot["x"] + dx, robot["y"] + dy
            if can_move(nx, ny):
                robot["x"], robot["y"] = nx, ny
            self._send({"ok": True, "robot": robot})

    def _send(self, obj):
        data = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()