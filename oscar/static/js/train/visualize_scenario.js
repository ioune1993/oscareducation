"use strict";

class ScenarioVisualization{

    //constructor(anchorID, btnPlusID, addElementDivID, textBlockElemID, textButtonID, videoBlockElemID, videoButtonID, imgBlockElemID, imgButtonID, mcqBlockElemID, mcqButtonID){
    constructor(json,anchorID,nextButtonID,previousButtonID, validateButtonID, endButtonID, blockID, gotoTextID, gotoImgID, gotoVidID, gotoMCQID, gotoPDFID, quitButtonID){
        this.anchor = document.getElementById(anchorID);
        this.nextButton = document.getElementById(nextButtonID);
        this.nextButton.addEventListener("click", this.nextButtonElement.bind(this), true);
        this.previousButton =  document.getElementById(previousButtonID);
        this.previousButton.addEventListener("click", this.previousButtonElement.bind(this), true);
        // this.validateButton = document.getElementById(validateButtonID);
        // this.validateButton.addEventListener("click", this.validateButtonElement.bind(this), true);
        this.endButton = document.getElementById(endButtonID);
        this.endButton.addEventListener("click", this.endButtonElement.bind(this), true);
        this.blockText = document.getElementById(blockID["textBlockID"]);
        this.blockImage = document.getElementById(blockID["imgBlockID"]);
        this.blockVideo = document.getElementById(blockID["videoBlockID"]);
        this.blockPDF = document.getElementById(blockID["pdfBlockID"]);
        this.blockMCQ = document.getElementById(blockID["mcqBlockID"]);


        this.progressBar = document.getElementById("progressBar");

        this.gotoText = document.getElementById(gotoTextID);
        this.gotoImg = document.getElementById(gotoImgID);
        this.gotoVid = document.getElementById(gotoVidID);
        this.gotoMCQ = document.getElementById(gotoMCQID);
        this.gotoPDF = document.getElementById(gotoPDFID);

        this.index = 0;
        this.lastButtonClicked = null;
        this.elements = json.elements;
        this.tabElementObject = [];
        this.first = true;

        for(let elem of this.elements){
            var goto = document.createElement('button');
            if(this.first)
            {
                goto.style.backgroundColor = "#f58025";
                this.first = false;
                this.lastButtonClicked = goto;
            }
            goto.setAttribute("data", elem.order);
            goto.classList.add("goToButton");
            if(elem.type == "TextElem"){
                let objectElem = new TextElem(elem, this.blockText, this.anchor);
                this.tabElementObject.push(objectElem);
                goto.innerHTML = this.gotoText.innerHTML;
                this.progressBar.appendChild(goto);
            }
            else if(elem.type == "ImgElem"){
                let objectElem = new ImageElem(elem, this.blockImage, this.anchor);
                this.tabElementObject.push(objectElem);
                goto.innerHTML = this.gotoImg.innerHTML;
                this.progressBar.appendChild(goto);
            }
            else if(elem.type == "ImgElemHardDrive"){
                let objectElem = new ImageElemHardDrive(elem, this.blockImage, this.anchor);
                this.tabElementObject.push(objectElem);
                goto.innerHTML = this.gotoImg.innerHTML;
                this.progressBar.appendChild(goto);
            }
            else if(elem.type == "VidElem"){
                let objectElem = new VideoElem(elem, this.blockVideo, this.anchor);
                this.tabElementObject.push(objectElem);
                goto.innerHTML = this.gotoVid.innerHTML;
                this.progressBar.appendChild(goto);
            }
            else if(elem.type == "PDFElem"){
                let objectElem = new PDFElem(elem, this.blockPDF, this.anchor);
                this.tabElementObject.push(objectElem);
                goto.innerHTML = this.gotoPDF.innerHTML;
                this.progressBar.appendChild(goto);
            }
            else if(elem.type == "MCQElem"){
                console.log(elem);
                let objectElem = new MCQElem(elem, this.blockMCQ, this.anchor);
                this.tabElementObject.push(objectElem);
                goto.innerHTML = this.gotoMCQ.innerHTML;
                this.progressBar.appendChild(goto);
            }
            goto.classList.add('gotoButton');
            goto.addEventListener("click", this.gotoButtonElement.bind(this), true)
        }
        this.tabElementObject[this.index].render();

        if (this.elements.length == 1){
            this.nextButtonElement.bind(this)();
        }
    }

    gotoButtonElement(elem){
        if(this.index == this.tabElementObject.length-1){
            this.nextButton.style.display = "inline";
            this.endButton.style.display = "none";
        }
        this.tabElementObject[this.index].hide();
        if(this.lastButtonClicked != null)
        {
            this.lastButtonClicked.style.backgroundColor = "white";
        }
        let button = elem;
        if (!elem.classList || !elem.classList.contains("gotoButton")){
            button = elem.target;
            if (!elem.target.classList.contains("gotoButton"))
            {
                button = button.parentNode;
            }
        }
        button.style.backgroundColor = "#f58025";
        this.lastButtonClicked = button;
        this.index = button.getAttribute("data");
        this.tabElementObject[this.index].render();

        if(this.index == 0){
            this.previousButton.style.display = "none"
        }
        else {
            this.previousButton.style.display = "inline"
        }
        if(this.index == this.tabElementObject.length-1){
            this.nextButton.style.display = "none";
            this.endButton.style.display = "inline";
        }
    }

    nextButtonElement(){
        if(this.index < this.tabElementObject.length-1){
            this.tabElementObject[this.index].hide();
            this.index++;
            this.tabElementObject[this.index].render();
            this.previousButton.style.display = "inline";
        }
        if(this.index == this.tabElementObject.length-1){
            this.nextButton.style.display = "none";
            this.endButton.style.display = "inline";
        }

        // go through the navigation button to find the one with the current
        // index and applie the function "gotoButtonElement" as if it has been click
        for(let e of document.getElementsByClassName("goToButton")){
            if (e.getAttribute("data") == this.index){
                this.gotoButtonElement(e)
            }
        }

    }

    previousButtonElement(){
        if(this.index > 0){
            this.tabElementObject[this.index].hide();
            this.index--;
            this.tabElementObject[this.index].render();
            this.nextButton.style.display = "inline";
            this.endButton.style.display = "none";
        }
        if(this.index == 0){
            this.previousButton.style.display = "none"
        }
        else {
            this.previousButton.style.display = "inline"
        }

        // go through the navigation button to find the one with the current
        // index and applie the function "gotoButtonElement" as if it has been click
        for(let e of document.getElementsByClassName("goToButton")){
            if (e.getAttribute("data") == this.index){
                this.gotoButtonElement(e)
            }
        }
    }

    endButtonElement(){
        console.log("test");
        var pathTab = window.location.pathname.split("/");
        var user_type = pathTab[1];
        var pk = pathTab[3]
        if(user_type == "student"){
            window.location.href = "/student/pedagogical/skill/"+pk;
        }else{
            window.location.href = "/professor/lesson/"+pk+"/#listscena";
        }

    }
}

function getJsonData(){

    var pathTab = window.location.pathname.split("/")
    var id = pathTab[pathTab.length - 1]

    let xhr = new XMLHttpRequest();

    xhr.open("GET", "/professor/train/data/"+id, false);

    xhr.send(null);
    // done
    if (xhr.readyState == 4 && xhr.status == 200) {
        var myArr = JSON.parse(xhr.responseText);
        console.log(myArr);

        return myArr;
    }
}

// initiation
window.onload = function(){
    let anchorID = "anchor";
    let nextButtonID = "nextElement";
    let previousButtonID = "previousElement";
    let validateButtonID = "validateElement";
    let endButtonID = "endElement";

    let quitButtonID = "quit";

    let gotoTextID = "idTextElemProg";
    let gotoImgID = "idImgElemProg";
    let gotoVidID = "idVideoElemProg";
    let gotoMCQID = "idMCQElemProg";
    let gotoPDFID = "idPDFElemProg";
    let json = getJsonData();


    let blockID = {"textBlockID":"textBlockElem","imgBlockID":"imgBlockElem","videoBlockID":"videoBlockElem","pdfBlockID":"pdfBlockElem","mcqBlockID":"mcqBlockElem"};
    new ScenarioVisualization(json, anchorID, nextButtonID, previousButtonID, validateButtonID, endButtonID, blockID, gotoTextID, gotoImgID, gotoVidID, gotoMCQID, gotoPDFID, quitButtonID);

};

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        var c_start = document.cookie.indexOf(c_name + "=");
        var c_end;
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

function editForm(){
    var pathTab = window.location.pathname.split("/")
    var id = pathTab[pathTab.length - 1]
    console.log("hello")
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/professor/train/delete_scenario/"+id, false ); // false for synchronous request
    xmlHttp.send( null );
    //return xmlHttp.responseText;
    console.log("hello")
    sendForm();
}

function getVideoId(url) {
    var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    var match = url.match(regExp);

    if (match && match[2].length == 11) {
        return match[2];
    } else {
        console.log("ERROR with video URL !")
        return 'error';
    }
}

class AbstractElem{
	constructor(anchor) {
        this.node = document.createElement("div");
        this.node.style.display = "block";
        this.anchor = anchor
		if (new.target === AbstractElem) {
			throw new TypeError("Cannot construct Abstract instances directly");
		}
	}

    render(){
        if(this.node.getElementsByClassName("boxclasse")[0].style.height > "400px"){
            this.node.getElementsByClassName("boxclasse")[0].style.height="400px";
        }
        this.anchor.appendChild(this.node);
        //document.getElementById("validateElement").style.display = "none";
    }

    hide(){
        this.anchor.removeChild(this.node);
    }



	delete() {
		throw new Error('You have to implement the method delete');
	}
}

function quitButton(){
    console.log("test");
    var pathTab = window.location.pathname.split("/");
    var user_type = pathTab[1];
    var pk = pathTab[3]
    if(user_type == "student"){
        window.location.href = "/student/pedagogical/skill/"+pk;
    }else{
        window.location.href = "/professor/lesson/"+pk+"/#listscena";
    }

}

class TextElem extends AbstractElem{
    constructor(elem, skull, anchor){
        // elem is the data to render
        // skull is the node element that is used as a base of this element
        super(anchor);
        if(elem != null)
            this.data = elem["data"];
            this.title = this.data["title"];
            this.content = this.data["content"];
            this.node.innerHTML = skull.innerHTML;
            this.node.getElementsByClassName("titre")[0].innerHTML = this.title;
            this.node.getElementsByClassName("content")[0].innerHTML = this.content;
            this.quitButton = this.node.getElementsByClassName("quit")[0];
            this.quitButton.addEventListener("click", quitButton, true);

    }
}

class ImageElem extends AbstractElem{
    constructor(elem, skull, anchor){
        super(anchor);
        if(elem != null){
            this.data = elem["data"];
            this.title = this.data["title"];
            this.content = this.data["url"];
            this.description = this.data["description"];
            this.node.innerHTML = skull.innerHTML;
            this.node.getElementsByClassName("titre")[0].innerHTML = this.title;
            this.node.getElementsByClassName("content")[0].setAttribute("src", this.content);
            this.node.getElementsByClassName("description")[0].innerHTML = this.description;
            this.quitButton = this.node.getElementsByClassName("quit")[0];
            this.quitButton.addEventListener("click", quitButton, true);
        }
    }
}

// CLass for image that has been recuperate from the directory
// Can be easily placed in the ImageElem Class => TODO
class ImageElemHardDrive extends AbstractElem{
    constructor(elem, skull, anchor){
        super(anchor);
        if(elem != null){
            this.data = elem["data"];
            this.title = this.data["title"];
            this.content = this.data["url"].split("oscareducation")[1];
            this.description = this.data["description"];
            this.node.innerHTML = skull.innerHTML;
            this.node.getElementsByClassName("titre")[0].innerHTML = this.title;
            this.node.getElementsByClassName("content")[0].setAttribute("src", this.content);
            this.node.getElementsByClassName("description")[0].innerHTML = this.description;
            this.quitButton = this.node.getElementsByClassName("quit")[0];
            this.quitButton.addEventListener("click", quitButton, true);
        }
    }
}

class VideoElem extends AbstractElem{
    constructor(elem, skull, anchor){
        super(anchor);
        if(elem != null){
            this.data = elem["data"];
            this.title = this.data["title"];
            this.content = this.data["url"];
            this.description = this.data["description"];
            this.node.innerHTML = skull.innerHTML;
            this.node.getElementsByClassName("titre")[0].innerHTML = this.title;
            let ID = getVideoId(this.content);
            this.embedURL = "//www.youtube.com/embed/" + ID;
            this.node.getElementsByClassName("content")[0].setAttribute("src", this.embedURL);
            this.node.getElementsByClassName("description")[0].innerHTML = this.description;
            this.quitButton = this.node.getElementsByClassName("quit")[0];
            this.quitButton.addEventListener("click", quitButton, true);
        }
    }
}

class PDFElem extends AbstractElem{
    constructor(elem, skull, anchor){
        super(anchor);
        if(elem != null){
            this.data = elem["data"];
            this.title = this.data["title"];
            this.content = this.data["url"];
            console.log(this.content);
            this.description = this.data["description"];
            this.node.innerHTML = skull.innerHTML;
            this.node.getElementsByClassName("titre")[0].innerHTML = this.title;
            this.node.getElementsByClassName("content")[0].setAttribute("src", this.content);
            this.node.getElementsByClassName("description")[0].innerHTML = this.description;
            this.quitButton = this.node.getElementsByClassName("quit")[0];
            this.quitButton.addEventListener("click", quitButton, true);
        }
    }
}

class MCQElem extends AbstractElem{
    constructor(elem, skull, anchor){
        super(anchor);
        if(elem != null){
            this.data = elem["data"];
            this.title = this.data["title"];
            this.question = this.data["question"];
            this.answers = this.data["answers"];
            this.tips = this.data["tips"];
            this.node.innerHTML = skull.innerHTML;
            this.node.getElementsByClassName("titre")[0].innerHTML = this.title;
            this.node.getElementsByClassName("question")[0].innerHTML = this.question;
            this.Ul = this.node.getElementsByClassName("answers");
            for(let answer of this.answers){
                let blocanswer = document.createElement("div");
                blocanswer.innerHTML = this.node.getElementsByClassName("blocanswer")[0].innerHTML;
                blocanswer.classList.add('blocanswer');
                blocanswer.getElementsByClassName("answer")[0].innerHTML = answer["answer"];
                //blocanswer.getElementsByClassName("isAnswer")[0].checked = false;
                this.Ul[0].appendChild(blocanswer);
            }

            this.validateButton = this.node.getElementsByClassName("validateElement")[0];
            this.validateButton.addEventListener("click", this.validate.bind(this), true);
            //
            // this.tipsButton = this.node.getElementsByClassName("tipsMCQ")[0];
            // this.tipsButton.addEventListener("click", this.showtips.bind(this), true);
            this.tipsButton = this.node.getElementsByClassName("tipsMCQ")[0];
            this.tipsButton.addEventListener("click", this.displayTips.bind(this), true);
            this.quitButton = this.node.getElementsByClassName("quit")[0];
            this.quitButton.addEventListener("click", quitButton, true);

        }
    }

    displayTips(){
        this.node.getElementsByClassName("tipsMCQ")[0].setAttribute("data-content", this.tips);
        this.node.getElementsByClassName("tipsMCQ")[0].setAttribute("data-placement", "bottom");
        this.node.getElementsByClassName("tipsMCQ")[0].setAttribute("data-html", "true");
        this.node.getElementsByClassName("tipsMCQ")[0].setAttribute("data-trigger", "focus");
        $('[data-toggle="popover"]').popover('show');
    }
    // showtips(){
    //     alert("Indice : " + this.tips);
    // }

    render(){
        if(this.node.getElementsByClassName("boxclasse")[0].style.height > "400px"){
            this.node.getElementsByClassName("boxclasse")[0].style.height="400px";
        }
        this.anchor.appendChild(this.node);
        var maxWidth = 0;
        var maxHeight = 0;
        var blocanswer = this.node.getElementsByClassName("answer");
        for(let i = 1; i < blocanswer.length; i++){
            if(maxWidth < blocanswer[i].clientWidth){
                maxWidth = blocanswer[i].clientWidth;
            }
            if(maxHeight < blocanswer[i].clientHeight){
                maxHeight = blocanswer[i].clientHeight;
            }
        }
        // console.log(blocanswer);
        for(let i = 1; i < blocanswer.length; i++){
            console.log(i);
            var newStyle = "width: "+maxWidth+"px ;height: "+maxHeight+"px; "+"display: flex; justify-content: center; flex-direction: column;"
            if (blocanswer[i].getElementsByClassName("answer")[0])
            {
                blocanswer[i].getElementsByClassName("answer")[0].setAttribute("style",newStyle);
            }
        }
    }

    validate(){
        let count = 1;
        let error_number = 0;
        for(let answer of this.answers){
            if(answer["solution"] != this.node.getElementsByClassName("blocanswer")[count].getElementsByClassName("isAnswer")[0].checked){
                error_number++;
                if (answer["solution"]){
                    this.node.getElementsByClassName("blocanswer")[count].style.borderColor = "#00bb00"; //00bb0082
                    this.node.getElementsByClassName("blocanswer")[count].style.backgroundColor = "#76f276";
                    this.node.getElementsByClassName("answer")[count].style.borderLeft = "solid #00bb00";
                }else{
                    this.node.getElementsByClassName("blocanswer")[count].style.borderColor = "#ff4040"; //ff404091
                    this.node.getElementsByClassName("blocanswer")[count].style.backgroundColor = "#fe7575";
                    this.node.getElementsByClassName("answer")[count].style.borderLeft = "solid #ff4040";
                }
                //this.node.getElementsByClassName("blocanswer")[count].getElementsByClassName("isFalse")[0].style.display = "inline-block";
            }
            else{
                if (answer["solution"]){
                    //this.node.getElementsByClassName("blocanswer")[count].getElementsByClassName("isFalse")[0].style.display = "inline-block";
                    //this.node.getElementsByClassName("blocanswer")[count].getElementsByClassName("isFalse")[0].setAttribute("src", "/static/img/icons/correct.png");
                    this.node.getElementsByClassName("blocanswer")[count].style.borderColor = "#00bb00";
                    this.node.getElementsByClassName("blocanswer")[count].style.backgroundColor = "#76f276";
                    this.node.getElementsByClassName("answer")[count].style.borderLeft = "solid #00bb00";
                }else {
                    //this.node.getElementsByClassName("blocanswer")[count].getElementsByClassName("isFalse")[0].style.display = "none";
                    this.node.getElementsByClassName("blocanswer")[count].style.borderColor = "grey";
                    this.node.getElementsByClassName("blocanswer")[count].style.backgroundColor = "";
                    this.node.getElementsByClassName("answer")[count].style.borderLeft = "solid grey";

                }

            }
            count++;
        }
        if(error_number > 0){
            this.node.getElementsByClassName("succededMCQ")[0].style.display = "none";
            this.node.getElementsByClassName("failedMCQ")[0].style.display = "block";
        }
        else{
            this.node.getElementsByClassName("failedMCQ")[0].style.display = "none";
            this.node.getElementsByClassName("succededMCQ")[0].style.display = "block";
        }
    }
}

function loadVideo(elem, embedURL) {
    elem.setAttribute("src", embedURL)
    elem.style.display = "block"
    elem.style.width = "100%"
}
