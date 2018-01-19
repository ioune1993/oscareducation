"use strict"
window.onload = function(){
    let scenarioList = document.getElementsByClassName("mycontentlist");
    if(scenarioList.length == 0){
        let emptyDiv = document.createElement("div");
        emptyDiv.classList.add("emptyListScenario");
        emptyDiv.innerHTML = "<div>Vous n'avez aucun scénario</div>";
        document.getElementsByClassName("mylist")[0].parentNode.parentNode.appendChild(emptyDiv);
    }
    else{
        // We get the list of skills from the haml
        let skillList = document.getElementsByClassName("skillList");
        //we iterate on eache scenario's skills list
        for(let i=0; i < skillList.length ; i++){
            //first we have to get rid of all space and newline characters
            let skills = skillList[i].innerHTML.split(" ");
            let array = [];
            for(let j = 0 ; j< skills.length ; j++){
                if(skills[j] != "" && skills[j] != "\n")
                    //then we put each skill between <a> block
                    array.push("<a>"+skills[j]+"</a>");
            }
            // console.log(array);
            var totalLength = array.length;
            //check if the number of skills exceed 3, if it's the case then just print 3 and add "..."
            while(array.length > 3){
                array.pop(array[array.length-1]);
            }
            if(totalLength > 3) array.push(" ...");
            skillList[i].innerHTML = array;
        }
    }

    let otherscenarioList = document.getElementsByClassName("othercontentlist");
    let otherlist = document.getElementsByClassName("otherlist");
    if(otherlist.length != 0 && otherscenarioList.length == 0){
        let emptyDiv = document.createElement("div");
        emptyDiv.classList.add("emptyListScenario");
        emptyDiv.innerHTML = "<div>Il n'y a pas de scénario disponible</div>";
        otherlist[0].parentNode.parentNode.appendChild(emptyDiv);
    }
    // else{
    //     // We get the list of skills from the haml
    //     let skillList = document.getElementsByClassName("skillForeignerList");
    //     //we iterate on eache scenario's skills list
    //     for(let i=0; i < skillList.length ; i++){
    //         //first we have to get rid of all space and newline characters
    //         let skills = skillList[i].innerHTML.split(" ");
    //         let array = [];
    //         for(let j = 0 ; j< skills.length ; j++){
    //             if(skills[j] != "" && skills[j] != "\n")
    //                 //then we put each skill between <a> block
    //                 array.push("<a>"+skills[j]+"</a>");
    //         }
    //         console.log(array);
    //         var totalLength = array.length;
    //         //check if the number of skills exceed 3, if it's the case then just print 3 and add "..."
    //         while(array.length > 3){
    //             array.pop(array[array.length-1]);
    //         }
    //         if(totalLength > 3) array.push(" ...");
    //         skillList[i].innerHTML = array;
    //     }
    // }

};

function ConfirmDelete(elem){
    if (confirm('Etes vous sur de vouloir supprimer cet objet ?'))
    {
        let id = elem.getAttribute('data');
        let xhr = new XMLHttpRequest();
        xhr.open("GET", "/professor/train/delete_scenario/"+id);
        xhr.send( null );

        let line = elem.parentNode.parentNode;
        let root = line.parentNode;
        root.removeChild(line);
    }
    else
    {
        console.log('no');
    }
}
