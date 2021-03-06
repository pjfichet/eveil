var pseudo;
var passwd1;
var passwd2;
var email;
var method;

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
	if (method == 'login') {
		if (typeof pseudo !== 'undefined' && typeof passwd1 !== 'undefined') {
			doSend('login ' + pseudo + ' ' + passwd1);
		}
	}
	if (method == 'create') {
		if (typeof pseudo !== 'undefined' && typeof passwd1 !== 'undefined'
		&& typeof passwd2 !== 'undefined' && typeof email !== 'undefined') {
			doSend('create ' + pseudo + ' ' + passwd1 + ' ' + passwd2 + ' ' + email);
		}
	}
}

function onClose(evt)
{
	document.getElementById("input").style.display = 'none';
	/* document.getElementById("output").style.display = 'none'; */
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
	//writeToScreen("> " + message); 
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

function stringToElem(string)
{
	// Convert a string do a dom element
	var template = document.createElement('template');
	string = string.trim();
	template.innerHTML = string;
	return template.content.firstChild;
}

function writeToScreen(message)
{
	var output = document.getElementById('output');
	output.appendChild(stringToElem(message));
	// set the size of #bottom to scroll above the fixed #input
	var h = document.getElementById("input").offsetHeight;
	document.getElementById("bottom").setAttribute("style", "height:" + h + "px");
	window.scroll(0, findPos(document.getElementById('bottom')));
}

function sendText() {
	var input = document.getElementById('inputText');
	doSend( input.value );
	input.value = '';
}

function dologin() {
	var form = document.getElementById('login');
	pseudo = form.pseudo.value;
	passwd1 = form.passwd.value;
	method = 'login';
	doConnect();
}

function docreate() {
	var form = document.getElementById('create');
	pseudo = form.pseudo.value;
	passwd1 = form.passwd.value;
	passwd2 = form.confirm.value;
	email = form.email.value;
	method = 'create';
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

