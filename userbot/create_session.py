from pyrogram import Client
import sys

app = Client("my_account", int(sys.argv[1]), sys.argv[2])

async def main():
    async with app:
        await app.send_message("me", "Hi there! I'm using **Pyrogram**")


app.run(main())
