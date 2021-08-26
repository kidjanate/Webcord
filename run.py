import asyncio
import discord
from discord.ext import commands
from PIL import Image
import io
import requests
from selenium import webdriver

from subprocess import Popen
from subprocess import call

import glob
import os

TOKEN = ps.getenv("TOKEN")
PREFIX = 'me!'
INTENTS = discord.Intents.default()
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')

@bot.command()
async def web(ctx, url):
    #clean <> tags
    if url.startswith("<") and url.endswith(">"):
        url = url[1:len(url)-1]

    if not str(url).startswith("https://"):
        return await ctx.send("Please type the website")

    
    
        
    print(url)
    
    msg = await ctx.send("Processing...")
    drv = webdriver.Chrome(executable_path="chromedriver.exe")
    drv.get(url)
    drv.save_screenshot("save.png")
    drv.quit()
    await msg.delete()
    await ctx.send(file=discord.File("save.png"))

@bot.command()
async def webvid(ctx, url):

    #clean <> tags
    if url.startswith("<") and url.endswith(">"):
        url = url[1:len(url)-1]

    if not str(url).startswith("https://"):
        return await ctx.send("Please type the website")

    msg = await ctx.send("Processing...")
    drv = webdriver.Chrome(executable_path="chromedriver.exe")
    drv.get(url)

    if "youtube.com" in url:
        drv.find_element_by_class_name("ytp-mute-button").click()
        drv.find_element_by_class_name("ytp-large-play-button").click()
       

    await msg.edit(content="Recording as gif file.")
    for i in range(50):
        drv.save_screenshot("session/"+str(i)+".png")
        await asyncio.sleep(0.01)

    fpin = "session/*.png"
    fpout = "out.gif"

    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fpin))]
    img.save(fp=fpout, format='GIF', append_images=imgs,
         save_all=True, duration=120, loop=0)

    for i in os.listdir("session"):
        os.remove("session/"+i)

    drv.quit()
    await msg.delete()
    await ctx.send(file=discord.File("out.gif"))



bot.run(TOKEN)
