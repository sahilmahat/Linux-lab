from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/troubleshoot/{issue}")
def troubleshoot(issue: str):
    solutions = {
        "disk-full": [
            "Run: `df -h` to check disk usage",
            "Run: `du -sh /*` to find large directories",
            "Clean up with: `sudo apt autoremove && sudo apt clean`"
        ],
        "service-not-starting": [
            "Run: `systemctl status <service-name>`",
            "Check logs: `journalctl -xe`",
            "Try restarting: `sudo systemctl restart <service-name>`"
        ],
        "high-cpu": [
            "Run: `top` or `htop` to see processes",
            "Find the culprit: `ps aux --sort=-%cpu | head -10`",
            "Kill if needed: `kill -9 <PID>`"
        ],
        "no-internet": [
            "Check interface: `ip a`",
            "Ping test: `ping 8.8.8.8`",
            "Restart network: `sudo systemctl restart NetworkManager`"
        ]
    }

    result = solutions.get(issue.lower())
    if result:
        return {"issue": issue, "steps": result}
    else:
        return {"issue": issue, "steps": ["No solution found. Try: `man <command>` or check logs."]}
