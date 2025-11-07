# DiscordbotDiscord Port Manager Bot

A simple, secure Discord bot that lets authorized users view, close, block, and unblock ports on a Linux (Ubuntu) server (designed for EC2).
Designed for teamwork — contains scripts, bot.py, systemd service file, and simple deployment steps.

Quick repo layout
discord-port-manager-bot/
├── bot.py
├── requirements.txt
├── .env.example
├── README.md
├── scripts/
│   ├── close_port.sh
│   ├── block_port.sh
│   └── unblock_port.sh
└── service/
    └── capstonebot.service

1. Before you start (prerequisites)

On your Ubuntu EC2 instance (or other Ubuntu server) ensure:

sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip ufw git lsof


You need a Discord bot token (create app at https://discord.com/developers/applications
).

You need your Discord user ID (enable Developer Mode in Discord then Right-click your username → Copy ID).

2. Clone & prepare the project
# clone repo or upload files
git clone https://github.com/<your-org-or-user>/discord-port-manager-bot.git
cd discord-port-manager-bot

# create venv and install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


requirements.txt (example):

discord.py==2.3.2
python-dotenv==1.0.1

3. Environment variables

Create .env in project root (DO NOT commit .env to git):

.env

DISCORD_TOKEN=your_discord_bot_token_here
AUTHORIZED_USER_ID=123456789012345678


You can also export these in shell or put them in the systemd unit (not recommended for secrets).

4. Scripts (what they do)

All scripts live in scripts/. Make them executable:

chmod +x scripts/*.sh

scripts/close_port.sh

Kills any process listening on the given port (uses lsof + kill -9).
Usage:

./scripts/close_port.sh 8080

scripts/block_port.sh

Blocks incoming TCP on the port using ufw.
Usage:

./scripts/block_port.sh 8080

scripts/unblock_port.sh

Removes the ufw block for the port.
Usage:

./scripts/unblock_port.sh 8080


Note: ufw commands require sudo. When run from the bot via subprocess, the bot process must have permissions to run those commands; if you start bot with a systemd service as the ubuntu user, sudo may ask for password. The recommended pattern is to give the service the necessary privileges (see Service section) or to use sudoers carefully. On EC2 usually running the bot as ubuntu and calling sudo from systemd is fine when service runs as root — but be mindful of security.

5. bot.py — what it does

Loads environment variables (python-dotenv).

Sets intents.message_content = True.

Commands (only allowed for AUTHORIZED_USER_ID):

!ping → simple alive check.

!ports [port] → list listeners (netstat).

!closeport <port> → runs ./scripts/close_port.sh <port>.

!blockport <port> → runs ./scripts/block_port.sh <port>.

!unblockport <port> → runs ./scripts/unblock_port.sh <port>.

!helpme → prints a list of commands.

Bot uses subprocess.check_output(..., shell=True, text=True) to call scripts and returns the script output into the channel.

6. Run the bot (manual)
source venv/bin/activate
python3 bot.py


Look in terminal for 🤖 Logged in as <botname>.

7. Run the bot as a systemd service (recommended for EC2)

Create the service unit service/capstonebot.service (example):

[Unit]
Description=Capstone Discord Bot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/discord-port-manager-bot
ExecStart=/home/ubuntu/discord-port-manager-bot/venv/bin/python3 /home/ubuntu/discord-port-manager-bot/bot.py
Restart=always
Environment="DISCORD_TOKEN=your_discord_token"
Environment="AUTHORIZED_USER_ID=your_user_id"

[Install]
WantedBy=multi-user.target


Install and start:

sudo cp service/capstonebot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable capstonebot
sudo systemctl start capstonebot
sudo systemctl status capstonebot


If your bot needs to run firewall commands via ufw and you get permission denied, either run the service as root (not ideal) or allow the necessary commands via sudoers for the service user (carefully). A common approach: run the service as a dedicated system user with sudo privileges for just the three scripts (use /etc/sudoers.d/ to limit). Don’t give NOPASSWD to wide commands.

8. How to test (step-by-step)

Start a small test listener on the EC2 instance:

# in one terminal
python3 -m http.server 8080


Verify it listens:

netstat -tuln | grep :8080
# or
sudo lsof -i :8080


In Discord (authorized user), run:

!ports 8080
!closeport 8080


Confirm closed:

netstat -tuln | grep :8080


To test firewall block/unblock (requires sudo):

!blockport 8080
# try connecting from another machine or check ufw rules
!unblockport 8080

9. Command list (for users)

!ping — bot replies pong 🏓.

!ports — list all listening sockets (netstat -tuln).

!ports <port> — list listeners for that port.

!closeport <port> — kill process listening on port.

!blockport <port> — block inbound TCP on that port (ufw).

!unblockport <port> — remove ufw block.

!helpme — show the commands overview.

10. Security & operational notes

Only the AUTHORIZED_USER_ID is allowed to invoke system commands; do not add multiple IDs unless you trust them.

Keep DISCORD_TOKEN secret. Use GitHub secrets, secrets manager, or put .env on the server only.

Do not commit .env to git. Add .env to .gitignore.

Running commands that kill processes or modify firewall rules is powerful — avoid exposing the bot to untrusted servers or users.

For ufw changes: run the service with appropriate privileges or configure sudoers to allow the scripts to run without prompting; restrict to exact script paths.

Logging: add an audit log in bot.py by appending to a logfile each action (timestamp, user ID, command, result).

11. Troubleshooting

bot.py errors about intents: enable Message Content Intent in Discord Developer Portal (Bot → Privileged Gateway Intents).

permission denied when running ufw or iptables: ensure service user has required privileges or use sudoers to allow those scripts.

No response in channel: confirm bot has Send Messages permission & is present in that channel.

netstat not installed: install net-tools with sudo apt install net-tools (or use ss).

If the service won't start — check sudo journalctl -u capstonebot -f for logs.

12. Contribution & workflow notes (team)

Recommended workflow for teammates:

Fork the repo (or create a branch).

Create a feature branch: git checkout -b feature/awesome

Make changes, run tests locally:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Commit and push the branch:

git push origin feature/awesome


Create a Pull Request to discord branch, request code review, merge after approvals.

Do not push secrets — use .env locally and GitHub Actions secrets for CI.

13. Example .env.example
DISCORD_TOKEN=your_discord_token_here
AUTHORIZED_USER_ID=123456789012345678

14. Optional improvements / roadmap

Add confirmation UI before destructive commands (reaction-based confirm).

Add audit log + remote log shipping (CloudWatch / ELK).

Add role-based authorization (allow role members, not just single user id).

Add TLS/web UI for status and quick actions (FastAPI + Uvicorn).

Add Dockerfile for containerized deploys.

15. License

Use MIT (or your preferred license). Add LICENSE file.
