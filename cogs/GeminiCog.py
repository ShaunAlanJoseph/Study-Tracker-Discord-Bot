from config import Gemini_API_Key
from discord.ext import commands
import google.generativeai as genai
import time

helpContext='''Study Tracker Commands
List of available commands and their usage
$ping
Responds with 'Pong!' and alternates messages.
$add_flashcard
Adds a new flashcard.
$list_flashcards
Lists all flashcards.
$flashcard_flash
Flashes a specific flashcard by ID.
$add_task
Adds a new task with a specified name.
$set_task
Sets the current task by name.
$set_task_by_id
Sets the current task by ID.
$add_description
Adds a description to the current task.
$list_tasks
Lists all tasks.
$remove_task
Removes a task by name.
$delete_task
Deletes a task by ID.
$mark_as_done
Marks a task as done by name.
$mark_as_started
Marks a task as started by name.
$mark_as_started_by_id
Marks a task as started by ID.
$mark_as_done_by_id
Marks a task as done by ID.
$set_due_date
Sets a due date for the current task.Format should be YYYY-MM-DD HH:MM:SS.
$query
Queries the Gemini API with your question and returns a response.
$pm
Sends a private message to you asking how the bot can help and you can talk to it.
$gemini enable
Enables Gemini to respond to every message in the server.
$gemini disable
Disables Gemini from responding to every message in the server.
!help <question> to ask a question related to the commands to the bot.(rn gemini is responding to the help command)

'''


genai.configure(api_key=Gemini_API_Key)
DISCORD_MAX_MESSAGE_LENGTH=2000
PLEASE_TRY_AGAIN_ERROR_MESSAGE='There was an issue with your question please try again.. '
Gemini=False
first_time=True
class GeminiAgent(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.model = genai.GenerativeModel('gemini-pro')

    @commands.Cog.listener()
    async def on_message(self,msg):
        try:
            if msg.content == "ping gemini-agent":
                await msg.channel.send("Agent is connected..")
            elif msg.content[:5] == "!help":
                 prompt=msg.content[5:]
                 global helpContext
                 response = self.gemini_generate_content(helpContext+prompt)
                 await self.send_message_in_chunks(msg.channel,response)
            elif 'Direct Message' in str(msg.channel) and not msg.author.bot:
                response = self.gemini_generate_content(msg.content)
                dmchannel = await msg.author.create_dm()
                await self.send_message_in_chunks(dmchannel,response) 
                global first_time
            elif(not msg.author.bot and Gemini):
                if first_time:
                    await msg.channel.send('Hi, I am Gemini Agent. How can I help you today?')
                    first_time=False
                else:
                    if(msg.content[0]!='$'):
                        response = self.gemini_generate_content(msg.content)
                        await self.send_message_in_chunks(msg.channel,response) 
        except Exception as e:
            await msg.channel.send("There was an error from serverside.. Please try again..")
        

    @commands.command()
    async def query(self,ctx,*,question):
        try:
            response = self.gemini_generate_content(question)
            await self.send_message_in_chunks(ctx,response)
            
        except Exception as e:
            await ctx.send("There was an error from serverside.. Please try again..")
    
    @commands.group()
    async def gemini(self,ctx):
        pass

    @gemini.command()
    async def enable(self,ctx):
        global Gemini,first_time
        Gemini=True
        await ctx.send('Gemini Agent is enabled..')
    
    @gemini.command()
    async def disable(self,ctx):
        global Gemini,first_time
        Gemini=False
        first_time=True
        await ctx.send('Gemini Agent is disabled..')

    @commands.command()
    async def pm(self,ctx):
        dmchannel = await ctx.author.create_dm()
        await dmchannel.send('Hi how can I help you today?')

    def gemini_generate_content(self, content, retries=4, delay=2):
        attempt = 0
        while attempt < retries:
            try:
                response = self.model.generate_content(content, stream=True)
                return response
            except Exception as e:
                print(f"Attempt {attempt + 1}: error in gemini_generate_content:", e)
                if attempt < retries - 1:
                    time.sleep(delay)
                attempt += 1
                return PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e)
        
    async def send_message_in_chunks(self,ctx,response):
        message = ""
        for chunk in response:
            message += chunk.text
            if len(message) > DISCORD_MAX_MESSAGE_LENGTH:
                extraMessage = message[DISCORD_MAX_MESSAGE_LENGTH:]
                message = message[:DISCORD_MAX_MESSAGE_LENGTH]
                await ctx.send(message)
                message = extraMessage
        if len(message) > 0:
            while len(message) > DISCORD_MAX_MESSAGE_LENGTH:
                extraMessage = message[DISCORD_MAX_MESSAGE_LENGTH:]
                message = message[:DISCORD_MAX_MESSAGE_LENGTH]
                await ctx.send(message)
                message = extraMessage
            await ctx.send(message)
