import discord
from discord.ext import commands
import random
import re
from urllib.request import urlopen

# The prefix that the bot responds to
client = commands.Bot(command_prefix=">")


# Defenition of news function with the number of articles as a parameter
def bbcnews(num_art):
    url = 'http://feeds.bbci.co.uk/news/world/rss.xml'  # URL
    page = urlopen(url).read()
    html = page.decode("utf-8")  # Make the url content into a string

    # Patterns that enclose each respective attribute
    patternItem = "<item.*?>.*?</item.*?>"
    patternTitle = '<title.*?>.*?</title.*?>'
    patternLink = '<link.*?>.*?</link.*?>'
    patternDate = '<pubDate.*?>.*?</pubDate.*?>'
    patternLastBuild = '<lastBuildDate.*?>.*?</lastBuildDate.*?>'

    news_items = re.findall(patternItem, str(html), re.DOTALL | re.IGNORECASE)
    news = []

    latdate = re.search(patternLastBuild, html, re.IGNORECASE).group()
    latdate = re.sub("<lastBuildDate.*?>|</lastBuildDate.*?>", "", latdate)
    y = 0

    while y != num_art:  # loop to only fetch as many articles as specified
        # Getting our title for each news_items in position y
        title = re.search(patternTitle, news_items[y], re.IGNORECASE).group()
        title = re.sub("<title.*?\[CDATA\[|]]></title.*?>", "", title)
        news.append("**" + title + "**")

        # Getting our date for each item
        date = re.search(patternDate, news_items[y], re.IGNORECASE).group()
        date = re.sub("<pubDate>|</pubDate.*?>", "", date)
        news.append(date)

        # Getting our links, cutting the html, and writing them in
        link = re.search(patternLink, news_items[y], re.IGNORECASE).group()
        link = re.sub("<link.*?>|</link.*?>", "", link)
        news.append("<" + link + ">")
        y += 1

    return news


@client.event  # On ready message
async def on_ready():
    print("Bot is ready")


@client.command()  # Command that will respond with the user's ping
async def wifidiff(ctx):
    await ctx.send(f"Diff: {round(client.latency * 1000)}ms")


@client.command()  # Command that will role a die of the client's choice
async def roll(ctx, *, num):
    val = str(random.randint(1, int(num)))
    print("User rolled" + val)
    await ctx.send(val)


@client.command()  # Command that will show x most recent news artiles from bbc
async def news(ctx, *, num_art):
    arts = bbcnews(int(num_art))
    for x in arts:
        await ctx.send(x)


@client.command()
async def commands(ctx):
    await ctx.send("Use \'>\' to send a command. My commands include news: \'>news (number of articles)\', dice: \'>roll (sides of die)\' and ping: \'>wifidiff\'")
    # Oops, I think I broke my style guide here...

client.run("enter bot token")
