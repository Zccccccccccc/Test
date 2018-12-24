from WebAmplifier.data import staticData
PowerTable = [
    [10, 124, 238, 352, 466, 580, 694, 808, 922, 1036, 1150, 1264, 1378, 1492, 1606, 1720, 1834],
    [13, 127, 241, 355, 469, 583, 697, 811, 925, 1039, 1153, 1267, 1381, 1495, 1609, 1723, 1837],
    [16, 130, 244, 358, 472, 586, 700, 814, 928, 1042, 1156, 1270, 1384, 1498, 1612, 1726, 1840],
    [19, 133, 247, 361, 475, 589, 703, 817, 931, 1045, 1159, 1273, 1387, 1501, 1615, 1729, 1843],
    [22, 136, 250, 364, 478, 592, 706, 820, 934, 1048, 1162, 1276, 1390, 1504, 1618, 1732, 1846],
    [25, 139, 253, 367, 481, 595, 709, 823, 937, 1051, 1165, 1279, 1393, 1507, 1621, 1735, 1849],
    [28, 142, 256, 370, 484, 598, 712, 826, 940, 1054, 1168, 1282, 1396, 1510, 1624, 1738, 1852],
    [31, 145, 259, 373, 487, 601, 715, 829, 943, 1057, 1171, 1285, 1399, 1513, 1627, 1741, 1855],
    [34, 148, 262, 376, 490, 604, 718, 832, 946, 1060, 1174, 1288, 1402, 1516, 1630, 1744, 1858],
    [37, 151, 265, 379, 493, 607, 721, 835, 949, 1063, 1177, 1291, 1405, 1519, 1633, 1747, 1861],
    [40, 154, 268, 382, 496, 610, 724, 838, 952, 1066, 1180, 1294, 1408, 1522, 1636, 1750, 1864],
    [43, 157, 271, 385, 499, 613, 727, 841, 955, 1069, 1183, 1297, 1411, 1525, 1639, 1753, 1867],
    [46, 160, 274, 388, 502, 616, 730, 844, 958, 1072, 1186, 1300, 1414, 1528, 1642, 1756, 1870],
    [49, 163, 277, 391, 505, 619, 733, 847, 961, 1075, 1189, 1303, 1417, 1531, 1645, 1759, 1873],
    [52, 166, 280, 394, 508, 622, 736, 850, 964, 1078, 1192, 1306, 1420, 1534, 1648, 1762, 1876],
    [55, 169, 283, 397, 511, 625, 739, 853, 967, 1081, 1195, 1309, 1423, 1537, 1651, 1765, 1879],
    [58, 172, 286, 400, 514, 628, 742, 856, 970, 1084, 1198, 1312, 1426, 1540, 1654, 1768, 1882],
    [61, 175, 289, 403, 517, 631, 745, 859, 973, 1087, 1201, 1315, 1429, 1543, 1657, 1771, 1885],
    [64, 178, 292, 406, 520, 634, 748, 862, 976, 1090, 1204, 1318, 1432, 1546, 1660, 1774, 1888],
    [67, 181, 295, 409, 523, 637, 751, 865, 979, 1093, 1207, 1321, 1435, 1549, 1663, 1777, 1891],
    [70, 184, 298, 412, 526, 640, 754, 868, 982, 1096, 1210, 1324, 1438, 1552, 1666, 1780, 1894],
    [73, 187, 301, 415, 529, 643, 757, 871, 985, 1099, 1213, 1327, 1441, 1555, 1669, 1783, 1897],
    [76, 190, 304, 418, 532, 646, 760, 874, 988, 1102, 1216, 1330, 1444, 1558, 1672, 1786, 1900],
    [79, 193, 307, 421, 535, 649, 763, 877, 991, 1105, 1219, 1333, 1447, 1561, 1675, 1789, 1903],
    [82, 196, 310, 424, 538, 652, 766, 880, 994, 1108, 1222, 1336, 1450, 1564, 1678, 1792, 1906],
    [85, 199, 313, 427, 541, 655, 769, 883, 997, 1111, 1225, 1339, 1453, 1567, 1681, 1795, 1909],
    [88, 202, 316, 430, 544, 658, 772, 886, 1000, 1114, 1228, 1342, 1456, 1570, 1684, 1798, 1912],
    [91, 205, 319, 433, 547, 661, 775, 889, 1003, 1117, 1231, 1345, 1459, 1573, 1687, 1801, 1915],
    [94, 208, 322, 436, 550, 664, 778, 892, 1006, 1120, 1234, 1348, 1462, 1576, 1690, 1804, 1918],
    [97, 211, 325, 439, 553, 667, 781, 895, 1009, 1123, 1237, 1351, 1465, 1579, 1693, 1807, 1921],
    [100, 214, 328, 442, 556, 670, 784, 898, 1012, 1126, 1240, 1354, 1468, 1582, 1696, 1810, 1924]
]
FreqTable = [
    15,
    103,
    191,
    279,
    367,
    455,
    543,
    631,
    719,
    807,
    895,
    983,
    1071,
    1159,
    1247,
    1335,
    1423,
    1511,
    1599,
    1687,
    1775,
    1863,
    1951,
    2039,
    2127,
    2215,
    2303,
    2391,
    2479,
    2567,
    2655
]
GainTable = [
    21,
    121,
    221,
    321,
    421,
    521,
    621,
    721,
    821,
    921,
    1021,
    1121,
    1221,
    1321,
    1421,
    1521,
    1621,
    1721,
    1821,
    1921,
    2021,
    2121,
    2221,
    2321,
    2421,
    2521
]
freq_mini = 10.5
freq_max = 13.5
freq_progress = 0.1

power_mini = 47
power_max = 63
power_progress = 1

gain_mini = 0
gain_max = 25
gain_progress = 1

a_Pass=[0,1,2,6,7]
b_Pass=[3,4,5]

def __getArray_index(num,num_mini,progress):
    '''
    通过具体数值获得数值所在表的具体位置索引
    :param num:
    :param num_mini:
    :param progress:
    :return:
    '''
    x = float('%.1f' % (num - num_mini))
    y = (x/progress)
    y = int(round(y))
    return y
def __getNum_index(num,numArray):
    '''
    通过具体数值获得数值所在表的具体位置索引
    :param num:具体数值
    :param numArray:数组
    :return:数组索引
    '''
    index = 0
    for p in range(0,len(numArray)):
        if numArray[p] <= num:
            index = p
        else:
            break
    return index
def __index_to_value(index , miniNum , progress):
    '''
    将数组索引转换为前端显示的值
    :param index:
    :param miniNum:
    :param progress:
    :return:
    '''
    return (index * progress) + miniNum
def power_to_v(power, freq):
    '''
    功率转电压
    :param power: 前端显示电压值
    :param freq: 前端显示频率值
    :return: 功率电压值
    '''
    y = __getArray_index(freq,freq_mini,freq_progress)
    x = __getArray_index(power,power_mini,power_progress)
    return PowerTable[y][x]
def freq_to_v(freq):
    '''
    频率转电压
    :param freq: 前端显示频率值
    :return: 频率电压值
    '''
    index = __getArray_index(freq,freq_mini,freq_progress)
    return FreqTable[index]
def gain_to_v(gain):
    '''
    增益转电压
    :param gain: 前端显示增益值
    :return: 增益电压值
    '''
    index = __getArray_index(gain,gain_mini,gain_progress)
    return GainTable[index]
def v_to_power(power_v,freq_v):
    '''
    电压转工率
    :param power_v:功率电压值
    :param freq_v:频率电压值
    :return:前端显示功率值
    '''
    y = __getNum_index(freq_v, FreqTable)
    x = __getNum_index(power_v,PowerTable[y])
    return __index_to_value(x,power_mini,power_progress)
def v_to_freq(freq_v):
    '''
    电压转频率
    :param freq_v:频率电压值
    :return:前端显示频率值
    '''
    index = __getNum_index(freq_v, FreqTable)
    return __index_to_value(index,freq_mini,freq_progress)
def v_to_gain(gain_v):
    '''
    电压转增益
    :param gain_v:增益电压值
    :return:前端显示增益值
    '''
    index = __getNum_index(gain_v, GainTable)
    return __index_to_value(index, gain_mini, gain_progress)
def checkPower(power):
    pass
def __reckonMainPanlPower(power_v,n_pass):
    '''
    获取主控板功率
    :param power_v: 功率电压
    :param n_pass: 通道编号
    :return:具体功率值
    '''
    if len(staticData.CONFIG_CHKNOBINf) == 0 :
        return power_v
    frequency = staticData.CONFIG_CHKNOBINf[str(n_pass)]['Frequency']#根据ab通道获取频率
    if power_v == 0:#电压等于0返回0
        return 0
    freqIndex = __getNum_index(frequency,FreqTable)
    if PowerTable[freqIndex][0]>power_v:#实际电压小于最左边得值则返回0
        return 0.001
    power = v_to_power(power_v,frequency)#通过频率、功率电压获取大概功率
    #到最大值就不取平均值了，直接取最大值，不然越界
    if power >= power_max:
        return power_max
    standard_power_v = power_to_v(power,frequency)#获取标准功率电压值
    d_value = power_v - standard_power_v#用实际功率电压减去标准功率电压获取功率差值
    powerIndex = __getNum_index(standard_power_v,PowerTable[freqIndex])
    if d_value > 0:
        power_progress_v = PowerTable[freqIndex][powerIndex+1] - PowerTable[freqIndex][powerIndex]
        d_value = round(d_value/power_progress_v,3) #用功率电压差值除以功率进步值得到所占步进值得比列
        #print(d_value)
    else:
        d_value=0
    return power+d_value
def getMainControlPanlPower(powerArray):
    '''
    获取主控板功率信息
    :param powerArray: 功率电压数组
    :return: 前端显示功率数组
    '''
    #print("转换前：")
    #print(powerArray)
    for i in range(0,len(powerArray)):
        n_pass=-1
        if i in a_Pass:
            n_pass = 0
        elif i in b_Pass:
            n_pass = 1
        if n_pass > -1:
            powerArray[i] = __reckonMainPanlPower(powerArray[i],n_pass)
    #print("转换后：")
    #print(powerArray)
    return powerArray
if __name__ == '__main__':
    pass