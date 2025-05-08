import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from playwright.async_api import async_playwright

# ==== CONFIGURATION ====
BOT_TOKEN = os.getenv("BOT_TOKEN") # Добавь токен как переменную окружения

# ==== ChatGPT Web Handler ====
async def ask_chatgpt(prompt: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        await context.add_cookies([
            {
                "name": "__Secure-next-auth.session-token",
                "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..mfYmbEZRFeoPGThN.QC-O6m7V9b55N5sUDcYoeFx6p3Md3jpAoAvWsYxYna5hTonfDuH-e7ZEmoeNl9QvZiNNcE5V4iwWhizsaCXwca4UOgjyGE2MnX2r4aQ4ntt3_4_Fuv3zBmgfOK-7uYxARZOphwlQwOQOg5OAAQ-LczAEMJffcnLn5HWT_E-YwlNC6s97GnCcqlYPmeadgCQUJvY_YZ1fz0lNIl-WfTSSFK_5QmVoX6C0SL_SItRNKgvajoQioVPY_hYWnmfWXaj_-Nxb5JRTEhVR5ovgF_CO3vvhMweX_eu3kCV_BMvL6WPdzgTma8C_7T_0CZiocF7JhWXL6uAfhn3lNKqpgWVkhjXt3NKXQYdMwDQemYLAGFa6txzCXaNKPcazxxqgPl7gpBf7YDtlE_qS4mshdcdy1hxmHd6wISjB4MEnWXBgVYgLgOUOLtcuh5HMnr7LUQvZsL-mXV1C1SfIqXteWySxDOgeve1MsdNz8xTjOOIGCRls1qo1xsDR6i1gs-pjoQkxXFcyL7M5sy7JGpmhy700nn5CsYVo52_PJv4dy4_RqIz0mVI1oCh1hWeyDq5ihBFjHiTPCRBTF-q92IrfiSTTkEnwtiZTuSEPWG4G0qlQwXc6AefbClvDst_52oXgmK6ViYQkpNhJGOcUw4pp-AUj3omCrtRTZqN47crNB4dXHauQQn2-7ToSH5r6MQ6USsjx7JgjD2Exhxy27ca_TMx-ISC3yTbqvXM_FjRhWd7NYWxSkNbZjBHSCnFr-bB9I1ozdjEnwfMldlI4FHE5z3GetYriyWloQbfrxPjWAC5vs0aYWnbecIXAM3ha6u2dnWCTp7S7tAEU1c9VGISAb2bnS69QYTYT71Q5Y7rlk92rXu01H5j8UVBHK5cbkPlUGrwFql1SukFQXmd5pV68sSCaJzou19R_HPAl-nQpEgaqjQsex_2uoYHQDqD-kiXtegQfDop8OilV3zbpYJaG1Kmv3zaUO0-50sbwjjtxTnvftTgG46KQWzLiqEyGh_eGn_rwsBSHxPTuBqkfoE06Aq5EOGWIm1l04f9i8rWSJkQUibiql0OR6kNxKssdblQtl8hOmYvmOZvSarrM0Lk-F1UJZ8dqZjcaHmeoPHvyD7j_uHynjSIvpHgNADa_GE5iavJWj8sRb4uMG11kBUUpV_RuZZRPtGa4iK1PYIbC0LKJ2pwaw_Tg2ZH2MizPIK_KhpSXUYoSCNV4gpOaAmh9_JDZyad_hmUvaoaIk8Syqermb9DvL7vCLWkH0wiUg2U9hiWSuiMdy0FL-I98iQi14S_Dnfc3H1YSLrQ-RsIN71zhY7hamgiPF-gUykYCzE_GCcBr-bt05rujDA2wUJCmJFqiPO7g9IKPziL3f3jaVtchTWh9C6bdVK_CRIR0IZ4-m4og3cTjnirhNKmWbbql245Sk8x2WrewsckwcgNR03AySCXCKZYyUkBTqA2mSI9tavzT0-sWj3UahsZJXDE_som8nlMVzOnT1U3-x3Tu8oe8To6KAj9BsE7OBhdDfb5xYlU53B2BDNb9RkM_v3sUs_hl87hO0qb7RFWGHNk8ZLmK_d9H4XT-j-JQWXIcJNZ713p5hoMK8KK8E-TDnwyWqSbzUy0xaqOGqC_LqHvbOSrCtlT7_Sde9lB2htupNGe4_82nM1pE98QnhQb40u_Qay89yZCP70v1Kh7l_VfhUmIeBLL_Bwp3HJJPo7dHIoUL-y7VAV33QZh6rdhCrADVZuE9aT7D-sDt-_S0H__0vrJuYyWEr2bRTZSF0gSWUp7Yq9fN7UZ7--NIqCevbX-RhlK9jmQnWdyMoit-Bt16pCK3qMy4Qo6PwG8hWcy_vnTVWFKtk8F_Tp6vkltquGgvDDP5xdqXGWddpvyiIATOzmhgEeeLTLv1pDG_Ol8NomiMdNnVTGEoY-zhjgOgQ2EdBRxnZ9tyg7d5KbrDHMzF-T8ZZqlayVUvLxYY9jjgEAvv8DbvxhKUROrhB6TAXdwB0-yE1O6PJkBe6x7-tr9xpMvEx003iJW9IvCT6H8N1dsZRuOxV9lI4N5vJlxbMhx7WI7RZgvB3Wo5Dun-mtN0BnVUejlDNxGzKIgrgwpebYkZLNb1OyORQggQg3ZABY6appnlFxhN_IwGin2sVCQpDIdckfViVFL55WagQe52bgxt9yhzsv_PbWImRvjpDZHwZ4Etsft4T71xvZw_LnBmiwwZO9vcGfhoxF28l1blfJlZjem4Bv2YTx8cVrO1kTuynpijyrraDSEZw3xYVAYg5fjvkxMEsq8slRtt_vrbsp56tu-FbAlzr3oj3c5x-pQRzfrcgPAMj7N6O6QT3Xpit8akaNd4XvW64z0VAydxiipEKcOO15yJEiu4IueIK6UH2MZGIrhhmCj9dVsdW5Acy-M-mCPKrWincCyjcp2HNV7Pkwd1Jx031EIlYMzCesazU8Zc74o0D559QZqlU8r_OztCFJQ7nLrrgke6WXfFjv__cCvoBjm5dFYdaLdH1D5XTiGT4bRFoK5sZlsoSe9A9Y1c8UDXMRYBoRgjfZS1MvQVfEPW29zlP7I7E4SWEVbTK7KzqW9ZcoVaU0_l9VSsoZE_7aEjd8kp4cgN3RFVQQGMb8MNXTuSz6Hcldyz91E7RXX0pX8yZrR8OEY-Sz_W8TV-KSmI6T37k1M4oXZcpycY9TrrvYQq5uxO8oTFuHrAc0F6-ptW6XB-Gt0nJj0sIp7cPyXBwINi43tZBlDWDCF_yGHIYgvq9w10lEOfDA_X4GFIMq8Fdy3oSHX9EOh1pwv27bTrVKMl0mmCEjHNRWtoTAMlcrE0XRb3ZgXAFuRvmVk3A396yj_ISdFNs4XUsPenvmHR3nxrREp5sSYII28pkqiR7RJ4wCjLRGE1rE-D-LsLY4-mi4DmNqmlCNqQtevixbFnZtwjlL5eZzJns4r2hF5U8Hht0MAAli3Kv7SN_asKorfOqsg8Upn9PNYrEACytDfk1TCwDs_ZOU846b9Frd5784RqI2dhGhAkrBvQX1h3wCv5_hXsP0nFd0M9m2EKzhRrIeCM8thfGjFXGne0wMAtMhoXMd5-Blqjlms8uBuuODQv4uJePyqxtH1__Oaon4tcHtviqd0STQJ66JiTrSo3BGSHTMH6ZILjUjN1nNSfpulz9YY8-2sOqrYNLHYmJekgWjYSuLJYSaZokgc1KpKx5NsdEkFcEtev47wNBFsrrtQRM09RdMgLuoDTKHzi3Dkxic_Kz_k0bx953dE5lRIcQI-7o87YicpGh0TMQV4iyIjf0xClCGXJCxzA4FJZuGan8UTgbN39HdZ7v6auWZj5YxMNYnoWzuBSKPkiFs6biqWde9Io0t87PFapYx-ik2TqmHpBQU9fc-mAhWIJsrcwZVLCQIzVFMC-5LwEgb_Vku0snVykCe4WgFq3di9qdCuyJMJuulm_FIOiblVlDPu-fQCtiBPjTtSXa_uS3F0hhWNwyXR3rrmGj1b2tmhGSdyda25XtyyOW80xHBmNV76xeXmqkokfT99lDK6BQ6HFUrkHTzAJgROuDeZZuA.CdmQXPq1RFQYCWOmM6xnXw",
                "domain": "chat.openai.com",
                "path": "/",
                "httpOnly": True,
                "secure": True,
                "sameSite": "Lax"
            }
        ])

        page = await context.new_page()
        await page.goto("https://chat.openai.com/")

        print("🟡 Открыл страницу ChatGPT, жду textarea...")
        content = await page.content()
        print("🔍 Первые 1000 символов страницы:\n", content[:1000])

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

# ==== Telegram Command Handler ====
async def gpt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Напиши запрос после команды /gpt")
        return

    await update.message.reply_text("🤔 Думаю...")
    response = await ask_chatgpt(prompt)
    await update.message.reply_text(response)

# ==== MAIN ====
from telegram.ext import ApplicationBuilder, CommandHandler

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("gpt", gpt_handler))

print("✅ Арис-бот запущен")
app.run_polling()

