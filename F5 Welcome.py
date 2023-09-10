# meta developer: @RobertGenie

from .. import loader, utils


@loader.tds
class FabricWelcome(loader.Module):
    """Greeting new users in the chat."""

    strings = {"name": "F5 Welcome"}

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

    async def welcomecmd(self, message):
        """- Enable/Disable greeting of new users in chat."""
        welcome = self.db.get("Welcome", "welcome", {})
        chatid = str(message.chat_id)
        args = utils.get_args_raw(message)
        if args == "clearall":
            self.db.set("Welcome", "welcome", {})
            return await message.edit(
                "✅ All module settings have been reset."
            )

        if chatid in welcome:
            welcome.pop(chatid)
            self.db.set("Welcome", "welcome", welcome)
            return await message.edit("❎ Деактивирован!")

        welcome.setdefault(chatid, {})
        welcome[chatid].setdefault("message", "Добро пожаловать в чат!")
        welcome[chatid].setdefault("is_reply", False)
        self.db.set("Welcome", "welcome", welcome)
        await message.edit("✅ Activate!")

    async def setwelcomecmd(self, message):
        """- Set a new greeting for new users in the chat.\nUse: .setwelcome <text (you can use {name}; {
        chat})>; nothing."""
        welcome = self.db.get("Welcome", "welcome", {})
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        chatid = str(message.chat_id)
        chat = await message.client.get_entity(int(chatid))
        try:
            if not args and not reply:
                return await message.edit(
                    "<b>Welcome new "
                    "users in "
                    f'"{chat.title}":</b>\n\n'
                    "<b>Status:</b> Enabled.\n"
                    f"<b>Welcome text:</b> {welcome[chatid]['message']}\n\n "
                    "<b>~ Set new welcome text "
                    "you can use the command :</b> "
                    ".setwelcome <текст>."
                )
            else:
                if reply:
                    welcome[chatid]["message"] = reply.id
                    welcome[chatid]["is_reply"] = True
                else:
                    welcome[chatid]["message"] = args
                    welcome[chatid]["is_reply"] = False
                self.db.set("Welcome", "welcome", welcome)
                return await message.edit(
                    "<b>✅ New greeting installed successfully.</b>"
                )
        except KeyError:
            return await message.edit(
                f'<b>Welcome new users in "{chat.title}":</b>\n\n '
                "<b>Status:</b> Disabled"
            )

    async def watcher(self, message):
        """Interesting watcher why? 🤔"""
        try:
            welcome = self.db.get("Welcome", "welcome", {})
            chatid = str(message.chat_id)
            if chatid not in welcome:
                return
            if message.user_joined or message.user_added:
                user = await message.get_user()
                chat = await message.get_chat()
                if not welcome[chatid]["is_reply"]:
                    return await message.reply(
                        (welcome[chatid]["message"]).format(
                            name=user.first_name, chat=chat.title
                        )
                    )
                msg = await self.client.get_messages(
                    int(chatid), ids=welcome[chatid]["message"]
                )
                await message.reply(msg)
        except:
            pass