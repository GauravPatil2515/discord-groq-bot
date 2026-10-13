# Facilitator Explainer Guide: Build a Discord AI Agent

This guide is designed to help you **understand, replicate, and clearly explain** the entire Discord AI Agent project to anyone (students, freshers, team members, or hackathon participants).

---

## 🧠 1. The Big Picture (Mental Model)

Before opening any tabs or code, explain the **3-Tier Architecture**:

```
[ User in Discord ]
        │  Types slash command (e.g. /agent or /summary)
        ▼
[ Discord Gateway / Server ]
        │  Routes command payload to our running bot
        ▼
[ Colab Notebook / Python Bot ] (The Coordinator)
        │  1. Receives command & validates permissions
        │  2. Collects channel messages (if /summary)
        │  3. Asynchronously sends prompt & messages to Groq
        ▼
[ GroqCloud API (LPU Inference) ] (The Brain)
        │  Runs LLM (e.g., qwen/qwen3.8-27b) ultra-fast
        ▼
[ Python Bot ] ──▶ Sends formatted response back ──▶ [ Discord User ]
```

### Key Analogy to Use When Explaining:
- **Discord** is the *Receptionist* (where users interact and type commands).
- **Python / Colab** is the *Office Manager* (coordinates permissions, gathers chat history, structures requests).
- **GroqCloud** is the *Analyst / Brain* (reads text, generates answers, summarizes decisions).

---

## 🔑 2. The Permission Matrix (Crucial Teaching Point)

Beginners always get confused by Discord permissions. Use this clear breakdown:

| Level | Where it is set | What it controls | Example |
|---|---|---|---|
| **1. Application Scopes** | Developer Portal ➔ OAuth2 / Install | What high-level Discord subsystems the bot accesses | `bot`, `applications.commands` |
| **2. Gateway Privileged Intents** | Developer Portal ➔ Bot settings | Real-time stream permissions Discord grants the bot | `Message Content Intent` (allows reading text body) |
| **3. Server / Channel Permissions** | Server Roles / Channel Settings | What channels the bot can view and read in a specific server | `View Channels`, `Read Message History`, `Send Messages` |
| **4. User Invoker Permissions** | User's role in the server | Who has authority to trigger sensitive commands | `Manage Server` (only managers can run `/summary`) |

---

## 🗺️ 3. Step-by-Step Island Walkthrough

### Island 00: Account & Environment Setup
- **What to do:**
  1. Have Discord desktop/web app open.
  2. Create a clean practice test server (e.g., "AI Workshop Lab") with channels: `#general`, `#ai-lab`, `#announcements`.
  3. Create an account on [GroqCloud Console](https://console.groq.com/).
  4. Open [Google Colab](https://colab.research.google.com/).
- **How to explain it:**
  *"We don't need any local setup, Docker, or high-end GPU laptops. We use Discord for the UI, Groq for lightning-fast free LLM inference, and Colab as a free cloud Python runtime."*

---

### Island 01: Discord Developer Portal
- **What to do:**
  1. Visit [discord.com/developers/applications](https://discord.com/developers/applications).
  2. Click **New Application** ➔ Name it `SkillUp AI Agent`.
  3. Go to **Bot** in sidebar ➔ Click **Reset Token** ➔ Copy the token immediately! (Save it safely; Discord only shows it once).
  4. Scroll down to **Privileged Gateway Intents** ➔ Turn on **Message Content Intent** ➔ Click **Save Changes**.
- **How to explain it:**
  - *Application* = The cloud container/project on Discord.
  - *Bot* = The virtual user that joins servers.
  - *Token* = The secret password the bot uses to log in.
  - *Message Content Intent* = Privacy protection. Discord doesn't give bots message text by default; you must explicitly enable it.

---

### Island 02: Invite Bot to Your Server
- **What to do:**
  1. In the Dev Portal, go to **Installation**.
  2. In **Installation Contexts**, check **Guild Install**.
  3. In **Default Install Settings**, select Scopes: `bot` and `applications.commands`.
  4. Select Permissions: `View Channels`, `Send Messages`, `Read Message History`.
  5. Copy the generated **Install Link**, open it in your browser, select your practice server, and click **Authorize**.
  6. In Discord: Enable **Developer Mode** (*User Settings ➔ Advanced ➔ Developer Mode*). Right-click your server icon ➔ **Copy Server ID** (`DISCORD_GUILD_ID`).
- **How to explain it:**
  *"We follow the Principle of Least Privilege: never grant Administrator permission when simple read/send permissions are enough."*

---

### Island 03: GroqCloud API Key
- **What to do:**
  1. Go to [console.groq.com/keys](https://console.groq.com/keys).
  2. Create a new key with label `skillup-discord-demo`.
  3. Copy the `gsk_...` key.
- **How to explain it:**
  *"Groq uses custom hardware called LPUs (Language Processing Units). Instead of waiting 10-15 seconds for a model to stream, Groq generates hundreds of tokens per second, making Discord interactions feel instant."*

---

### Island 04: Secrets Setup
- **What to do in Colab:**
  1. In Google Colab, click the **Key icon (🔑 Secrets)** on the left sidebar.
  2. Add three secrets:
     - `DISCORD_BOT_TOKEN`
     - `GROQ_API_KEY`
     - `DISCORD_GUILD_ID`
  3. **Crucial:** Turn ON the toggle **"Notebook access"** for all three secrets!
- **How to explain it:**
  *"Never hardcode API keys or bot tokens inside Python code. If you share your screen or notebook, anyone can steal your credentials. Colab Secrets inject keys directly into memory."*

---

### Island 05: Code Architecture Breakdown

Walk through the code in logical blocks:

#### Block 1: Clean Restart / Re-run Guard
```python
old_bot = globals().get("_skillup_bot")
old_task = globals().get("_skillup_task")
if old_bot is not None and not old_bot.is_closed():
    await old_bot.close()
```
**Why:** In Colab or interactive notebooks, re-running a cell starts a duplicate bot without killing the old socket connection. This code gracefully disconnects the old bot first.

#### Block 2: Fast Guild Command Sync
```python
class SkillUpBot(commands.Bot):
    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD)
        synced = await self.tree.sync(guild=GUILD)
```
**Why:** Global slash commands take up to **1 hour** to propagate across Discord. Guild-scoped commands sync **instantly** (within seconds), which is critical for live workshop demonstrations!

#### Block 3: `/agent` with Deferral
```python
await interaction.response.defer(thinking=True)
```
**Why:** Discord has a strict **3-second timeout** for slash commands. If your LLM takes 3.5 seconds, Discord throws "The application did not respond". `defer(thinking=True)` tells Discord: *"I'm working on it, show a thinking state for up to 15 minutes."*

#### Block 4: Message Length Guard
```python
if len(answer) <= 1850:
    await interaction.followup.send(answer)
else:
    report = discord.File(io.BytesIO(answer.encode("utf-8")), "agent_answer.txt")
```
**Why:** Discord has a strict **2000 character limit** per message. If the AI generates an in-depth essay, sending raw text crashes the bot. Wrapping excess text into an attached file prevents errors.

#### Block 5: `/summary` Permission & Privacy Guard
```python
if not member.guild_permissions.manage_guild:
    return  # Only managers can inspect server logs
...
await interaction.followup.send(..., ephemeral=True)
```
**Why:** Summaries are sensitive. The code restricts execution to users with `Manage Server` and returns the file `ephemeral=True` (visible ONLY to the invoker).

---

## 🎤 4. 10-Minute Live Demo Script (Step-by-Step)

Follow this exact order when presenting:

1. **Test 1: `/ping`**
   - *Action:* Type `/ping` in `#general`.
   - *Result:* `Pong! Your SkillUp bot is online.`
   - *Explanation:* *"This validates the WebSocket handshake between Discord and Python. No LLM has been touched yet."*

2. **Test 2: `/agent`**
   - *Action:* Type `/agent prompt: Explain what an API is in 2 sentences.`
   - *Result:* Instant response from Groq.
   - *Explanation:* *"Notice the speed. Discord routed the slash command to Python, Python sent an async request to Groq, and Groq responded via LPU in milliseconds."*

3. **Test 3: Seed Conversation**
   - *Action:* Switch to `#ai-lab`. Post 3 dummy messages:
     - *"Team, we decided to use Groq for model inference."*
     - *"Riya is finalizing the presentation slides by 5 PM."*
     - *"Vikram will configure the Discord bot server permissions."*

4. **Test 4: `/summary`**
   - *Action:* Type `/summary messages_per_channel:30`.
   - *Result:* Bot analyzes channels and delivers `skillup_server_summary.txt` as a private ephemeral file.
   - *Explanation:* *"The bot extracted messages, stripped bot messages, verified permissions, sent the transcript as context data to Groq, and extracted structured decisions and action items."*

5. **Test 5: `/help`**
   - *Action:* Type `/help`.
   - *Result:* Clean ephemeral command menu.

---

## 🛠️ 5. Troubleshooting Cheat Sheet

| Symptom | Cause | Solution |
|---|---|---|
| **Bot is Offline** | Colab runtime stopped or disconnected. | Click "Connect" in Colab and re-run the cell. |
| **"PrivilegedIntentsRequired"** | Message Content Intent is disabled. | In Dev Portal ➔ Bot ➔ Toggle ON "Message Content Intent" ➔ Save. |
| **Commands don't appear in Discord** | Scope missing or server ID wrong. | Re-invite with `applications.commands` scope and verify `DISCORD_GUILD_ID`. |
| **Groq 401 Unauthorized** | Invalid API Key. | Re-generate key at `console.groq.com/keys` and update `GROQ_API_KEY`. |
| **Groq 404 Model Not Found** | Model name deprecated. | Use `qwen/qwen3.8-27b` or fallback to `llama-3.3-70b-versatile`. |
| **Summary says "Permission Denied"** | User lacks Manage Server permission. | Grant your Discord user role the Manage Server permission in server settings. |
| **Bot responds twice** | Multiple runtimes running simultaneously. | Close old Colab tabs or rerun cell so the shutdown hook terminates the old socket. |
