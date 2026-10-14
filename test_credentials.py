#!/usr/bin/env python3
"""Credentials & Connectivity Pre-flight Test
Run this script before your live demo to verify all keys and permissions!
Usage:
    python3 test_credentials.py
"""

import asyncio
import contextlib
import os

from dotenv import load_dotenv

load_dotenv()

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_status(step: str, ok: bool, details: str = ""):
    symbol = f"{GREEN}✓{RESET}" if ok else f"{RED}✗{RESET}"
    print(f"[{symbol}] {step}")
    if details:
        indent = "    "
        print(f"{indent}{details}")


async def test_groq(api_key: str, model: str):
    from groq import AsyncGroq

    try:
        client = AsyncGroq(api_key=api_key)
        resp = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Respond with the word 'READY'."}],
            max_completion_tokens=10,
        )
        content = resp.choices[0].message.content.strip()
        return True, f"Groq responded successfully: '{content}' using model '{model}'"
    except Exception as e:
        return False, f"Groq test failed: {type(e).__name__} - {e}"


async def test_discord(token: str, guild_id: int):
    try:
        import discord
    except ImportError:
        return (
            False,
            "Package 'discord.py' is not installed. Run: pip install -r requirements.txt",
        )

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    success = False
    message = ""

    ready_event = asyncio.Event()

    @client.event
    async def on_ready():
        ready_event.set()

    try:
        # Connect briefly to verify token and guild
        login_task = asyncio.create_task(client.start(token))

        with contextlib.suppress(asyncio.TimeoutError):
            await asyncio.wait_for(ready_event.wait(), timeout=15.0)

        if client.is_ready():
            guild = client.get_guild(guild_id)
            if guild:
                success = True
                message = f"Connected as {client.user}. Found Guild: '{guild.name}' (ID: {guild.id}) with {len(guild.text_channels)} text channels."
            else:
                success = False
                message = f"Connected as {client.user}, but Guild ID {guild_id} was NOT found in the bot's server list. Make sure the bot is invited to this server!"
        else:
            success = False
            message = "Client did not reach ready state in time (15s timeout)."

        await client.close()
        login_task.cancel()
        with contextlib.suppress(Exception):
            await login_task

    except Exception as e:
        success = False
        message = f"Discord login error: {type(e).__name__} - {e}"

    return success, message


async def main():
    print(f"{YELLOW}=== SkillUp Discord AI Agent Pre-flight Verification ==={RESET}\n")

    token = os.getenv("DISCORD_BOT_TOKEN")
    groq_key = os.getenv("GROQ_API_KEY")
    guild_id_str = os.getenv("DISCORD_GUILD_ID")
    model = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")

    # Step 1: Environment Variables Check
    missing = []
    if not token:
        missing.append("DISCORD_BOT_TOKEN")
    if not groq_key:
        missing.append("GROQ_API_KEY")
    if not guild_id_str:
        missing.append("DISCORD_GUILD_ID")

    if missing:
        print_status(
            "Environment variables loaded",
            False,
            f"Missing: {', '.join(missing)} in .env file.",
        )
        print(
            f"\n{YELLOW}Tip:{RESET} Create a .env file from .env.example with your actual credentials.\n"
        )
        return

    try:
        guild_id = int(guild_id_str)
        print_status("Environment variables syntax valid", True, f"Guild ID: {guild_id}")
    except ValueError:
        print_status("DISCORD_GUILD_ID format", False, "Must be numeric digits only.")
        return

    # Step 2: Test Groq API
    print("\nTesting GroqCloud API connection...")
    ok_groq, groq_msg = await test_groq(groq_key, model)
    print_status("GroqCloud Inference", ok_groq, groq_msg)

    # Step 3: Test Discord Bot Connection
    print("\nTesting Discord Gateway connection...")
    ok_discord, discord_msg = await test_discord(token, guild_id)
    print_status("Discord Bot Gateway & Guild", ok_discord, discord_msg)

    print("\n" + "=" * 50)
    if ok_groq and ok_discord:
        print(f"{GREEN}ALL CHECKS PASSED! You are ready to run or explain the live demo.{RESET}")
    else:
        print(
            f"{RED}SOME CHECKS FAILED. Please review the errors above and update your .env or Discord settings.{RESET}"
        )


if __name__ == "__main__":
    asyncio.run(main())
