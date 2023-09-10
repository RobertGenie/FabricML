# scope: hikka_only
# meta developer: @RobertGenie

import asyncio
import random
import aiohttp
import io
import requests

from hikkatl.types import Message

from .. import loader, utils

async def create_image(prompt: str, model: str) -> dict:
    url = "https://api.prodia.com/v1/job"
    
    payload = {
        "prompt": prompt,
        "model": model,
        "sampler": "DPM++ 2M Karras",
        "upscale": False,
        "aspect_ratio": "portrait",
        "steps": 30,
        "seed": random.randint(-1, 9999999)
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": "a37d23ca-f23f-48cb-b747-a596a43c6fb9"
    }
    try:
        tries = 60
        async with aiohttp.ClientSession() as ses:
            async with ses.post(url, json=payload, headers=headers) as response:
                data = await response.json()
                jobid = data['job'].strip()

                while tries > 0:
                    tries -= 1

                    async with ses.get(f'{url}/{jobid}', headers=headers) as response:
                        data = await response.json()
                        if data['status'] == 'succeeded':
                            return {
                                'status': 'succeeded',
                                'model': model,
                                'data': data
                            }

                    await asyncio.sleep(1)

                return {
                    'status': 'error',
                    'error': 'Timed out '
                }
    except Exception as error:
        return {
                'status': 'error',
                'error': error
            }

@loader.tds
class FabricDraw(loader.Module):
    """Generate any photo using AI."""

    strings = {
        "name": "F5 Draw"
    }

    async def drawcmd(self, message):
        args = utils.get_args_raw(message)
        models = [
        'anything-v4.5-pruned.ckpt [65745d25]',
        'Realistic_Vision_V2.0.safetensors [79587710]',
        'openjourney_V4.ckpt [ca2f377f]'
        ]

        model = random.choice(models)

        await utils.answer(message, 'Generation...')
        image = await create_image(args, model)

        image = io.BytesIO(
                (
                    await utils.run_sync(
                        requests.get,
                        f"{image['data']['imageUrl']}?download=1",
                        stream=True,
                    )
                ).content
            )
        image.name = "FabricML_FabricDraw.png"

        images = []
        images.append(image)
        await asyncio.sleep(3)

        await utils.answer_file(
            message,
            images,
            f"Request: {args}\nModel: {model}"
        )
