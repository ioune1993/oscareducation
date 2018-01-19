"use strict";

class ScenarioCreation {

    //constructor(anchorID, btnPlusID, addElementDivID, textBlockElemID, textButtonID, videoBlockElemID, videoButtonID, imgBlockElemID, imgButtonID, mcqBlockElemID, mcqButtonID){
    constructor(param){
        this.anchor = document.getElementById(param.anchorID);
        this.btnPlus = document.getElementById(param.btnPlusID);
        this.addElementDiv = document.getElementById(param.addElementDivID);
        this.addElementOption = false; // at start it is not shown
        this.btnPlus.addEventListener("click", this.showDiffElements.bind(this), true);

        this.textBlockElem = document.getElementById(param.textBlockElemID);
        this.textButton = document.getElementById(param.textButtonID);
        this.textButton.addEventListener("click", this.makeBlockElemText.bind(this), true);

        this.videoBlockElem = document.getElementById(param.videoBlockElemID);
        this.videoButton = document.getElementById(param.videoButtonID);
        this.videoButton.addEventListener("click", this.makeBlockElemVideo.bind(this), true);

        this.imgBlockElem = document.getElementById(param.imgBlockElemID);
        this.imgButton = document.getElementById(param.imgButtonID);
        this.imgButton.addEventListener("click", this.makeBlockElemImg.bind(this), true);


        this.mcqBlockElem = document.getElementById(param.mcqBlockElemID);
        this.mcqButton = document.getElementById(param.mcqButtonID);
        this.mcqButton.addEventListener("click", this.makeBlockElemMcq.bind(this), true);


    }

    makeBlockElemText(){
        let newelem = document.createElement("div");
        newelem.classList.add('textBlockElem');
        newelem.innerHTML = this.textBlockElem.innerHTML;
        this.anchor.appendChild(newelem);
    }

    makeBlockElemImg(){
        let newelem = document.createElement("div")
        newelem.classList.add('imgBlockElem');
        newelem.innerHTML = this.imgBlockElem.innerHTML;
        this.anchor.appendChild(newelem);
    }

    // makeBlockElemVideo(){
    //     //TODO : adapter les liens
    //     let newelem = document.createElement("input");
    //     newelem.setAttribute("placeholder", "URL de votre vidéo");
    //     newelem.innerHTML = this.videoBlockElem.innerHTML;
    //     this.anchor.appendChild(newelem);
    //     newelem.style.display = "block";
    //     newelem.style.width = "100%";
    //
    // }

    makeBlockElemVideo(){
        let newelem = document.createElement("div");
        newelem.classList.add('videoBlockElem');
        newelem.innerHTML = this.videoBlockElem.innerHTML;
        this.anchor.appendChild(newelem);
    }

    makeBlockElemMcq(){
        //TODO remplacer par QCM
        let newelem = document.createElement("input");
        newelem.innerHTML = this.mcqBlockElem.innerHTML;
        this.anchor.appendChild(newelem);
        newelem.style.display = "block";
    }

    showDiffElements(){
        if(this.addElementOption) {
            this.addElementDiv.style.display = "none";
        }else {
            this.addElementDiv.style.display = "block";
        }

        this.addElementOption = !this.addElementOption

    }
}

function loadImage(elem){
    var root = elem.parentNode.childNodes;
    root[1].setAttribute("src", root[7].value);
    return false;
}

function loadVideo(elem){
    var root = elem.parentNode.childNodes;
    console.log(root);
    var ID = getVideoId(root[7].value);
    var embedURL = "//www.youtube.com/embed/" + ID
    root[1].setAttribute("src", embedURL);
    root[1].style.display = "block"
    return false;
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

function removeElem(elem){
    var root = elem.parentNode.parentNode;
    root.parentNode.removeChild(root);
    return false;
}

// initiation
window.onload = function(){
    let btnPlusID = "addElement"; //document.getElementById("addElement");
    let anchorID = 'whiteBox';
    let addElementDivID = 'addElementDiv';

    let textBlockElemID = "textBlockElem";
    let textButtonID = "addElementTxt";

    let videoBlockElemID = "videoBlockElem";
    let videoButtonID = "addElementVideo";
    let loadVidID = "loadVideo";
    let loadVidButtonID = "addVid";

    let mcqBlockElemID = "mcqBlockElem";
    let mcqButtonID = "addElementMcq";

    let imgBlockElemID = "imgBlockElem";
    let imgButtonID = "addElementImg";

    let loadImgID = "loadImage";
    let loadImgButtonID = "addImg";

    let removeImageID = "removeImage";

    let param = {
        "btnPlusID":"addElement",
        "anchorID":"whiteBox",
        "addElementDivID": "addElementDiv",
        "textBlockElemID": "textBlockElem",
        "textButtonID": "addElementTxt",

        "videoBlockElemID": "videoBlockElem",
        "videoButtonID": "addElementVideo",
        /*"loadVidID": "loadVideo",
        "loadVidButtonID": "addVid",*/

        "mcqBlockElemID": "mcqBlockElem",
        "mcqButtonID": "addElementMcq",

        "imgBlockElemID": "imgBlockElem",
        "imgButtonID": "addElementImg",

        /*"loadImgID": "loadImage",
        "loadImgButtonID": "addImg",

        "removeImageID": "removeImage",*/
    }

    /*new ScenarioCreation(anchorID,
                        btnPlusID,
                        addElementDivID,
                        textBlockElemID,
                        textButtonID,
                        videoBlockElemID,
                        videoButtonID,
                        imgBlockElemID,
                        imgButtonID,
                        mcqBlockElemID,
                        mcqButtonID);*/
    new ScenarioCreation(param)

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

 function sendForm() {
     /*let emptyfield = false
     let form = document.getElementById("whiteBox");
     form.setAttribute("method", "POST");
     form.setAttribute("action", "/professor/train/save_scenario");

     let listOfIDfield = ["creator", "title", "skill", "topic", "grade_level", "instructions", "public"];
     for(let key in listOfIDfield){
         console.log("key : " + listOfIDfield[key]);
         let elem = document.getElementById(listOfIDfield[key])
         if(elem){

             let hiddenField = document.createElement("input");
             hiddenField.setAttribute("type", "hidden");
             hiddenField.setAttribute("name", listOfIDfield[key]);

             if (elem.type == "checkbox"){
               //hiddenField.setAttribute("type", "checkbox");
               //hiddenField.setAttribute("checked", elem.checked);
               //hiddenField.setAttribute("value", (elem.checked?"True":"False"));
               hiddenField.setAttribute("value", "True");
               //hiddenField.setAttribute("required", false);
               console.log(elem.checked)
             }else{
               console.log(elem.value)
               hiddenField.setAttribute("value", elem.value);
             }

             if(!elem.value || elem.value == ""){
                 emptyfield = true
             }

             form.appendChild(hiddenField);
         }
     }
     if (!emptyfield) {
         form.submit();
     }else {
         console.error("Empty field");
     }*/

     let data = {}
     let listOfParamIDfield = ["creator", "title", "skill", "topic", "grade_level", "instructions", "public"];

     for(let id of listOfParamIDfield){
         let elem = document.getElementById(id);
         data[id] = elem.value;
     }

     console.log(data);


     let data3 = {"creator": "super_creator",
                 "titre": "super_titre",
                 "skill": "super_skill",
                 "topic": "super_topic",
                 "grade_level": "super grade",
                 "instructions": "super_instructions",
                 "public": "False",
                 "elements":[{"type": "TextElem", "data":{"title": "JHKNLJHKNL", "content": "my content"}},
                             {"type": "TextElem", "data":{"title": "PPPPPPPPPPPPPP", "content": "my content"}}],
         }
         // construct an HTTP request
     let xhr = new XMLHttpRequest();

     xhr.open("POST", "/professor/train/save_scenario", true);
     xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
     xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"))
     // send the collected data as JSON
     //xhr.send(JSON.stringify(data));

     xhr.onloadend = function () {
         // done
         console.log(data);
         console.log("done");
     };

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
