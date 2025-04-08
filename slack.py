import requests

def send_message(token, channel, msg):
    # Slack API endpoint
    url = "https://slack.com/api/chat.postMessage"

    # Your Slack OAuth Token (Bot User OAuth Token)
    slack_token = token

    # The channel to which you want to send the message
    slack_channel = channel

    # The message you want to send
    message = msg

    # Headers to authenticate the request
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }

    # Payload with the message and channel
    payload = {
        "channel": slack_channel,
        "text": message
    }

    #    Sending the POST request to Slack API
    response = requests.post(url, headers=headers, json=payload)

    # Check the response from Slack API
    if response.status_code == 200 and response.json().get("ok"):
        print("Message sent successfully!")
    else:
        print("Error sending message:", response.text)
