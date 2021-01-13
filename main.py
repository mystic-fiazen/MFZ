import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "shit", "fucked up", "oh damn", "suck", "bitter", "heartbroken", "melancholy", "pessimistic", "somber", "wistful", "dumb" ]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!",
  "You will be successful one day, Just keep working hard!",
  "Stop it, Get some help!",
  "I don't think you suck, Your awesome! (honestly saying)",
  "I'm sure you'll get a girl/boy someday",
  "Aye, Don't be a dank memer.",
  "Listen, Your the most inspirational person I ever met. So don't dare say that. It makes me sad....",
  "How do I convince this guy that he/she could be the next Jeff Kinney/Liz Pichon?",
  "That's it, Your fired for demotivating yourself.",
  "Your the one who told me I will become successful one day and now your saying THIS to me? Bruh."
]  

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.idle, activity=discord.Game('Chicken Wings 3D')) 
  print('Bot is ready') 

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event     
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("new"):
    encouraging_message = msg.split("new",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("del"):
    encouragements = lol 
    if "encouragements" in db.keys():
      index = int(msg.split("del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("responding"):
    value = msg.split("responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")



keep_alive()
client.run(os.getenv('TOKEN'))  