round = function(value) {
    return Number(value.toFixed(0));
}

var getMouseCoords = function(brd, e, i) {
    var cPos = brd.getCoordsTopLeftCorner(e, i),
    absPos = JXG.getPosition(e, i),
    dx = absPos[0]-cPos[0],
    dy = absPos[1]-cPos[1];

    return new JXG.Coords(JXG.COORDS_BY_SCREEN, [dx, dy], brd);
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
    this.to_add_entries = [];

    this.addAvailableGraphentry = function(kind) {
        that.to_add_entries.push(kind);
    }

    this.brd.on('move', function(){
        for (var i = 0; i < that.points.length; ++i) {
            var point = that.points[i];
            point.moveTo([round(point.X()), round(point.Y())]);
            document.getElementById(html_id + "-" + "point" + "-" + i + "-X").value = round(point.X());
            document.getElementById(html_id + "-" + "point" + "-" + i + "-Y").value = round(point.Y());
        }
    });

    this.brd.on('down', function(e) {
        var canCreate = true, i, coords, el;

        if (e[JXG.touchProperty]) {
            // index of the finger that is used to extract the coordinates
            i = 0;
        }
        coords = getMouseCoords(that.brd, e, i);

        for (el in that.brd.objects) {
            if(JXG.isPoint(that.brd.objects[el]) && that.brd.objects[el].hasPoint(coords.scrCoords[1], coords.scrCoords[2])) {
                canCreate = false;
                break;
            }
        }

        if (canCreate && that.to_add_entries.length > 0) {
            var point = that.brd.create(that.to_add_entries.shift(), [round(coords.usrCoords[1]), round(coords.usrCoords[2])]);
            that.points.push(point);
        }
    });
}
