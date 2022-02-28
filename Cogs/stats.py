# import
from Utils.data import *

# class
class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

# all
    @commands.cooldown(config("cooldown")[0], config("cooldown")[1], commands.BucketType.user)
    @commands.command()
    async def all(self, ctx):
        embed = discord.Embed(title='All my API requests',
                              description=await request('stats', ctx.command),
                              color=color())
        await ctx.send(embed=embed)

# failed
    @commands.cooldown(config("cooldown")[0], config("cooldown")[1], commands.BucketType.user)
    @commands.command()
    async def failed(self, ctx):
        embed = discord.Embed(title='My failed API requests',
                              description=await request('stats', ctx.command),
                              color=color())
        await ctx.send(embed=embed)

# history
    @commands.cooldown(config("cooldown")[0], config("cooldown")[1], commands.BucketType.user)
    @commands.command()
    async def history(self, ctx):
        requested_list = await request('stats', ctx.command)
        embed = discord.Embed(title='My API request history',
                              color=color())
        for requested_item in requested_list:
            embed.add_field(name=requested_item["name"], value=requested_item["value"])
        await ctx.send(embed=embed)

# most_endpoint
    @commands.cooldown(config("cooldown")[0], config("cooldown")[1], commands.BucketType.user)
    @commands.command()
    async def most_endpoint(self, ctx):
        requested_data = await request('stats', ctx.command)
        embed = discord.Embed(title='My most used API endpoint',
                              description=f'{requested_data["name"]} with {requested_data["value"]} requests',
                              color=color())
        await ctx.send(embed=embed)

# most_endpoints
    @commands.cooldown(config("cooldown")[0], config("cooldown")[1], commands.BucketType.user)
    @commands.command()
    async def most_endpoints(self, ctx):
        requested_list = await request('stats', ctx.command)
        embed = discord.Embed(title='My most used API endpoints',
                              color=color())
        limiter = 0
        for requested_item in requested_list:
            if not limiter > 14:
                embed.add_field(name=requested_item["name"], value=requested_item["value"])
                limiter += 1
        await ctx.send(embed=embed)

# most_type
    @commands.cooldown(config("cooldown")[0], config("cooldown")[1], commands.BucketType.user)
    @commands.command()
    async def most_type(self, ctx):
        requested_data = await request('stats', ctx.command)
        embed = discord.Embed(title='My most used API respond type',
                              description=f'{requested_data["name"]} with {requested_data["value"]} requests',
                              color=color())
        await ctx.send(embed=embed)

# most_types
    @commands.cooldown(config("cooldown")[0], config("cooldown")[1], commands.BucketType.user)
    @commands.command()
    async def most_types(self, ctx):
        requested_list = await request('stats', ctx.command)
        embed = discord.Embed(title='My most used API respond types',
                              color=color())
        for requested_item in requested_list:
            embed.add_field(name=requested_item["name"], value=requested_item["value"])
        await ctx.send(embed=embed)

# setup
def setup(bot):
    bot.add_cog(Stats(bot))
