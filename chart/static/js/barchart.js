/*
    Every function must follow the format chart_nameInCamelCase
    TODO ; il faut gerer qund plusieurs questions sont posee; on peut avoir plusieurs reponses, mais pas plusieurs questions
*/

var bars = [[]];
var AxisX = [];
var AxisY = [];
var boardBarChart = [];
var zeroX = [];
var zeroY = [];
var maxX = [];
var maxY = [];
var points = [[]];
var precisionValue = [];
var chart_opacity = 1;
$( document ).ready(function() {
    chart_refresh();
});

function chart_changeInput($scope)
{
    $scope.barGraphX = "abscisses";
    $scope.barGraphY = "ordonnees";
    $scope.stepX = 1;
    $scope.stepY = 1;
    $scope.precisionValue = 1;

    $scope.zeroX = -1;
    $scope.zeroY = -1;
    $scope.maxX = 10;
    $scope.maxY = 10;

    $scope.sector = 90;
    $scope.labelPie = "secteur";
}

function chart_refresh()
{
    var graphics = document.getElementsByClassName("chartQuestion");  //find all charts on the page
    for(var i = 0;i<graphics.length;i++){
        console.log("found "+graphics.length+" graphics");
        chart_createChart(graphics[i]);  //create the element founded
    }
    chart_createBarChartFromForm()

    if($("#barchart-hiddenInput"))
    {
        //update the hidden field every 1/2 second. It works.
        setInterval(function(){
            var bar = [];
            for(var i = 0;i<points[0].length;i++){
                bar.push(chart_getPointValue(points[0],i)());
            }

            $("#barchart-hiddenInput").val(bar);

        }, 500);

    }

    if($("#piechart-hiddenInput"))
    {
        //update the hidden field every 1/2 second. It works.
        setInterval(changePieChartHiddenInput, 500);

    }

}

function chart_setBars()
{
	this.bars = [[]];
}

function chart_setPoints()
{
	this.points = [[]];
}

function chart_addBar(bar,which)
{
	this.bars[which].push(bar);
}

function chart_addPoint(point,which)
{
	this.points[which].push(point);
}
function chart_removeBar(which)
{
	this.bars[which].pop();
}

function chart_removePoint(which)
{
	this.points[which].pop();
}

function chart_setAxis(AxisX,AxisY,which)
{
	this.AxisX[which] = AxisX;
	this.AxisY[which] = AxisY;
}

function chart_setOrigin(zX,zY,mX,mY,which)
{
	this.zeroX[which] = zX;
	this.zeroY[which]= zY;
	this.maxX[which]= mX;
	this.maxY[which] = mY;
}


function chart_updateForStudent()
{
    graphics = document.getElementsByClassName("chartQuestionStudent");
	var element;
	for(var i = 0;i<graphics.length;i++)
	{

        element = graphics[i];
        var rawData = $(element).data( "chart-raw" );
        var rawData2 = $(element).data( "chart-raw2" );
        var rawData3 = $(element).data( "chart-raw3" );

        precisionValue[i] = 1;
        element.id = "board"+i;
        var r = {};
        r.AxisX = " nope";
        r.AxisY = " Nope";
        var box = [-1, 5, 5, -1];


        if(rawData2 != null)
        {
            rawData = chart_parse_orderedDict(rawData2);
        }
        if( rawData3 != null)
        {
            rawData = chart_parse_orderedDict(rawData3);
        }
        /*
            if there is data given from the server, we must parse it.
            We all write bad code, but if it works, it works.
            Don't judge, morty.
        */
        if(rawData != undefined)
        {
            var test =String(rawData);
            for(var temp = 0;temp<100;temp++) // I don't know why, but we must pass the regex as much as there answers
                test = test.replace(/u'(?=[^:]+')/g, "'").replace(/'/g, '"').replace('u"', '"').replace("False", 'false').replace("True", 'true').replace('"{', '{').replace('}"', '}').replace('u"', '"')


            var parsed =  JSON.parse(test);
            r = parsed[0];
            if(rawData2 != null)r = parsed;
            if(rawData3 != null)r = parsed;
            box = [r.zeroX, r.maxY,r.maxX,r.zeroY];
        }

        let board = JXG.JSXGraph.initBoard(element.id,{ id:"chart-barChartFromForm-"+i,axis:false,showCopyright:false, boundingbox:box});
        this.boardBarChart[i] = board;
        xaxis = board.create('axis', [[0,0],[1,0]],
                    {name:r.AxisX,
                    withLabel:true,
                    label: {
                        position:'rt',
                        offset:[-15,20]
                        }
                    });
        yaxis = board.create('axis', [[0,0],[0,1]],
                    {name:AxisY,
                    withLabel:true,
                    label: {
                        position:'rt',
                        offset:[20,0]
                        }
                    });
        var temp =[];
        if(this.points[i] == undefined) this.points[i] = [];
        if(this.bars[i] == undefined) this.bars[i] = [];
        for(var j = 0;j<this.points[i].length;j++)
        {
            let p = this.boardBarChart[i].create('point',[j+1,this.points[i][j].Y()],{name:'',size:7,face:'^'});
            temp.push(p);
        }
        this.points[i] = temp;
        this.bars[i] = []
        for(var j = 0;j<this.points[i].length;j++)
        {
            this.bars[i].push(chart_getPointValue(this.points[i],j));
        }
        let chart;
        if(this.bars[i] != undefined)
            if(this.bars[i].length >0)
                 char = board.create('chart', [this.bars[i]],
                            {chartStyle:'bar', width:1, labels:this.bars[i],
                             colorArray:['#8E1B77','#BE1679','#DC1765','#DA2130','#DB311B','#DF4917','#E36317','#E87F1A','#F1B112','#FCF302','#C1E212'], shadow:false});

	}


}


function chart_createBarChartFromForm()
{
	graphics = document.getElementsByClassName("chartQuestionBarchart");
	var element;
	for(var i = 0;i<graphics.length;i++)
    {
  		var type = $(graphics[i]).data( "chart-type" );
		if(type == "chart-barchart")
        {
            var barGraphX = $(".barGraphX").eq(i).val();
            var barGraphY = $(".barGraphY").eq(i).val();

            var stepX = $(".stepX").eq(i).val();
            var stepY = $(".stepY").eq(i).val();

            var zX = parseInt($(".zeroX").eq(i).val());
            var zY = parseInt($(".zeroY").eq(i).val());
            precisionValue = parseFloat($(".precisionValue").eq(i).val());
            if(precisionValue<=0)precisionValue = 1;

            var mX = parseInt($(".maxX").eq(i).val());
            var mY = parseInt($(".maxY").eq(i).val());
            element = graphics[i];

        	if(this.points == undefined && this.bars == undefined)
        	{
        		chart_setPoints(i);
        	}
        	chart_setBars(i);
        	chart_setAxis(barGraphX,barGraphY,i);
        	chart_setOrigin(zX,zY,mX,mY,i);

            element.id = "board"+i;
            let board = JXG.JSXGraph.initBoard(element.id,{ id:"chart-barChartFromForm-"+i,fillOpacity:chart_opacity,axis:false,showCopyright:false, boundingbox: [this.zeroX[i], this.maxY[i], this.maxX[i], this.zeroY[i]]});
            this.boardBarChart[i] = board;
        	xaxis = board.create('axis', [[0,0],[1,0]],
        				{name:this.AxisX[i],
        				withLabel:true,
        				label: {
        					position:'rt',
        					offset:[-15,20]
        					}
        				});
        	yaxis = board.create('axis', [[0,0],[0,1]],
        				{name:this.AxisY[i],
        				withLabel:true,
        				label: {
        					position:'rt',
        					offset:[20,0]
        					}
        				});
        	var temp =[];
            if(this.points[i] == undefined) this.points[i] = [];
            if(this.bars[i] == undefined) this.bars[i] = [];
        	for(var j = 0;j<this.points[i].length;j++)
        	{
        		let p = this.boardBarChart[i].create('point',[j+1,this.points[i][j].Y()],{name:'',size:7,face:'^'});
        		temp.push(p);
        	}
        	this.points[i] = temp;
        	for(var j = 0;j<this.points[i].length;j++)
        	{
                this.bars[i].push(chart_getPointValue(this.points[i],j));
            }
            let chart;
            if(this.bars[i] != undefined)
                if(this.bars[i].length >0)
                     char = board.create('chart', [this.bars[i]],
                        {chartStyle:'bar', width:1, labels:this.bars[i],fillOpacity:chart_opacity,
                         colorArray:['#8E1B77','#BE1679','#DC1765','#DA2130','#DB311B','#DF4917','#E36317','#E87F1A','#F1B112','#FCF302','#C1E212'], shadow:false});

        }
	}



}

function chart_createChart(element)
{
    var type = $(element).data( "chart-type" );

    var rawData = $(element).data( "chart-raw" );
    var rawData2 = $(element).data( "chart-raw2" );
    var rawData3 = $(element).data( "chart-raw3" );
    var dataArr = $(element).data("chart-percent");
    var board;
    if(type.includes("chart-barchart"))
    {
        var box = [-1, 5, 5, -1];

        if(rawData2 != null)
        {
            rawData = chart_parse_orderedDict(rawData2);
        }
        if( rawData3 != null)
        {
            rawData = chart_parse_orderedDict(rawData3);
        }
        /*
            if there is data given from the server, we must parse it.
            We all write bad code, but if it works, it works.
            Don't judge, morty.
        */
        if(rawData != undefined)
        {
            var test =String(rawData);
            for(var temp = 0;temp<100;temp++) // I don't know why, but we must pass the regex as much as there is answers. I hope there won't be more than 100
                test = test.replace(/u'(?=[^:]+')/g, "'").replace(/'/g, '"').replace('u"', '"').replace("False", 'false').replace("True", 'true').replace('"{', '{').replace('}"', '}').replace('u"', '"')


            var parsed =  JSON.parse(test);
            let r = parsed[0];
            if(rawData2 != null)r = parsed;
            if(rawData3 != null)r = parsed;
            box = [r.zeroX, r.maxY,r.maxX,r.zeroY];
        }

        let board = JXG.JSXGraph.initBoard(element.id, { axis:true,showCopyright:false, boundingbox: box,showNavigation : false});
        this.boardBarChart[0] = board;
       	var l = [];
       	var bar = [];
       	p = [];
        for(var i = 0;i<l.length;i++){
        	var point = board.create('point', [i+1,l[i]],{name:'',size:7,face:'^'});
        	p.push(point);
        }

        for(var i = 0;i<p.length;i++){
        	bar.push(chart_getPointValue(p,i));
        }

        let chart;
        if(this.bars[0] != undefined && rawData == undefined)
            if(this.bars[0].length >0)
                 char = board.create('chart', [this.bars[0]],
                            {chartStyle:'bar', width:1, labels:this.bars[0],
                             colorArray:['#8E1B77','#BE1679','#DC1765','#DA2130','#DB311B','#DF4917','#E36317','#E87F1A','#F1B112','#FCF302','#C1E212'], shadow:false});


    }

    chart_updateForStudent();
}

function chart_getPointValue(points,index)
{
	return function(){
		return chart_roundToStep(points[index].Y(),precisionValue);
	}
}


function chart_add(element)
{
    var index = $(".btn-addBar").index(element);
	var newBarY = parseInt($(".newBarY").eq(index).val());
	var p = this.boardBarChart[index].create('point',[this.bars[index].length+1,newBarY],{name:'',size:7,face:'^'});
	chart_addBar(newBarY,index);
	chart_addPoint(p,index);
    chart_update();
}


function chart_btnUpdate(element)
{
    var index = $(".btn-updateBar").index(element);
    chart_createBarChartFromForm();

}
function chart_update()
{
    chart_createBarChartFromForm();
    chart_updateForStudent();

}



function chart_changeScopeQuestions(questions)
{
    var counterBar = 0;
    var counterPie = 0;
    for(var i = 0;i<questions.length;i++)
    {
        if(questions[i].type == "chart-barchart")
        {
            for(var j = 0;j<questions[i].answers.length;j++)
            {
                questions[i].answers[j].chart = chart_getJSONBar(counterBar);
                counterBar++;
            }
        }
        if(questions[i].type == "chart-piechart")
        {
            for(var j = 0;j<questions[i].answers.length;j++)
            {
                questions[i].answers[j].chart = chart_getJSONPie(counterPie);
                counterPie++;
            }
        }
    }
    return questions;
}


function chart_deleteLastBar(element)
{
    var index = $(".btn-deleteBar").index(element);
    chart_removeBar(index);
    chart_removePoint(index);
    chart_update();
}

function chart_getJSONBar(index)
{
    pointValue = [];
    if(bars[index] == undefined)bars[index] = [];
    for(var i = 0;i<bars[index].length;i++)
    {
        pointValue.push(bars[index][i]());
    }
    return JSON.stringify({
        "point":pointValue,
        "AxisX":AxisX[index],
        "AxisY":AxisY[index],
        "zeroX":zeroX[index],
        "zeroY":zeroY[index],
        "maxX":maxX[index],
        "maxY":maxY[index],
        "precisionValue":precisionValue[index]
    });
}

function chart_roundToStep(number,step)
{
    var lowest = step * Math.floor(number/step);
    var highest = step * Math.ceil(number/step);
    if(number-lowest > highest-number)return highest;
    return lowest;
}

function chart_parse_orderedDict(orderedDictStr)
{
    return orderedDictStr.substring(orderedDictStr.indexOf("chart")+9,orderedDictStr.lastIndexOf('}')+1);
}
