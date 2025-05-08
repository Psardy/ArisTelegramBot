import os
import asyncio
from telethon import TelegramClient, events
from playwright.async_api import async_playwright

# ==== CONFIGURATION ====
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = 'anon'
TRIGGER_PREFIX = '/gpt '

# ==== TELEGRAM CLIENT ====
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ==== ChatGPT Web Handler ====
async def ask_chatgpt(prompt: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        await context.add_cookies([
            {
                "name": "__Secure-next-auth.session-token",
                "value": "твой_токен_здесь",
                "domain": ".chat.openai.com",
                "path": "/",
                "httpOnly": True,
                "secure": True
            }
            # Добавь остальные куки, если нужно
        ])

        page = await context.new_page()
        await page.goto("https://chat.openai.com/")

        await page.wait_for_selector('textarea')
        await page.fill('textarea', prompt)
        await page.press('textarea', 'Enter')

        await page.wait_for_timeout(10000)
        responses = await page.query_selector_all(".markdown")
        if responses:
            text = await responses[-1].inner_text()
        else:
            text = "🤖 Не удалось получить ответ от ChatGPT."

        await browser.close()
        return text

# ==== TELEGRAM MESSAGE HANDLER ====
@client.on(events.NewMessage)
async def handler(event):
    if not event.raw_text.startswith(TRIGGER_PREFIX):
        return

    prompt = event.raw_text[len(TRIGGER_PREFIX):]
    await event.reply("🤔 Думаю...")
    response = await ask_chatgpt(prompt)
    await event.reply(response)

# ==== MAIN LOOP ====
async def main():
    await client.start()
    print("✅ Арис активен в Telegram. Жду сообщений...")
    await client.run_until_disconnected()

asyncio.run(main())
