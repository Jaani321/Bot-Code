import discord
from discord.ext import commands
import youtube_dl
import os
import json

# Load config
with open("config.json") as f:
    config = json.load(f)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Pehle voice channel me join ho jao.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Main kisi bhi voice channel me nahi hoon.")

@bot.command()
async def play(ctx, url):
    if not ctx.voice_client:
        await ctx.invoke(bot.get_command('join'))

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': 'song.%(ext)s',
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    ctx.voice_client.stop()
    ctx.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename),
                          after=lambda e: os.remove(filename))

    await ctx.send(f"Playing: {info['title']}")

bot.run(config["token"])
