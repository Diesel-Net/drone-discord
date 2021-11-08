[![Build Status](https://drone.kiwi-labs.net/api/badges/Diesel-Net/drone-discord/status.svg)](https://drone.kiwi-labs.net/Diesel-Net/drone-discord)

# drone-discord
#### **Summary**
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A solution for posting [Drone](https://github.com/drone/drone)'s build logs to Discord. 
Comprising of 2 small main components, calling this a _bot_ seems like a bit of a stretch. 
It's more like a glorified logger with the ability to be modified or extended to support other communication platforms (like Slack).

#### **Why?**
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A drone server can [easily be configured](https://discourse.drone.io/t/how-to-use-global-webhooks/3755) to post all of it's events to an HTTP endoint of your choosing. 
Just knowing that fact made Discord's low-effort webhooks solution (similar to Discord's [GitHub integration](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)) very tempting. 
It would have done the job just fine, however this was limited to only being able to create new messages. I specifically wanted the ability to update existing messages as well.

#### **Components**
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The main (and only necessary) component that does all the work, is a very tiny Rest API (Flask App) for receiving the webhook events from the configured Drone Server. Once the payload is received and verified, Discord's REST API is then used to log the events nicely in the configured channel. A Mongo database is deployed with this service for added robustness.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For the other piece (optional), there is some minimal code hacked together with the sole purpose of connecting to the Gateway (WebSocket) API for being able to accuratley reflect the bot user's _Online_ status. This client process periodically checks-in on the Rest API to make sure it's healthy and adjusts the bot user's online presence accordingly.
It might be worth point out that this service is currently leveraging [`discord.py`](https://pypi.org/project/discord.py/) which is no longer being maintained, however I am confident that this _should_ work for quite some time until Discord's Gateway API changes dramatically, for any reason.



## Implementation Notes

- HTTP server
  - Trigger off of [drone events](https://discourse.drone.io/t/how-to-use-global-webhooks/3755) sent directly to my bot (over LAN)
  - Use [Flask](https://flask.palletsprojects.com/en/2.0.x/)
    - Webhook receiving endoint
      - HTTP POST
      - Verifies [HTTP Signatures](https://datatracker.ietf.org/doc/html/draft-cavage-http-signatures-10) from Drone
    - Healthcheck endpoint for both docker swarm and the bot service
      - HTTP GET
  - Data persistence
    - Discord message ID's
    - Use [pymongo](https://pymongo.readthedocs.io/en/stable/) to talk to MongoDB instance

- Discord Bot
  - Configured to post drone build updates in a specific channel
  - Not public, sense configured with a specific Drone instance and Discord server. However, a user may clone/fork or do whatever to deploy on their own system's if so desired
  - Use [discord.py](https://pypi.org/project/discord.py/)
    - [Hearbeating](https://discord.com/developers/docs/topics/gateway#heartbeating) to display online/offline status
    - Periodically checks if HTTP Server is healthy

- Logic
  - Create a new message on every new drone build
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
  - Other metadata to embed?
    - repo name
    - build number
    - version (branch, tag, commit)
    - link to build in drone
    - build time (how long did build take)
    - others?





## Deployment
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Deployed on docker swarm, automated with Ansible and Drone CI of course! A convenience script is provided to deploy manually, if needed.
```bash
source deploy.sh
```



## Run it locally

#### Bot
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

#### HTTP Server

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
