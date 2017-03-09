var msgBlock = document.getElementById("msgCover_home");
var msgElements = document.getElementById("msg_home").children;

function closeMsg(event) {
	if(event.target == msgBlock || event.target == msgElements[0] || event.keyCode == 27) {
		msgBlock.style.display = "none";
	} 
}

msgBlock.onclick = function() {closeMsg(event)};
window.onkeydown = function() {closeMsg(event)};