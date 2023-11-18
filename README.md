curl -v -X POST -H "X-API-KEY: 00000000-0000-0000-0000-000000000000" --data "`cat test.md`" "https://api.relay.md/v1/doc?filename=foobar.md"
curl -v -H "X-API-KEY: 00000000-0000-0000-0000-000000000000" -H "Content-Type: text/markdown" https://api.relay.md/v1/doc/8ff0f894-4c51-46ea-8c7e-b8bff9273c05
curl -v -H "X-API-KEY: 00000000-0000-0000-0000-000000000000" https://api.relay.md/v1/doc/8ff0f894-4c51-46ea-8c7e-b8bff9273c05

