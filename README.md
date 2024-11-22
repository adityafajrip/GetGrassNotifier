
# GetGrass Telegram Notifier

This is a Telegram Notifier Bot designed to send automatic notifications twice a day, at 12:00 AM UTC and 12:00 PM UTC. The bot retrieves and shares real-time earnings data from the app.getgrass.io platform, including:
Today’s Earnings, Total Earnings, Stage, Epoch Name, Start Date, End Date, Total Active Networks & List of Network with 0 IP Score

![Preview](https://github.com/adityafajrip/GetGrassNotifier/blob/main/Demo.png)


With this bot, users can stay updated on their earnings without having to manually check their Grass.io account. It’s a simple and efficient way to receive notifications on the go, ensuring you never miss important earnings updates!

https://t.me/GrassNotifierBot


## Features

- Add Token
- View Token
- Change Token
- Remove Token
- Check Earning (Stage, Epoch Name, Period, Today's Earning, Total Earning, Total Uptime, Total Network/IPs Connected & IPs with 0 Network Score)


## 📦Installation

```bash
  git clone https://github.com/adityafajrip/GetGrassNotifier.git
  cd GrassNotifier
```
## Install dependencies:

```bash
pip install -r requirements.txt
```
## Configuration

```bash
Change the file name from .env_copy to .env 
insert your Telegram bot token & IPData api key (Optional) the bot still running.
```

## Requirement

```python
Python 3.11 - Latest
```

## Usage

```python
pip install -r requirements.txt
python main.py
```

## FAQ: Why Are My Points Not Increasing or Different from the Dashboard?

Q: Why aren't my points increasing?
A: The bot fetches the points data directly from the API. If the data returned from the API is the same, then the points displayed in the bot will match the API response.

Q: Why do my points in the bot not match what’s shown in the dashboard?
A: The bot shows the points based on the data fetched from the API. If there's a discrepancy, it could be due to updates not reflected yet on the API or sync issues. Always check the API response for the most accurate data.

Q: Is the data from the bot always up-to-date?
A: The bot fetches the latest data available at the time of the request. However, if the API has a delay in updating, the displayed points might not immediately match what's on the dashboard.

Q: How can I make sure my points are correctly displayed?
A: Make sure you're using a valid API token and that the API response is returning correct and up-to-date data. If there’s an issue, try refreshing or re-authenticating the token.

## How to Get Authorization?

![Here](https://github.com/adityafajrip/GetGrassNotifier/blob/main/assets/tutorial.gif)


## Authors

- [@adityafajrip](https://www.github.com/adityafajrip) and my partner Chat GPT.

