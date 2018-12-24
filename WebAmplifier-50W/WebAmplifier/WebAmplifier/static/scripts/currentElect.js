
window.onload = function () {


    var values = []
    //栅压
    createDivGateVoltage("divGateVoltage")
    //for (var i = 0; i < 70; i++) {
    //    values[i] = Math.floor(i)
    //}
    //onChangeGateVoltageByTag(0, values)
    //onChangeGateVoltageByTag(1, values)


    //正向功率，反向功率
    //初始化250个0点
    while (posData.length < 250) {
        posData.push(0);
        nagData.push(0);
    }
    var res = [];
    for (var i = 0; i < posData.length; ++i) {
        res.push([i, 0])
    }
    plotPos = createPlot("dynamic-chartPos", res)
    plotPos.draw()
    plotNag = createPlot("dynamic-chartNag", res)
    plotNag.draw()

    heatMapA = createTemperature("heatmapContainerA")
    heatMapA.generate()

    //创建电流板
    for (var i = 1; i <= 5 * 13 + 5; ++i) {
        currentElectBoardA.push([i, 0])
    }
    currentChartA = createCurrentChart("divACurrentBoard", currentElectBoardA)
    currentChartA.draw()

    //for (var i = 1; i < 6; i++) {
    //    var valuesCur = []
    //    for (var j = 0; j < 13; j++) {
    //        valuesCur[j] = j * 100
    //    }
    //    onChangeCurrentElectByID(i, valuesCur)
    //}
    //{
    //    var valuesCur = []
    //    for (var j = 0; j < 5; j++) {
    //        valuesCur[j] = j * 100
    //    }
    //    onChangeCurrentElectByID(6, valuesCur)
    //}


    var temperatures = []
    for (var i = 0; i < 8; i++) {
        temperatures[i] = 50
    }
    heatMapA.update(temperatures)

    onCreateFansTableStatus("fansTable")

}


var currentElectBoardA = []

//动态修改电流表，8路*13路电流,500W,13+13+13+13+13+5 = 70路电流，最后一路为驱动电流
function onChangeCurrentElectByID(electricityID, currentElectStatus) {

    //未加载完js，不修改前端
    if (document.readyState != "complete") {
        return
    }



    if (electricityID <= 5) {
        for (var i = 0; i < 13; i++) {
            var index = (electricityID - 1) * 13 + i
            currentElectBoardA[index] = [index + 1, currentElectStatus[i]]
        }
        currentChartA.setData([currentElectBoardA])
        currentChartA.draw()

        //修改电流板A的总共数据
        var totalValue = 0
        for (var i = 0; i < currentElectBoardA.length; i++) {
            totalValue = totalValue + currentElectBoardA[i][1]
        }
        $('#currentBoradATotal').text(totalValue / 1000 + "A")

    } else if (electricityID == 6) {
        for (var i = 0; i < 5; i++) {
            var index = (electricityID - 1) * 13 + i
            currentElectBoardA[index] = [index + 1, currentElectStatus[i]]
        }
        currentChartA.setData([currentElectBoardA])
        currentChartA.draw()

        //修改电流板A的总共数据
        var totalValue = 0
        for (var i = 0; i < currentElectBoardA.length; i++) {
            totalValue = totalValue + currentElectBoardA[i][1]
        }
        $('#currentBoradATotal').text(totalValue / 1000 + "A")
    }

    //修改栅压板上的电流表
    if (electricityID <= 5) {
        for (var i = 0; i < currentElectStatus.length; i++) {
            var index = (electricityID - 1) * 13 + i + 1
            var aValue = document.getElementById("aCurrentdivGateVoltage-" + index)
            aValue.innerText = "电流" + currentElectStatus[i] + "mA"

            var divProcessBar = document.getElementById("processBarCurrentdivGateVoltage-" + index);
            divProcessBar.setAttribute("style", "width:" + currentElectStatus[i] / 50 + "%")
            divProcessBar.setAttribute("aria-valuenow", currentElectStatus[i] / 50)
        }
    } else if (electricityID == 6) {

        for (var i = 0; i < 5; i++) {
            var index = (electricityID - 1) * 13 + i + 1
            var aValue = document.getElementById("aCurrentdivGateVoltage-" + index)
            aValue.innerText = "电流" + currentElectStatus[i] + "mA"

            var divProcessBar = document.getElementById("processBarCurrentdivGateVoltage-" + index);
            divProcessBar.setAttribute("style", "width:" + currentElectStatus[i] / 50 + "%")
            divProcessBar.setAttribute("aria-valuenow", currentElectStatus[i] / 50)
        }

        document.getElementById("aCurrentdivGateVoltage-70").innerText = "电流" + currentElectStatus[4] + "mA"
        document.getElementById("processBarCurrentdivGateVoltage-70").setAttribute("style", "width:" + currentElectStatus[4] / 50 + "%")
        document.getElementById("processBarCurrentdivGateVoltage-70").setAttribute("aria-valuenow", currentElectStatus[4] / 50)
    } 
}

//动态修改电流表，一级驱动电流
function onChangeFirstCurrentElectByID(electricityID, currentElectStatu) {
    //未加载完js，不修改前端
    if (document.readyState != "complete") {
        return
    }


    if (electricityID == 0) {

        currentElectBoardA[53] = [53, currentElectStatu]
        currentChartA.setData([currentElectBoardA])
        currentChartA.draw()

        document.getElementById("aCurrentdivGateVoltage-105").innerText = "电流" + currentElectStatu + "mA"
        document.getElementById("processBarCurrentdivGateVoltage-105").setAttribute("style", "width:" + currentElectStatu / 50 + "%")
        document.getElementById("processBarCurrentdivGateVoltage-105").setAttribute("aria-valuenow", currentElectStatu / 50)


        var totalValue = 0
        for (var i = 0; i < currentElectBoardA.length; i++) {
            totalValue = totalValue + currentElectBoardA[i][1]
        }
        $('#currentBoradATotal').text(totalValue + "mA")

    } else if (electricityID == 1) {
        currentElectBoardB[53] = [53, currentElectStatu]
        currentChartB.setData([currentElectBoardB])
        currentChartB.draw()

        document.getElementById("aCurrentdivGateVoltage-106").innerText = "电流" + currentElectStatu + "mA"
        document.getElementById("processBarCurrentdivGateVoltage-106").setAttribute("style", "width:" + currentElectStatu / 50 + "%")
        document.getElementById("processBarCurrentdivGateVoltage-106").setAttribute("aria-valuenow", currentElectStatu / 50)

        var totalValue = 0
        for (var i = 0; i < currentElectBoardA.length; i++) {
            totalValue = totalValue + currentElectBoardB[i][1]
        }
        $('#currentBoradBTotal').text(totalValue + "mA")
    }

}

//动态修改电流表，6路*13路电流
function onChangeFirstCurrentElectByID(currentElectStatu) {
    //未加载完js，不修改前端
    if (document.readyState != "complete") {
        return
    }


    currentElectBoardA[52] = [52, currentElectStatu]
    currentChartA.setData([currentElectBoardA])
    currentChartA.draw()

}

//动态创建8*13路电流板
var currentChartA

//创建电流表
function createCurrentChart(PlotName, data) {

    var plot = $.plot("#" + PlotName, [data], {
        series: {
            lines: {
                show: true,
                lineWidth: 1,
                fill: 0.25,
            },

            color: 'rgba(255,255,255,0.7)',
            shadowSize: 0,
            points: {
                show: true,
            }
        },

        yaxis: {
            min: 0,
            max: 6000,
            tickColor: 'rgba(255,255,255,0.15)',
            tickDecimals: 0,
            font: {
                lineHeight: 13,
                style: "normal",
                color: "rgba(255,255,255,0.8)",
            },
            shadowSize: 0,
        },
        xaxis: {
            tickColor: 'rgba(255,255,255,0)',
            tickDecimals: 0,
            font: {
                lineHeight: 13,
                style: "normal",
                color: "rgba(255,255,255,0.8)",
            }
        },
        grid: {
            borderWidth: 1,
            borderColor: 'rgba(255,255,255,0.25)',
            labelMargin: 10,
            hoverable: true,
            clickable: true,
            mouseActiveRadius: 6,
        },
        legend: {
            show: false
        }
    });

    $('#' + PlotName).bind("plothover", function (event, pos, item) {
        if (item) {
            var x = item.datapoint[0].toFixed(2),
                y = item.datapoint[1].toFixed(2);
            $("#linechart-tooltip").html("电流" + ~~x + "路= " + y + "mA").css({ top: item.pageY + 5, left: item.pageX + 5 }).fadeIn(200);
        }
        else {
            $("#linechart-tooltip").hide();
        }
    });
    $("<div id='linechart-tooltip' class='chart-tooltip'></div>").appendTo("body");

    return plot
}

function onSaveCurrentList() {
    var time = new Date()
    var timeNow = time.getFullYear() + "-" + time.getMonth() + "-" + time.getDate() + "-" + time.getHours() + "-" + time.getMinutes() + "-" + time.getSeconds() + "-" + time.getMilliseconds()
    timeNow = timeNow + ".txt"
    content = currentElectBoardA + "\r\n" + currentElectBoardB
    download(timeNow, content)
}

function download(filename, content, contentType) {
    if (!contentType) contentType = 'application/octet-stream';
    var a = document.createElement('a');
    var blob = new Blob([content], { 'type': contentType });
    a.href = window.URL.createObjectURL(blob);
    a.download = filename;
    a.click();
}
