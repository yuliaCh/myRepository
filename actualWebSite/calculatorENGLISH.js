function add() {
	var showResult = function(value1,value2) {return value1+value2;}
	getNumbers(showResult);
}

function substract() {
	var showResult = function(value1,value2) {return value1-value2;}
	getNumbers(showResult);
}

function multiply() {
	var showResult = function(value1,value2) {return value1*value2;}
	getNumbers(showResult);
}

function divide() {
	var showResult = function(value1,value2) {
			if (value2==0){
				document.getElementById("number2").value = "";
				return "Error";
			}
			else {
				return value1/value2;
			}
		}	
	getNumbers(showResult);
}


function getNumbers(fn) {
	var value1 = +document.getElementById("number1").value,
	    value2 = +document.getElementById("number2").value;
	if (isNaN(value1) && isNaN(value2)) {
		substitute("number1");
		substitute("number2");
	}
	else if (isNaN(value1)) {
		substitute("number1");
	}
	else if (isNaN(value2)) {
		substitute("number2");
	}
	else {
    	document.getElementById("resultField").value = fn(value1,value2);
    }
}

function substitute(id) {
		document.getElementById(id).value = "";
		document.getElementById("resultField").value = "Error"
}

