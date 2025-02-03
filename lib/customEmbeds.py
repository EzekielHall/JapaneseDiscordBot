import discord
from lib.japanesedata import Grammar, Word


def generateTranslationEmbed(result: list[str, str], passage: str, nickname: str, interaction: discord.Interaction) -> discord.Embed:
    embed = discord.Embed(
        color = discord.Color.red()
    )

    embed.add_field(
        name = "Translated (" + ("日本語)" if result[1] == "en" else "English)"),
        value = result[0],
        inline = False
    )

    embed.add_field(
        name = "Original (" + ("English)" if result[1] == "en" else "日本語)"),
        value = passage,
        inline = False
    )

    embed.set_footer(
        text = (nickname if nickname else interaction.user.name) + "さんからの依頼"
    )

    return embed

def generateDebugEmbed(latency: int, uptime: int) -> discord.Embed:
    embed = discord.Embed(
        color = discord.Color.yellow()
    )

    embed.add_field(
        name = "Latency:",
        value = f"{latency}ms",
        inline = False
    )

    embed.add_field(
        name = "Uptime:",
        value = f"{uptime}",
        inline = False
    )

    return embed

def genereateWordEmbed(word: Word) -> discord.Embed:
    embed = discord.Embed(
        color=discord.Color.red()
    )

    embed.add_field(
        name = "Word",
        value = word.word,
        inline=False
    )

    embed.add_field(
        name = "Kana",
        value = word.kana,
        inline=False
    )

    embed.add_field(
        name = "Meaning",
        value = word.meaning,
        inline=False
    )

    embed.add_field(
        name = "Part of Speech",
        value = word.partOfSpeech,
        inline = False
    )

    embed.add_field(
        name = "Example Sentence (JP)",
        value = word.japaneseExample,
        inline = False
    )

    embed.add_field(
        name = "Example Sentence (EN)",
        value = f"||{word.englishExample}||"
    )

    embed.add_field(
        name = "Jisho Link",
        value = word.jishoLink,
        inline = False
    )

    return embed


def generateGrammarEmbed(grammar: Grammar) -> discord.Embed:
    embed = discord.Embed(
        color=discord.Color.red()
    )

    embed.add_field(
        name = "Word",
        value = grammar.word,
        inline=False
    )

    embed.add_field(
        name = "Romaji",
        value = grammar.romaji,
        inline=False
    )

    embed.add_field(
        name = "Meaning",
        value = grammar.meaning,
        inline=False
    )

    for i, example in enumerate(grammar.exampleSentences):
        embed.add_field(
            name = f"Example Sentence {i+1}",
            value = f"{example[0]}\n||{example[1]}||",
            inline=False
        )

    embed.add_field(
        name = "More Details",
        value = grammar.pageLink,
        inline=False
    )

    embed.set_image(
        url = grammar.imageNoteLink
    )

    return embed

def generateDailyWordEmbed(index: int, word: Word) -> discord.Embed:
    embed: discord.Embed = genereateWordEmbed(word)
    embed.title = f"Daily Word Day {index+1}"
    return embed

def generateDailyGrammarEmbed(index: int, grammar: Grammar) -> discord.Embed:
    embed: discord.Embed = generateGrammarEmbed(grammar)
    embed.title = f"Daily Grammar Day {index+1}"
    return embed
