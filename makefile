
WEBSOCK=https://github.com/dpallot/simple-websocket-server.git

start:
	python eveil.py

reset:
	rm data.db

SimpleWebSocketServer:
	git clone $(WEBSOCK)


