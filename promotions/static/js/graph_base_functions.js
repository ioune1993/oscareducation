round = function(value) {
    return Number(value.toFixed(0));
}

var getMouseCoords = function(e, i) {
    var cPos = brd.getCoordsTopLeftCorner(e, i),
    absPos = JXG.getPosition(e, i),
    dx = absPos[0]-cPos[0],
    dy = absPos[1]-cPos[1];

    return new JXG.Coords(JXG.COORDS_BY_SCREEN, [dx, dy], brd);
}

down = function(e) {
    var canCreate = true, i, coords, el;

    if (e[JXG.touchProperty]) {
        // index of the finger that is used to extract the coordinates
        i = 0;
    }
    coords = getMouseCoords(e, i);

    for (el in brd.objects) {
        if(JXG.isPoint(brd.objects[el]) && brd.objects[el].hasPoint(coords.scrCoords[1], coords.scrCoords[2])) {
            canCreate = false;
            break;
        }
    }

    if (canCreate && points.length < 2) {
        var point = brd.create('point', [round(coords.usrCoords[1]), round(coords.usrCoords[2])]);
        points.push(point);

        if (points.length == 2) {
            brd.create('line', [points[0], points[1]])
        }
    }
}

// var brd = JXG.JSXGraph.initBoard('box', {boundingbox: [-5, 5, 5, -5], axis:true});

// brd.create("line", [[1, 1], [2, 3]], {strokeColor: 'green'})
// brd.create("line", [[-3, 4], [4, 3]], {strokeColor: 'red', straightFirst: false})
// brd.create("line", [[-1, 1], [2, -3]], {strokeColor: 'gold', straightFirst: false, straightLast: false})

// var lin = brd.create('line', ["A", "B"])

// brd.on('down', down);

function Graph(html_id) {
    var that = this;

    this.brd = JXG.JSXGraph.initBoard(html_id, {boundingbox: [-5, 5, 5, -5], axis: true});
    this.brd.options.point.showInfobox = false;
    this.points = [];

    this.addPoint = function(X, Y) {
        that.points.push(that.brd.create('point', [X, Y]));
    }

    this.brd.on('move', function(){
        for (var i = 0; i < that.points.length; ++i) {
            var point = that.points[i];
            point.moveTo([round(point.X()), round(point.Y())]);
            document.getElementById(html_id + "-" + "point" + "-" + i + "-X").value = round(point.X());
            document.getElementById(html_id + "-" + "point" + "-" + i + "-Y").value = round(point.Y());
        }
    });
}
