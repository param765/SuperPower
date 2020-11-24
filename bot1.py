 
'''
using discord.py version 1.0.0a
'''
import discord
import random
import asyncio
import re
import multiprocessing
import threading
import concurrent
import datetime



#BOT_OWNER_ROLE = 'Community | Runner' # change to what you need
#BOT_OWNER_ROLE_ID = "544387608378343446"



 
oot_channel_id_list = [
"773602512204201994", #Vedantu D
"773887570920472576", #Vedantu G

]


answer_pattern = re.compile(r'(not|n|e)?([1-3]{1})(\?)?(cnf|c|cf|conf|w|apg)?(\?)?$', re.IGNORECASE)
print(answer_pattern)
apgscore = 800
nomarkscore = 450
markscore = 222

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("COMMUNITY SELF BOT")
        print("Connected to discord naf.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))
        


    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        self.answer_scores = answer_scores

        # embed creation
        value=random.randint(0,0xffffff)
        self.embed=discord.Embed(title="**Crowd Answer Results!**", description="", color=0x04B4AE)
        self.embed.add_field(name="`**__OPTION ❶__**`", value="0.00", inline=False)
        self.embed.add_field(name="`**__OPTION ❷__**`", value="0.00", inline=False)
        self.embed.add_field(name="`**__OPTION ❸__**`", value="0.00", inline=False)
        self.embed.add_field(name="(Crowd Answer)[https://www.google.com/]", value="0",inline=False)
        #self.embed.add_field(name="(Erased Answer)[https://www.google.com/]", value="0",inline=False)
        self.embed.set_footer(text=f"  Developed By :- Paramjeet", icon_url="https://cdn.discordapp.com/attachments/757929955278585918/774646003130433556/732925603854024714.gif")
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/716464269792903208/780839997820633147/1606237070799.png")
         #self.embed.set_image(url="https://i.imgur.com/b6fW3cI.gif")
        # await bot.add_reaction(message = "self.embed",emoji = ":wink")
        # await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):

         

        one_check = ""
        two_check = ""
        three_check = ""
        mark_check_one=""
        mark_check_two=""
        mark_check_three=""
        one_cross =""
        two_cross =""
        three_cross =""
        best_answer = "** **   **Fetching** **:-** <a:yellowload:780827930376536115> "
        erased_answer = "** **   **Erasing** **:- ** <:Eraser:760424482002960406> "
              

        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        #best_answer = '<a:loading:656220884553695240>'
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        wrong = lst_scores.index(lowest)+1
       #global wrong             

        if highest > 0:
            if answer == 1:
                one_check = f"<:emoji_15:746745204333346827>"
                mark_check_one = "<a:emoji_9:707523490881994763>"
                best_answer = "**  ** **Answer** **:-**  <:emoji_15:746745204333346827> <a:emoji_12:746566205183361113>"
                   
            else:
                one_check = ""

            if answer == 2:
                two_check = f"<:emoji_16:746745224436645898>"
                mark_check_two = "<a:emoji_9:707523490881994763>"
                best_answer = "**  ** **Answer** **:-**  <:emoji_16:746745224436645898> <a:emoji_12:746566205183361113>"
                   
            else:
                two_check = ""

            if answer == 3:
                three_check = f"<:emoji_16:746745242400849920>"
                mark_check_three = "<a:emoji_9:707523490881994763>"
                best_answer = "**  ** **Answer** **:-**  <:emoji_16:746745242400849920> <a:emoji_12:746566205183361113>"
                   
            else:
                three_check = ""

            

        if lowest < 0:
            if wrong == 1:
                one_cross = "<:emoji_10:746565682837192767>"
                erased_answer = "** ** **Answer** :one: =<:Eraser:760424482002960406>" 
               
            if wrong == 2:
                two_cross = "<:emoji_10:746565682837192767>"
                erased_answer = "** ** **Answer** :two: = <:Eraser:760424482002960406>" 
               
            if wrong == 3:
                three_cross = "<:emoji_10:746565682837192767>"
                erased_answer = "** ** **Answer** :three: = <:Eraser:760424482002960406>" 
               

			
        self.embed.set_field_at(0, name="**__Answer ➊__**", value=f"**[{lst_scores[0]}](https://discord.com/)** {one_check}{one_cross}")
        self.embed.set_field_at(1, name="**__Answer ❷__**", value=f"**[{lst_scores[1]}](https://discord.com/)** {two_check}{two_cross}") 
        self.embed.set_field_at(2, name="**__Answer ❸__**", value=f"**[{lst_scores[2]}](https://discord.com/)** {three_check}{three_cross}") 
        self.embed.set_field_at(3, name="**__Crowd Answer :-__**", value=best_answer)
        #self.embed.set_field_at(4, name="**__Eraser Answer :-__**", value=erased_answer)
                   

        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("COMMUNITY SELF BOT")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))
        

        await self.clear_results()
        await self.update_embeds()

        await asyncio.sleep(5)
        await self.change_presence(activity=discord.Activity(type=1,name='Connected Private!!'))
        await asyncio.sleep(5)

    async def on_message(self, message):


 # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "$b":
              await message.delete()
              #if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
              self.embed_msg = None
              await self.clear_results()
              await self.update_embeds()
              self.embed_msg = \
                   await message.channel.send('',embed=self.embed)
              #await self.embed_msg.add_reaction("<a:EmojiResolvable:768525399067983912>")
                 #await self.embed_msg.add_reaction("<a:emoji_18:748739056762093608>")
                #await self.embed_msg.add_reaction(":white_check_mark:")
               # await self.embed_msg.add_reaction("<a:muscle:656210170333888562>")
                  
              self.embed_channel_id = message.channel.id 
          #  else:
       #        await message.channel.send("**_Chal Nikal pahle fursat me ye tere liye nahi h bsdk_**😝")
         #   return


        #if message.content.startswith('$dlo'):
          #await message.delete()
          #if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
          #embed = discord.Embed(title="<:locog:656214123524128829>**Loco Trivia Answer!**", description="", color=0x00ff00)
          #embed.add_field(name="**__BOT STATUS__**", value="ONLINE🟢`(Auto Run)`", inline=False)
          #embed.add_field(name="**__BOT COMMAND__**", value="`$lo`", inline=False)
          #embed.add_field(name="**__BOT CONNECTION__**", value="ALL PRIVATE SERVER", inline=False)
          #embed.set_footer(text=f"©Loco Trivia Beta v1.13 | </> with 💟 by Ashwin#4734!", \
            #icon_url="https://cdn.discordapp.com/attachments/660019723140071435/660068972372295681/IMG_20191220_225620.jpg")
          #embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/656554502543114248/663261544146272277/556321441058914305.png")
          #embed.set_image(url="https://i.imgur.com/b6fW3cI.gif")
          #await message.channel.send(embed=embed)
          

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NzI0NTYxNzg5MzQxNDAxMDk4.XvB-wA.ckrqOWiNJHh96EFewMvLqELEJJw'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NzE0OTEyMzY4MDMwNzc3MzY0.X71CYg.1p2Iu-O7dCE8xYKQx8S8Dhavui4',
                                     bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=3)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()
