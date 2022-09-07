import asyncio
import time


async def wait_for_port(
    host: str, port: int, duration: int = 10, delay: int = 2
) -> bool:
    tmax = time.time() + duration

    while time.time() < tmax:
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=5
            )
            writer.close()
            await writer.wait_closed()

            return True
        except Exception:
            if delay:
                await asyncio.sleep(delay)

    return False
