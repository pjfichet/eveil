var pseudo;
var passwd1;
var passwd2;
var email;
var type;

function doInit()
{
	document.getElementById("input").style.display = 'none';
	document.getElementById("output").style.display = 'none';
	document.getElementById("create").style.display = 'none';
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
	document.getElementById("input").style.display = 'block';
	document.getElementById("output").style.display = 'block';
	document.getElementById("login").style.display = 'none';
	document.getElementById("create").style.display = 'none';
	doSend(type, pseudo, passwd1, passwd2, email);
}

function onClose(evt)
{
	document.getElementById("input").style.display = 'none';
	document.getElementById("output").style.display = 'none';
	document.getElementById("create").style.display = 'none';
	document.getElementById("login").style.display = 'block';
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

function findPos(obj)
{
	// Finds y value of given object
    var curtop = 0;
    if (obj.offsetParent) {
        do {
            curtop += obj.offsetTop;
        } while (obj = obj.offsetParent);
    return [curtop];
    }
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

function login() {
	var form = document.getElementById('login');
	type = 'login';
	pseudo = form.getElementById('pseudo').value;
	passwd1 = form.getElementById('passwd').value;
	doConnect();
}

function create() {
	var form = document.getElementById('create');
	type = 'create';
	pseudo = form.getElementById('pseudo').value;
	passwd1 = form.getElementById('passwd').value;
	passwd2 = form.getElementById('confirm').value;
	email = form.getElementById('email').value;
	doConnect();
}

function changeForm() {
	var login = document.getElementById('login');
	var create = document.getElementById('create');
	if (document.getElementById("create").style.display == 'none')
	{
		create.pseudo.value = login.pseudo.value;
		create.passwd.value = login.passwd.value;
		document.getElementById("create").style.display = 'block';
		document.getElementById("login").style.display = 'none';
	} else {
		login.pseudo.value = create.pseudo.value;
		login.passwd.value = create.passwd.value;
		document.getElementById("create").style.display = 'none';
		document.getElementById("login").style.display = "block";
	}
}


window.addEventListener("load", doInit, false);

