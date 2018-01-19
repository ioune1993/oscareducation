var questions = null; // store questions gather once from site
var rated_resources = null;
var currentid = null;
function make_question(parent,question_stm,q_id,value) {
    if (value<=0) {
        value=0;
    }
	var d = document;
	var p = d.createElement("p");
	p.className = "lead";
	p.innerHTML = question_stm;
	var divy = d.createElement("div");
	divy.id = "StarId";
	divy.setAttribute("qid",q_id);
	if (value>0) {
	    divy.setAttribute("stars",value);
    }
	divy.className = "rating-stars text-center";
	parent.append(p);
	p.append(divy);
	var ul = d.createElement("ul");
	ul.id = "stars";
	ul.innerHTML = "<b class='small'>pas du tout</b>";
	divy.append(ul);
	var array = ["Mauvais","Passable","satis","bien", "excellent"];
	for (var i=1;i<=5;i++) {
		var li = d.createElement("li");
		if (i<=value) {
		    li.className='star small selected';
        } else {
		    li.className='star small';
        }
		li.setAttribute("data-value", i);
		li.title = array[i-1];
		ul.append(li);
		li.innerHTML = "<i class='fa fa-star fa-fw'></i>";
	}
	ul.innerHTML += "<b class='small'>excellente</b>";
};

function makeQuestionnaire(parent,id,json_ss) {
    if (Object.keys(json_ss["data"]).length === 0 && json_ss.constructor === Object) {
        console.log("empty json object");
        return;
    }
    console.log(json_ss);
    json_ob = json_ss;
    questions = json_ob;
	var d = document;
	var div = d.createElement("div");
	div.id = "questions";
	div.setAttribute("rid",id);
	div.style="border:1px solid grey;padding: 3px;";
	parent.append(div);
	for (var key in json_ob["data"]) {
	    if (rated_resources.hasOwnProperty(id)) {
            make_question(div, json_ob["data"][key][0], key, json_ob["data"][key][1]);
        } else {
            make_question(div, json_ob["data"][key][0], key,0);
        }
	}
	// add button
	var p = d.createElement("p");
	p.className = "small";
	p.innerHTML = "Commentaire (optionnel): <br>";
	var text = d.createElement("textarea");
	text.id = "comment";
	text.setAttribute("maxlength","300");
	text.rows = "7";
	text.cols = "42";
	text.innerHTML = json_ss["comment"];
	p.append(text);
	div.append(p);
	var but = d.createElement("button");
	but.className = "button";
	but.id = "buttonSubmit";
	but.innerHTML = "Soumettre";
	div.append(but);

	/* IMPORTANT initFunctions() set the functions that handles all the created html clicks etc.. !!*/
    initFunctions();
};

function showStudAvg(id) {
    if ($("#popupdiv").length <= 0) {
        makePopup($("#big" + id), id, "Student votes");
        $('[data-popup=popup]').fadeIn();
        makeChart(id,"stud");
    } else {
        $('[data-popup=popup]').fadeOut(350);
        $("#popupdiv").remove();
    }
};

function showProfAvg(id,t) {
    if ($("#popupdiv").length <= 0) {
        makePopup($("#big" + id), id, "Professor votes");
        $('[data-popup=popup]').fadeIn();
        makeChart(id,"prof");
    } else {
        $('[data-popup=popup]').fadeOut(350);
        $("#popupdiv").remove();
    }
};

function showQ(id) {
    var owner = $("#big" + id).attr('owner');
    var q = $("#questions");
    if (owner !== "true") { // if user is owner do not show questionnaire
        console.log("Questionnaire: " + id);
        if (q.length <= 0) {
            // no questionnaire present
            makerating($("#big" + id).parent(), id);
        } else {
            if (q.attr("rid") == id) {
                q.remove();
            } else {
                if (q.hasClass('voted')) {
                    q.remove();
                    makerating($("#big" + id).parent(), id);
                } else {
                    q.attr("rid", id);
                    q.appendTo($("#big" + id).parent());
                }
            }
        }
    }
};

function makePopup(parent,id,title) {
	var d = document;
	var p = d.createElement("div");
	p.id = "popupdiv";
	p.className = "popup";
	p.setAttribute("rid",id);
	p.setAttribute("data-popup", "popup");
	var div = d.createElement("div");
	div.className = "popup-inner";
	var h = d.createElement("h2");
	h.innerHTML = "Statistiques: "+title;
	var container = d.createElement("div");
	container.id = "chartContainer";
	container.style = "height: 300px; width: 100%;";
	var close = d.createElement("a");
	close.className = "popup-close";
	close.setAttribute("data-popup-close","popup");
	close.href = "#";
	close.innerHTML = "x";
	parent.append(p);
	p.append(div);
	div.append(h);
	div.append(container);
	div.append(close);

    // Load close handler
	$('[data-popup-close]').on('click', function (e) {
        $('[data-popup=popup]').fadeOut(350);
        e.preventDefault();
        e.stopPropagation();
        $("#popupdiv").remove();
    });
}

function makeChart(id,type) {
    $.ajax({
        url: "average/", // the endpoint
        type: "POST", // http method
        data: {"id": id, "type": type}, // data sent with the post request
        // handle a successful response
        success: function (json_returned) {
            var chart = new CanvasJS.Chart("chartContainer",{
                animationEnable: false,
                theme: 'light1',
                axisY: {title: "Nombres d'étoiles",maximum: 5}
            });
            var d = new Object();
            /* Json returned: key is question id and value is an array:
             *  array[0] is average vote and array[1] is the question statement */
            d['type'] = "column";
            d['dataPoints'] = [];
            for (var key in json_returned) {
                var point = new Object();
                point['y'] = parseFloat(json_returned[key][0]);
                point['label'] = json_returned[key][1]+"";
                d['dataPoints'].push(point);
            }
            chart.options.data = [];
            chart.options.data.push(d);
            chart.render();
            //preventDefault();
        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": b" + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function send_stars(json_s) {
	/* Function to send new ratings to server and do something with return valueconsole.log(ratingValue1);
       json_s should be a json string containing 3 keys: 'id' (resource id), 'comment' and 'rated'.
       the value associated with the 'rated' key is a json with key the question id and the number
         of stars votes by to user as value.The 'comment' key is associated to a string value that
           represents the comment left by the user and id key is the resource id value
         ex. { "id": "123", "rated": { "1":"2", "2":"3"}, "comment":"I like the way comment work" }
	*/
	try {
		JSON.parse(json_s);
	} catch (e){
		console.log("invalid JSON");
		return;
	}
	$.ajax({
		url : "rate/", // the endpoint
		type : "POST", // http method
       	data : { json_str: json_s }, // data sent with the post request
       	// handle a successful response
       	success : function(json_returned) {
			// Use json to set average for each question
           	$(document).find("#questions").html("Votes: <br>"+json_returned);
           	$(document).parent().addClass('voted');
           	$("#questions").remove();
           	// reset so if user reclicks on vote, it displays new vote from database
           	questions = null;
           	var j = JSON.parse(json_s);
           	rated_resources[j['id']] = j["rated"];
           	currentid = null;
           	alert("Thanks for your vote!");
       	},
       	// handle a non-successful response
       	error : function(xhr,errmsg,err) {
           console.log(xhr.status + ": b" + xhr.responseText); // provide a bit more info about the error to the console
       	}
	});
};

function initFunctions() {
    /* Default value for star rating and responses*/
    /* Handles everything when mouse over star rating */
    $('#stars li').on('mouseover', function () {
        var onStar = parseInt($(this).data('value'), 10); // The star currently mouse on
        // Now highlight all the stars that's not after the current hovered star
        $(this).parent().children('li.star').each(function (e) {
            if (e < onStar) {
                $(this).addClass('hover');
            }
            else {
                $(this).removeClass('hover');
            }
        });
    }).on('mouseout', function () {
        $(this).parent().children('li.star').each(function (e) {
            $(this).removeClass('hover');
        });
    });
    $("#buttonSubmit").on('click', function () {
    	var s = $(".rating-stars");
    	var json = new Object();
        var r = new Object();
        var id = $("#questions").attr('rid');
        var count = 0;
        for (var i=0;i<s.length;i++) {
			if (s[i].getAttribute("stars") != undefined) {
				count+=1;
			}
			r[s[i].getAttribute("qid")] = s[i].getAttribute("stars");
		}
		if (count != s.length) {
        	alert('Veiller répondre à toutes les questions')
		} else {
        	var comment = $("#comment").val();
        	json["id"] = id;
        	json["comment"] = comment;
        	json["rated"] = r;

        	$("#questions").addClass("voted");
        	$("#questions").fadeOut();
        	var resend = true; // on submit force resend server
        	if (rated_resources.hasOwnProperty(id)) {
        	    for (var key in rated_resources[id]) {
        	        if (rated_resources[id][key] != json["rated"][key]) {
                        resend=true;
                    }
                }
            } else {
        	    send_stars(JSON.stringify(json));
        	    return;
            }
            if (resend) {
                send_stars(JSON.stringify(json));
            } else {
        	    $("#questions").remove();
                // reset so if user reclicks on vote, it displays new vote from database
                questions = null;
                rated_resources[json['id']] = json["rated"];
                currentid = null;
            }
		}
    });
    /* Handles everything when we click on the stars */
    $('#stars li').on('click', function () {
        var onStar = parseInt($(this).data('value'), 10); // The star currently selected
        var stars = $(this).parent().children('li.star');
        var parent = $(this).parent().parent();
        parent.attr("stars", onStar);
        for (i = 0; i < stars.length; i++) {
            $(stars[i]).removeClass('selected');
        }
        for (i = 0; i < onStar; i++) {
            $(stars[i]).addClass('selected');
        }
    });
};
function setratedresources(jsond) {
    rated_resources = JSON.parse(jsond);
}

function makerating(parent,id) {
	/* Get questions from server only if we never called it!
	    1 request to server!
	*/
	if (rated_resources.hasOwnProperty(id)) {
    }
    if (questions == null) {
        ajaxsendmakerating(parent, id);
    }
    else {
	    if (currentid == id) {
            makeQuestionnaire(parent, id, questions);
        }else {
	        ajaxsendmakerating(parent, id);
        }
    }
};

function ajaxsendmakerating(parent,id) {
    $.ajax({
        url: "makerating/", // the endpoint
        type: "POST", // http method
        data: {"id": id}, // data sent with the post request
        // handle a successful response
        success: function (json_returned) {/*
                        json_returned is a json object with as key the question id and as associated value
                           an array of question string and value (0 if not voted else)
                    */
            makeQuestionnaire(parent, id, json_returned);
            questions = json_returned;
            console.log(json_returned);
            currentid = id;
        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": b" + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function setfill() {
    var fill_board = 0;
		var update_board = setInterval(function()
		{
			fill_board += 1;
			$('#fillBoard').css('height', (fill_board+'%'));
	    	//$('#fillIcon').css('margin-top', ((100 - fill)+'%'));
	    	if (fill_board == 65) {
	    		clearInterval(update_board);
	    	}

	    }, 10);
}
