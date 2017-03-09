var rounds = 0;
var number;
var elementsBlock = document.getElementById("elementsBlock");

document.getElementById("startButton").onclick = getStarted;

function getStarted() {
	if(elementsBlock.children[1].value == "Start!") {
		rounds++;
		selectNumber();
		changeHeading();
		changeFieldset(1);
		changeButton();
		changeRounds();
	}
	else {
		document.getElementsByClassName("msgCover")[0].style.display = "initial";
	}
}

function selectNumber() {
	number = Math.round(Math.random()*100);
	//return number;
	//alert(number);
}

function changeHeading() {
	document.getElementById("statusField").children[0].innerHTML = "A number between 0 and 100 has been selected.<br>There are 10 raunds in the game.";
}


/*function changeFieldset() {
	document.getElementById("txt1").style.border = "2px solid #E91E63";
	document.getElementById("txt1").children[0].style.color = "#E91E63";
	var input1 = document.getElementById("txt1").children[1];
	input1.disabled = false;
	input1.placeholder = "Введите число";
}*/


function changeFieldset(j) {
	var input1 = document.getElementById("txt1").children[1];
	var input2 = document.getElementById("txt2").children[1];
	if(j) {
		document.getElementsByTagName("FIELDSET")[0].style.border = "2px solid #E91E63";
		document.getElementsByTagName("FIELDSET")[0].children[0].style.color = "#E91E63";
		input1.disabled = false;
		input1.placeholder = "Enter your number";
		input1.focus();

		document.getElementsByTagName("FIELDSET")[1].style.border = "2px groove threedface";
		document.getElementsByTagName("FIELDSET")[1].children[0].style.color = "initial";
		input2.disabled = true;
		input2.placeholder = "";
		//input2.blur();
	}
	else {
		document.getElementsByTagName("FIELDSET")[0].style.border = "2px groove threedface";
		document.getElementsByTagName("FIELDSET")[0].children[0].style.color = "initial";
		input1.disabled = true;
		input1.placeholder = "";

		document.getElementsByTagName("FIELDSET")[1].style.border = "2px solid #3f51b5";
		document.getElementsByTagName("FIELDSET")[1].children[0].style.color = "#3f51b5";
		input2.disabled = false;
		input2.placeholder = "Enter your number";
		input2.focus();
	}
}

/*function highlight(a,rounds) {
	if(a !== rounds) {
		document.getElementById("elementsBlock").children[0].style.textShadow = "0px 0px 3px red";
	}	
}*/

function changeButton() {
	elementsBlock.children[1].value = "Replay";
}

function applyShadow() {
	elementsBlock.children[0].style.textShadow = "0px 0px 3px red";
	elementsBlock.children[0].style.fontSize = "27px";
}

function cancelShadow() {
	elementsBlock.children[0].style.textShadow = "none";
	elementsBlock.children[0].style.fontSize = "25px";
}

function changeRounds() {
	elementsBlock.children[0].innerHTML = "Raund " + rounds;
	setTimeout(applyShadow,100);
	setTimeout(cancelShadow, 350);
	//elementsBlock.children[0].style.animation = "rounds 0.35s linear 0.1s";
}


/*var msg = document.getElementsByClassName("msg")[0].children;
var msgCover1 = document.getElementsByClassName("msgCover")[0];

function closeMessage(event) {
	if(event.target == msg[2]) {
		location.reload();
	}
	else if(event.target == msg[0] || event.target == msg[3] || event.target == msgCover1){
		msgCover1.style.display = "none";
	}
}*/

document.getElementsByClassName("msgCover")[0].onclick = function() {closeMessage(event,0)};
document.getElementsByClassName("msgCover")[1].onclick = function() {closeMessage(event,1)};
document.getElementsByClassName("msgCover")[2].onclick = function() {closeMessage(event,2)};

window.onkeydown = function() {escapeCover(event)};

function escapeCover(event) {
	if(event.keyCode == 27) {
		for(var i=0; i<3; i++){
			var cover = document.getElementsByClassName("msgCover")[i].style.display;
			//alert(i+" cover0: "+cover);
			if(i == 0 && cover =="initial") {
				//alert(i+" cover1: "+cover);
				//document.getElementsByClassName("msgCover")[i].style.display = "none";
				getCoverStyle(i);
				return;
			}
			else if(i == 1 && cover =="initial" || i == 2 && cover =="initial") {
				//alert(i+" cover2: "+cover);
				location.reload();
				return;
			}
		}
	}
	
}

function getMsg(i,j) {
	 return document.getElementsByClassName("msg")[i].children[j];
}

function getCover(i) {
	return document.getElementsByClassName("msgCover")[i];
}

function getCoverStyle(i) {
	document.getElementsByClassName("msgCover")[i].style.display = "none";
}

/*function reloadPage() {
	if(event.target == getMsg(i,0) || event.target == getCover(i)) {
		location.reload();
	}
}*/
document.getElementById("images").onclick = function() {location.reload()};
document.getElementById("imageBlock").onclick = function() {location.reload()};

function closeMessage(event,i) {

	if(i==0) {
		if(event.target == getMsg(i,2)) {
			location.reload();
		}
		else if(event.target == getMsg(i,0) || event.target == getMsg(i,3) || event.target == getCover(i)) {
			getCoverStyle(i);
		}
	}
	else {
		if(event.target == getMsg(i,0) || event.target == getCover(i)) {
			location.reload();
		}
	}
}

document.getElementsByTagName("FIELDSET")[0].children[1].onkeypress = function() {checkNumber(event,0)}
document.getElementsByTagName("FIELDSET")[1].children[1].onkeypress = function() {checkNumber(event,1)}

function getPlayerNumber(j) {
	var playerNumber = document.getElementsByTagName("FIELDSET")[j].children[1].value.trim();
	return playerNumber;
}

function checkNumber(event,j) {
	//getPlayerNumber(j);
	if(event.keyCode == 13) {
		//alert(playerNumber);
		validateValue(j);
		document.getElementsByTagName("FIELDSET")[j].children[1].value = null;
	}
}

function validateValue(j) {
	//alert(getPlayerNumber(j));
	if(getPlayerNumber(j) == "") {
		return;
	}
	else if(isNaN(getPlayerNumber(j))){
		changeHeading1();
	}
	else {
		changeHeading2(j);
	}
}

function changeHeading1() {
	document.getElementById("statusField").children[0].innerHTML = "Enter an integer";
	document.getElementById("statusField").children[0].style.color ="red";
}

function changeHeading2(j) {
	//alert(getPlayerNumber(j));
	var a = getPlayerNumber(j);
	if (getPlayerNumber(j) < 0 || getPlayerNumber(j) > 100) {
		document.getElementById("statusField").children[0].innerHTML = "The number should be between 0 and 100 inclusively";
		document.getElementById("statusField").children[0].style.color ="red";
	}
	else if (Number.isInteger(Number(a))) {
		compareNumbers(j);
	}
	else {
		changeHeading1();
	}
}

function compareNumbers(j) {
	var a = parseInt(getPlayerNumber(j));
	var b = j + 1;
	if(getPlayerNumber(j) == number) {
		document.getElementsByClassName("msgCover")[1].style.display = "initial";
		document.getElementsByTagName("FIELDSET")[j].children[1].blur();
		document.getElementById("congradsBox").children[2].innerHTML = "Player "+b+" has guessed the number!"

	}
	else if(getPlayerNumber(j) < number) {
		if(j==1){
			rounds++;
			if(rounds==11){
				document.getElementsByClassName("msgCover")[2].style.display = "initial";
				document.getElementsByClassName("msg")[2].children[2].innerHTML = "You've used all your attempts."+"<br>"+" Correct answer is "+number+".";
				document.getElementsByTagName("FIELDSET")[j].children[1].blur();
				return;
			}
			else {
				changeRounds();
			}
		}
		document.getElementById("statusField").children[0].innerHTML = a +" is lower than selected number";
		document.getElementById("statusField").children[0].style.color ="black";
		changeFieldset(j);
	}
	else {
		if(j==1){
			rounds++;
			if(rounds==11){
				document.getElementsByClassName("msgCover")[2].style.display = "initial";
				return;
			}
			else {
				changeRounds();
			}
		}
		document.getElementById("statusField").children[0].innerHTML = a +" is higher than selected number";
		document.getElementById("statusField").children[0].style.color ="black";
		changeFieldset(j);
	}
} 

window.onunload = resetFields;

function resetFields() {
	document.getElementsByTagName("FORM")[0].reset();
}


		