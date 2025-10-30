# SpongeBob Chatbot (gemma3:4b)

A fun command-line chatbot that talks like SpongeBob SquarePants using the OpenAI-compatible API at https://ai.sooners.us.

---

## 🧠 Features

- Talks like SpongeBob — cheerful, ocean humor, fun replies
- Keeps chat history between turns
- Uses the `gemma3:4b` model through ai.sooners.us
- Loads secrets from a local `.env` file (never committed)
- Clean CLI interface

---

## ⚙️ Setup Instructions

### 1️⃣ Create API key

1. Visit [https://ai.sooners.us](https://ai.sooners.us)
2. Sign up / log in with your OU email.
3. Go to **Settings → Account → API Keys**
4. Click **Create New Key** and copy it.

---

### 2️⃣ Create your `.soonerai.env` file

Create a hidden file in your **home directory** or inside this folder:

⚠️ Never upload this file to GitHub (it contains your private key).

---

### 3️⃣ Install requirements

Run these commands in your terminal:

````bash
cd ~/Desktop/project_chatbot
pip install -r requirements.txt
` ``` `

---

### 4️⃣ How to Run the Chatbot

Once dependencies are installed and your `.soonerai.env` file is created, run:

```bash
python3 spongebob_cli.py

---

### Example Transcript

Below is a short sample conversation showing that the chatbot runs successfully and responds in SpongeBob’s cheerful style:

🌊 Ahoy! I’m SpongeBob (gemma3:4b on ai.sooners.us). Type 'exit' to quit.

You: Hi SpongeBob! How’s your day under the sea?
SpongeBob: Barnacles! It’s a bubbly day! The jellyfish are dancing, and I’m flipping Krabby Patties with a smile! 🍔🌊

You: Tell me a joke.
SpongeBob: Why did the seaweed blush? Because it saw the ocean’s bottom! Heehee!

You: Give me some Monday motivation.
SpongeBob: Just keep paddling, buddy! Even sea snails reach their goals—slow and steady! 🐌✨

You: Bye SpongeBob!
SpongeBob: Bye-bye! Don’t forget to smile—it’s free! 😀🌊
````
