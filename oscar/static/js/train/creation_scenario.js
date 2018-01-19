"use strict";

let counterBlock = 0;
class ScenarioCreation {

    //constructor(anchorID, btnPlusID, addElementDivID, textBlockElemID, textButtonID, videoBlockElemID, videoButtonID, imgBlockElemID, imgButtonID, mcqBlockElemID, mcqButtonID){
    constructor(param){
        this.data = this.getJsonData();

        this.anchor = document.getElementById(param.anchorID);
        this.btnPlus = document.getElementById(param.btnPlusID);
        this.addElementDiv = document.getElementById(param.addElementDivID);
        this.DiffElem = document.getElementById(param.DiffElem);
        this.addElementOption = false; // at start it is not shown


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

        this.pdfBlockElem = document.getElementById(param.pdfBlockElemID);
        this.pdfButton = document.getElementById(param.pdfButtonID);
        this.pdfButton.addEventListener("click", this.makeBlockElemPDF.bind(this), true);

        this.saveScenarioButton = document.getElementById(param.saveScenarioButtonID);
        this.saveScenarioButton.addEventListener("click", this.editForm.bind(this), true);

        this.sideNavBar = document.getElementById(param.sideNavBar) ;
        this.textBlockNav = document.getElementById(param.idTextElemNav);
        this.videoBlockNav = document.getElementById(param.idVideoElemNav);
        this.mcqBlockNav = document.getElementById(param.idMCQElemNav);
        this.imgBlockNav = document.getElementById(param.idImgElemNav);
        this.pdfBlockNav = document.getElementById(param.idPDFElemNav);

        this.skillsRender();

        this.fillPage();
    }

    skillsRender(){
        if (this.data["skills"]){
            for(var skill of this.data["skills"])
            {
                var newelem = document.createElement("span");
                newelem.innerHTML = '<button type="button" title="" ng-click="removeSkill(skill)" class="btn btn-primary selected-skill ng-binding">' + skill + "</button>"
                newelem.classList.add("ng-scope");
                newelem.setAttribute("ng-repeat", "skill in toTestSkills");
                newelem.addEventListener("click", deleteSkill,true);
                document.getElementsByClassName("well")[0].appendChild(newelem);
                var newLine = document.createElement("span");
                newLine.innerHTML = "\n<!-- end ngRepeat: skill in toTestSkills -->"
                document.getElementsByClassName("well")[0].appendChild(newLine);
            }
        }
    }

    makeBlockElemText(){
        var newelem = document.createElement("div");
        newelem.classList.add('textBlockElem');
        newelem.innerHTML = this.textBlockElem.innerHTML;
        newelem.setAttribute("id", counterBlock);
        this.anchor.appendChild(newelem);

        var ul = document.getElementById("simpleList");
        let newNavElem = document.createElement("div");
        newNavElem.classList.add('divElemNav');
        newNavElem.setAttribute("id", "navitem" + counterBlock);
        newNavElem.innerHTML = this.textBlockNav.innerHTML;
        newNavElem.setAttribute("href", "#" + counterBlock);

        ul.appendChild(newNavElem);
        counterBlock = counterBlock +1;
    }

    makeBlockElemImg(){
        let newelem = document.createElement("div")
        newelem.classList.add('imgBlockElem');
        newelem.innerHTML = this.imgBlockElem.innerHTML;
        newelem.setAttribute("id", counterBlock);
        this.anchor.appendChild(newelem);

        var ul = document.getElementById("simpleList");
        let newNavElem = document.createElement("div");
        newNavElem.classList.add('divElemNav');
        newNavElem.setAttribute("id", "navitem" + counterBlock);
        newNavElem.innerHTML = this.imgBlockNav.innerHTML;
        newNavElem.setAttribute("href", "#" + counterBlock);

        ul.appendChild(newNavElem);
        counterBlock = counterBlock +1;
    }

    makeBlockElemVideo(){
        let newelem = document.createElement("div");
        newelem.classList.add('videoBlockElem');
        newelem.innerHTML = this.videoBlockElem.innerHTML;
        newelem.setAttribute("id", counterBlock);
        this.anchor.appendChild(newelem);

        var ul = document.getElementById("simpleList");
        let newNavElem = document.createElement("div");
        newNavElem.classList.add('divElemNav');
        newNavElem.setAttribute("id", "navitem" + counterBlock);
        newNavElem.innerHTML = this.videoBlockNav.innerHTML;
        newNavElem.setAttribute("href", "#" + counterBlock);

        ul.appendChild(newNavElem);
        counterBlock = counterBlock +1;
    }

    makeBlockElemPDF(){
        let newelem = document.createElement("div");
        newelem.classList.add('pdfBlockElem');
        newelem.innerHTML = this.pdfBlockElem.innerHTML;
        newelem.setAttribute("id", counterBlock);
        this.anchor.appendChild(newelem);

        var ul = document.getElementById("simpleList");
        let newNavElem = document.createElement("div");
        newNavElem.classList.add('divElemNav');
        newNavElem.setAttribute("id", "navitem" + counterBlock);
        newNavElem.innerHTML = this.pdfBlockNav.innerHTML;
        newNavElem.setAttribute("href", "#" + counterBlock);

        ul.appendChild(newNavElem);
        counterBlock = counterBlock +1;
    }

    makeBlockElemMcq(){
        let newelem = document.createElement("div");
        newelem.classList.add('mcqBlockElem');
        newelem.innerHTML = this.mcqBlockElem.innerHTML;
        newelem.setAttribute("id", counterBlock);
        this.anchor.appendChild(newelem);
        newelem.style.display = "block";

        var ul = document.getElementById("simpleList");
        let newNavElem = document.createElement("div");
        newNavElem.classList.add('divElemNav');
        newNavElem.setAttribute("id", "navitem" + counterBlock);
        newNavElem.innerHTML = this.mcqBlockNav.innerHTML;
        newNavElem.setAttribute("href", "#" + counterBlock);
        console.log(newNavElem);

        ul.appendChild(newNavElem);
        counterBlock = counterBlock +1;
    }


    getElemInputBlockText(elemText){
        // let title = elemText.childNodes[1].childNodes[3].value;
        // let content = elemText.childNodes[1].childNodes[6].value;
        // console.log(elemText.getElementsByClassName('titre_text_Elem'));
        let title = elemText.getElementsByClassName('titre_text_Elem')[0].value;
        let content = elemText.getElementsByClassName('desc_text_Elem')[0].value;
        return {"type":"TextElem", "data":{"title": title, "content": content}}
    }

    /*
     *  We can get 2 images by 2 ways:
     *      - from url: the value from the url input is thus not empty
     *      - from oscar directories: the value from the url input is thus empty.
     *          We have to get the data from the image preview in base 64 in order to save it.
     *          When the scenario is edited, the image will be presented as a path from the directory
     */
    getElemInputBlockImage(elemImage){
        let title = elemImage.getElementsByClassName('title_img')[0].value;
        if(!elemImage.getElementsByClassName('url_img_Elem')[0].value){
            // Getting from directory:
            let url = elemImage.getElementsByClassName("imgprev")[0].getAttribute("src");
            //If no image has been set, the url value will be null so we have to initialize it
            if(!url){
                url = "";
                let description = elemImage.getElementsByClassName('desc_img_Elem')[0].value;
                return {"type":"ImgElem", "data":{"title": title, "url": url, "description" : description}}
            }
            let description = elemImage.getElementsByClassName('desc_img_Elem')[0].value;
            return {"type":"ImgElemHardDrive", "data":{"title": title, "url": url, "description" : description}}
        }
        else{
            // Getting from url:
            let url = elemImage.getElementsByClassName('url_img_Elem')[0].value;
            let description = elemImage.getElementsByClassName('desc_img_Elem')[0].value;
            return {"type":"ImgElem", "data":{"title": title, "url": url, "description" : description}}
        }
    }

    getElemInputBlockVideo(elemVideo){
        let title = elemVideo.getElementsByClassName('titre_vid_Elem')[0].value;
        let url = elemVideo.getElementsByClassName('url_vid_Elem')[0].value;
        console.log("The video url:",url);
        let description = elemVideo.getElementsByClassName('desc_vid_Elem')[0].value;
        return {"type":"VidElem", "data":{"title": title, "url": url, "description" : description}}
    }

    getElemInputBlockPDF(elemPDF){
        let title = elemPDF.getElementsByClassName('titre_pdf_Elem')[0].value;
        let url = elemPDF.getElementsByClassName('url_pdf_Elem')[0].value;
        let description = elemPDF.getElementsByClassName('desc_pdf_Elem')[0].value;
        return {"type":"PDFElem", "data":{"title": title, "url": url, "description" : description}}
    }

    getElemInputBlockMCQ(elemMCQ){

        let title = elemMCQ.getElementsByClassName('titre_MCQ_Elem')[0].value;
        let question = elemMCQ.getElementsByClassName('question_MCQ_Elem')[0].value;
        let tips = elemMCQ.getElementsByClassName('tipsMCQ')[0].value;
        let answers = [];
        for (let elem of elemMCQ.getElementsByClassName('repLine')){
             let reponse = elem.getElementsByClassName("answer")[0].value;
             let checked = elem.getElementsByClassName("answer1isvalid")[0].checked;
             answers.push({"answer": reponse, "solution": checked});

        }
        return {"type":"MCQElem", "data":{"title": title, "question": question, "tips": tips, "answers" : answers}}

    }

    // get the JSON data when editing in order to retrieve the elements
    getJsonData(){

        var pathTab = window.location.pathname.split("/")
        var id = pathTab[pathTab.length - 1]


        if(id != ""){ // If we get a number id, i.e. we want to edit a scenario
            let xhr = new XMLHttpRequest();

            xhr.open("GET", "/professor/train/data/"+id, false);

            xhr.send(null);
            // done
            if (xhr.readyState == 4 && xhr.status == 200) {
                var myArr = JSON.parse(xhr.responseText);

                return myArr;
            }
        }
        else{
            return {elements:[]};
        }
    }

    // make a filled element
    makeFilledText(index){
        let newelem = document.createElement("div");
        newelem.classList.add('textBlockElem');
        newelem.innerHTML = this.textBlockElem.innerHTML;
        newelem.setAttribute("id", index);
        newelem.getElementsByClassName('titre_text_Elem')[0].value = this.data["elements"][index]["data"]["title"]
        newelem.getElementsByClassName('desc_text_Elem')[0].value = this.data["elements"][index]["data"]["content"]
        this.anchor.appendChild(newelem);

        let ul = document.getElementById("simpleList");
        let newNavElem = document.createElement("div");
        newNavElem.classList.add('divElemNav');
        newNavElem.setAttribute("id", "navitem"+ index);
        newNavElem.innerHTML = this.textBlockNav.innerHTML;
        if (this.data["elements"][index]["data"]["title"] != ""){
            newNavElem.getElementsByTagName('label')[0].innerHTML = this.data["elements"][index]["data"]["title"]
        }

        ul.appendChild(newNavElem);
    }

    makeFilledImg(index){
        let newelem = document.createElement("div")
        newelem.classList.add('imgBlockElem');
        newelem.innerHTML = this.imgBlockElem.innerHTML;
        newelem.setAttribute("id", index);
        newelem.getElementsByClassName('title_img')[0].value = this.data["elements"][index]["data"]["title"]
        newelem.getElementsByClassName('url_img_Elem')[0].value = this.data["elements"][index]["data"]["url"]
        newelem.getElementsByClassName('desc_img_Elem')[0].value = this.data["elements"][index]["data"]["description"]
        newelem.getElementsByClassName('imgprev')[0].setAttribute("src", this.data["elements"][index]["data"]["url"]);
        this.anchor.appendChild(newelem);

        var ul = document.getElementById("simpleList");
        let newNavElem = document.createElement("div");
        newNavElem.classList.add('divElemNav');
        newNavElem.setAttribute("id", "navitem"+ index)
        newNavElem.innerHTML = this.imgBlockNav.innerHTML;
        if (this.data["elements"][index]["data"]["title"] != ""){
            newNavElem.getElementsByTagName('label')[0].innerHTML = this.data["elements"][index]["data"]["title"]
        }

        ul.appendChild(newNavElem);
    }

    /**
     *   When an Image is get from the directory, it's path adress contains all the directories from the root
     *   We then have to take only the part after the oscareducation directory. That is why we split and take the part second part
     */
    makeFilledImgHardDrive(index){
        let newelem = document.createElement("div")
        newelem.classList.add('imgBlockElem');
        newelem.innerHTML = this.imgBlockElem.innerHTML;
        newelem.setAttribute("id", index);
        newelem.getElementsByClassName('title_img')[0].value = this.data["elements"][index]["data"]["title"]
        newelem.getElementsByClassName('url_img_Elem')[0].value = this.data["elements"][index]["data"]["url"].split("oscareducation")[1];
        newelem.getElementsByClassName('desc_img_Elem')[0].value = this.data["elements"][index]["data"]["description"]
        newelem.getElementsByClassName('imgprev')[0].setAttribute("src", this.data["elements"][index]["data"]["url"].split("oscareducation")[1]);
        this.anchor.appendChild(newelem);

        var ul = document.getElementById("simpleList");
        let newNavElem = document.createElement("div");
        newNavElem.classList.add('divElemNav');
        newNavElem.setAttribute("id", "navitem"+ index)
        newNavElem.innerHTML = this.imgBlockNav.innerHTML;
        if (this.data["elements"][index]["data"]["title"] != ""){
            newNavElem.getElementsByTagName('label')[0].innerHTML = this.data["elements"][index]["data"]["title"]
        }

        ul.appendChild(newNavElem);
    }

    makeFilledVid(index){
        let newelem = document.createElement("div");
        newelem.classList.add('videoBlockElem');
        newelem.innerHTML = this.videoBlockElem.innerHTML;
        newelem.setAttribute("id", index);
        newelem.getElementsByClassName('titre_vid_Elem')[0].value = this.data["elements"][index]["data"]["title"]
        newelem.getElementsByClassName('url_vid_Elem')[0].value = this.data["elements"][index]["data"]["url"]
        newelem.getElementsByClassName('desc_vid_Elem')[0].value = this.data["elements"][index]["data"]["description"]
        loadVideo(newelem.getElementsByClassName('addVid')[0])
        this.anchor.appendChild(newelem);

        var ul = document.getElementById("simpleList");
        let newNavElem = document.createElement("div");
        newNavElem.classList.add('divElemNav');
        newNavElem.setAttribute("id", "navitem"+ index)
        newNavElem.innerHTML = this.videoBlockNav.innerHTML;
        if (this.data["elements"][index]["data"]["title"] != ""){
            newNavElem.getElementsByTagName('label')[0].innerHTML = this.data["elements"][index]["data"]["title"]
        }

        ul.appendChild(newNavElem);
    }

    makeFilledPDF(index){
        let newelem = document.createElement("div");
        newelem.classList.add('pdfBlockElem');
        newelem.innerHTML = this.pdfBlockElem.innerHTML;
        newelem.setAttribute("id", index);
        newelem.getElementsByClassName('titre_pdf_Elem')[0].value = this.data["elements"][index]["data"]["title"]
        newelem.getElementsByClassName('url_pdf_Elem')[0].value = this.data["elements"][index]["data"]["url"]
        newelem.getElementsByClassName('desc_pdf_Elem')[0].value = this.data["elements"][index]["data"]["description"]
        newelem.getElementsByClassName('pdfprev')[0].setAttribute("src", this.data["elements"][index]["data"]["url"]);
        this.anchor.appendChild(newelem);

        var ul = document.getElementById("simpleList");
        let newNavElem = document.createElement("div");
        newNavElem.classList.add('divElemNav');
        newNavElem.setAttribute("id", "navitem"+ index)
        newNavElem.innerHTML = this.pdfBlockNav.innerHTML;
        if (this.data["elements"][index]["data"]["title"] != ""){
            newNavElem.getElementsByTagName('label')[0].innerHTML = this.data["elements"][index]["data"]["title"]
        }

        ul.appendChild(newNavElem);
    }

    makeFilledMcq(index){
        let newelem = document.createElement("div");
        newelem.classList.add('mcqBlockElem');
        newelem.innerHTML = this.mcqBlockElem.innerHTML;
        newelem.setAttribute("id", index);
        // filling the title and the question
        newelem.getElementsByClassName('titre_MCQ_Elem')[0].value = this.data["elements"][index]["data"]["title"]
        newelem.getElementsByClassName('question_MCQ_Elem')[0].value = this.data["elements"][index]["data"]["question"]
        newelem.getElementsByClassName('tipsMCQ')[0].value = this.data["elements"][index]["data"]["tips"]

        // filling the first and the second answer of the mcq (because they are mandatory)
        newelem.getElementsByClassName('answer1')[0].value = this.data["elements"][index]["data"]["answers"][0]["answer"]
        newelem.getElementsByClassName('answer1isvalid')[0].checked = this.data["elements"][index]["data"]["answers"][0]["solution"]

        newelem.getElementsByClassName('answer2')[0].value = this.data["elements"][index]["data"]["answers"][1]["answer"]
        newelem.getElementsByClassName('answer2isvalid')[0].checked = this.data["elements"][index]["data"]["answers"][1]["solution"]

        // optionally filling the other answers
        for(let i = 2;i<this.data["elements"][index]["data"]["answers"].length;i++)
        {
            addReponseFilled(newelem.getElementsByClassName('panel-body')[0], this.data["elements"][index]["data"]["answers"][i]);
        }

        // this.anchor.getElementsByClassName("list_answers")[0].appendChild(newelem);

        this.anchor.appendChild(newelem);
        newelem.style.display = "block";

        var ul = document.getElementById("simpleList");
        let newNavElem = document.createElement("div");
        newNavElem.classList.add('divElemNav');
        newNavElem.setAttribute("id", "navitem"+ index)
        newNavElem.innerHTML = this.mcqBlockNav.innerHTML;
        if (this.data["elements"][index]["data"]["title"] != ""){
            newNavElem.getElementsByTagName('label')[0].innerHTML = this.data["elements"][index]["data"]["title"]
        }

        ul.appendChild(newNavElem);
    }

    fillPage()
    {
        if(this.data){
            for(let i = 0;i<this.data["elements"].length;i++)
            {
                if(this.data["elements"][i]["type"] == "TextElem")
                {
                    this.makeFilledText(i);
                }
                else if(this.data["elements"][i]["type"] == "ImgElemHardDrive")
                {
                    this.makeFilledImgHardDrive(i);
                }
                else if(this.data["elements"][i]["type"] == "ImgElem")
                {
                    this.makeFilledImg(i);
                }
                else if(this.data["elements"][i]["type"] == "VidElem")
                {
                    this.makeFilledVid(i);
                }
                else if(this.data["elements"][i]["type"] == "PDFElem")
                {
                    this.makeFilledPDF(i);
                }
                else if(this.data["elements"][i]["type"] == "MCQElem")
                {
                    this.makeFilledMcq(i);
                }
            }
        }
    }

    editForm(){
        var pathTab = window.location.pathname.split("/")
        var id = pathTab[pathTab.length - 1]
        if (id == "") {
            id = pathTab[pathTab.length - 2]
        }
        if (id != "create_scenario") {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", "/professor/train/delete_scenario/"+id, false ); // false for synchronous request
            xmlHttp.send( null );
            //return xmlHttp.responseText;
        }
        this.sendForm();
    }

    sendForm() {

        let data = {};
        let listOfParamIDfield = ["title", "topic", "grade_level", "instructions", "public", "backgroundImage"];


        for(let id of listOfParamIDfield){
            let elem = document.getElementById(id);
            if(id=="public")
            {
                data[id] = elem.checked;
            }
            else
            {
                data[id] = elem.value;
            }


        }
        // get skills
        data["skill"] = "";
        data["skills"] = [];
        let skillsBox = document.getElementById("skillsBox");
        for(let skillBox of skillsBox.childNodes){
            if(skillBox.classList && skillBox.classList.contains("ng-scope") && skillBox.getElementsByTagName("button")[0]) {
                let skill = skillBox.getElementsByTagName("button")[0].innerHTML.trim();
                data["skills"].push(skill)
            }
        }

        data["elements"] = []

        for(let i = 0; i < this.anchor.childNodes.length; i++)
        {

            let classElem = this.anchor.childNodes[i].className;

            if(classElem == "textBlockElem")
            {
                data["elements"].push(this.getElemInputBlockText(this.anchor.childNodes[i]));
            }
            else if(classElem == "videoBlockElem")
            {
                data["elements"].push(this.getElemInputBlockVideo(this.anchor.childNodes[i]));
            }
            else if(classElem == "imgBlockElem")
            {
                data["elements"].push(this.getElemInputBlockImage(this.anchor.childNodes[i]));
            }
            else if(classElem =="mcqBlockElem")
            {
                data["elements"].push(this.getElemInputBlockMCQ(this.anchor.childNodes[i]));
            }
            else if(classElem =="pdfBlockElem")
            {
                data["elements"].push(this.getElemInputBlockPDF(this.anchor.childNodes[i]));
            }
        }

        //construct an HTTP request

        let xhr = new XMLHttpRequest();

        xhr.open("POST", "/professor/train/save_scenario", true);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"))

        // send the collected data as JSON
        xhr.send(JSON.stringify(data));
        var pathArray = window.location.pathname.split( '/' );
        var pk = pathArray[4]
        var new_url = "/professor/lesson/"+pk+"/#listscena"
        xhr.onloadend = function () {
            window.location.href = new_url;
        };
    }

}
function cancelCreation(elem){
    if (confirm('Etes vous sur de vouloir annuler la création de ce scénario ?'))
    {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", "/professor/train/cancel_scenario/", false ); // false for synchronous request
        xmlHttp.send( null );
        var pathArray = window.location.pathname.split( '/' );
        var pk = pathArray[4];
        var new_url = "/professor/lesson/"+pk+"/#listscena";
        window.location.href = new_url;
    }
    else
    {
        console.log('no');
    }
}

function loadImage(elem){
    let root = elem.parentNode;
    let imgPreview = root.getElementsByClassName("imgprev")[0];
    imgPreview.setAttribute("src", root.getElementsByClassName("url_img_Elem")[0].value);
    return false;
}

function loadImageElem(elem){
    let root = elem.parentNode;
    let imgPreview = root.getElementsByClassName("imgprev")[0];
    imgPreview.setAttribute("src", root.getElementsByClassName("url_img_Elem")[0].value);
    root.getElementsByClassName("importButton")[0].value = "";
}

function loadFile(event, elem){
    let root = elem.parentNode;
    var reader = new FileReader();
    reader.onload = function(){
        let imgPreview = root.getElementsByClassName("imgprev")[0];
        imgPreview.setAttribute("src", reader.result);
    }
    reader.readAsDataURL(event.target.files[0]);
    root.getElementsByClassName("url_img_Elem")[0].value = "";
    return false
}

function loadPDF(elem){
    let root = elem.parentNode;
    let pdfPreview = root.getElementsByClassName("pdfprev")[0];
    let pdfURL = root.getElementsByClassName("url_pdf_Elem")[0].value;
    var embedURL = "http://docs.google.com/gview?url=" + pdfURL + "&embedded=true";
    pdfPreview.setAttribute("src", embedURL);
    pdfPreview.setAttribute("type", "application/pdf");
    pdfPreview.style.display = "block";
    return false;
}

function loadVideo(elem){
    let root = elem.parentNode;
    let url = root.getElementsByClassName("url_vid_Elem")[0].value;
    if(url == ""){
        return false;
    }
    let ID = getVideoId(url);
    let embedURL = "//www.youtube.com/embed/" + ID
    let videoIframe = root.getElementsByTagName("iframe")[0]
    videoIframe.setAttribute("src", embedURL);
    videoIframe.style.display = "block";
    return false;
}

// Transforms the video URL into its embed version for better hosting support
function getVideoId(url) {
    var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    var match = url.match(regExp);

    if (match && match[2].length == 11) {
        return match[2];
    } else {
        return 'error';
    }
}
//Add a response on the MCQ.
function addReponse(elem){
    var root = elem.parentNode.parentNode;
    let count = 0;
    let repLineElem = null;
    for(let subElem of root.getElementsByClassName('list_answers')[0].childNodes){
        if (subElem.className == "repLine"){
            count++;
            if(repLineElem == null){
                repLineElem = subElem;
            }
        }
    }
    if (count < 4) {
        let newelem = document.createElement("div");
        newelem.classList.add('repLine');
        newelem.innerHTML = repLineElem.innerHTML;
        let txt = repLineElem.getElementsByClassName('labelanswer')[0].innerHTML;
        newelem.getElementsByClassName('labelanswer')[0].innerHTML = txt.substring(0,txt.length -2) + (count +1) +':';
        newelem.getElementsByClassName('removeReponse')[0].style.display = "inline";
        root.getElementsByClassName('list_answers')[0].appendChild(newelem);
        if (count >= 3) {
            let button = root.getElementsByClassName('btn-primary addReponse')[0];
            button.style.display = "none";
        }
    }
    return false;
}

function addReponseFilled(root, answer){
    let count = 0;
    let repLineElem = null;
    for(let subElem of root.getElementsByClassName('list_answers')[0].childNodes){
        if (subElem.className == "repLine"){
            count++;
            if(repLineElem == null){
                repLineElem = subElem;
            }
        }
    }
    if (count < 4) {
        let newelem = document.createElement("div");
        newelem.classList.add('repLine');
        newelem.innerHTML = repLineElem.innerHTML;
        // TODO: virer ces childnodes
        let txt = repLineElem.childNodes[1].innerHTML;
        newelem.childNodes[1].innerHTML = txt.substring(0,txt.length -2) + (count +1);
        newelem.childNodes[7].style.display = "inline";
        newelem.getElementsByClassName('answer1')[0].value = answer["answer"]
        newelem.getElementsByClassName('answer1isvalid')[0].checked = answer["solution"]
        root.getElementsByClassName('list_answers')[0].appendChild(newelem);
    }

    //root.parentNode.removeChild(root);
    return false;
}
//This function permits to delete a principal block and also in the sideBar
function removeElem(elem){
    if (confirm('Etes vous sur de vouloir supprimer cet objet ?'))
    {
        var root = elem.parentNode.parentNode;
        var ul = document.getElementsByClassName("divElemNav");
        var id = root.getAttribute("id");
        var supNode = document.getElementById("navitem"+ id);
        supNode.parentNode.removeChild(supNode);
        root.parentNode.removeChild(root);
    }
    else
    {
    }
}

function deleteSkill(elem) {
    var parent = elem.target.parentNode;
    parent.removeChild(elem.target);
}
//This function permits to minimize or enlarge the element except Parameters.
function enlargeElem(elem){
    var root = elem.parentNode.parentNode;
    let miniElem = root.getElementsByClassName("panel-body")[0];
    var rootbutton = elem.parentNode;
    let buttonmini = rootbutton.getElementsByClassName("minimizeElem")[0];
    let buttonenla = rootbutton.getElementsByClassName("enlargeElement")[0];
    if(miniElem.style.display=="none"){
        miniElem.style.display = "block";
        buttonmini.style.display = "block";
        buttonenla.style.display = "none";
    }
    else {
        miniElem.style.display = "none";
        buttonmini.style.display = "none";
        buttonenla.style.display = "block";
    }
}
function auto_growth_textarea(elem){
    elem.style.height = "5px";
    elem.style.height = (elem.scrollHeight)+"px";
}
//This function permits to delete an answer in the MCQ exercise.
function removeReponse(elem){
    var root = elem.parentNode.parentNode.parentNode.parentNode;
    let count = 0;
    let repLineElem = null;
    for(let subElem of root.getElementsByClassName('list_answers')[0].childNodes){
        if (subElem.className == "repLine"){
            count++;
        }
    }
    if (count -1 <= 3){
        let button = root.getElementsByClassName('btn-primary addReponse')[0];
        button.style.display = "block";
    }
    var delrep = elem.parentNode;
    delrep.parentNode.removeChild(delrep);
    return false;
}




//This function permits to fill automatically the field on the navBar when the user is writting the title of the content.
function fillTitle(elem){
    var root = elem.parentNode.parentNode;
    var navitemId = "navitem" + root.getAttribute("id");
    setInterval(function(){
        var titre = elem.value;
        var titrenavbarelem = document.getElementById(navitemId).getElementsByTagName("label")[0];
        if (titre == ""){
            console.log("in");
            if(titrenavbarelem.classList.contains("textetitre")){
                titre = "Texte";
            }
            else if (titrenavbarelem.classList.contains("imagetitre")){
                titre = "Image";
            }
            else if (titrenavbarelem.classList.contains("videotitre")){
                titre = "Vidéo";
            }
            else if (titrenavbarelem.classList.contains("qcmtitre")){
                titre = "QCM";
            }
            else if (titrenavbarelem.classList.contains("pdftitre")){
                titre = "PDF";
            }
        }
        document.getElementById(navitemId).getElementsByTagName("label")[0].innerHTML = titre;
    }, 0);
}

// initiation
window.onload = function(){


    if(typeof angular == 'undefined') {
      console.log("errror");
    }else {
      console.log("no error");
    }



    let param = {
        "btnPlusID":"addElement",
        "anchorID":"whiteBox",
        "addElementDivID": "addElementDiv",
        "DiffElem": "DiffElem",
        "textBlockElemID": "textBlockElem",
        "textButtonID": "addElementTxt",
        "idTextElemNav": "idTextElemNav",
        "idImgElemNav": "idImgElemNav",
        "idVideoElemNav": "idVideoElemNav",
        "idMCQElemNav": "idMCQElemNav",
        "idPDFElemNav": "idPDFElemNav",
        "sideNavBar" : "navFixed",

        "videoBlockElemID": "videoBlockElem",
        "videoButtonID": "addElementVideo",
        /*"loadVidID": "loadVideo",
        "loadVidButtonID": "addVid",*/

        "mcqBlockElemID": "mcqBlockElem",
        "mcqButtonID": "addElementMcq",

        "imgBlockElemID": "imgBlockElem",
        "imgButtonID": "addElementImg",

        "pdfBlockElemID": "pdfBlockElem",
        "pdfButtonID": "addElementPDF",
        "saveScenarioButtonID": "saveScenario"


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
