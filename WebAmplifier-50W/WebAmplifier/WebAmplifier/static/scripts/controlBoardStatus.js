//1000W当前功能按钮为true，2000W为false
//功能按钮
function onChangeControlBoardAByFront() {
    setControlBoardSwitchAPath()
}

function onChangeControlBoardMode(a) {
    //未加载完js，不修改前端
    if (document.readyState != "complete") {
        return
    }
    if (a == 0) {
        $('#ControlBoardA').bootstrapSwitch('setState', false)
    } else {
        $('#ControlBoardA').bootstrapSwitch('setState', true)
    }
}

$(document).on('click', '.number-spinner button', function () {
    var btn = $(this),
        oldValue = btn.closest('.number-spinner').find('input').val().trim(),
        newVal = 0;

    var sendDiv = btn.closest('.number-spinner').find('input')[0]
    if (sendDiv.id == 'inputAPathFrequency') {
        if (btn.attr('data-dir') == 'up') {
            if (oldValue < 13.5) {
                newVal = parseFloat(oldValue) + 0.1;
                newVal = newVal.toFixed(1)
            } else {
                newVal = 13.5;
            }
        } else {
            if (oldValue > 10.5) {
                newVal = parseFloat(oldValue) - 0.1;
                newVal = newVal.toFixed(1)
            } else {
                newVal = 10.5;
            }
        }
    } else if (sendDiv.id == 'inputAPathGain') {
        if (btn.attr('data-dir') == 'up') {
            if (oldValue < 25) {
                newVal = parseInt(oldValue) + 1;
            } else {
                newVal = 25;
            }
        } else {
            if (oldValue > 0) {
                newVal = parseInt(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
    } else if (sendDiv.id == 'inputAPathPower') {
        if (btn.attr('data-dir') == 'up') {
            if (oldValue < 63) {
                newVal = parseInt(oldValue) + 1;
            } else {
                newVal = 63;
            }
        } else {
            if (oldValue > 47) {
                newVal = parseInt(oldValue) - 1;
            } else {
                newVal = 47;
            }
        }
    } 

    btn.closest('.number-spinner').find('input').val(newVal);


    var sendId = -1;
    if (sendDiv.id == 'inputAPathGain' || sendDiv.id == 'inputAPathFrequency' || sendDiv.id == 'inputAPathPower') {
        //A增益A频率A功率
        var gain = $("#inputAPathGain").val()
        var frequency = $("#inputAPathFrequency").val()
        var power = $("#inputAPathPower").val()

        setSetControlBoardSpin(0, gain, frequency, power)
    }
});

function onChangeControlBoardSpin(msg) {
    //未加载完js，不修改前端
    if (document.readyState != "complete") {
        return
    }

    $("#inputAPathGain").val(msg.Gain);
    $("#inputAPathFrequency").val(msg.Frequency);
    $("#inputAPathPower").val(msg.Power);

}

var plotPos, plotNag;
//合并功率
function createPlot(PlotName, data) {

    var plot = $.plot("#" + PlotName, [data], {
        series: {
            label: "Data",
            lines: {
                show: true,
                lineWidth: 1,
                fill: 0.25,
            },
            color: 'rgba(255,255,255,0.2)',
            shadowSize: 0,
        },
        yaxis: {
            min: 0,
            max: 1000,
            tickColor: 'rgba(255,255,255,0.15)',
            font: {
                lineHeight: 13,
                style: "normal",
                color: "rgba(255,255,255,0.8)",
            },
            shadowSize: 0,

        },
        xaxis: {
            tickColor: 'rgba(255,255,255,0.15)',
            show: true,
            font: {
                lineHeight: 13,
                style: "normal",
                color: "rgba(255,255,255,0.8)",
            },
            shadowSize: 0,
            min: 0,
            max: 250
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
    $("#" + PlotName).bind("plothover", function (event, pos, item) {
        if (item) {
            var x = item.datapoint[0].toFixed(2),
                y = item.datapoint[1].toFixed(2);
            $("#dynamic-chart-tooltip").html(item.series.label + " of " + x + " = " + y).css({ top: item.pageY + 5, left: item.pageX + 5 }).fadeIn(200);
        }
        else {
            $("#dynamic-chart-tooltip").hide();
        }
    });

    $("<div id='dynamic-chart-tooltip' class='chart-tooltip'></div>").appendTo("body");

    return plot
}


//功率显示,显示AB路功率
function onChangeControlBoardPower(powers) {
    //未加载完js，不修改前端
    if (document.readyState != "complete") {
        return
    }
    //这是修改AB路功率

    var divName = "#ControlBoardPower1"
    $(divName).closest('.pie-chart-tiny').data('easyPieChart').update(powers[0] / 10);
    var aStr = "#aControlBoardPower1"
    if (bIsShowingW) {
        $(aStr).text(~~powers[0])
    } else {
        $(aStr).text(~~convertWTodBm(powers[0]))
    }



    //修改合并功率
    if (posData.length > 250) {
        posData = posData.slice(1);
    }
    if (nagData.length > 250) {
        nagData = nagData.slice(1);
    }
    posData.push(powers[1])
    nagData.push(powers[2])

    var posRes = []
    var nagRes = []
    for (var i = 0; i < posData.length; ++i) {
        posRes.push([i, posData[i]])
    }
    for (var i = 0; i < nagData.length; ++i) {
        nagRes.push([i, nagData[i]])
    }

    if (plotPos != null) {
        plotPos.setData([posRes])
        plotPos.draw()
    }
    if (plotNag != null) {
        plotNag.setData([nagRes])
        plotNag.draw()
    }
}

//动态修改栅压表
function onChangeGateVoltageByTag(tag, values) {
    //未加载完js，不修改前端
    if (document.readyState != "complete") {
        return
    }

    var divName = "divGateVoltage"

    if (tag == 0) {
        for (var i = 1; i < 71; i++) {
            var aValue = document.getElementById("a" + divName + "-" + i)
            aValue.innerText = "栅压" + values[i - 1] + "mV"

            var divProcessBar = document.getElementById("processBar" + divName + "-" + i);
            divProcessBar.setAttribute("style", "width:" + values[i - 1] / 50 + "%")
            divProcessBar.setAttribute("aria-valuenow", values[i - 1] / 50)
        }
    } else {
        for (var i = 71; i < 140; i++) {
            var aValue = document.getElementById("a" + divName + "-" + i)
            aValue.innerText = "栅压" + values[i - 71] + "mV"

            var divProcessBar = document.getElementById("processBar" + divName + "-" + i);
            divProcessBar.setAttribute("style", "width:" + values[i - 71] / 50 + "%")
            divProcessBar.setAttribute("aria-valuenow", values[i - 71] / 50)
        }
    }
}

//动态创建栅压表
function createDivGateVoltage(idName) {

    for (var i = 0; i < 69; i++) {

        var mainDiv = document.getElementById("gateVoltageAndCurrent" + (Math.floor(i / 10) + 1))

        var div = document.createElement('div')
        var value = 0
        div.innerHTML =
            "<div class='row'>\
                <div class='col-md-4'>\
                    <div class='m-b-10'>\
                        <a>第" + (i * 2 + 1) + "路:</a><a id=a" + idName + "-" + (i * 2 + 1) + ">栅压" + value + "mV</a>\
                        <div class='btn-group' style='float: right;'>\
                            <button type='button' class='btn btn-sm' onclick='onClickGateVoltageUp(this.parentNode.parentNode)'>↑</button>\
                            <button type='button' class='btn btn-sm' onclick='onClickGateVoltageDown(this.parentNode.parentNode)'>↓</button>\
                        </div>\
                        <div class='progress'>\
                            <div id='processBar" + idName + "-" + (i * 2 + 1) + "' class='progress-bar progress-bar-success' role='progressbar' aria-valuenow='" + value / 50 + "' aria-valuemin='0' aria-valuemax='5000' style='width: " + value / 50 + "%'></div>\
                        </div>\
                    </div>\
                </div>\
                <div class='col-md-4'>\
                    <div class='m-b-10'>\
                        <a>第" + (i * 2 + 2) + "路:</a><a id=a" + idName + "-" + (i * 2 + 2) + ">栅压" + value + "mV</a>\
                        <div class='btn-group' style='float: right;'>\
                            <button type='button' class='btn btn-sm' onclick='onClickGateVoltageUp(this.parentNode.parentNode)'>↑</button>\
                            <button type='button' class='btn btn-sm' onclick='onClickGateVoltageDown(this.parentNode.parentNode)'>↓</button>\
                        </div>\
                        <div class='progress'>\
                            <div id='processBar" + idName + "-" + (i * 2 + 2) + "' class='progress-bar progress-bar-success' role='progressbar' aria-valuenow='" + value / 50 + "' aria-valuemin='0' aria-valuemax='3000' style='width: " + value / 50 + "%'></div>\
                        </div>\
                    </div>\
                </div>\
                <div class='col-md-4'>\
                    <div class='m-b-10'>\
                        <a>第" + (i + 1) + "路:</a><a id=aCurrent" + idName + "-" + (i + 1) + ">电流" + value + "mA</a>\
                        <div class='progress progress-striped active'>\
                            <div id='processBarCurrent" + idName + "-" + (i + 1) + "' class='progress-bar' role='progressbar' aria-valuenow='" + value / 50 + "' aria-valuemin='0' aria-valuemax='3000' style='width: " + value / 50 + "%'></div>\
                        </div>\
                    </div>\
                </div>\
            </div>"

        mainDiv.appendChild(div)
    }

    {
        var i = 69

        var mainDiv = document.getElementById("gateVoltageAndCurrent8")
        var div = document.createElement('div')
        var value = 0
        div.innerHTML =
            "<div class='row'>\
                <h5>驱动栅压</h5>\
                <div class='col-md-6'>\
                    <div class='m-b-10'>\
                        <a>驱动栅压第" + (i * 2 + 1) + "路:</a><a id=a" + idName + "-" + (i * 2 + 1) + ">栅压" + value + "mV</a>\
                        <div class='btn-group' style='float: right;'>\
                            <button type='button' class='btn btn-sm' onclick='onClickGateVoltageUp(this.parentNode.parentNode)'>↑</button>\
                            <button type='button' class='btn btn-sm' onclick='onClickGateVoltageDown(this.parentNode.parentNode)'>↓</button>\
                        </div>\
                        <div class='progress'>\
                            <div id='processBar" + idName + "-" + (i * 2 + 1) + "' class='progress-bar progress-bar-success' role='progressbar' aria-valuenow='" + value / 50 + "' aria-valuemin='0' aria-valuemax='5000' style='width: " + value / 50 + "%'></div>\
                        </div>\
                    </div>\
                </div>\
                <div class='col-md-12'>\
                    <div class='m-b-10'>\
                        <a>驱动电流第" + (i + 1) + "路:</a><a id=aCurrent" + idName + "-" + (i + 1) + ">电流" + value + "mA</a>\
                        <div class='progress progress-striped active'>\
                            <div id='processBarCurrent" + idName + "-" + (i + 1) + "' class='progress-bar' role='progressbar' aria-valuenow='" + value / 50 + "' aria-valuemin='0' aria-valuemax='3000' style='width: " + value / 50 + "%'></div>\
                        </div>\
                    </div>\
                </div>\
            </div>"

        mainDiv.appendChild(div)
    }

}

function onClickGateVoltageUp(div) {
    var step = parseInt($('#inputGateVoltageStep').val())

    var divValue = div.children[1]
    var path = divValue.id.split("-")[1]   //这是第几路
    path = path - 1
    var value = parseInt(divValue.innerText.replace("栅压", "").replace("mV", "")) //将栅压mv都删掉
    value = value + step
    divValue.innerText = "栅压" + value + "mV"
    setGateVoltageStatus(path, value)
}

function onClickGateVoltageDown(div) {
    var step = parseInt($('#inputGateVoltageStep').val())
    var divValue = div.children[1]
    var path = divValue.id.split("-")[1]   //这是第几路
    path = path - 1
    var value = parseInt(divValue.innerText.replace("栅压", "").replace("mV", "")) //将栅压mv都删掉
    value = value - step
    divValue.innerText = "栅压" + value + "mV"
    setGateVoltageStatus(path, value)
}

//显示
function onAlertMsg(str) {
    var alertDiv = document.getElementById('alertDiv')
    alertDiv.innerHTML = "<h3><span class='label label-danger'>检测到告警</span></h3>\
                            <button class='btn btn-sm' data-toggle='modal' href='#modalWarning'>点击查看告警</button>"

    var warningListDiv = document.getElementById('warnigMessageList')
    var msgDiv = document.createElement('div')
    msgDiv.className = "alert alert-danger alert-icon"
    msgDiv.innerHTML = str + "\
        <i class='icon'>\&#61907;</i ><a href='#' class='close' data-dismiss='alert'>&times;</a>"
    warningListDiv.appendChild(msgDiv)
}

function onClearAlertMsg() {
    var alertDiv = document.getElementById('alertDiv')
    alertDiv.innerHTML = "<h3><span class='label label-success'>状态正常</span></h3>"
    document.getElementById('warnigMessageList').innerHTML = ""
}



var bIsShowingW = true

function convertToW() {
    var units = document.getElementsByName("aControlBoardPowerUnit")
    for (var i = 0; i < units.length; i++) {
        units[i].innerText = "W"
    }
    bIsShowingW = true
}

function convertTodBm() {
    var units = document.getElementsByName("aControlBoardPowerUnit")
    for (var i = 0; i < units.length; i++) {
        units[i].innerText = "dBm"
    }
    bIsShowingW = false
}


//上传栅压表
function onUploadCurrentGateVotage() {
    var selectedFile = document.getElementById("uploadVotageFile").files[0];
    var reader = new FileReader()
    reader.readAsText(selectedFile);

    reader.onload = function (oFREvent) {//读取完毕从中取值
        var pointsTxt = oFREvent.target.result
        //分10路下发
        var splitList = pointsTxt.split("\r\n")
        if (splitList.length < 7) {
            alert("小于7路")
            return
        }

        //将前100路拼接，并下发
        var firstList = []
        for (var i = 0; i < 5; i++) {
            var tempList = splitList[i].split(":")[1].split(",")
            for (var j = 0; j < 20; j++) {

                if (tempList[j] == undefined) {
                    break;
                }

                firstList.push(tempList[j])
            }
        }

        var secondList = []
        for (var i = 5; i < 7; i++) {
            var tempList = splitList[i].split(":")[1].split(",")
            for (var j = 0; j < 20; j++) {

                //已拼接完毕
                if (tempList[j] == undefined) {
                    break;
                }
                secondList.push(tempList[j])
            }
        }

        socket.emit('F2S_ContinueGateVoltageStatus', {
            "Tag": 0,
            "List": firstList
        })

        socket.emit('F2S_ContinueGateVoltageStatus', {
            "Tag": 100,
            "List": secondList
        })

    }
}
