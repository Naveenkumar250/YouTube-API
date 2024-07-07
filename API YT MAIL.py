import os
import googleapiclient.discovery
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set up the YouTube Data API key
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
api_key = 'API key'

# Set up Gmail credentials - use your generated app password here
email_address = "naveen.m.chsm@gmail.com"
email_password = "Application Password"

# Function to search for channels by name
def search_channels_by_name(query):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        q=query,
        part="snippet",
        type="channel",
        maxResults=10
    )
    response = request.execute()

    channels = []
    for item in response["items"]:
        channel_info = {
            "title": item["snippet"]["title"],
            "channel_id": item["snippet"]["channelId"],
            "description": item["snippet"]["description"],
            "channel_url": f"https://www.youtube.com/channel/{item['snippet']['channelId']}"
        }
        channels.append(channel_info)
        channel_statistics = get_channel_statistics(channel_info["channel_id"])
        channel_info.update(channel_statistics)

    return channels

# Function to get channel statistics
def get_channel_statistics(channel_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.channels().list(
        part="statistics",
        id=channel_id
    )
    response = request.execute()

    if response["items"]:
        statistics = response["items"][0]["statistics"]
        return {
            "video_count": int(statistics["videoCount"]),
            "subscriber_count": int(statistics["subscriberCount"]),
            "view_count": int(statistics["viewCount"])
        }
    else:
        return {
            "video_count": 0,
            "subscriber_count": 0,
            "view_count": 0
        }

# Function to send email
def send_email(to_email, subject, message):
    try:
        # Set up SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(email_address, email_password)

        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Send email
        server.sendmail(email_address, to_email, msg.as_string())
        server.close()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", str(e))

# Example usage
search_query = input("Enter channel name to search: ")
channels = search_channels_by_name(search_query)

# Get max statistics
max_subscribers = max(channel['subscriber_count'] for channel in channels)
max_videos = max(channel['video_count'] for channel in channels)
max_views = max(channel['view_count'] for channel in channels)

# Filter channels with lower statistics
filtered_channels = []
for channel in channels:
    if (channel['subscriber_count'] < max_subscribers and
            channel['video_count'] < max_videos and
            channel['view_count'] < max_views):
        filtered_channels.append(channel)

#add some sentence
extra_sentence = "this are the channels are listed for copied your channel's content"

# Find the channel with maximum statistics
max_channel = max(channels, key=lambda x: (x['subscriber_count'], x['video_count'], x['view_count']))

# Prepare information about lower channels
lower_channels_info = "\n\nLower channels information:\n"
for channel in filtered_channels:
    lower_channels_info += f"Channel: {channel['title']}\n"
    lower_channels_info += f"channelid:{channel['channel_id']}\n"
    lower_channels_info += f"description:{channel['description']}\n"
    lower_channels_info += f"Subscribers: {channel['subscriber_count']}\n"
    lower_channels_info += f"Videos: {channel['video_count']}\n"
    lower_channels_info += f"Views: {channel['view_count']}\n\n"
    lower_channels_info += f"Channel URL: {channel['channel_url']}\n\n"

# Construct message
message = f"Hello {max_channel['title']},\n\nWe are gathering some channels information that are copied your contents listed below :\n\n"
message += f"Your Channel: {max_channel['title']}\n"
message += f"channelid:{channel['channel_id']}\n"
message += f"description:{channel['description']}\n"
message += f"Subscribers: {max_channel['subscriber_count']}\n"
message += f"Videos: {max_channel['video_count']}\n"
message += f"Views: {max_channel['view_count']}\n\n"
message += f"Channel URL: {max_channel['channel_url']}\n\n"
message += lower_channels_info
message += f"{extra_sentence}\n\nBest regards,\n[naveen]"

# Send email to max channel
send_email("naveenkumarmoorthi1020@gmail.com", "channels information", message)


