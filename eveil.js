function doInit()
{
	document.getElementById("sendButton").style.display = 'none';
	document.getElementById("inputText").style.display = 'none';
	document.getElementById("input").onkeypress = function(ev) {
		if (ev.keyCode == 13 || ev.which == 13) {
			document.getElementById("sendButton").click();
			ev.preventDefault();
		}
	};
}
function doConnect()
{
	ws = new WebSocket("ws://127.0.0.1:5678");
	ws.onopen = function (evt) { onOpen(evt) };
	ws.onclose = function (evt) { onClose(evt) };
	ws.onmessage = function (evt) { onMessage(evt) };
	ws.onerror = function(evt) { onError(evt) };
}

function onOpen(evt)
{
	document.getElementById("sendButton").style.display = 'inline-block';
	document.getElementById("inputText").style.display = 'inline-block';
	document.getElementById("connectButton").style.display = 'none';
}

function onClose(evt)
{
	document.getElementById("sendButton").style.display = 'none';
	document.getElementById("inputText").style.display = 'none';
	document.getElementById("connectButton").style.display = 'inline-block';
}

function onMessage(evt)
{
	writeToScreen(evt.data);
}

function onError(evt)
{
	writeToScreen('Error: ' + evt.data);
	ws.close();
}

function doSend(message)
{
	writeToScreen("> " + message); 
	ws.send(message);
}

function writeToScreen(message)
{
	var output = document.getElementById('output'),
	p = document.createElement('p');
	p.innerHTML = (message);
	output.appendChild(p);
	window.scroll(0, findPos(document.getElementById('input')));
}

function sendText() {
	doSend( document.getElementById('inputText').value );
}

//Finds y value of given object
function findPos(obj) {
    var curtop = 0;
    if (obj.offsetParent) {
        do {
            curtop += obj.offsetTop;
        } while (obj = obj.offsetParent);
    return [curtop];
    }
}

window.addEventListener("load", doInit, false);

