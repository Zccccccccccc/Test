//创建socket io连接
var socket = io.connect(location.protocol +'//' + document.domain + ':' +location.port);
socket.emit('connect_event',{ data: document.domain });

//以下是socketio通信
//test

var posData = []
var nagData = []

socket.on('test', function (msg) {

    onAlertMsg("aaaaaaaaaaaaaaaaaaaaaaa")
});


//切换服务器A通道开关，消息机制
function setControlBoardSwitchAPath() {
    socket.emit('F2S_ControlBoardSwitchAPath')
}



//获取模式
socket.on('S2F_ControlBoardMode', function (msg) {
    var a = msg.A
    onChangeControlBoardMode(a)
})

//获取功率
socket.on('S2F_ControlBoardPower', function (msg) {
    var power = msg.Power
    onChangeControlBoardPower(power)
})

//获取主控板旋钮信息
socket.on('S2F_ControlBoardSpin', function (msg) {
    onChangeControlBoardSpin(msg)
})

//设置旋钮信息
function setSetControlBoardSpin(path, gain, frequency, power) {

    socket.emit('F2S_SetControlBoardSpin', {
        "Gain": gain,
        "Frequency": frequency,
        "Power": power
     })
}

//以下是告警信息
//通知栅压板告警
socket.on('S2F_GateBoardWarning', function (msg) {

    var gateBoardWarning = msg.GateBoardWarning
    if (gateBoardWarning == 1) {
        onAlertMsg("检测到栅压板异常")
    }
})

//温度告警信息
socket.on('S2F_TempBoardWarning', function (msg) {

    var tempBoardWarning = msg.TempBoardWarning
    if (tempBoardWarning == 1) {
        onAlertMsg("检测到温度板异常")
    }
})

//风扇告警信息
socket.on('FanBoardWarning', function (msg) {

    var fanBoardWarning = msg.FanBoardWarning
    if (fanBoardWarning == 1) {
        onAlertMsg("检测到温度板异常")
    }

})

//主控告警信息
socket.on('S2F_MainBoardWarning', function (msg) {

    var mainBoardWarning = msg.MainBoardWarning
    if (mainBoardWarning == 1) {
        onAlertMsg("检测到主控板异常")
    }

})

//过欠压检测板A信息
socket.on('S2F_VolBoardAWarning', function (msg) {

    var paths = msg.VolBoardAWarning
    var alertMsg = ""
    for (var i = 0; i < paths.length; i++) {
        var path = paths[i];
        alertMsg = alertMsg + "检测到过欠压A板第" + path + "路异常!"
    }
    onAlertMsg(alertMsg)
})

//偏置板A信息  
socket.on('S2F_OffsetBoardAWarning', function (msg) {

    var paths = msg.OffsetBoardAWarning
    var alertMsg = ""
    for (var i = 0; i < paths.length; i++) {
        var path = paths[i]
        alertMsg = alertMsg + "检测到偏置A板第" + path + "路异常!"
    }
    onAlertMsg(alertMsg)
})


//板块失联告警
var boardList = ["正常", "主控板", "告警板", "温度检测板1", "温度检测板2", "栅压板",
    "过欠压板1", "过欠压板2", "过欠压板3", "过欠压板4", "过欠压板5", "过欠压板6",
    "风扇检测板1", "风扇检测板2", "风扇检测板3"]
socket.on('S2F_BoardDisconnectWarning', function (msg) {
    var boardTag = msg.BoardTag
    var alertMsg = "检测到" + boardList[boardTag] + "断开连接";
    onAlertMsg(alertMsg)
})


//风扇数组状态信息
socket.on('S2F_FansStatus', function (msg) {
    var fansStatus = msg.FansStatus
    var tag = msg.Tag
    onChangeFansStatusByPath(tag, fansStatus)
})

//温度数组状态信息
socket.on('S2F_TemperatureStatus', function (msg) {
    var temperatureStatus = msg.TemperatureStatus
    onChangeTemperatureStatusByPath(temperatureStatus)
});

//栅压数组状态信息 
socket.on('S2F_GateVoltageStatus', function (msg) {
    var gateVoltageTag = msg.GateVoltageTag
    var gateVoltageStatus = msg.GateVoltageStatus
    onChangeGateVoltageByTag(gateVoltageTag, gateVoltageStatus)
})

//设置栅压（调试使用）
function setGateVoltageStatus(path, gateVoltage) {
    socket.emit('F2S_GateVoltageStatus', { GateVoltagePath: path, GateVoltage: gateVoltage})
}

//电流状态信息,500W,13+13+13+13+13+5 = 70路电流，最后一路为驱动电流
socket.on('S2F_ElectricityStatus', function (msg) {
    var electricityStatus = msg.ElectricityStatus
    var electricityID = msg.ElectricityID
    onChangeCurrentElectByID(electricityID, electricityStatus)
})

//电流状态信息 
socket.on('S2F_FirstElectricityStatus', function (msg) {
    var electricityStatu = msg.ElectricityStatus
    var electricityID = msg.ElectricityID
    onChangeFirstCurrentElectByID(electricityID, electricityStatu)
})


