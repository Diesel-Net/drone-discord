curl -X POST \
-H 'Signature: keyId="hmac-key",algorithm="hmac-sha256",signature="c/OTttF1uIwJF9kfn94ocOvOLJhrFx+n0mtedWOm8+0=",headers="date digest"' \
-H 'X-Drone-Event: repo' \
-H 'Date: Fri, 12 Nov 2021 23:33:47 GMT' \
-H 'Digest: SHA-256=kCit1zUa+1aDpnZhDSBCa0iVYPTeF6k2jCjHwE2lnQY=' \
-H "Content-type: application/json" \
-d '{ "action": "enabled" }' 'http://localhost:5000'
