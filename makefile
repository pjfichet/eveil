
WEBSOCK=https://github.com/dpallot/simple-websocket-server.git

SimpleWebSocketServer:
	git clone $(WEBSOCK)

start:
	python eveil.py

reset:
	rm data.db
