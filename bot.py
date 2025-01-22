import discord
from discord import app_commands
from discord.ext import commands
from time import time
from datetime import timedelta

from lib.logging import log
from lib.initConfig import importConfig
from lib.translation import CustomTranslator

BOOT_TIME = time()
translator = CustomTranslator()

# Config reading
CONFIG = importConfig()
TOKEN = CONFIG["DISCORD"]["BOT_TOKEN"]
GUILD_ID = CONFIG["DISCORD"]["GUILD_ID"]

# Disdcord bot initialization
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">", intents=intents)


@bot.event
async def on_ready():
    try:
        await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        log(f"Logged in as {bot.user}.")
    except Exception as e:
        log(f"Failed to sync commands: {e}")

@bot.tree.command(name="translate", description="Auto-detects and translates sentences.", guild=discord.Object(id=GUILD_ID))
async def botTranslateToEnglish(interaction: discord.Interaction, passage: str):
    await interaction.response.send_message("Processing your request...", ephemeral=True)

    result = translator.translate(passage)
    if result == None:
        await interaction.channel.send(f"Prompt: {passage}\nNeither English or Japanese deteced.")
        return
    
    nickname = interaction.user.nick
    
    languageEmbed = discord.Embed(
        color = discord.Color.red()
    )

    languageEmbed.add_field(
        name = "Translated (" + ("日本語)" if result[1] == "en" else "English)"),
        value = result[0],
        inline = False
    )

    languageEmbed.add_field(
        name = "Original (" + ("English)" if result[1] == "en" else "日本語)"),
        value = passage,
        inline = False
    )

    languageEmbed.set_footer(
        text = (nickname if nickname else interaction.user.name) + "さんからの依頼"
    )

    log(
        (nickname if nickname else interaction.user.name) + " used /translate : " + passage + "  -->  " + result[0]
    )

    await interaction.channel.send(embed=languageEmbed)

@bot.tree.command(name="debug", description="Check the bot's stats/info.", guild=discord.Object(id=GUILD_ID))
async def debug(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    uptime = timedelta(time() - BOOT_TIME)

    debug_msg = (
        f"Latency is {latency}ms\n" +
        f"Uptime: {uptime}"
    )

    debug_log_msg = (
        f"Latency: {latency}; Uptime: {uptime}"
    )

    log(debug_log_msg)
    await interaction.response.send_message(debug_msg)

bot.run(TOKEN)