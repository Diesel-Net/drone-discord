# signed with key: webhook-secret

curl -X POST \
-H 'Signature: keyId="hmac-key",algorithm="hmac-sha256",signature="nMQOWQSyloFPh3ZB8Uoh/D9QyzCtnVf0tk/jemJm058=",headers="date digest"' \
-H 'X-Drone-Event: user' \
-H 'Date: Fri, 12 Nov 2021 23:33:47 GMT' \
-H 'Digest: SHA-256=kCit1zUa+1aDpnZhDSBCa0iVYPTeF6k2jCjHwE2lnQY=' \
-H "Content-type: application/json" \
-d @test/user_updated.json 'http://localhost:5000'
