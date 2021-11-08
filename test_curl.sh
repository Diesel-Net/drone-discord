curl -XPOST \
-H 'Signature: "hmac-key",algorithm="hmac-sha256",signature="25qusRMTpcGA6q+TO0IjlSLQJ1N+rzi9aENjeB5B+PQ=",headers="date digest"' \
-H 'Date: Wed, 28 Oct 2020 23:05:22 GMT' \
-H 'Digest: SHA-256=9H4/Wp3eNf5Ucx7TKTu8pyloEgW8SViM52q5tjuDh9U=' \
-H "Content-type: application/json" \
-d '{ test: "ok" }' 'http://localhost:5000/hook'
