import discord
from discord.ext import commands, tasks
import youtube_dl
from random import choice


youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
	'format': 'bestaudio/best',
	'outtmpl':'%(extractor)s-%(id)s-%(title)s.%(ext)s',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0'
}

ffmpeg_options = {
	'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


client = commands.Bot(command_prefix = ">")

@client.event
async def on_ready():
	change_status.start()
	print("Djak 7afid")


status = ["with little kids", "chila", "lala manich nel3eb"]


@tasks.loop(seconds=20)
async def change_status():
	await client.change_presence(activity=discord.Game(choice(status)))

@client.command(name="ping", help="this commands returns the latency of the bot i think")
async def ping(ctx):
	await ctx.send(f"**Pong!** Latency:{round(client.latency * 1000)}ms")

@client.command(name="die", help="give the bot a death sentence")
async def die(ctx):
	responces=["why have you brought my short life to an end","I have a famillia, kill them instead","yes please!","no lol","no u","kima 9alek ice cube, niggas whith attitude"]
	await ctx.send(choice(responces))

@client.command(name="hello", help="wiiii 7bibiiii")
async def hello(ctx, *args):
	await ctx.send("Ouii papiii " + " ".join(args))


@client.command(name='play', help='This command makes the bot join the voice channel')
async def play(ctx, url=""):
	if not ctx.message.author.voice:
		await ctx.send("connect to a voice channle oumbe3d sahel")
		return
    
	else:
		channel = ctx.message.author.voice.channel

	if not ctx.message.guild.voice_client:
		await channel.connect()


		server = ctx.message.guild
		voice_channle = server.voice_client
		if url == "":
			return
		else:
			async with ctx.typing():
				player = await YTDLSource.from_url(url, loop=client.loop)
				voice_channle.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
				await ctx.send(f'**Now playing:** {player.title}')
	else:
		
		server = ctx.message.guild
		voice_channle = server.voice_client
		if url == "":
			return
		else:
			async with ctx.typing():
				player = await YTDLSource.from_url(url, loop=client.loop)
				voice_channle.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
				await ctx.send(f'**Now playing:** {player.title}')





@client.command(name="stop", help="used to stops the song and kicks the bot out of the voice channle")
async def stop(ctx):
	if ctx.message.guild.voice_client:
		voice_client = ctx.message.guild.voice_client
		await ctx.send("sar heka t7awzouni")
		await voice_client.disconnect()
	else:
		await ctx.send("manich mconecti")


@client.command(name='skip', help='This command stops the song!')
async def skip(ctx):
	if ctx.message.guild.voice_client:
		server = ctx.message.guild
		voice_channel = server.voice_client
		await ctx.send("Skipped :rage:")

		voice_channel.stop()
	else:
		await ctx.send("manich mconecti")


client.run("token here")
