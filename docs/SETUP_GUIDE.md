# Comprehensive Step-by-Step Setup Guide

This guide walks you through every configuration step required to launch your bot, from Discord portal registration to GroqCloud API key creation and running locally or in Colab.

---

## Part 1: Discord Developer Portal Configuration

### Step 1: Create Your Application
1. Navigate to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click the **New Application** button in the upper-right corner.
3. Enter an application name (e.g., `SkillUp AI Agent`) and accept Discord's terms.
4. Click **Create**.

### Step 2: Configure the Bot User & Token
1. In the left navigation menu, click **Bot**.
2. Click **Reset Token**, confirm the prompt, and **Copy** the token immediately.
   > **Note:** Store this token securely. Discord will never display this token again.
3. Scroll down to **Privileged Gateway Intents**.
4. Enable the toggle for **Message Content Intent**.
   > **Critical:** If this toggle is disabled, Discord will throw `PrivilegedIntentsRequired` when the bot connects.
5. Click **Save Changes** at the bottom of the page.

### Step 3: Configure Guild Installation & OAuth2 Permissions
1. In the left sidebar, click **Installation**.
2. Under **Installation Contexts**, ensure **Guild Install** is checked.
3. Under **Default Install Settings**:
   - **Scopes**: Select `bot` and `applications.commands`.
   - **Permissions**: Select:
     - `View Channels`
     - `Send Messages`
     - `Read Message History`
     - `Attach Files`
4. Copy the generated **Install Link**.
5. Paste the link into a new browser tab, select your target Discord server, and click **Authorize**.

---

## Part 2: Discord Server ID Retrieval

1. Open your Discord desktop or web application.
2. Go to **User Settings** (gear icon) ➔ **Advanced** (under App Settings).
3. Enable the **Developer Mode** toggle.
4. Close settings.
5. In your server list on the left, right-click the server icon where the bot was installed.
6. Click **Copy Server ID**.
   - This numeric string (e.g. `123456789012345678`) is your `DISCORD_GUILD_ID`.

---

## Part 3: GroqCloud API Key

1. Navigate to [GroqCloud Console](https://console.groq.com/).
2. Create an account or sign in.
3. In the sidebar, navigate to **API Keys** (`https://console.groq.com/keys`).
4. Click **Create API Key**.
5. Give the key a descriptive name (e.g., `discord-agent-workshop`).
6. Copy the resulting key (starts with `gsk_...`).

---

## Part 4: Running the Bot

### Option A: Running with Google Colab (Zero-Install Setup)

1. Open [Google Colab](https://colab.research.google.com/).
2. Click **File** ➔ **Upload notebook**, and upload `SkillUp_Discord_AI_Agent.ipynb`.
3. In Colab's left sidebar, click the **Secrets icon (🔑)**.
4. Add the following three secrets:
   | Secret Name | Value |
   |---|---|
   | `DISCORD_BOT_TOKEN` | Your copied bot token |
   | `GROQ_API_KEY` | Your `gsk_...` key |
   | `DISCORD_GUILD_ID` | Your copied server ID |
5. **Important:** Enable the **Notebook access** toggle for all three secrets.
6. Click **Runtime** ➔ **Run all** (or press `Ctrl+F9`).
7. Wait until the output prints:
   ```text
   Slash commands synced: ['ping', 'agent', 'summary', 'help']
   ONLINE: SkillUp AI Agent#0000 | Server ID: 123456789012345678
   ```
8. The bot is now live in your server!

---

### Option B: Running Locally with Virtual Environment

1. Clone or open the repository folder:
   ```bash
   cd /path/to/discord-groq-bot
   ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your `.env` file:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and fill in your three values:
   ```env
   DISCORD_BOT_TOKEN=your_actual_token_here
   GROQ_API_KEY=gsk_your_actual_key_here
   DISCORD_GUILD_ID=your_numeric_server_id_here
   GROQ_MODEL=qwen/qwen3.8-27b
   ```
5. Run the pre-flight verification:
   ```bash
   python test_credentials.py
   ```
6. Start the bot:
   ```bash
   python bot.py
   ```


