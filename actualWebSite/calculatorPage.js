function add() {
	var addNumbers = function(value1,value2) {return value1+value2;}
	getNumbers(addNumbers);
	
}

function getNumbers(fn) {
	var value1 = +document.getElementById("number1").value,
	    value2 = +document.getElementById("number2").value;
	
		if (isNaN(value1) || isNaN(value2)) {
		substitute("number1");
		substitute("number2");
		substitute("resultField");
	}
	else {
		document.getElementById("resultField").value = fn(value1,value2);
	}

	function substitute(id) {
		document.getElementById(id).value = "";
	}
}

