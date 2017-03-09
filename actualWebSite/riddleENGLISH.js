var number = 0,
    answerBlock = document.getElementsByClassName("answerBlock"),
    incorrectAnswer = 0;

function getQuestionBlock(index,text) {
	document.getElementsByClassName("questionBlock")[index].style.display = text;
}
 
function getAnswerBlock(index, text) {
	answerBlock[index].style.display = text;
}

function getResultsBlock(text){
	document.getElementById("resultsBlock").style.display = text;
}

function getHeading(index,text) {
	document.getElementsByTagName("H4")[index].innerHTML = text;
}

function showAnswer(element) {
	
	var i = element.getAttribute("data-number"),
		sibling = element.previousElementSibling;
		/*defaultV = sibling.defaultValue;*/
	function getCorrectAnswer(data) {
		return sibling.getAttribute(data);
	}
		/*correctAnswer = sibling.getAttribute("data-answer"),
		correctAnswer1 = sibling.getAttribute("data-answer1");*/

	switch(playersAnswer = sibling.value.toUpperCase().trim()) {
		case getCorrectAnswer("data-answer"):
		case getCorrectAnswer("data-answer1"):
			getQuestionBlock(i,"none");
			getAnswerBlock(i, "initial");
			number++;
			break;
		case "":
			sibling.value = null;
			break;
		default:
			getHeading(i,"Your answer is incorrect :(");
			getQuestionBlock(i,"none");
			getAnswerBlock(i, "initial");
			number++;
			incorrectAnswer++;
	}
		
	
	/* playersAnswer = sibling.value.toUpperCase().trim();
	test:{
	if(playersAnswer == "") {
		sibling.value = defaultV;
		break test;
	}
		
	else if(playersAnswer !== correctAnswer && playersAnswer !== correctAnswer1) {
		heading[i].innerHTML = "Вы не угадали :(";
		questionBlock[i].style.display = "none";
		answerBlock[i].style.display = "initial";
		number++;
		incorrectAnswer++;
	}
	else {
		questionBlock[i].style.display = "none";
		answerBlock[i].style.display = "initial";
		number++;
	}
	} */	
	
	if(number == 4){
		setTimeout(showResult,2000);
	}
}

function showResult(){
	document.getElementById("correctlyAnswered").innerHTML = number - incorrectAnswer;
	getResultsBlock("initial");
	number = 0;
	incorrectAnswer = 0;
}

function hideResult(event){
	var closeButton = document.getElementById("closeButton");
	var block = document.getElementById("resultsBlock").style.display;
	if(event.target == closeButton || event.target == resultsBlock || event.keyCode == 27 && block == "initial") {
		getResultsBlock("none");
		var j;
		for(j=0;j<answerBlock.length; j++){
			getAnswerBlock(j, "none");
			getQuestionBlock(j,"initial");
			document.getElementById("question"+j).value = "";
			getHeading(j,"You've answered correctly!");
		}
	}
	
}

for(var i=0; i<4; i++) {
	document.getElementsByTagName("FORM")[i].onsubmit = function(){return false};
}

window.onkeydown = function() {hideResult(event)};

/*function cancelResultsBlock(event) {
	var block = document.getElementById("resultsBlock").style.display;
	if(event.keyCode == 27 && block == "initial") {
		hideResult(event);
	}
} */

window.onunload = resetFields;

function resetFields() {
	var forms = document.getElementsByTagName("FORM");
	for(var i=0; i<forms.length; i++) {
		forms[i].reset();
	}	
}