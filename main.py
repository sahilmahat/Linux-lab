from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import Base, engine
from app.routes import auth_routes, issues_routes
from app import models
from app.routes import auth_routes, issues_routes, ai_routes

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LinuxLab", version="2.0")

# Include routers
app.include_router(auth_routes.router)
app.include_router(issues_routes.router)
app.include_router(ai_routes.router)
# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")
@app.get("/login")
def login_page():
    return FileResponse("static/login.html")

@app.get("/signup")
def signup_page():
    return FileResponse("static/signup.html")

@app.get("/dashboard")
def dashboard_page():
    return FileResponse("static/dashboard.html")
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
        ],
        "ram-full": [
            "Check memory usage: `free -h`",
            "Find memory-hungry processes: `ps aux --sort=-%mem | head -10`",
            "Clear page cache: `sudo sync && sudo sysctl -w vm.drop_caches=3`",
            "Check swap usage: `swapon --show`",
            "Kill a process: `kill -9 <PID>`"
        ],
        "swap-full": [
            "Check swap: `swapon --show`",
            "Disable and re-enable swap: `sudo swapoff -a && sudo swapon -a`",
            "Consider adding more swap: `sudo fallocate -l 2G /swapfile`"
        ],
        "ssh-connection-refused": [
            "Check if SSH service is running: `sudo systemctl status ssh`",
            "Start SSH if stopped: `sudo systemctl start ssh`",
            "Check SSH port: `sudo ss -tlnp | grep ssh`",
            "Allow SSH through firewall: `sudo ufw allow 22`"
        ],
        "ssh-permission-denied": [
            "Verify SSH key permissions: `chmod 600 ~/.ssh/id_rsa`",
            "Check authorized_keys: `cat ~/.ssh/authorized_keys`",
            "Check SSH config: `sudo nano /etc/ssh/sshd_config`",
            "Restart SSH: `sudo systemctl restart ssh`"
        ],
        "ssh-timeout": [
            "Check network connectivity: `ping <server-ip>`",
            "Check firewall rules: `sudo ufw status`",
            "Try verbose mode: `ssh -v user@server`"
        ],
        "apt-update-error": [
            "Fix broken packages: `sudo apt --fix-broken install`",
            "Clean apt cache: `sudo apt clean && sudo apt autoclean`",
            "Update package list: `sudo apt update`",
            "Try: `sudo dpkg --configure -a`"
        ],
        "package-not-found": [
            "Update package list first: `sudo apt update`",
            "Search for package: `apt search <package-name>`",
            "Enable universe repo: `sudo add-apt-repository universe`",
            "Try snap: `sudo snap install <package-name>`"
        ],
        "dpkg-locked": [
            "Find locking process: `sudo lsof /var/lib/dpkg/lock-frontend`",
            "Kill that process: `sudo kill -9 <PID>`",
            "Remove lock files: `sudo rm /var/lib/dpkg/lock-frontend`",
            "Fix dpkg: `sudo dpkg --configure -a`"
        ],
        "port-blocked": [
            "Check firewall status: `sudo ufw status verbose`",
            "Allow a specific port: `sudo ufw allow <port>`",
            "Check if port is in use: `sudo ss -tlnp | grep <port>`",
            "Reload firewall: `sudo ufw reload`"
        ],
        "firewall-locked-out": [
            "Disable ufw temporarily: `sudo ufw disable`",
            "Allow your IP: `sudo ufw allow from <your-ip>`",
            "Re-enable: `sudo ufw enable`"
        ],
        "check-open-ports": [
            "List all open ports: `sudo ss -tlnp`",
            "Check specific port: `sudo ss -tlnp | grep <port>`",
            "Using netstat: `sudo netstat -tulpn`"
        ],
        "process-not-responding": [
            "Find the process: `ps aux | grep <process-name>`",
            "Graceful kill: `kill <PID>`",
            "Force kill: `kill -9 <PID>`",
            "Kill by name: `pkill <process-name>`"
        ],
        "zombie-process": [
            "Find zombie processes: `ps aux | grep Z`",
            "Get parent PID: `ps -o ppid= -p <zombie-PID>`",
            "Kill the parent: `kill -9 <parent-PID>`"
        ],
        "background-jobs": [
            "List background jobs: `jobs`",
            "Bring to foreground: `fg %<job-number>`",
            "Send to background: `bg %<job-number>`",
            "Run in background: `command &`",
            "Detach from terminal: `nohup command &`"
        ],
        "disk-mount-error": [
            "List all disks: `lsblk`",
            "Mount manually: `sudo mount /dev/sdX /mnt/mydisk`",
            "Check fstab: `sudo nano /etc/fstab`",
            "Verify mount: `df -h`"
        ],
        "filesystem-corrupt": [
            "Unmount first: `sudo umount /dev/sdX`",
            "Run filesystem check: `sudo fsck -y /dev/sdX`",
            "Check disk health: `sudo smartctl -a /dev/sdX`"
        ],
        "file-not-found": [
            "Search for file: `find / -name <filename> 2>/dev/null`",
            "Use locate: `locate <filename>`",
            "Update locate database: `sudo updatedb`"
        ],
        "permission-denied": [
            "Check file permissions: `ls -la <file>`",
            "Give permission: `sudo chmod 755 <file>`",
            "Change owner: `sudo chown $USER:<group> <file>`",
            "Run with sudo: `sudo <command>`"
        ],
        "user-not-in-sudoers": [
            "Switch to root: `su -`",
            "Add to sudo group: `usermod -aG sudo <username>`",
            "Edit sudoers: `visudo`"
        ],
        "add-new-user": [
            "Create user: `sudo adduser <username>`",
            "Add to sudo: `sudo usermod -aG sudo <username>`",
            "Set password: `sudo passwd <username>`"
        ],
        "service-stopped": [
            "Check status: `sudo systemctl status <service-name>`",
            "Start service: `sudo systemctl start <service-name>`",
            "Enable on boot: `sudo systemctl enable <service-name>`",
            "Check logs: `journalctl -u <service-name> -n 50`"
        ],
        "service-failed": [
            "Check what went wrong: `sudo systemctl status <service-name>`",
            "Read full logs: `journalctl -u <service-name> --no-pager`",
            "Reset failed state: `sudo systemctl reset-failed <service-name>`",
            "Restart: `sudo systemctl restart <service-name>`"
        ]
    }

    result = solutions.get(issue.lower())
    if result:
        return {"issue": issue, "steps": result}
    else:
        return {"issue": issue, "steps": ["No solution found. Try: `man <command>` or check logs with `journalctl -xe`"]}

@app.get("/issues")
def list_issues():
    return {
        "categories": {
            "Disk & Storage": ["disk-full", "disk-mount-error", "filesystem-corrupt", "file-not-found"],
            "Memory": ["ram-full", "swap-full"],
            "Network": ["no-internet", "ssh-connection-refused", "ssh-permission-denied", "ssh-timeout"],
            "Packages": ["apt-update-error", "package-not-found", "dpkg-locked"],
            "Firewall & Ports": ["port-blocked", "firewall-locked-out", "check-open-ports"],
            "Processes": ["high-cpu", "process-not-responding", "zombie-process", "background-jobs"],
            "Users & Permissions": ["permission-denied", "user-not-in-sudoers", "add-new-user"],
            "Services": ["service-not-starting", "service-stopped", "service-failed"]
        }
    }
