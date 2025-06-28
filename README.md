


#🧠 git‑sage

**Your AI-powered composer of GitHub contribution insights.**

git‑sage is a Flask-based web app that fetches a GitHub user’s activity commits, pull requests, and issues and employs OpenAI to generate clear, actionable summaries. Each summary is paired with auto-generated tags (e.g., `bugfix`, `feature`) to help you reflect on your coding patterns.

---

## ✨ Features

- 🔎 Fetches recent GitHub activities (commits, PRs, issues)
- 🤖 Uses OpenAI to produce clean, human-readable summaries
- 🏷️ Auto-tags activities for quick categorization
- 📊 Displays counts and a timeline of contributions
- 🎨 Built with Flask and Bootstrap for a responsive UI

---

## 💡 Use Cases

- 🧠 Generate weekly/monthly summaries of your contributions  
- 👨‍💻 Enhance resumes or developer portfolios with AI-crafted insights  
- 🔍 Track your coding habits and focus areas  
- 📈 Build quick personal dashboards or analytics tools

---

## 🛠️ Technologies Used

- **Flask** – Backend web server  
- **OpenAI API** – Summaries and insights via ChatGPT  
- **GitHub REST API** – Fetching user contributions  

---
Bootstrap – Responsive UI styling
---
## 📦 Getting Started

### 1. Clone the repository:
```bash
git clone https://github.com/SCodezz/git-sage.git
cd git-sage
````

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables:

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-openai-api-key-here
GITHUB_TOKEN=your-github-token-here
```


### 4. Run the application:

```bash
python server.py
```

Then open your browser at: [http://localhost:5000](http://localhost:5000)

---

## 🔧 Environment Variables

| Variable         | Description                                    |
| ---------------- | ---------------------------------------------- |
| `OPENAI_API_KEY` | Key for accessing OpenAI to generate summaries |
| `GITHUB_TOKEN`   | GitHub token (optional) to increase API limits |

---

## 📁 Project Structure

```plaintext
git-sage/
├── templates/
│   └── index.html        # Frontend UI template
├── server.py             # Flask app logic and API routes
├── requirements.txt      # Python dependencies
├── .env.example          # Template for environment variables
├── .gitignore            # Ignores .env and other temp files
└── README.md             # This file
```



---

## 👤 Author

**Shreya S** — GitHub: [@SCodezz](https://github.com/SCodezz)



---


