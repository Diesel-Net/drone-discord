[![Build Status](https://drone.kiwi-labs.net/api/badges/Diesel-Net/drone-discord/status.svg)](https://drone.kiwi-labs.net/Diesel-Net/drone-discord)

# drone-discord
#### **Summary**
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A solution for posting [Drone](https://www.drone.io/)'s build logs to Discord. 
Comprised of just 2 small main components, calling this a _bot_ seems like a bit of a stretch. 
It's more like a glorified logger with the ability to be modified or extended to support other communications platforms (like Slack) if so desired.

#### **Why?**
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A drone server can [easily be configured](https://discourse.drone.io/t/how-to-use-global-webhooks/3755) to post all of it's events to an HTTP endoint of your choosing. 
Just knowing that fact made Discord's low-effort webhooks solution (much like Discord's [GitHub integration](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)) look very tempting.
It would have done the job just fine, however this was limited to only being able to create new messages. I specifically wanted the ability to update existing messages as well.

#### **Components**
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The main (and only necessary) component that does all the work, is a tiny Rest API (Flask App) for receiving the webhook events from the configured Drone Server. Once the payload is received and verified, Discord's REST API is then used to log the events nicely in the configured channel. A Mongo database is deployed with this service for added robustness.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For the other piece (optional), there is some minimal code hacked together with the sole purpose of connecting to the Gateway (WebSocket) API for being able to accurately reflect the bot user's _Online_ status. This client process periodically checks-in on the Rest API to make sure it's healthy and adjusts the bot user's online presence accordingly.
It might be worth pointing out that this service is currently leveraging [`discord.py`](https://pypi.org/project/discord.py/) which is [no longer being maintained](https://gist.github.com/Rapptz/4a2f62751b9600a31a0d3c78100287f1), however I am confident that this _should_ still work for quite some time until Discord's Gateway API changes dramatically, for any reason. Thus an area of improvement could be to implement a lightweight Discord Websocket client from scratch, having only the features that it needs. 


## Implementation Notes

- Server (REST API)
  - Trigger off of [drone events](https://discourse.drone.io/t/how-to-use-global-webhooks/3755) sent directly to my bot (over LAN)
  - Uses [`Flask`](https://flask.palletsprojects.com/en/2.0.x/) microframework
  - Uses [`Gunicorn`](https://gunicorn.org/) as a production-ready webserver in front of flask
    - Webhook receiving endoint
      - HTTP POST
      - Verifies [HTTP Signatures](https://datatracker.ietf.org/doc/html/draft-cavage-http-signatures-10) from Drone
      - Configured to post drone events in a specific discord channel
    - Healthcheck endpoint
      - HTTP GET
      - Used by both docker and the client service
  - Data persistence
    - Drone events states?
    - Discord message ID's
    - Use [`PyMongo`](https://pymongo.readthedocs.io/en/stable/) to talk to MongoDB instance
  - Configuration
    - Discord bot token
    - Discord channel
    - Webhook endoint
    - Healthcheck endpoint
    - MongoDB
    - Gunicorn (docker only)

- Client (Websocket Connection)
  - Use [`discord.py`](https://pypi.org/project/discord.py/)
    - Leverages [hearbeating](https://discord.com/developers/docs/topics/gateway#heartbeating) to display online/offline status
  - Periodically checks if HTTP Server is healthy
    - Sets the bot user to offline in Discord if no 200 Ok response
  - Configuration
    - Discord bot token
    - Healthcheck URL

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
  - Other metadata/fields to embed?
    - repo name
    - build number
    - version (branch, tag, commit)
    - link to build in drone
    - build time (how long did build take)
    - others?


## Toolchain
- Python 3.9.7
- Ansible 4.6.0
- Ansible-Core 2.11.5
- Docker-Engine 20.10.8
- Docker-CLI 20.10.8


## Deployments
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Deployed onto docker swarm, and automated with Drone and Ansible.
A convenience script is provided to invoke the ansible playbook manually if needed. You will need to ensure a proper SSH configuration and have a [default Ansible vault password set](https://docs.ansible.com/ansible/latest/user_guide/vault.html#setting-a-default-password-source). Please see [deploy.sh](deploy.sh) for hints.
```bash
source deploy.sh
```


## Run it Locally
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;You will need a valid `.env` containing the necessary key/value pairs for configuration. This file should be added to .gitignore to prevent accidentally committing any secrets. Please read more about [`python-dotenv`](https://pypi.org/project/python-dotenv/) if you are unfamiliar with the syntax. 

```bash
# .env
DRONE_WEBHOOK_SECRET=webhook-secret
DISCORD_TOKEN=secret-token
DISCORD_CHANNEL_ID=873357168118755348
HEALTHCHECK_INTERVAL=10
HEALTHCHECK_URL=http://localhost:5000/health

MONGO_DATABASE=drone-discord
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=secret-password
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Each component needs to executed in it's own terminal window, as they are started using blocking calls.

#### MongoDB
1. Create Python Virtual Environment and activate it
   ```bash
   python3 -m venv mongo-venv && source mongo-venv/bin/activate
   ```

2. install python dependencies
   ```bash
   pip install "python-dotenv[cli]"
   ````

2. Start MongoDB container.
   Note that the `docker run` command is not able to see env vars for `-p` option so you will have to change the port numbers manually if going with a non-default configuration.
   ```bash
   dotenv run \
     docker run \
      -p 27017:27017 \
      -e MONGO_INITDB_ROOT_USERNAME \
      -e MONGO_INITDB_ROOT_PASSWORD \
      mongo
   ```

#### HTTP Server
1. Create Python Virtual Environment and activate it
   ```bash
   python3 -m venv server-venv && source server-venv/bin/activate
   ```

2. Install python depenencies
   ```bash
   pip install -r server-requirements.txt
   ```

3. Start Flask Development Server.
   ```bash
   flask run
   ```

   You may choose to reset the development database at any time.
   ```bash
   flask init-db
   ````


#### Websocket Client
1. Create Python Virtual Environment and activate it
   ```bash
   python3 -m venv client-venv && source client-venv/bin/activate
   ```

2. Install python depenencies
   ```bash
   pip install -r client-requirements.txt
   ```

3. Start Discord client.
   ```bash
   python client.py
   ```

#### Drone Events
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;There should be a collection of test curls in the root of this repository. These are useful for simulating drone events when running locally.
```bash
source test/repo_enabled.sh
source test/repo_disabled.sh

```
