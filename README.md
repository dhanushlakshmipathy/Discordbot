# Discord Port Manager Bot

A simple, secure Discord bot that lets an authorized user view, close, block, and unblock ports on an Ubuntu server (designed for EC2). Intended for small teams — includes bot.py, helper scripts, and a systemd unit example.

---

## Quick repo layout

- bot.py
- requirements.txt
- .env.example
- README.md
- scripts/
  - close_port.sh
  - block_port.sh
  - unblock_port.sh
- service/
  - capstonebot.service

---

## Features

- Authorized single-user control for:
  - List listening ports
  - Kill process listening on a port
  - Block/unblock inbound TCP via ufw
- Basic help and health check commands
- Uses subprocess to call audited scripts (scripts/*)

---

## Prerequisites (Ubuntu / EC2)

Run on the server:

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip ufw git lsof net-tools
```

Create a Discord Application and Bot at:
https://discord.com/developers/applications

Enable "Message Content Intent" for the bot in the Developer Portal.

---

## Install & run locally

1. Clone or upload repo to your server:
   git clone https://github.com/<your-org-or-user>/discord-port-manager-bot.git
   cd discord-port-manager-bot

2. Create virtualenv and install:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create `.env` in project root (DO NOT commit this file):

   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   AUTHORIZED_USER_ID=123456789012345678
   ```

4. Make scripts executable:
   ```sh
   chmod +x scripts/*.sh
   ```

5. Run:
   ```sh
   source venv/bin/activate
   python3 bot.py
   ```

Look for "🤖 Logged in as <botname>" in the terminal.

---

## Example scripts (summary)

- scripts/close_port.sh
  - Finds and kills process listening on a given port (uses lsof + kill).
  - Usage: `./scripts/close_port.sh 8080`

- scripts/block_port.sh
  - Adds a ufw deny rule for inbound TCP on the given port.
  - Usage: `./scripts/block_port.sh 8080`

- scripts/unblock_port.sh
  - Removes the deny rule for the given port.
  - Usage: `./scripts/unblock_port.sh 8080`

Note: ufw commands require sudo. See Service section for recommended approaches.

---

## bot.py — behavior

- Loads env vars via python-dotenv.
- Required intents: message_content = True.
- Only the user with ID matching AUTHORIZED_USER_ID can run commands.
- Commands:
  - `!ping` — pong 🏓
  - `!ports` — list all listening sockets (`netstat -tuln` / `ss`)
  - `!ports <port>` — show listeners for a specific port
  - `!closeport <port>` — runs `scripts/close_port.sh <port>`
  - `!blockport <port>` — runs `scripts/block_port.sh <port>`
  - `!unblockport <port>` — runs `scripts/unblock_port.sh <port>`
  - `!helpme` — prints command overview

The bot executes the scripts and returns stdout/stderr to the Discord channel. Output is audited — consider adding file-based logging.

---

## systemd service example

File: `service/capstonebot.service` (example):

```ini
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
```

Install and enable:

```sh
sudo cp service/capstonebot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable capstonebot
sudo systemctl start capstonebot
sudo systemctl status capstonebot
```

If ufw/kill needs sudo, either:
- Run service as root (not ideal), or
- Use /etc/sudoers.d/ to allow the service user to run the specific scripts with NOPASSWD and strict path constraints.

---

## Testing

Start a test listener:

```sh
python3 -m http.server 8080
```

Check listener:

```sh
netstat -tuln | grep :8080
sudo lsof -i :8080
```

From authorized Discord user run:

- `!ports 8080`
- `!closeport 8080`
- `!blockport 8080`
- `!unblockport 8080`

---

## Security notes

- Keep DISCORD_TOKEN secret. Do not commit `.env`.
- Only add trusted user IDs to AUTHORIZED_USER_ID.
- Prefer limiting sudo to explicit script paths via sudoers.
- Consider adding an audit log (timestamp, user, command, result).
- Avoid running the bot with unnecessary privileges.

---

## Troubleshooting

- Intents errors: enable Message Content Intent in Developer Portal.
- Permission denied for ufw: check sudoers or service user privileges.
- Bot not responding: ensure it has Send Messages permission and is in the channel.
- netstat missing: install net-tools or change to `ss`.

Check logs:
- Journal: `sudo journalctl -u capstonebot -f`
- bot stdout if running in terminal.

---

## Contributing

- Fork, create a branch, implement changes, run locally, open a PR.
- Do not push secrets. Use GitHub secrets for CI.

---

## .env.example

```
DISCORD_TOKEN=your_discord_token_here
AUTHORIZED_USER_ID=123456789012345678
```

---

## License

MIT (add LICENSE file)