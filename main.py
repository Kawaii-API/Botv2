from Utils.data import *

# file check
logger.info('\u001b[35m[CHECK] Starting the file check...')
for file in ['Utils/data.py', 'Data/tokens.json', 'Data/config.json', 'Cogs/gif.py', 'Cogs/image.py', 'Cogs/info.py', 'Cogs/stats.py', 'Cogs/text.py']:
    try:
        pathlib.Path(file).resolve(strict=True)
    except FileNotFoundError:
        logger.warning(f'{file} file not found (Press enter to start anyway)')
        input('')
        logger.info('\u001b[33mThe warning message was skipped, so the startup procedure continues.')
    else:
        logger.info(f'\u001b[32m{file} file found')
logger.info(f'\u001b[35m[SUCCESS] Files check completed!')

# intents
intents = discord.Intents.default()
intents.message_content = True  # You will need the message content intent to run this bot. If you can't use this intent you have to rewrite the bot to slash commands.

# bot
class Kawaii(commands.AutoShardedBot):
    def __init__(self):
        self.bot = self
        self.news = None
        super().__init__(shard_count=config('shards'),
                         case_insensitive=True,
                         command_prefix=config("prefix"),
                         activity=discord.Game(name=config("status")),
                         description=config("description"),
                         intents=intents,
                         help_command=None)

# load cogs
        logger.info('\u001b[35m[CHECK] Starting cog loading...')
        for filename in os.listdir('Cogs'):
            if filename.endswith('.py'):
                try:
                    self.bot.load_extension(f'Cogs.{filename[:-3]}')
                except Exception as e:
                    logger.warning(f'The cog {filename} could not be loaded (Press enter to start anyway)')
                    logger.error(e)
                    input('')
                    logger.info('\u001b[33mThe warning message was skipped, so the startup procedure continues.')
                else:
                    logger.info(f'\u001b[32mThe cog {filename} was loaded')
        logger.info(f'\u001b[35m[SUCCESS] Cog loading completed!')

# on ready
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'\u001b[35m[SUCCESS] Bot is online!')
        logger.info('\u001b[36mBot information:')
        logger.info(f'\u001b[36m-Name: {self.bot.user.name}')
        logger.info(f'\u001b[36m-ID: {self.bot.user.id}')
        logger.info(f'\u001b[36m-Developer: {await self.bot.fetch_user(config("developer"))}')
        logger.info(f'\u001b[36m-Version: {config("version")}')
        logger.info(f'\u001b[36m-Shards: {config("shards")}')
        logger.info(f'\u001b[36m-Guilds: {len(self.bot.guilds)}')
        logger.info(f'\u001b[36m-Users: {len(self.bot.users)}')

# error handler
    @commands.Cog.listener()
    async def on_command_error(self, context, error):
        if isinstance(error, CommandNotFound):
            return
        if "Unknown Message" in str(error):
            return
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title='You are on cooldown!',
                                  description=str(error).replace("You are on cooldown. ", ""),
                                  color=color())
            await send(context,
                       embed=embed,
                       view=discord.ui.View(discord.ui.Button(label=f'Help',
                                                              style=discord.ButtonStyle.link,
                                                              url=config("support"))),
                       delete_after=10)
            return
        embed = discord.Embed(title='Something went wrong!',
                              description=str(error),
                              color=color())
        await send(context,
                   embed=embed,
                   view=discord.ui.View(discord.ui.Button(label=f'Help',
                                                          style=discord.ButtonStyle.link,
                                                          url=config("support"))),
                   delete_after=10)
        logger.error(f"{context.message.content} | {error}")
        return

# process commands
    async def process_commands(self, message: discord.Message) -> None:
        ctx = await self.get_context(message)
        if not ctx.command:
            return
        if not ctx.guild:
            embed = discord.Embed(title='Command denied',
                                  description='Invite the bot into a server to use this command.',
                                  color=color())
            embed.set_footer(text='Commands are disabled in the DM\'s.')
            await send(ctx, embed=embed)
            return
        await ctx.trigger_typing()
        await self.invoke(ctx)

# run command message
    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

# close
    async def close(self):
        await super().close()

# run
    def run(self):
        super().run(tokens("discord"),
                    reconnect=True)


# main
if __name__ == '__main__':
    bot = Kawaii()
    try:
        bot.run()
    except Exception:
        logger.error(f'The login attempt failed due to an invalid discord token!')
