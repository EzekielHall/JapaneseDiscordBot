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

# NOTE: Depriciated until furthur notice
# @bot.tree.command(name="translate-to-english", description="Replies with a translation to English.", guild=discord.Object(id=GUILD_ID))
# async def botTranslateToEnglish(interaction: discord.Interaction, message: str):
#     text = translateToEnglish(message)
#     await interaction.channel.send(text)

# @bot.tree.command(name="translate-to-japanese", description="Replies with a translation to Japanese.", guild=discord.Object(id=GUILD_ID))
# async def botTranslateToJapanese(interaction: discord.Interaction, text_to_translate: str):
#     text = translateToJapanese(text_to_translate)

#     nickname = interaction.user.nick
#     if nickname:
#         desc_text = "Requested by: " + nickname + f" ({interaction.user.name})"
#     else:
#         desc_text = "Requested by: " + interaction.user.name

#     embed = discord.Embed(
#         title = "Translation to Japanese",
#         description = desc_text,
#         color = discord.Color.red()
#     )
#     embed.add_field(name="Original", value=text_to_translate, inline=False)
#     embed.add_field(name="Translated", value=text, inline=False)

#     await interaction.channel.send(embed=embed)

@bot.tree.command(name="debug", description="Check the bot's stats/info.", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(
        f"Latency is {latency}ms\n",
        f"Uptime: {timedelta(time() - BOOT_TIME)}"
    )

bot.run(TOKEN)