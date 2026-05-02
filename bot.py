import discord
from discord.ext import commands
from mcrcon import MCRcon

DISCORD_TOKEN = ""

RCON_HOST = "localhost" 
RCON_PORT = 25575
RCON_PASSWORD = ""

ALLOWED_USER_IDS = [] 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def send_rcon_command(command: str) -> str:
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            return mcr.command(command)
    except Exception as e:
        return f"Error: {e}"
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    
@bot.command()
async def hello(ctx):
    await ctx.send("Hello from Discord bot!")

@bot.command()
async def say(ctx, *, message):
    send_rcon_command(f"say [Discord] {message}")
    await ctx.send("✅ Sent to Minecraft")

@bot.command()
async def players(ctx):
    response = send_rcon_command("list")
    await ctx.send(f"```{response}```")

@bot.command()
async def kick(ctx, player: str):
    if ctx.author.id not in ALLOWED_USER_IDS:
        return await ctx.send("❌ You are not allowed to use this command.")

    send_rcon_command(f"kick {player}")
    await ctx.send(f"👢 Kicked {player}")

@bot.command()
async def ban(ctx, player: str, *, reason="Banned by admin"):
    if ctx.author.id not in ALLOWED_USER_IDS:
        return await ctx.send("❌ You are not allowed to use this command.")

    send_rcon_command(f"ban {player} {reason}")
    await ctx.send(f"🔨 Banned {player} | Reason: {reason}")

@bot.command()
async def unban(ctx, player: str, *, reason="Unbanned by admin"):
    if ctx.author.id not in ALLOWED_USER_IDS:
        return await ctx.send("❌ You are not allowed to use this command.")

    send_rcon_command(f"pardon {player}")
    await ctx.send(f"🔨 Unbanned {player} | Reason: {reason}")

@bot.command()
async def cmd(ctx, *, command: str):
    if ctx.author.id not in ALLOWED_USER_IDS:
        return await ctx.send("❌ You are not allowed to use this command.")

    response = send_rcon_command(command)
    await ctx.send(f"```{response}```")

bot.run(DISCORD_TOKEN)
