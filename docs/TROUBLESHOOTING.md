# Troubleshooting & Common Issues Guide

Use this guide to diagnose and resolve errors encountered during setup, gateway connection, or command execution.

---

## Quick Diagnostic Checklist

Before diving into specific errors, run the pre-flight verification script:
```bash
python test_credentials.py
```
This tests:
1. Valid presence and formatting of all environment variables.
2. Direct connection and inference on GroqCloud.
3. Authenticated handshake with the Discord Gateway and verification that the Guild exists in the bot's server list.

---

## 1. Discord Gateway & Authentication Issues

### `discord.errors.PrivilegedIntentsRequired: Shard ID None is requesting privileged intents that have not been enabled`
- **Cause**: The bot code requests `intents.message_content = True`, but the intent was not enabled in Discord's developer portal.
- **Solution**:
  1. Open [Discord Developer Portal](https://discord.com/developers/applications).
  2. Select your Application ➔ Click **Bot** on the left menu.
  3. Scroll down to **Privileged Gateway Intents**.
  4. Toggle **Message Content Intent** to ON.
  5. Click **Save Changes** and restart your bot.

---

### `discord.errors.LoginFailure: Improper token has been passed`
- **Cause**: The `DISCORD_BOT_TOKEN` in `.env` or Colab secrets is incorrect, contains extra spaces, or was revoked.
- **Solution**:
  1. Go to Developer Portal ➔ **Bot** ➔ Click **Reset Token**.
  2. Copy the freshly generated token.
  3. Ensure there are no quotes or extra spaces around the token in `.env`.

---

### Commands do not appear when typing `/` in Discord
- **Cause A**: Bot was invited without the `applications.commands` OAuth2 scope.
  - **Fix**: Re-invite the bot using an install URL that includes `scopes=bot%20applications.commands`.
- **Cause B**: `DISCORD_GUILD_ID` does not match the server you are in.
  - **Fix**: Right-click your server icon with Developer Mode enabled, copy the Server ID, and update `DISCORD_GUILD_ID`.
- **Cause C**: Global commands were synced instead of guild commands.
  - **Fix**: Verify `self.tree.copy_global_to(guild=GUILD)` and `self.tree.sync(guild=GUILD)` are executed in `setup_hook`.

---

## 2. GroqCloud & LLM API Errors

### `groq.AuthenticationError: Error code: 401 - {'error': {'message': 'Invalid API Key'}}`
- **Cause**: The `GROQ_API_KEY` is invalid or expired.
- **Solution**:
  1. Visit [console.groq.com/keys](https://console.groq.com/keys).
  2. Generate a new key and update `GROQ_API_KEY`.

---

### `groq.NotFoundError: Error code: 404 - {'error': {'message': 'The model does not exist'}}`
- **Cause**: The model string in `GROQ_MODEL` is deprecated or unavailable in your region.
- **Solution**:
  1. The default model is `qwen/qwen3.8-27b`.
  2. Alternatively, switch to another supported model in `.env`:
     ```env
     GROQ_MODEL=llama-3.3-70b-versatile
     ```

---

### `groq.RateLimitError: Error code: 429`
- **Cause**: Exceeded requests-per-minute (RPM) or tokens-per-minute (TPM) limits on the free Groq tier.
- **Solution**:
  1. Wait 60 seconds before issuing another prompt.
  2. In `/summary`, lower `messages_per_channel` (e.g. from 50 to 15).

---

## 3. Discord Interaction & Runtime Errors

### `discord.errors.NotFound: 404 Not Found (error code: 10062): Unknown interaction`
- **Cause**: Discord expects an interaction acknowledgment within **3.0 seconds**. If your LLM or message fetching takes longer without deferral, Discord invalidates the interaction token.
- **Solution**:
  - Ensure `await interaction.response.defer(thinking=True)` is called as the very first line of your slash command handler before any network requests.

---

### `discord.errors.HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body (content: Must be 2000 or fewer in length)`
- **Cause**: LLM response exceeded Discord's maximum message limit of 2,000 characters.
- **Solution**:
  - The codebase includes an automatic fallback: if length > 1850 chars, it converts the output into a `.txt` buffer and sends it as an attachment (`io.BytesIO`). Verify that the bot has `Attach Files` permission in the channel.

---

### `/summary` returns: "Only members with Manage Server permission can run this report"
- **Cause**: The user invoking `/summary` does not hold the `manage_guild` permission in the Discord server.
- **Solution**:
  - In your server settings ➔ Roles ➔ grant your user's role the **Manage Server** permission, or test with the server owner account.

---

### Bot responds twice to every command
- **Cause**: Two instances of the bot are running concurrently (e.g., both a local terminal and a Colab cell running simultaneously).
- **Solution**:
  - Terminate any background python processes (`pkill -f bot.py`) or close the redundant Colab tab.
