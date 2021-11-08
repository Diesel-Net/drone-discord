[![Build Status](https://drone.kiwi-labs.net/api/badges/Diesel-Net/drone-discord/status.svg)](https://drone.kiwi-labs.net/Diesel-Net/drone-discord)

# drone-discord
A solution for posting Drone CI Server's build logs to Discord. 


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This bot is comprised of 2 main components and even calling it a _bot_ is a bit of a stretch. It's more like a logger. A drone server can easily be configured to post all of it's events to the url of your choosing. Just knowing that made Discord's low-effort Channel webhooks solution (similar to the Drone's official GitHub integration) very tempting, 
which would have done the job just fine, however I wanted to ability to edit existing messages as well as creating new messages.
The main (and only necessary) component that does all the work, is a very tiny Rest API (Flask App) for receiving the webhook events from the configured Drone Server. Once the payload is received and verified, Discord's REST API is then used to log the events nicely in the configured channel.
For the other piece, there is some minimal code hacked together with the soul purpose of connecting to the Gateway (WebSocket) API for being able to accuratley reflect the bot user's _Online_ status. This process periodically checks-in on the Rest API to make sure it's healthy and adjusts the bot user's online presence accordingly.
It might be worth point out that this part of the project is currently leveraging [`discord.py`](https://pypi.org/project/discord.py/) which is no longer being maintained, however I am confident that this _should_ work for quite some time until Discord's Gateway API changes dramatically, for any reason.


## Deployment
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Deployed on docker swarm, automated with Ansible and Drone CI of course! A convenience script is provided to deploy manually, if needed.
```bash
source deploy.sh
```

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
  - Not public, sense configured with a specific Drone instance and Discord server. However, a user may clone/fork do whatever to deploy on their own system's if so desired
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
