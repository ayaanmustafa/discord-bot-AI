with open("token.txt") as f:
    token = f.read()
#https://discord.com/api/oauth2/authorize?client_id=756421877118795808&permissions=0&scope=bot

import discord,requests,json,random,pickle,wikipedia
from textblob import TextBlob
from bot_talk import get_response, predict_classes
from tensorflow.keras.models import load_model
from google_search import google
from wordsapi import get_word_data

intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('model.h5')

def make_request(error):
  
    resp  = requests.get("https://api.stackexchange.com/"+"2.2/search?order=desc&tagged=python&sort=activity&intitle={}&site=stackoverflow".format(error))
    return resp.json()

def get_urls(json_dict):
    url_list = []
    count = 0
    for i in json_dict['items']:
        if i["is_answered"]:
            url_list.append(i["link"])
        count+=1
        if count == len(i) or count == 4:
            break
    return url_list

def get_meme():
    meme_list = [
    "https://giphy.com/gifs/achievementhunter-rooster-teeth-achievement-hunter-off-topic-ah-4JVTF9zR9BicshFAb7",
    "https://media1.giphy.com/media/lkdH8FmImcGoylv3t3/200.webp?cid=ecf05e47nvnk1q8w5wwtcj080433th7s9e4nx9b2qjklw2sj&rid=200.webp",
    "https://c.tenor.com/L3BFEHXWz9sAAAAj/funny-lmao.gif",
    "https://media.tenor.com/images/62d8b9a588c67c78e44f8998f02b1403/tenor.gif",
    "https://media.tenor.com/images/e16e5d256db4a49a0a059284ef65194f/tenor.gif",
    "https://media.tenor.com/images/940aa71f1fd59cb9f058c0a94dfac432/tenor.gif",
    "https://usersnap.com/blog/wp-content/uploads/2015/12/funny-cat-year2015-web-dev.gif",
    "https://www.liveabout.com/thmb/9oyhVbEg1OHIPqxsUSe9Pif61U8=/640x640/filters:no_upscale():max_bytes(150000):strip_icc()/superdog-treadmill-5af44eb2eb97de003d8c771d.gif",
    "https://media.tenor.com/images/d81f39f1f5849eee1c9aa7b0a3c0fe31/tenor.gif",
    "https://i.imgur.com/o1k0PLm.gif",
    "https://www.transformationmarketing.com/wp-content/uploads/2018/03/giphy-downsized.gif",
    "https://miro.medium.com/max/692/1*9PYEkmnHDS2ygawLE0e0XQ.gif",
    "https://media.tenor.com/images/53bd03f6d91aea0a2070fd2b57c25724/tenor.gif",
    "https://data.whicdn.com/images/181476985/original.gif",
    "https://www.animatedimages.org/data/media/499/animated-fun-image-0217.gif",
    "https://media.tenor.com/images/2e1694da01f2285f4ea9921fe5e1d3dc/tenor.gif"]
    meme = random.choice(meme_list)
    return meme

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + f" -{json_data[0]['a']}"
    return quote

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content   

    if message.content.startswith("!inspire") or TextBlob(msg).sentiment.polarity < -0.1:
        quote = get_quote()
        await message.channel.send(quote)


    if message.content.startswith("!entertain") or TextBlob(msg).sentiment.polarity > 0.1 :
        meme = get_meme()
        await message.channel.send(meme)



    if message.content.startswith("!chat"):
        user_chat = msg.split("!chat")[1]
        ints = predict_classes(user_chat)
        result = get_response(ints, intents)
        await message.channel.send(result) 



    if message.content.startswith("!wiki"):
        user_chat = msg.split("!wiki")[1]
        try:
            result = wikipedia.summary(user_chat, sentences=2)
        except wikipedia.exceptions.DisambiguationError as e:
            result = e.options
        except wikipedia.exceptions.PageError as e:
            result = "Try something else"
        await message.channel.send(f"```{result}```") 
    


    if message.content.startswith("!play"):
        channel = message.channel
        await channel.send("Choose a number between 1-10. Enter numerical values only.") #message that tells about the start of the game

        number1 = random.randint(1,10)        
        number2 = str(number1)

        def check(m):
            return m.content == number2 and m.channel == channel
        try:
            msg = await client.wait_for('message', check=check)
            await channel.send("Correct answer {.author}" .format(msg))
        except Exception as e:
            await channel.send("Check inputs!")




    if message.content.startswith("!repeat"):
        split = msg.split(" ")
        txt = split[1]
        num = int(split[2])
        for i in range(num):
            await message.channel.send(txt)



    if message.content.startswith("!sos"):
        channel = message.channel
        try:
            split = msg.split("!sos")
            error = split[1]
            await channel.send(f"```Searching for{error}...```")
            json2 = make_request(error)
            await channel.send("```Possible results:```")
            for i in get_urls(json2):
                await channel.send(f"{i}")
        except Exception as e:
            await channel.send(e)    
            


    if message.content.startswith("!google"):
        channel = message.channel
        try:
            split = msg.split("!google")
            query = split[1]
            await channel.send(f"```Searching for{query}...```")
            await channel.send(f"```{google(query)}```")
        except Exception as e:
            await channel.send(e)     



    if message.content.startswith("!word-info"):
        channel = message.channel
        try:
            split = msg.split("!word-info")
            query = split[1]
            await channel.send(f"Searching for{query}...")
            await channel.send(f"**Defination:** ```{get_word_data(query)[0]}```")
            await channel.send(f"**Stems:** ```{get_word_data(query)[1]}```")
            await channel.send(f"**Synonyms:** ```{get_word_data(query)[2]}```")
        except Exception as e:
            await channel.send(e)    
   
client.run(token)
