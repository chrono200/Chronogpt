# Chronogpt
ChronoGPT is a cyberpunk-style AI chat assistant for Termux, powered by OpenRouter.

# ChronoGPT

A terminal AI assistant built for Termux. Powered by OpenRouter, designed by Chrono.

ChronoGPT brings AI chat into your Android terminal with a dark cyberpunk-style interface. No complicated dashboard. Open Termux, launch ChronoGPT, and start chatting.

## What it can do

- Chat with AI directly from your terminal
- Stream responses as they're generated
- Connect to models available through OpenRouter
- Change the active model
- Keep conversation history while the session is running
- Use simple commands to control the chat

## Before you start

You'll need:

- An Android phone with Termux
- An internet connection
- Python and Git
- Your own OpenRouter API key

Get your key here: https://openrouter.ai/keys

## Get it running

### 1. Update Termux

Start by updating your packages:

```bash
pkg update && pkg upgrade
```

### 2. Install Python and Git

```bash
pkg install python git
```

### 3. Download ChronoGPT

Clone the repository:

```bash
git clone https://github.com/chrono200/Chronogpt.git
cd Chronogpt
```

### 4. Install the Python dependency

```bash
python -m pip install -r requirements.txt
```

If pip refuses to install packages into your main Python environment, create a virtual environment instead:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 5. Connect your OpenRouter key

ChronoGPT needs an API key to talk to OpenRouter.

Create one at https://openrouter.ai/keys, then run:

```bash
export OPENROUTER_API_KEY="YOUR_API_KEY"
```

Replace `YOUR_API_KEY` with your own key. Keep it private. This command sets it for the current shell session.

### 6. Launch ChronoGPT

```bash
python chronogpt.py
```

That's it. If the setup is correct and your selected model is available, ChronoGPT should start in your terminal.

## Commands

Inside the chat:

- `/help` — see the available commands
- `/clear` — clear the current conversation
- `/model` — check the active model
- `/exit` — close ChronoGPT

You can also try these options from the terminal if they're supported by your installed version:

```bash
python chronogpt.py --models
python chronogpt.py --set-model MODEL_ID
```

Replace `MODEL_ID` with a model ID available through OpenRouter.

## If something goes wrong

**Authentication error?** Check your API key and make sure it hasn't been revoked.

**Model unavailable?** Check the model ID and its availability on OpenRouter.

**Rate limit or insufficient credits?** Some models have usage limits or costs. Free availability isn't guaranteed.

**Missing Python package?** Run:

```bash
python -m pip install -r requirements.txt
```

## A quick security note

Your API key belongs to you. Don't upload it to GitHub, include it in screenshots, or share it with other users. Every user should configure their own key.

## What's next?

ChronoGPT is still being developed. The goal is to make setup easier, improve the experience, and eventually make it installable through a proper Termux package repository.

Built by Chrono.
