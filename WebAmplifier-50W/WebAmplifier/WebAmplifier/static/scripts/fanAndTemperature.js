var heatMapA, heatMapB

function createTemperature(idName) {
    /*  legend code */
    // we want to display the gradient, so we have to draw it
    var legendCanvas = document.createElement('canvas');
    legendCanvas.width = 100;
    legendCanvas.height = 10;


    // create a heatmap instance
    var heatmap = h337.create({
        container: document.getElementById(idName),
        maxOpacity: .5,
        radius: 55,
        blur: .75,
        // update the legend whenever there's an extrema change
        //onExtremaChange: function onExtremaChange(data) {
        //    updateLegend(data);
        //}
    });


    var height = document.getElementById(idName).offsetHeight
    var width = document.getElementById(idName).offsetWidth

    //定死的17个温度检测点
    var point2Dlist = [
        [605, 336],
        [452, 336],
        [605, 250],
        [452, 250],

        [207, 336],
        [55, 336],
        [207, 250],
        [55, 250],

        [605, 133],
        [452, 133],
        [605, 47],
        [452, 47],

        [207, 133],
        [55, 133],
        [207, 47],
        [55, 47],

        [width / 2, height / 2]
    ]

    // generate 1000 datapoints
    heatmap.generate = function () {
        var t = [];
        for (var i = 0; i < 17; i++) {
            t.push({ x: point2Dlist[i][0], y: point2Dlist[i][1], value: 0, radius: 40 })
        }
        heatmap.setData({
            min: 0,
            max: 100,
            data: t
        });
    };

    heatmap.update = function (temperatures) {
        var t = [];
        for (var i = 0; i < 17; i++) {
            t.push({ x: point2Dlist[i][0], y: point2Dlist[i][1], value: temperatures[i], radius: 40 })
        }
        heatmap.setData({
            min: 0,
            max: 100,
            data: t
        });
    }
    var heatmapTooltip = document.getElementById(idName + 'Tooltip')
    document.getElementById(idName).onmousedown = function (ev) {
        var value = heatmap.getValueAt({
            x: ev.layerX,
            y: ev.layerY
        })
        var transl = 'translate(' + (ev.layerX + 15) + 'px, ' + (ev.layerY + 15) + 'px)';
        heatmapTooltip.style.webkitTransform = transl;
        heatmapTooltip.innerHTML = value + "℃"
    }

    // initial generate
    return heatmap
    //// whenever a user clicks on the ContainerWrapper the data will be regenerated -> new max & min
    //document.getElementById('heatmapContainerWrapper').onclick = function () { generate(); };
}



//风扇状态显示
function onChangeFansStatusByPath(tag, fansStatus) {

    //未加载完js，不修改前端
    if (document.readyState != "complete") {
        return
    }

    console.log(tag, fansStatus)
    if (tag <= 1) {
        for (i = 0; i < 16; i++) {
            if (fansStatus[i] == 1) {
                document.getElementById("fansTdInner" + (tag * 16 + i)).innerHTML = "<span class='label label-success'>Normal</span>"
            } else if (fansStatus[i] == 0) {
                document.getElementById("fansTdInner" + (tag * 16 + i)).innerHTML = "<span class='label label-danger'>Error</span>"
            }
        } 
    } else if (tag == 2) {
        for (i = 0; i < 5; i++) {
            if (fansStatus[i] == 1) {
                document.getElementById("fansTdInner" + (tag * 16 + i)).innerHTML = "<span class='label label-success'>Normal</span>"
            } else if (fansStatus[i] == 0) {
                document.getElementById("fansTdInner" + (tag * 16 + i)).innerHTML = "<span class='label label-danger'>Error</span>"
            }
        } 
    }
    
}

function onCreateFansTableStatus(name) {
    var tableBody = document.getElementById(name) 
    for (var i = 0; i < 37; i = Number(i) + Number(3)) {
        var divTr = document.createElement("tr")
        divTr.innerHTML = "<tr>\
                                <td>" + "编号" + i +"</td>\
                                <td id=" + "fansTdInner" + i +"></td>\
                                <td>" + "编号" + (i + 1) + "</td>\
                                <td id=" + "fansTdInner" + (i + 1) +"></td>\
                                <td>" + "编号" + (i + 2) + "</td>\
                                <td id=" + "fansTdInner" + (i + 2) +"></td>\
                            </tr >"
        tableBody.appendChild(divTr)
    }
}


function onChangeTemperatureStatusByPath(temperatureStatus) {
    //未加载完js，不修改前端
    if (document.readyState != "complete") {
        return
    }

    var temperatures = []
    //更新A板温度
    for (var i = 0; i < 8; i++) {
        temperatures[i] = temperatureStatus[i] * 0.1
    }
    heatMapA.update(temperatures)
    //更新B板温度
    for (var i = 0; i < 8; i++) {
        temperatures[i] = temperatureStatus[i + 8] * 0.1
    }
    heatMapB.update(temperatures)
}