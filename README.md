[![Build Status](https://drone.kiwi-labs.net/api/badges/Diesel-Net/drone-discord/status.svg)](https://drone.kiwi-labs.net/Diesel-Net/drone-discord)

# drone-discord
Discord bot for Drone CI build logs. 
This bot is comprised of 2 main components and even calling it a "bot" is a bit of a stretch. 
Drone CI can easily be configured to post all of it's event to the url of your choosing. 
I contemplated using Drone's Channel webhooks (much like the GitHub integration), 
which would have done the job okay, however I wanted to ability to not just create a message but update an existing message as well.
There is some minimal code hacked together for connecting to the Gateway (WebSocket) API with the soul purpose of being able to accuratley reflect the bot user's _Online_ status. 
I am currently leveraging [`discord.py`](https://pypi.org/project/discord.py/) which is no longer being maintained, however this should work for quite awhile unless the core websocket's API changes dramatically for any reason in the future.
The other main piece is a minimal Flask App for receiving the webhook events from the configured Drone CI Server.

## Links

- [Discord Developer Portal](https://discord.com/developers)
  - Flask supports asyncio operations as of 2.0


### Notes

- HTTP server
  - Trigger off of Drone events sent directly to my bot (over LAN)
    - [How to use global webhooks](https://discourse.drone.io/t/how-to-use-global-webhooks/3755)
    - [HTTP Signatures](https://datatracker.ietf.org/doc/html/draft-cavage-http-signatures-10)
  - Use [Flask](https://flask.palletsprojects.com/en/2.0.x/)
    - Might be overkill for one simple HTTP endpoint
  - Add healthcheck endpoint for the persistent "bot" connection

- Discord Bot
  - Posts drone build logs in specific channel
  - Use [discord.py](https://pypi.org/project/discord.py/)
    - Just to display online/offline status
      - Periodically hit a healthcheck endpoint on the api

  - Create a new message on every new build
    - "Build started"
      - Yellow
      - spinning wheel emoji while build is in progress?

  - Edit same message with build status
    - "Build success"
      - Green
      - Green checkmark emoji?
    - "Build failure"
      - Red
      - Red X emoji?

  - Other metadata
    - repo name
    - build number
    - version (branch, tag, commit)
    - link to build in drone
    - build time (how long did build take)
    - others?

  - Data persistence
    - MongoDB
      - Overkill?
      - Would be better than storing message ID's in memory in case of reboot or crash


### Bot
1. Create Python Virtual Environment and activate it
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install python depenencies
   ```bash
   pip insall -r bot-requirements.txt
   ```

3. TODO...

### HTTP Server

1. Create Python Virtual Environment and activate it
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install python depenencies
   ```bash
   pip insall -r api-requirements.txt
   ```
   ```bash
   python3 -m venv api-venv
   source api-venv/bin/activate
   
   ```
