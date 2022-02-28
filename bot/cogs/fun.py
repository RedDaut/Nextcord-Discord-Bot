import nextcord, asyncio, aiohttp, io,json, random, urllib
from nextcord.ext import commands
import platform
from io import BytesIO
import utils.json

class MemeBtn(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Next Meme", style=nextcord.ButtonStyle.green, emoji="⏩")
    async def nextmeme(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        memeApi = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme")
        memeData = json.load(memeApi)

        memeUrl = memeData["url"]
        memeName = memeData["title"]
        memePoster = memeData["author"]
        memeReddit = memeData["subreddit"]
        memeLink = memeData["postLink"]

        memeEmbed = nextcord.Embed(title=memeName, color=0x14cccc)
        memeEmbed.set_author(
            name="OpenSourceGames Utility", icon_url=interaction.client.user.display_avatar)
        memeEmbed.set_image(url=memeUrl)
        memeEmbed.set_footer(
            text=f"Meme by: {memePoster} | Subreddit: {memeReddit} | Post: {memeLink}")

        await interaction.response.edit_message(embed=memeEmbed) 

    @nextcord.ui.button(label="End Interaction", style=nextcord.ButtonStyle.secondary)
    async def end(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
         await interaction.response.send_message(f"{interaction.user.mention} we have closed the interaction.", ephemeral=True) 
         for child in self.children: 
            child.disabled = True 
            await interaction.message.edit(view=self)  


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

     # Listener
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----") 
    
    @commands.command()
    async def echo(self, ctx, *, message=None):
        """
        A simple command that repeats the users input back to them.
        """
        message = message or "Please provide the message to be repeated."
        await ctx.message.delete()
        await ctx.send(message)
        
    @commands.command(name="8ball", aliases=["eightball", "8b"], description="Let the 8 Ball Predict!\n")
    async def eightball(self, ctx, *, question):
        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            "I'm feeling well",
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Better not tell you now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'I cannot predict now.',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'VEry doubtfull.',
            'I am tired. *proceeds with sleeping*',
            'As I see it, yes.',
            'Yes.',
            'Positive',
            'From my point of view, yes',
            'Convinced.',
            'Most Likley.',
            'Chances High',
            'No.',
            'Negative.',
            'Not Convinced.',
            'Perhaps.',
            'Not Sure',
            'Mayby',
            'Im to lazy to predict.'
        ]
        await ctx.send(f":8ball: Question: {question}\n:8ball: Answer: {random.choice(responses)}")

    @commands.command(name="meme", description="Replies with a meme.")
    async def meme(self, ctx):
        view = MemeBtn()
        memeApi = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme")
        memeData = json.load(memeApi)

        memeUrl = memeData["url"]
        memeName = memeData["title"]
        memePoster = memeData["author"]
        memeReddit = memeData["subreddit"]
        memeLink = memeData["postLink"]

        memeEmbed = nextcord.Embed(title=memeName, color=0x14cccc)
        memeEmbed.set_author(
            name="OpenSourceGames Utility", icon_url=self.bot.user.display_avatar)
        memeEmbed.set_image(url=memeUrl)
        memeEmbed.set_footer(
            text=f"Meme by: {memePoster} | Subreddit: {memeReddit} | Post: {memeLink}")
        await ctx.send(embed=memeEmbed, view=view)
   

    @commands.command(name="emoji", aliases=["eadd"], description="Adds an external img (through the link of the img provided) as gif in your server.")
    async def emoji(self, ctx, url: str, *, name):
        guild = ctx.guild
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    imgOrGif = BytesIO(await r.read())
                    eValue = imgOrGif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=eValue, name=name)
                        await ctx.send(f":{name}: emoji added to your server successfully!")
                        await ses.close()
                    else:
                        await ctx.send(f'😞 **Sorry we are unable to add this emoji** | {r.status}')
                except nextcord.HTTPException:
                    await ctx.send("📁 Your file size is too big.")


    @commands.command(name="emojify", description="Emojify your text here.") 
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def emojify(self, ctx, *, text):
        emojis = []
        for beans in text:
            if beans.isdecimal():
                num2word = {
                    "0" : 'zero', 
                    "1": 'one', 
                    "2": "two", 
                    "3": "three", 
                    "4" : "four", 
                    "5":"five", 
                    "6":"six", 
                    "7":"seven", 
                    "8":"eight", 
                    "9": "nine"
                }
                emojis.append(f":{num2word.get(beans)}: ")

            elif beans.isalpha():
                text = beans.lower()
                emojis.append(f":regional_indicator_{text}: ")
            elif beans == "!":
                beans = ":grey_exclamation:"
                emojis.append(beans)
            elif beans == "?":
                beans = ":grey_question:"
                emojis.append(beans)
            elif beans == "*":
                beans = ":asterisk:"
                emojis.append(beans)
            else:
                emojis.append(beans)

        await ctx.send(''.join(emojis))

    
def setup(bot):
    bot.add_cog(Fun(bot))
