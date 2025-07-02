import requests
def post_to_slack(message: dict):
    """
    Posts a stylish message to a Slack channel using a webhook URL.

    Args:
        message (dict): The last record from the conversation array, containing role, content, speaker, and timestamp.
    """
    webhook_url = "https://hooks.slack.com/services/XXXXX"
    
    speaker = message.get('speaker', 'Unknown')
    content = message.get('content', '')
    timestamp = message.get('ts', 'Unknown')

    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"\n*{speaker}*: {content}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Timestamp: {timestamp}"
                    }
                ]
            }
        ]
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print("Message posted successfully.")
    else:
        print(f"Error posting message: {response.status_code}, {response.text}")
