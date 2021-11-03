[![Build Status](https://drone.kiwi-labs.net/api/badges/Diesel-Net/drone-discord/status.svg)](https://drone.kiwi-labs.net/Diesel-Net/drone-discord)

# drone-discord
Discord bot for Drone CI Server


### Notes

- Trigger off of Drone events sent directly to my bot (over LAN)
  - Due to this setup, this bot will only work with my Drone server, so most likely won't allow public installs (on other discord servers)
  - https://discourse.drone.io/t/how-to-use-global-webhooks/3755

- Create a new message on every new build
  - "Build started"
    - Yellow
    - spinning wheel emoji while build is in progress?

- Update same message with build status
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
