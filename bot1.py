 
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


BOT_OWNER_ROLE = 'Daynite World | Runner' # change to what you need
#BOT_OWNER_ROLE_ID = "544387608378343446"
  
 

 
oot_channel_id_list = [
"710186409151168544", #loco
"569420128794443776", #unt
"709419284975059014", #ukt loco
"708939235259973652", #galaxy loco
"681891490208677958", #best loco
"650009503453937693", #tf loco

]


answer_pattern = re.compile(r'(not|n|e)?([1-3]{1})(\?)?(cnf|c|cf)?(\?)?$', re.IGNORECASE)
print(answer_pattern)
apgscore = 441
nomarkscore = 333
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
        self.embed=discord.Embed(title="", description="**Crowd Answer Results!**", color=0x04B4AE)
        self.embed.add_field(name="`**__Answer ❶__**`", value="0.00", inline=False)
        self.embed.add_field(name="`**__Answer ❷__**`", value="0.00", inline=False)
        self.embed.add_field(name="`**__Answer ❸__**`", value="0.00", inline=False)
        self.embed.add_field(name="**__Erased Answer :-__**", value="0",inline=False)
        self.embed.add_field(name="**__Crowd Answer :-__**", value="0",inline=False)
        self.embed.set_footer(text=f" ☆ Boat [ Trivia ]| ραrαмʝєєт || єαgℓє™#5629™〢", icon_url="https://cdn.discordapp.com/attachments/684305785928286213/710355842180055078/Screenshot_2020-03-17-18-22-32-298.jpeg")
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/684305785928286213/710355842180055078/Screenshot_2020-03-17-18-22-32-298.jpeg")
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
        best_answer = "** **   **Fetching** **:-**"
        erased_answer = "** **   **Erasing** **:-**"
              

        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        #best_answer = '<a:loading:656220884553695240>'
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        wrong = lst_scores.index(lowest)+1
       #global wrong             

        if highest > 0:
            if answer == 1:
                one_check = "✅"
                mark_check_one = ""
                best_answer = "**  ** **Answer** **:-**  :one:"
                   
            else:
                one_check = ""

            if answer == 2:
                two_check = "✅"
                mark_check_two = ""
                best_answer = "**  ** **Answer** **:-**  :two:"
                   
            else:
                two_check = ""

            if answer == 3:
                three_check = "✅"
                mark_check_three = ""
                best_answer = "**  ** **Answer** **:-**  :three:"
                   
            else:
                three_check = ""

            

        if lowest < 0:
            if wrong == 1:
                one_cross = "❌"
                erased_answer = "** ** **Answer** :one: = :x:" 
               
            if wrong == 2:
                two_cross = "❌"
                erased_answer = "** ** **Answer** :two: = :x:" 
               
            if wrong == 3:
                three_cross = "❌"
                erased_answer = "** ** **Answer** :three: = :x:" 
               

			
        self.embed.set_field_at(0, name="**__Aɴsᴡᴇʀ ❶__**", value="**{0}.00**{1}{2}".format(lst_scores[0], one_check, one_cross)) 
        self.embed.set_field_at(1, name="**__Aɴsᴡᴇʀ ❷__**", value="**{0}.00**{1}{2}".format(lst_scores[1], two_check, two_cross)) 
        self.embed.set_field_at(2, name="**__Aɴsᴡᴇʀ ❸__**", value="**{0}.00**{1}{2}".format(lst_scores[2], three_check, three_cross)) 
        self.embed.set_field_at(3, name="**__Erased Answer :-__**", value=erased_answer)
        self.embed.set_field_at(3, name="**__Crowd Answer :-__**", value=best_answer)
                   

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
        await self.change_presence(activity=discord.Activity(type=1,name='Loco Trivia Answers!!'))
        await asyncio.sleep(5)

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "lo":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
               # await self.embed_msg.add_reaction("<:right:670810748804399105>")
                #await self.embed_msg.add_reaction("<a:success:646229590200549386>")
                #await self.embed_msg.add_reaction(":white_check_mark:")
               # await self.embed_msg.add_reaction("<a:muscle:656210170333888562>")
                  
                self.embed_channel_id = message.channel.id
          #  else:
       #         await message.channel.send("**_Chal Nikal pahle fursat me ye tere liye nahi h bsdk_**😝")
         #   return


        #if message.content.startswith('bt'):
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
    loop.create_task(bot.start('NzQ2NTcyMjg5NTk1NjcwNTQ4.X0CRoA.LdJdr0mL9fHf8y6nkqF6ePmqzlk'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NzE0OTEyMzY4MDMwNzc3MzY0.XvAezA.akqXKP6SXWJHLYstf4e2NjOCdOU',
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
