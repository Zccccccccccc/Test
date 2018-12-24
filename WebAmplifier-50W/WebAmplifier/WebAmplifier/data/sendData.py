import math

from WebAmplifier.data.drainPanel import DrainPanel
from WebAmplifier.data.fanPanel import FanPanel
from WebAmplifier.data.gatePanel import GatePanel
from WebAmplifier.data.mainControlPanel import MainControlPanel
from WebAmplifier.data.tempPanel import TempPanel
from WebAmplifier.data.warningPanel import WarningPanel
from WebAmplifier.data.amplifierPanel import AmplifierPanel
#初始化各板子，保持单列模式

amplifierPanel = AmplifierPanel()
if __name__ == '__main__':
    print(amplifierPanel.getWorkInf(0x1))
    #print(fanPanel.getIP(10))
    #print(tempPanel.getTempInf(0))
    #print(tempPanel.getTempInf(1))
    #mainControlPanel.addPant()
    #mainControlPanel.addPant()
    #tempPanel.addPant()
    #drainPanel.addPant(7)
    #drainPanel.addPant(0)
    #print(fanPanel.getFanInf(0))
    #print(fanPanel.getFanSpeedInf(2))
    #drainPanel.setPant(1,10)
    #print(drainPanel.getPant(1))
    #print(mainControlPanel.getPant())
    #print(tempPanel.getPant())
    pass

