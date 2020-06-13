
start:
	python eveil.py

reset:
	rm -f data.db

new: reset start

WEBSOCK=https://github.com/dpallot/simple-websocket-server.git
SimpleWebSocketServer:
	git clone $(WEBSOCK)


