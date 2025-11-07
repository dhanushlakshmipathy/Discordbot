import os
import subprocess
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


def is_authorized(ctx):
    return ctx.author.id == AUTHORIZED_USER_ID


def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)


@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")


@bot.command()
async def ping(ctx):
    await ctx.send("pong 🏓")


@bot.command()
async def ports(ctx, port: int = None):
    try:
        cmd = f"sudo netstat -tuln | grep :{port}" if port else "sudo netstat -tuln"
        out = run_cmd(cmd)
        await ctx.send(f"```\n{out[:1800]}\n```" if out.strip() else "No listeners found.")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"⚠️ Error:\n```\n{e.output}\n```")


@bot.command()
async def closeport(ctx, port: int):
    if not is_authorized(ctx):
        await ctx.send("❌ Unauthorized.")
        return
    try:
        out = run_cmd(f"./scripts/close_port.sh {port}")
        await ctx.send(out)
    except subprocess.CalledProcessError as e:
        await ctx.send(f"⚠️ Error:\n```\n{e.output}\n```")


@bot.command()
async def blockport(ctx, port: int):
    if not is_authorized(ctx):
        await ctx.send("❌ Unauthorized.")
        return
    try:
        out = run_cmd(f"./scripts/block_port.sh {port}")
        await ctx.send(out)
    except subprocess.CalledProcessError as e:
        await ctx.send(f"⚠️ Error:\n```\n{e.output}\n```")


@bot.command()
async def unblockport(ctx, port: int):
    if not is_authorized(ctx):
        await ctx.send("❌ Unauthorized.")
        return
    try:
        out = run_cmd(f"./scripts/unblock_port.sh {port}")
        await ctx.send(out)
    except subprocess.CalledProcessError as e:
        await ctx.send(f"⚠️ Error:\n```\n{e.output}\n```")


@bot.command()
async def helpme(ctx):
    help_text = (
        "**Available Commands:**\n"
        "`!ping` - check bot status\n"
        "`!ports` - show active ports\n"
        "`!closeport <port>` - kill process on port\n"
        "`!blockport <port>` - block inbound port\n"
        "`!unblockport <port>` - remove firewall block\n"
    )
    await ctx.send(help_text)


bot.run(DISCORD_TOKEN)
