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
        # Original issues
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

        # Memory issues
        "ram-full": [
            "Check memory usage: `free -h`",
            "Find memory-hungry processes: `ps aux --sort=-%mem | head -10`",
            "Clear page cache: `sudo sync && sudo sysctl -w vm.drop_caches=3`",
            "Check swap usage: `swapon --show`",
            "Kill a process: `kill -9 <PID>`"
        ],
        "swap-full": [
            "Check swap: `swapon --show`",
            "See what's using swap: `smem -s swap -r | head -10`",
            "Disable and re-enable swap to clear it: `sudo swapoff -a && sudo swapon -a`",
            "Consider adding more swap: `sudo fallocate -l 2G /swapfile`"
        ],

        # SSH problems
        "ssh-connection-refused": [
            "Check if SSH service is running: `sudo systemctl status ssh`",
            "Start SSH if stopped: `sudo systemctl start ssh`",
            "Check SSH port: `sudo ss -tlnp | grep ssh`",
            "Check firewall: `sudo ufw status`",
            "Allow SSH through firewall: `sudo ufw allow 22`"
        ],
        "ssh-permission-denied": [
            "Check your username is correct",
            "Verify SSH key permissions: `chmod 600 ~/.ssh/id_rsa`",
            "Check authorized_keys: `cat ~/.ssh/authorized_keys`",
            "Check SSH config: `sudo nano /etc/ssh/sshd_config`",
            "Restart SSH: `sudo systemctl restart ssh`"
        ],
        "ssh-timeout": [
            "Check network connectivity: `ping <server-ip>`",
            "Verify the server IP/hostname is correct",
            "Check firewall rules on server: `sudo ufw status`",
            "Try with verbose mode: `ssh -v user@server`"
        ],

        # Package manager issues
        "apt-update-error": [
            "Fix broken packages: `sudo apt --fix-broken install`",
            "Clean apt cache: `sudo apt clean && sudo apt autoclean`",
            "Update package list: `sudo apt update`",
            "Remove bad repo if any: `sudo nano /etc/apt/sources.list`",
            "Try: `sudo dpkg --configure -a`"
        ],
        "package-not-found": [
            "Update package list first: `sudo apt update`",
            "Search for package: `apt search <package-name>`",
            "Check if universe repo is enabled: `sudo add-apt-repository universe`",
            "Try snap: `sudo snap install <package-name>`"
        ],
        "dpkg-locked": [
            "Find the process locking dpkg: `sudo lsof /var/lib/dpkg/lock-frontend`",
            "Kill that process: `sudo kill -9 <PID>`",
            "Remove lock files: `sudo rm /var/lib/dpkg/lock-frontend`",
            "Fix dpkg: `sudo dpkg --configure -a`",
            "Then retry: `sudo apt update`"
        ],

        # Firewall & ports
        "port-blocked": [
            "Check firewall status: `sudo ufw status verbose`",
            "Allow a specific port: `sudo ufw allow <port>`",
            "Allow a service: `sudo ufw allow ssh` or `sudo ufw allow http`",
            "Check if port is in use: `sudo ss -tlnp | grep <port>`",
            "Reload firewall: `sudo ufw reload`"
        ],
        "firewall-locked-out": [
            "If on a VPS, use the provider's console to access",
            "Disable ufw temporarily: `sudo ufw disable`",
            "Allow your IP: `sudo ufw allow from <your-ip>`",
            "Re-enable: `sudo ufw enable`"
        ],
        "check-open-ports": [
            "List all open ports: `sudo ss -tlnp`",
            "Check specific port: `sudo ss -tlnp | grep <port>`",
            "Using netstat: `sudo netstat -tulpn`",
            "Check with nmap: `nmap localhost`"
        ],

        # Process management
        "process-not-responding": [
            "Find the process: `ps aux | grep <process-name>`",
            "Try graceful kill first: `kill <PID>`",
            "Force kill if needed: `kill -9 <PID>`",
            "Kill by name: `pkill <process-name>`",
            "Kill all instances: `killall <process-name>`"
        ],
        "zombie-process": [
            "Find zombie processes: `ps aux | grep Z`",
            "Get parent PID: `ps -o ppid= -p <zombie-PID>`",
            "Kill the parent process: `kill -9 <parent-PID>`",
            "Zombie processes are usually harmless but indicate a bug in the parent"
        ],
        "background-jobs": [
            "List background jobs: `jobs`",
            "Bring job to foreground: `fg %<job-number>`",
            "Send to background: `bg %<job-number>`",
            "Run a command in background: `command &`",
            "Detach from terminal: `nohup command &`"
        ],

        # File system errors
        "disk-mount-error": [
            "List all disks: `lsblk`",
            "Check disk info: `sudo fdisk -l`",
            "Mount manually: `sudo mount /dev/sdX /mnt/mydisk`",
            "Check fstab for errors: `sudo nano /etc/fstab`",
            "Verify mount: `df -h`"
        ],
        "filesystem-corrupt": [
            "Unmount the disk first: `sudo umount /dev/sdX`",
            "Run filesystem check: `sudo fsck -y /dev/sdX`",
            "If root filesystem, boot into recovery mode first",
            "Check disk health: `sudo smartctl -a /dev/sdX`"
        ],
        "file-not-found": [
            "Search for file: `find / -name <filename> 2>/dev/null`",
            "Search in current directory: `find . -name <filename>`",
            "Use locate for faster search: `locate <filename>`",
            "Update locate database: `sudo updatedb`"
        ],

        # User & group management
        "permission-denied": [
            "Check file permissions: `ls -la <file>`",
            "Give yourself permission: `sudo chmod 755 <file>`",
            "Change file owner: `sudo chown $USER:<group> <file>`",
            "Run with sudo: `sudo <command>`",
            "Check your groups: `groups`"
        ],
        "user-not-in-sudoers": [
            "Switch to root: `su -`",
            "Add user to sudo group: `usermod -aG sudo <username>`",
            "Or edit sudoers file: `visudo`",
            "Verify: `groups <username>`"
        ],
        "add-new-user": [
            "Create user: `sudo adduser <username>`",
            "Add to sudo group: `sudo usermod -aG sudo <username>`",
            "Set password: `sudo passwd <username>`",
            "Verify user: `id <username>`"
        ],

        # Service checker
        "service-stopped": [
            "⚠️ Your service appears to be stopped!",
            "Check status: `sudo systemctl status <service-name>`",
            "Start the service: `sudo systemctl start <service-name>`",
            "Enable on boot: `sudo systemctl enable <service-name>`",
            "Check logs if it fails: `journalctl -u <service-name> -n 50`"
        ],
        "service-failed": [
            "⚠️ Service is in FAILED state!",
            "Check what went wrong: `sudo systemctl status <service-name>`",
            "Read full logs: `journalctl -u <service-name> --no-pager`",
            "Reset failed state: `sudo systemctl reset-failed <service-name>`",
            "Try restarting: `sudo systemctl restart <service-name>`"
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
            "File System": ["disk-mount-error", "filesystem-corrupt", "file-not-found"],
            "Users & Permissions": ["permission-denied", "user-not-in-sudoers", "add-new-user"],
            "Services": ["service-not-starting", "service-stopped", "service-failed"]
        }
    }
