# imports | This bot is adapted for PyCord 2.0
from discord.ext.commands import CommandNotFound
from discord.ext import commands, tasks
from pymongo import MongoClient
from datetime import datetime
from time import perf_counter
import coloredlogs
import platform
import requests
import discord
import logging
import aiohttp
import asyncio
import pathlib
import psutil
import json
import os
import re

# config
def config(argument: str):
    return json.load(open(r'Data/config.json', 'r'))[argument]

# tokes
def tokens(argument: str):
    return json.load(open(r'Data/tokens.json', 'r'))[argument]

# log
coloredlogs.install(fmt='\u001b[34m[%(asctime)s] \u001b[31m[%(levelname)s] \u001b[37m%(message)s')
logger = logging.getLogger('discord')
handler = logging.FileHandler(filename=f'Log/{datetime.utcnow().strftime("%d-%m-%Y")}.log',
                              encoding='utf-8',
                              mode='a+')
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s'))
logger.addHandler(handler)

# embed color
def color():
    return int(eval(config("color").replace("#", '0x')))

# api request
async def request(main_endpoint: str, sub_endpoint: str, response_type: str = 'json'):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://kawaii.red/api/{main_endpoint}/{sub_endpoint}/token={tokens("api")}&type={response_type}/') as r:
            js = await r.json()
            return js["response"]

# gif embed
async def send_gif(ctx, message):
    embed = discord.Embed(title=str(ctx.command).capitalize(),
                          color=int(eval(config("color").replace("#", '0x'))))
    if message:
        embed = discord.Embed(title=str(ctx.command).capitalize(),
                              description='> ' + message,
                              color=int(eval(config("color").replace("#", '0x'))))
    embed.set_image(url=await request('gif', ctx.command))
    await send(ctx, embed=embed)

# send message
async def send(ctx, content=None, embed=None, file=None, view=None, delete_after=None):
    try:
        msg = await ctx.message.reply(content=content,
                                      embed=embed,
                                      file=file,
                                      view=view,
                                      delete_after=delete_after,
                                      mention_author=False)
        return msg
    except Exception:
        msg = await ctx.send(content=content,
                             embed=embed,
                             file=file,
                             view=view,
                             delete_after=delete_after)
        return msg
