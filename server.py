# server.py
from flask import Flask, request, jsonify, render_template
import requests
from datetime import datetime, timedelta
import os
import openai
import re
import json

app = Flask(__name__)

app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
app.config['GITHUB_TOKEN'] = os.getenv('GITHUB_TOKEN', 'your-github-token-here')  

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze GitHub contributions for a user"""
    data = request.json
    username = data.get('username')
    days = int(data.get('days', 7))
    
    if not username:
        return jsonify({"error": "Username required"}), 400

    try:
        # ser profile
        user_data = get_user_profile(username)
        
        # recent activity
        contributions = get_recent_activity(username, days)
        
        # Generate AI summary
        summary = generate_summary(contributions) if contributions else "No recent activity found"
        
        # Extract tags
        tags = extract_tags(contributions)
        
        return jsonify({
            "avatar_url": user_data.get('avatar_url'),
            "name": user_data.get('name', username),
            "bio": user_data.get('bio', ''),
            "public_repos": user_data.get('public_repos', 0),
            "commit_count": sum(1 for c in contributions if c['type'] == 'commit'),
            "pr_count": sum(1 for c in contributions if c['type'] == 'pr'),
            "issue_count": sum(1 for c in contributions if c['type'] == 'issue'),
            "summary": summary,
            "tags": list(set(tags)),
            "contributions": contributions
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_user_profile(username):
    """Fetch GitHub user profile"""
    headers = {'Authorization': f'token {app.config["GITHUB_TOKEN"]}'} if app.config['GITHUB_TOKEN'] else {}
    response = requests.get(f'https://api.github.com/users/{username}', headers=headers)
    if response.status_code != 200:
        raise Exception(f"User '{username}' not found")
    return response.json()

def get_recent_activity(username, days):
    """Fetch recent GitHub activity"""
    since_date = (datetime.now() - timedelta(days=days)).isoformat()
    headers = {'Authorization': f'token {app.config["GITHUB_TOKEN"]}'} if app.config['GITHUB_TOKEN'] else {}
    
    # Get events
    events = requests.get(
        f'https://api.github.com/users/{username}/events',
        params={'per_page': 100},
        headers=headers
    )
    
    if events.status_code != 200:
        return []
    
    events = events.json()
    
    contributions = []
    for event in events:
        event_date = event.get('created_at', '')
        if not event_date or event_date < since_date:
            continue
            
        if event['type'] == 'PushEvent':
            for commit in event['payload'].get('commits', []):
                contributions.append({
                    "type": "commit",
                    "title": commit['message'].split('\n')[0],
                    "date": event_date,
                    "repo": event['repo']['name']
                })
        elif event['type'] == 'PullRequestEvent':
            pr = event['payload']['pull_request']
            contributions.append({
                "type": "pr",
                "title": pr['title'],
                "date": event_date,
                "repo": event['repo']['name']
            })
        elif event['type'] == 'IssuesEvent':
            issue = event['payload']['issue']
            contributions.append({
                "type": "issue",
                "title": issue['title'],
                "date": event_date,
                "repo": event['repo']['name']
            })
    
    # Sort by date descending
    contributions.sort(key=lambda x: x['date'], reverse=True)
    return contributions[:15]  # Return max 15 items

def generate_summary(contributions):

    if not contributions:
        return "No recent activity found"
    
    activities = "\n".join([f"- {c['type'].upper()}: {c['title']} ({c['repo']})" for c in contributions])
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": """You summarize GitHub activity with these rules:
1. Group identical/similar items together
2. Remove technical implementation details unless crucial
3. Start each bullet with a verb
4. Include the impact/benefit
5. Maximum 3-5 bullet points"""
                },
                {
                    "role": "user", 
                    "content": f"Clean and summarize these activities:\n{activities}"
                }
            ],
            temperature=0.3,
            max_tokens=200
        )
        summary = response.choices[0].message['content'].strip()
        return summary if summary.startswith('•') else f"• {summary}"
    except Exception as e:
        return generate_fallback_summary(contributions)

def generate_fallback_summary(contributions):
    """Fallback when OpenAI fails"""
    unique_activities = {}
    for c in contributions:
        key = c['title'].split(':')[0].split('(')[0].strip()
        unique_activities[key] = unique_activities.get(key, 0) + 1
    
    bullets = []
    for activity, count in unique_activities.items():
        if count > 1:
            bullets.append(f"• Made {count} improvements to {activity}")
        else:
            bullets.append(f"• {activity}")
    
    return '\n'.join(bullets[:5]) or "• Various code improvements"


def extract_tags(contributions):
    """Extract tags from contributions using rule-based approach"""
    tags = []
    for c in contributions:
        content = c['title'].lower()
        if any(word in content for word in ['fix', 'bug', 'error', 'resolve']):
            tags.append('bugfix')
        elif any(word in content for word in ['feat', 'add', 'implement', 'create', 'new']):
            tags.append('feature')
        elif any(word in content for word in ['doc', 'readme', 'comment', 'guide']):
            tags.append('documentation')
        elif any(word in content for word in ['refactor', 'optimize', 'improve']):
            tags.append('refactoring')
        elif any(word in content for word in ['test', 'coverage', 'spec']):
            tags.append('testing')
    return tags if tags else ['development']

if __name__ == '__main__':
    app.run(debug=True, port=5000)