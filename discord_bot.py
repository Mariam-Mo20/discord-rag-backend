import discord
import requests
import os 
# Backend API Endpoints
API_URL = "http://localhost:5000/api/rag-query"
FEEDBACK_URL = "http://localhost:5000/api/feedback"

# Discord Intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.reactions = True

# Discord Client
client = discord.Client(intents=intents)

# Constants
MAX_DISCORD_MESSAGE_LENGTH = 2000
message_answer_map = {}  # Cache to store question/answer by message ID

def split_message(message):
    """Split long messages to fit Discord message length limit."""
    return [message[i:i + MAX_DISCORD_MESSAGE_LENGTH] for i in range(0, len(message), MAX_DISCORD_MESSAGE_LENGTH)]

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    print("✅ Bot is ready and listening to events")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_msg = message.content
    thinking_msg = await message.channel.send("Thinking...")  # Initial quick reply

    try:
        response = requests.post(API_URL, json={
            "user_id": str(message.author.id),
            "question": user_msg
        })

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            chunks = split_message(answer)
            sent_msgs = []

            
            if chunks:
                await thinking_msg.edit(content=chunks[0])
                sent_msgs.append(thinking_msg)

        
                for chunk in chunks[1:]:
                    sent_msg = await message.channel.send(chunk)
                    sent_msgs.append(sent_msg)

            if sent_msgs:
                message_answer_map[sent_msgs[0].id] = {
                    "question": user_msg,
                    "answer": answer
                }

                # Add reaction emojis for feedback
                for emoji in ["👍", "👎"]:
                    await sent_msgs[0].add_reaction(emoji)
        else:
            await message.channel.send("❌ Error contacting backend.")
    except Exception as e:
        await message.channel.send(f"⚠️ Error: {str(e)}")

@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        return  

    print(f"🔁 Reaction detected on message ID {payload.message_id} from user {payload.user_id}")

    msg_id = payload.message_id

    if msg_id in message_answer_map:
        qa = message_answer_map[msg_id]
        question = qa["question"]
        answer = qa["answer"]

        emoji_rating_map = {
            "👎": "bad",
            "👍": "good",
        }

        emoji_str = str(payload.emoji.name)
        rating = emoji_rating_map.get(emoji_str)

        channel = await client.fetch_channel(payload.channel_id)

        if rating is None:
            await channel.send("⚠️ Please use one of the star ratings.")
            return

        payload_data = {
            "user_id": str(payload.user_id),
            "question": question,
            "answer": answer,
            "rating": rating,
            "comment": ""
        }

        try:
            res = requests.post(FEEDBACK_URL, json=payload_data)
            print(f"[FEEDBACK] Sent payload: {payload_data} | Response: {res.status_code}")
            await channel.send(f"Thanks for your feedback")
        except Exception as e:
            await channel.send("Error saving feedback.")
    else:
        print("🔸 Reaction not linked to bot message")
        print(f"📨 Keys in map: {list(message_answer_map.keys())}")
        print(f"📌 Reaction on: {payload.message_id}")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
client.run(DISCORD_TOKEN)
