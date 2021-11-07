[![Build Status](https://drone.kiwi-labs.net/api/badges/Diesel-Net/drone-discord/status.svg)](https://drone.kiwi-labs.net/Diesel-Net/drone-discord)

# drone-discord
Discord bot for Drone CI build logs

## Links

- [Discord Developer Portal](https://discord.com/developers)
- [`discord.py` API Reference](https://discordpy.readthedocs.io/en/latest/api.html#)


### Notes

- HTTP server
  - Trigger off of Drone events sent directly to my bot (over LAN)
    - [How to use global webhooks](https://discourse.drone.io/t/how-to-use-global-webhooks/3755)
    - [HTTP Signatures](https://datatracker.ietf.org/doc/html/draft-cavage-http-signatures-10)
  - Use [Flask](https://flask.palletsprojects.com/en/2.0.x/)
    - Might be overkill for one simple HTTP endpoint

- Discord Bot
  - Posts drone build logs in specific channel
  - Use [discord.py](https://pypi.org/project/discord.py/)

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


### Setup Environment
1. Create Python Virtual Environment and activate it
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install python depenencies
```bash
pip insall -r requirements.txt
```

3. TODO...

### Flask Server notes

- https://modelpredict.com/wht-requirements-txt-is-not-enough

```bash
python3 -m venv flask-venv
source flask-venv/bin/activate
pip install -e .
```
