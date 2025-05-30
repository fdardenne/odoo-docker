#launchctl load ~/Library/LaunchAgents/com.fdardenne.odoocker.dashboard.plist
#cat /tmp/dashboard.log
from flask import Flask, render_template_string
import subprocess

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Odoo Containers</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f7fa;
            margin: 0;
            padding: 2rem;
        }
        h1 {
            color: #333;
            margin-bottom: 2rem;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }
        .card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .card h2 {
            margin-top: 0;
            font-size: 1.4rem;
            color: #222;
        }
        .card p {
            margin: 0.5rem 0;
            word-break: break-all;
        }
        .buttons {
            margin-top: 1rem;
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        .buttons a {
            text-decoration: none;
            padding: 0.5rem 0.9rem;
            border-radius: 6px;
            background-color: #1a73e8;
            color: white;
            font-weight: bold;
            transition: background-color 0.2s;
        }
        .buttons a:hover {
            background-color: #155cc0;
        }
        .small {
            font-size: 0.9rem;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>Odoo Containers</h1>
    <div class="grid">
    {% for name in containers %}
        <div class="card">
            <h3>{{ name["name"] }}</h3>
            <p class="small"><a href="http://{{ url }}.localhost" target="_blank">http://{{ name["url"] }}.localhost</a></p>
            <div class="buttons">
                <a href="http://{{ name["url"] }}.localhost/odoo?debug=assets" target="_blank">Open</a>
                <a href="http://{{ name["url"] }}.localhost/web/tests?debug=assets" target="_blank">Hoot</a>
            </div>
        </div>
    {% endfor %}
    </div>
</body>
</html>
"""

def get_odoo_containers():
    try:
        result = subprocess.run(
            ["/usr/local/bin/docker", "ps", "--format", "{{.Names}} {{.Image}}"],
            capture_output=True, text=True, check=True
        )
        containers = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            name, image = line.split(maxsplit=1)
            if "odoo" in image.lower():
                url = "".join(c if c.isalnum() or c == '-' else '-' for c in name)
                containers.append({"name": name, "url": url})
        return containers
    except subprocess.CalledProcessError:
        return []

@app.route("/")
def index():
    containers = get_odoo_containers()
    return render_template_string(TEMPLATE, containers=containers)

if __name__ == "__main__":
    app.run(debug=True)
