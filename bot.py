import discord
from discord import app_commands
from discord.ext import commands
from time import time
from datetime import timedelta
from os import path

from lib.myLogging import log
from lib.initConfig import importConfig
from lib.translation import CustomTranslator
from lib.userdata import UserDataHandler

BOOT_TIME = time()
translator = CustomTranslator()
userdataHandler = UserDataHandler()

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
    await interaction.response.send_message("Processing your request...", ephemeral=True, delete_after=5)

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

    userdataHandler.incrementTranslationCount(interaction.user)

    log(
        (nickname if nickname else interaction.user.name) + " used /translate : " + passage + "  -->  " + result[0]
    )

    await interaction.channel.send(embed=languageEmbed)

@bot.tree.command(name="debug", description="Check the bot's stats/info.", guild=discord.Object(id=GUILD_ID))
async def debug(interaction: discord.Interaction):
    if userdataHandler.getUser(interaction.user)["admin"]:
        latency = round(bot.latency * 1000)
        uptime = timedelta(seconds=int(time() - BOOT_TIME))

        debug_msg = (
            f"Latency is {latency}ms\n" +
            f"Uptime: {uptime}"
        )

        debug_log_msg = (
            f"{interaction.user.name}; Latency: {latency}; Uptime: {uptime}"
        )

        log(debug_log_msg)
        await interaction.response.send_message(debug_msg)
    else:
        await interaction.response.send_message("You do not have permission to debug.")

@bot.command(name = "getData")
async def reload(ctx: commands.Context):
    if userdataHandler.getUser(ctx.author)["admin"]:
        if path.exists("./data/userdata.json"):
            userdataFile = discord.File("./data/userdata.json", filename=f"{int(time())}.json")
            await ctx.author.send(file = userdataFile)
    else:
        await ctx.send("You do not have permission to use this.", delete_after = 5)
    await ctx.message.delete()

@bot.tree.command(name="reload", description="Reloads various parts of the bot.", guild=discord.Object(id=GUILD_ID))
async def reload(interaction: discord.Interaction):
    # TODO: Add stuff that should be reloaded here
    if not userdataHandler.getUser(interaction.author)["admin"]:
        await interaction.response.send_message("You do not have permission to debug.", delete_after=5)
    else:
        pass

bot.run(TOKEN)