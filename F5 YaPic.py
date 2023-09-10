# meta developer: @RobertGenie

from telethon.tl.types import Message
from .. import loader, utils

@loader.tds
class FabricYaPic(loader.Module):
    """Searches for a picture from Yandex based on your request."""

    strings = {"name": "F5 YaPic"}

    @loader.unrestricted
    async def spiccmd(self, message):
        """- Search"""
        text = utils.get_args_raw(message)
        if not text:
            await message.edit("❌ Request not specified")
            return
        text_with_plus = text.replace(" ", "+")
        link = f"https://yandex.uz/images/touch/search/?text={text_with_plus}"
        try:
            await self.inline.form(
                message=message,
                text=f"🔍 Your photo on request  \"{text}\" found",
                reply_markup=[
                    [
                        {
                            "text": "Link to photo ",
                            "url": link,
                        }
                    ],
                    [{"text": "Close", "action": "close"}],
                ],
                **({"photo": link}),
            )
        except:
            await message.edit(f"❌ Couldn't find the image you requested \"{text}\".")
