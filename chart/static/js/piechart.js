dataArr = [[]];
labels = [[]];
colors = ['#0F408D','#6F1B75','#CA147A','#DA2228','#E8801B','#FCF302','#8DC922','#15993C','#87CCEE','#0092CE']
function chart_createPieChartFromForm()
{
	graphics = document.getElementsByClassName("chartQuestionPiechart");
	var element;
	for(var i = 0;i<graphics.length;i++)
    {
  		var type = $(graphics[i]).data( "chart-type" );
		if(type == "chart-piechart")
	    {
			var sector = (($(".sector").eq(i).val())/360)*100;
			var label = $(".labelPie").eq(i).val();

			$(".sector").eq(i).val('');

			while(dataArr.length<=i)dataArr.push([]);
			while(labels.length<=i)labels.push([]);


			var sum = dataArr[i].reduce(function(a, b) { return a + b; }, 0);
			if(sector == undefined ||sector == null || sector == '')
			{
				continue;
			}
			if(sum+sector>100){
				alert('la valeur entrée est trop grande ! Veuillez la réduire ou supprimer des portions précedentes');
				continue;
			}

			this.dataArr[i].push(sector)
			this.labels[i].push(label)
	    	{
	    		create_pieChart(graphics[i],i);
	    	}
		}
	}
}


var changePieChartHiddenInput = function()
{
    var data = {"data":dataArr[0],"labels":labels[0]}
    $("#piechart-hiddenInput").val(JSON.stringify(data));
    console.log($("#piechart-hiddenInput").val())

}

function create_pieChart(element,index)//complete is a boolean determining if the pieChart is complete or not
{
	var colorsChart = [];
	var labelsChart = [];
	var sum = 0;
	var lastPortion = [];

	for(var i = 0;i<dataArr[index].length;i++)
	{
		colorsChart.push(colors[i%colors.length]);
		labelsChart.push(labels[index][i%labels.length]);
		sum+=dataArr[index][i];
	}


	if(sum < 100)
	{
		lastPortion.push(100-sum);
		colorsChart.push('white');
		labelsChart.push(' ');
	}
	element.id = "board"+index;
	board = JXG.JSXGraph.initBoard(element.id, {id:"chart-pieChartFromForm-"+index,showNavigation:false, showCopyright:false, boundingbox: [-5, 5, 5, -5]});
	board.containerObj.style.backgroundColor = 'white';
	board.options.label.strokeColor = 'black';
	board.suspendUpdate();
	let a = board.create('chart', this.dataArr[index].concat(lastPortion),
		{chartStyle:'pie',
		 colors:colorsChart,
		 fillOpacity:1, center:[0,0], strokeColor:'black', highlightStrokeColor:'black', strokeWidth:0,
		 labels:labelsChart,
		 highlightColors:['#E46F6A','#F9DF82','#F7FA7B','#B0D990','#69BF8E','#BDDDE4','#92C2DF','#637CB0','#AB91BC','#EB8EBF'],
		 highlightOnSector:false,
		 highlightBySize:false
		}
	);
	board.unsuspendUpdate();

}

function chart_deleteLastPie(element)
{
    var index = $(".btn-deletePie").index(element);
	this.dataArr[index].pop()
	this.labels[index].pop()
	create_pieChart(document.getElementsByClassName("chartQuestionPiechart")[index],index)
}

function chart_getJSONPie(index)
{
    return JSON.stringify({
        "point":dataArr[index],
        "labels":labels[index]
    });
}
