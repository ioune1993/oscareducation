function validateExerciceController($scope, $http, $sce, $timeout, $location) {
    $scope.uploadFile = function(files) {
        var reader = new FileReader();
        reader.readAsDataURL(files[0]);
        reader.addEventListener("load", function() {
            console.log("yay")
            $scope.base64img = reader.result;
            $scope.$digest();
        })

    };

    $scope.addAnswerField = function(question, index){
  			elem = document.getElementById("blank-text"+index);
  			text = elem.value;
  			matches = text.match(/#\[\d+]#/g);
  			if (matches === null) { //If it is the first field
  				text += "#[1]#";
  				elem.value = text; //Update input form
  			}
  			else{ //If we already have fields
  			    newText = "";
  			    for(var i = 0; i < matches.length; i++) { //Reorder fields in order
                    newText += text.substring(0,text.indexOf(matches[i])); //Append text before field
                    text = text.slice(text.indexOf(matches[i])+matches[i].length, text.length); //Remove added text
                    newText += "#["+ (i+1) + "]#";//Add field in order
                }
                newText += text;
  				newText += "#["+(matches.length+1)+"]#";
  			    elem.value = newText //Update input form
  			}
  			question["instructions"] = elem.value; //Update object for DB
  			elem.focus();//Request focus on text inputfo
            console.log(question)
    };

    $scope.parseTableQuestion = function(question){
        var counter = 0;
        for(var i = 0; i < question.table.length; i++){
          for(var j = 0; j < question.table[i].length; j++){
              var textTrimmed = question.table[i][j].replace(/\s/g,'');
              console.log("Debug parsable table");
              console.log(textTrimmed);
              var matches = textTrimmed.match(/#\[\d]#/g);
              console.log(matches);
              if(textTrimmed.length == 0 || matches != null){
                  counter++;
                  question.table[i][j] = "#["+counter+"]#";
              }
          }
        }
        return counter;
    };

    $scope.isPlaceholder = function (question) {
        if (question["answers"].length > 0){ //If we have fields, don't disable the button
            return true;
        }
        if(question["instructions"] == undefined) {
            //If for some reason the user erased the instructions, no placeholder
            return false;
        }
        matches = question["instructions"].match(/#\[\d]#/g);
        return matches != null; //If no match, no placeholder
    }

    $scope.parseFieldsInQuestion = function (topIndex, question) {
        var numberBlank = 0;
        if(question.type == "fill-table-blanks"){
            numberBlank = $scope.parseTableQuestion(question);

        }else {
            var elem = document.getElementById("blank-text"+topIndex);
            var text = elem.value;
            //console.log(question);
            var matches = text.match(/#\[/g);
            if (matches == null) { //No placeholders in the instructions
                for (i = 0; i < question["answers"].length; i++) {
                    question["answers"].splice(i, 1); //Remove the field
                    $scope.renderMathquil(topIndex, i, question, 0);
                }
                return; //Quit !
            }
            numberBlank = matches.length;
        }
        if (numberBlank > question["answers"].length) { //If we have blanks to add
            for (var i = question["answers"].length; i < numberBlank; i++) {
                question["answers"].push({
                    type: "text", //start as text by default
                    answers: [{
                        text: "",
                        latex: ""
                    }]
                });
                $scope.renderMathquil(topIndex, i, question, 0);
            }
        }else if(numberBlank < question["answers"].length){ //If we have blanks to remove
            for (i = numberBlank; i < question["answers"].length; i++) {
                question["answers"].splice(i, 1); //Remove the field
                $scope.renderMathquil(topIndex, i, question, 0);
            }
        }

    };

    //Wipe the possible answers for a field when changing answer type.
    //Otherwise mathquill display causes a display bug
    $scope.wipeAnswersInField = function (question, answerIndex){
        question["answers"][answerIndex-1].answers = [];
    };

    $scope.addBlankAnswer = function (topIndex, question, blankID) {
        question["answers"][blankID-1].answers.push(
            {"text": "",
             "latex": ""
            }
        );
        $timeout(function() {
            //console.log("blank id"+blankID);
            //console.log("question subanswer length : "+question.answers[0].answers.length);

            $scope.renderMathquil(topIndex, blankID - 1, question, question.answers[blankID-1].answers.length - 1);
        }, 100);
        //Pushing empty answers to iterate, maybe change that ?
    };

    $scope.removeAnswerBlank = function (question, blankID, index) {
        question["answers"][blankID-1].answers.splice(index, 1)
    };

    /**
     * when question.type == "fill-table-blanks"
     * add a row in the table, max of 10
     *
     * @param table the table object
     */
    $scope.addRowTableBlank = function (table){
    		ROW_LIMIT = 10;
        nRows = table.length;
        nCols = table[0].length;
				if (nRows < ROW_LIMIT){
		      newLine = [];
		      for(var i = 0; i < nCols; i++){
		          newLine.push("");
		      }
		      table.push(newLine);
        }
        else{
        	alert("Impossible d'avoir plus de " + ROW_LIMIT + " lignes par tableau.");
        }
    };

    /**
     * when question.type == "fill-table-blanks"
     * add a column in the table, max of 10
     *
     * @param table the table object
     */
    $scope.addColumnTableBlank = function (table){
    		COLUMN_LIMIT = 10;
        nRows = table.length;
        nCols = table[0].length;

        if(nCols < COLUMN_LIMIT) {
            for (var i = 0; i < nRows; i++) {
                table[i].push("");
            }
        }
        else{
            alert("Impossible d'avoir plus de " + COLUMN_LIMIT + " colonnes par tableau");
        }
    };

    /**
     * when question.type == "fill-table-blanks"
     * remove a row in the table
     *
     * @param table the table object
     * @param x index of row to remove
     */
    $scope.removeRowTableBlank = function (table, x){
        if(table.length > 1){
            table.splice(x,1);
        }
        else{
            $scope.flag = true;
        }
    };

    /**
     * when question.type == "fill-table-blanks"
     * remove a column in the table
     *
     * @param table the table object
     * @param y index of column to remove
     */
    $scope.removeColumnTableBlank = function(table, y){
        if(table[0].length > 1){
            for(var i = 0; i < table.length; i++){
                table[i].splice(y,1)
            }
        }
    };
    
    $scope.tableHasField =  function(table){
    	for(var i = 0; i < table.length; i++){
    		for(var j = 0; j < table[i].length; j++){
    			matches = table[i][j].match(/#\[\d+]#/g);
					if (table[i][j] == "" || matches != null) {
						return false;
					}
    		}
    	}
    	return true;
    };



    $scope.validateExercice = function() {
        $http.post("validate/", {"questions": $scope.questions, "testable_online": $scope.testable_online})
            .error(function() {
                console.log("error")
                $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-danger">Une erreur s\'est produite, nous en avons été alerté.</div>');
            })
            .success(function(data) {
                console.log("success");
                if (data.yaml.result == "error") {
                    $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-danger"> <b>Erreur:</b> ' + data.yaml.message + '</b></div>');
                    $scope.exerciceIsValid = false;
                } else {
                    $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-success">' + data.yaml.message + '</b></div>');

                    $scope.yamlRendering = $sce.trustAsHtml(data.rendering);
                    $scope.htmlRendering = $sce.trustAsHtml($scope.html);

                    $timeout(function() {

                        $('#exercice-rendering-yaml input[type="submit"]').addClass("disabled");
                        MathJax.Hub.Typeset(document.getElementById("exercice-rendering-panel"));

                        $($scope.questions).each(function(index, value) {
                            if (value.type == "graph") {
                                var graph = new Graph('graph-' + index)
                                $(value.answers).each(function(_, answer) {
                                    graph.addPoint(answer.graph.coordinates.X, answer.graph.coordinates.Y)
                                })
                            }
                        })

                    }, 0);

                    $scope.exerciceIsValid = true;
                }
            })

    };

    $scope.proposeToOscar = function() {
        var yaml = $scope.yaml;
        var html = $scope.html;
        var skill_code = $scope.skillCode;

        if (!skill_code) {
            $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-danger"><b>Erreur :</b> vous devez sélectionner une compétence pour pouvoir proposer l\'exercice à Oscar.</div>');
            return;
        }

        $("#submit-pull-request").addClass("disabled");

        $http.post("submit/", {"questions": $scope.questions, "html": html, "skill_code": skill_code, "image": $scope.base64img, "testable_online": $scope.testable_online})
            .success(function(data) {
                if ($scope.forTestExercice && inUpdateMode) {
                    window.location.href =  "../../" + data.id + "/for_test_exercice/" + $scope.forTestExercice + "/";
                } else if ($scope.forTestExercice) {
                    window.location.href =  "../" + data.id + "/for_test_exercice/" + $scope.forTestExercice + "/";
                } else if (inUpdateMode) {
                    window.location.href = "..";
                }

                $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-success">L\'exercice a correctement été soumis, merci !<br />Vous pouvez le voir <a href="' + data.url + '" target="_blank">ici</a>.</div>');
                //console.log(data);

                $scope.yaml = "";
                $scope.html = "";
                $scope.skillCode = "";
                $scope.image = null;
                $scope.base64img = "";
                $scope.exerciceIsValid = ""
                $scope.htmlRendering = ""
                $scope.yamlRendering = ""
                $scope.testable_online = true;

                $scope.questions = [{
                    "instructions": "",
                    "type": "",
                    "answers": [{
                        "text": "",
                        "latex": "",
                        "correct": false,
                    }],
                    "source": "",
                    "indication": "",
                }]
            })
            .error(function() {
                //console.log($scope.questions);
                $scope.yamlValidationResult = $sce.trustAsHtml('<div class="alert alert-danger">Une erreur s\'est produite, nous en avons été alerté.</div>');
            })
            .finally(function() {
                //console.log($scope.questions);
                $timeout(function() {
                    $("#submit-pull-request").removeClass("disabled");
                }, 0);
            })
    };

    $scope.onChangeQuestionType = function(topIndex, question) {
        if (question.type.startsWith("math") || question.type.startsWith("fill")) {
            $timeout(function() {
                for (var i = 0; i < question.answers.length; ++i)
                    $scope.renderMathquil(topIndex, i, question)
            }, 100);
        }
        if (question.type.startsWith("fill")){
            question.answers = [];
            if(question.type === "fill-table-blanks"){
                question.table =  [["",""],["",""]];
            }
            $timeout(function() {
                console.log("fill text blanks rendering mathquill");
                $scope.renderMathquil(topIndex, 0, question, 0);
            }, 100);
        }
        //console.log("question :");
        //console.log(question);
    };

    $scope.onChangeRadio = function(question, answer) {
        if (question.type != "radio")
            return;

        if (answer.correct !== true)
            return;

        for (a in question.answers) {
            var a = question.answers[a];
            if (a !== answer && a.correct === true) {
                a.correct = false;
            }
        }
    };

    $scope.onChangeGraphAnswerType = function(graph) {
        if (graph.type == "point") {
            graph["coordinates"] = {
                "X": "",
                "Y": "",
            }
        }
    };

    $scope.addAnswer = function(topIndex, question) {
        question["answers"].push({
            text: "",
            latex: "",
            graph: {type: ""},
            correct: false
        })

        if (question.type.startsWith("math")) {
            $timeout(function() {
                $scope.renderMathquil(topIndex, question.answers.length - 1, question);
            }, 100);
        }
    };

    $scope.removeAnswer = function(question, answer) {
        question["answers"].splice(question["answers"].indexOf(answer), 1);
    };

    $scope.addQuestion = function() {
        $scope.questions.push({
            "instructions": "",
            "type": "",
            "answers": [{
                "text": "",
                latex: "",
                graph: {type: ""},
                "correct": false
            }],
            "source": "",
            "indication": "",
        })
    };

    $scope.removeQuestion = function(question) {
        $scope.questions.splice($scope.questions.indexOf(question), 1);
    };

    var checkIfEditingExercice = function() {
        // this is a horrible hack to get to make this code works both for
        // create and edition of exercices :(
        let uri = window.location.href.split("#")[0].split("/").filter(function(a) { return a }).slice(-1);

        if (uri[0] != "update") {
            console.log("New ercercice mode");
            return;
        }

        inUpdateMode = true;

        $http.get("json/").success(function(data) {
            $scope.skillCode = data.skillCode;
            $scope.html = data.html;
            $scope.yaml = data.yaml;
            $scope.questions = data.questions;
            for(var i = 0; i < $scope.questions.length; i++){ //Iterate trough
                for(var j = 0; j < $scope.questions[i].answers.length; j++){
                    if($scope.questions[i].type == "fill-text-blanks") { //Replace incorrect field if question fill-in
                        $scope.questions[i].answers[i] = $scope.questions[i].answers[i].text;
                    }
                }
            }
            // TODO yamlRendering/htmlRendering et image
            $timeout(function() {
                for (var i = 0; i < $scope.questions.length; ++i) {
                    if ($scope.questions[i].type.startsWith("math") || $scope.questions[i].type.startsWith("fill")) {
                        //console.log("a");
                        //console.log($scope.questions[i])
                        for (var j = 0; j < $scope.questions[i].answers.length; ++ j) {
                            $scope.renderMathquil(i, j, $scope.questions[i])
                        }
                    }
                }
            }, 100);
        })
    };

    $scope.renderMathquil = function(topIndex, answerIndex, question, subAnswerIndex=-1) {
        /*console.log("topIndex: " + topIndex);
        console.log("answerIndex: " + answerIndex);
        console.log("subAnswer: "+ subAnswerIndex);*/
        if (answerIndex != null) {
            if(subAnswerIndex < 0){
              query = $(".mathquill-" + topIndex + "-" + answerIndex);
            }else {
              query = $(".mathquill-" + topIndex + "-" + answerIndex + "-" + subAnswerIndex);
            }
        } else {
            query = $(".mathquill-" + topIndex);
            //console.log("question type :"+question.type);
            if(question.type.startsWith("fill")){
              //console.log("initiating mathquill question field")
              query = $(".mathquill-" + topIndex + "-0");
            }
        }
        renderMathquil(query, function(MQ, index, mq) {
            var mathquill = MQ.MathField(mq, {
                handlers: {
                    edit: function() {
                        //console.log("======> " + answerIndex);
                        if(subAnswerIndex >= 0){
                          question.answers[answerIndex].answers[subAnswerIndex].latex = mathquill.latex();
                        }
                        else{
                          question.answers[answerIndex].latex = mathquill.latex();
                        }
                        //console.log(question.answers[answerIndex].latex);
                        //console.log($scope.questions);
                    }
                }
            });

            //console.log(question.answers);
            if (subAnswerIndex < 0 && question.answers[answerIndex].text) {
                mathquill.latex(question.answers[answerIndex].text);
            }
            if (subAnswerIndex >= 0 && question.answers[answerIndex].answers[subAnswerIndex].text) {
                mathquill.latex(question.answers[answerIndex].answers[subAnswerIndex].text);
            }

            var keyboard = $($(mq).parent().children()[0]);

            return [mathquill, keyboard];
        });
    };

    $scope.skillCode = $location.search().code;

    // if we are creating a question for a skill for a test
    $scope.forTestExercice = $location.search().for_test_exercice;
    $scope.html = "";
    $scope.yaml = "";
    $scope.yamlRendering = "";
    $scope.htmlRendering = "";
    $scope.image = null;
    $scope.base64img = "";
    $scope.testable_online = true;

    var inUpdateMode = false;

    $scope.questions = [{
        instructions: "",
        type: "",
        answers: [{
            text: "",
            latex: "",
            graph: {type: ""},
            correct: false,
        }],
        source: "",
        indication: "",
    }];


    $scope.yamlValidationResult = "";
    $scope.exerciceIsValid = false;

    checkIfEditingExercice();


}
