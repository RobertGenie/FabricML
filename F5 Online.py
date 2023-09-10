# meta developer: @RobertGenie

from asyncio import sleep

from .. import loader


@loader.tds
class FabricOnline(loader.Module):
    """Eternal online who will read messages in chats."""

    strings = {"name": "F5 Online"}

    async def client_ready(self, client, db):
        self.db = db

    async def onlinecmd(self, message):
        """- Enable/Disable eternal online"""
        if not self.db.get("Eternal Online", "status"):
            self.db.set("Eternal Online", "status", True)
            await message.edit("<b>🟢 Eternal online enabled.</b>")
            while self.db.get("Eternal Online", "status"):
                msg = await message.client.send_message(
                    "me", "🧶 FabricOnline 🧶"
                )
                await msg.delete()
                await sleep(1000)

        else:
            self.db.set("Eternal Online", "status", False)
            await message.edit("<b>🔴 Eternal online disabled.</b>")

    async def watcher(self, message):
        if self.db.get("Eternal Online", "status"):
            await message.client.send_read_acknowledge(
                message.chat_id, clear_mentions=True
            )
