# -*- coding: utf-8 -*-
from datetime import datetime
from copy import deepcopy
import sxtwl
from flask import render_template, request, Blueprint, jsonify
from flask_login import current_user, login_required
from databank.extensions import db
from databank.models import PersonData, Location

bazi_bp = Blueprint('bazi', __name__)

Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ShX = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
numCn = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏",
        "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
        "立冬", "小雪", "大雪"]
ymc = ["十一", "十二", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
rmc = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
       "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
       "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]
XiZ = ['摩羯', '水瓶', '双鱼', '白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手']
WeekCn = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]

ten_deities = {
    '甲': {'甲': '比肩', "乙": '劫财', "丙": '食神', "丁": '伤官', "戊": '偏财',
          "己": '正财', "庚": '七杀', "辛": '正官', "壬": '偏印', "癸": '正印', "子": '沐浴',
          "丑": '冠带', "寅": '建', "卯": '帝旺', "辰": '衰', "巳": '病', "午": '死',
          "未": '墓', "申": '绝', "酉": '胎', "戌": '养', "亥": '长生', '库': '未_',
          '本': '木', '克': '土', '被克': '金', '生我': '水', '生': '火', '合': '己', '冲': '庚'},
    '乙': {'甲': '劫财', "乙": '比肩', "丙": '伤官', "丁": '食神', "戊": '正财',
          "己": '偏财', "庚": '正官', "辛": '七杀', "壬": '正印', "癸": '偏印', "子": '病',
          "丑": '衰', "寅": '帝旺', "卯": '建', "辰": '冠带', "巳": '沐浴', "午": '长生',
          "未": '养', "申": '胎', "酉": '绝', "戌": '墓', "亥": '死', '库': '未_',
          '本': '木', '克': '土', '被克': '金', '生我': '水', '生': '火', '合': '庚', '冲': '辛'},
    '丙': {'丙': '比肩', "丁": '劫财', "戊": '食神', "己": '伤官', "庚": '偏财',
          "辛": '正财', "壬": '七杀', "癸": '正官', "甲": '偏印', "乙": '正印', "子": '胎',
          "丑": '养', "寅": '长生', "卯": '沐浴', "辰": '冠带', "巳": '建', "午": '帝旺',
          "未": '衰', "申": '病', "酉": '死', "戌": '墓', "亥": '绝', '库': '戌_',
          '本': '火', '克': '金', '被克': '水', '生我': '木', '生': '土', '合': '辛', '冲': '壬'},
    '丁': {'丙': '劫财', "丁": '比肩', "戊": '伤官', "己": '食神', "庚": '正财',
          "辛": '偏财', "壬": '正官', "癸": '七杀', "甲": '正印', "乙": '偏印', "子": '绝',
          "丑": '墓', "寅": '死', "卯": '病', "辰": '衰', "巳": '帝旺', "午": '建',
          "未": '冠带', "申": '沐浴', "酉": '长生', "戌": '养', "亥": '胎', '库': '戌_',
          '本': '火', '克': '金', '被克': '水', '生我': '木', '生': '土', '合': '壬', '冲': '癸'},
    '戊': {'戊': '比肩', "己": '劫财', "庚": '食神', "辛": '伤官', "壬": '偏财',
          "癸": '正财', "甲": '七杀', "乙": '正官', "丙": '偏印', "丁": '正印', "子": '胎',
          "丑": '养', "寅": '长生', "卯": '沐浴', "辰": '冠带', "巳": '建', "午": '帝旺',
          "未": '衰', "申": '病', "酉": '死', "戌": '墓', "亥": '绝', '库': '辰_',
          '本': '土', '克': '水', '被克': '木', '生我': '火', '生': '金', '合': '癸', '冲': ''},
    '己': {'戊': '劫财', "己": '比肩', "庚": '伤官', "辛": '食神', "壬": '正财',
          "癸": '偏财', "甲": '正官', "乙": '七杀', "丙": '正印', "丁": '偏印', "子": '绝',
          "丑": '墓', "寅": '死', "卯": '病', "辰": '衰', "巳": '帝旺', "午": '建',
          "未": '冠带', "申": '沐浴', "酉": '长生', "戌": '养', "亥": '胎', '库': '辰_',
          '本': '土', '克': '水', '被克': '木', '生我': '火', '生': '金', '合': '甲', '冲': ''},
    '庚': {'庚': '比肩', "辛": '劫财', "壬": '食神', "癸": '伤官', "甲": '偏财',
          "乙": '正财', "丙": '七杀', "丁": '正官', "戊": '偏印', "己": '正印', "子": '死',
          "丑": '墓', "寅": '绝', "卯": '胎', "辰": '养', "巳": '长生', "午": '沐浴',
          "未": '冠带', "申": '建', "酉": '帝旺', "戌": '衰', "亥": '病', '库': '丑_',
          '本': '金', '克': '木', '被克': '火', '生我': '土', '生': '水', '合': '乙', '冲': '甲'},
    '辛': {'庚': '劫财', "辛": '比肩', "壬": '伤官', "癸": '食神', "甲": '正财',
          "乙": '偏财', "丙": '正官', "丁": '七杀', "戊": '正印', "己": '偏印', "子": '长生',
          "丑": '养', "寅": '胎', "卯": '绝', "辰": '墓', "巳": '死', "午": '病',
          "未": '衰', "申": '帝旺', "酉": '建', "戌": '冠带', "亥": '沐浴', '库': '丑_',
          '本': '金', '克': '木', '被克': '火', '生我': '土', '生': '水', '合': '丙', '冲': '乙'},
    '壬': {'壬': '比肩', "癸": '劫财', "甲": '食神', "乙": '伤官', "丙": '偏财',
          "丁": '正财', "戊": '七杀', "己": '正官', "庚": '偏印', "辛": '正印', "子": '帝旺',
          "丑": '衰', "寅": '病', "卯": '死', "辰": '墓', "巳": '绝', "午": '胎',
          "未": '养', "申": '长生', "酉": '沐浴', "戌": '冠带', "亥": '建', '库': '辰_',
          '本': '水', '克': '火', '被克': '土', '生我': '金', '生': '木', '合': '丁', '冲': '丙'},
    '癸': {'壬': '劫财', "癸": '比肩', "甲": '伤官', "乙": '食神', "丙": '正财',
          "丁": '偏财', "戊": '正官', "己": '七杀', "庚": '正印', "辛": '偏印', "子": '建',
          "丑": '冠带', "寅": '沐浴', "卯": '长生', "辰": '养', "巳": '胎', "午": '绝',
          "未": '墓', "申": '死', "酉": '病', "戌": '衰', "亥": '帝旺', '库': '辰_',
          '本': '水', '克': '火', '被克': '土', '生我': '金', '生': '木', '合': '戊', '冲': '丁'},

}


@bazi_bp.route('/')
def index():
    chart_person = PersonData.query.filter_by(id=1).one()
    born_location = Location.query.filter_by(id=chart_person.location_id).one()
    born_time = chart_person.born_time
    born_time_str = born_time.strftime("%Y-%m-%d %H:%M:%S")
    gender = chart_person.gender  # 0 为女 1 为男
    gender_str = "女" if gender == 0 else "男"
    print(gender_str + " " + born_time_str + " " + born_location.province + " " + born_location.city)
    if born_time.hour == 23:
        day_add = 1
        hour_add = -23
    else:
        day_add = 0
        hour_add = 0
    day = sxtwl.fromSolar(born_time.year, born_time.month, born_time.day + day_add)
    yTG = day.getYearGZ()
    mTG = day.getMonthGZ()
    dTG = day.getDayGZ()
    hTG = day.getHourGZ(born_time.hour + hour_add)
    yg = Gan[yTG.tg]
    yz = Zhi[yTG.dz]
    mg = Gan[mTG.tg]
    mz = Zhi[mTG.dz]
    dg = Gan[dTG.tg]
    dz = Zhi[dTG.dz]
    hg = Gan[hTG.tg]
    hz = Zhi[hTG.dz]
    # 地支藏干
    # 子(0)里藏癸(9) 丑(1)藏己(5)癸(9)辛(7) 寅(2)藏甲(0)丙(2)戌(10) 卯(3)藏乙(1) 辰(4)藏戊(4)乙(1)癸(9) 巳(5)藏丙(2)庚(6)戊(4)\
    # 午(6)藏丁(3)己(5) 未(7)藏己(5)丁(3)乙(1) 申(8)藏庚(6)壬(8)戊(4) 酉(9)藏辛(7) 戌(10)藏戊(4)辛(7)丁(3) 亥(11)藏壬(8)甲(0)
    # 同性同元素为比肩 异性同元素为劫财 同性克我者为七杀 异性克我者为正官 同性生我者为偏印 异性生我者为正印 同性我克者为偏财 异性我克者为正财
    # 十神规律没找到
    print(yg + yz + " " + mg + mz + " " + dg + dz + " " + hg + hz)
    canggan_dic = {0: [9, -1, -1], 1: [5, 9, 7], 2: [0, 2, 10], 3: [1, -1, -1], 4: [4, 1, 9], 5: [2, 6, 4],
                   6: [3, 5, -1],
                   7: [5, 3, 1], 8: [6, 8, 4], 9: [7, -1, -1], 10: [4, 7, 3], 11: [8, 0, -1]}
    year_canggan = canggan_dic[yTG.dz]
    month_canggan = canggan_dic[mTG.dz]
    day_canggan = canggan_dic[dTG.dz]
    hour_canggan = canggan_dic[hTG.dz]
    mapper = ten_deities[Gan[dTG.tg]]
    for i in range(3):
        for item in [year_canggan, month_canggan, day_canggan, hour_canggan]:
            canggan = item[i]
            if canggan == -1:
                print("    ", end=" ")
            else:
                print(mapper[Gan[canggan]], end=" ")

        print("\n", end="")

    # 年干阳男/年干阴女 大运顺排
    # 年干阴男/年干阴女 大运逆排
    clockwise = (yTG.tg + gender) % 2 != 0
    # 查找某日前后的第二个节气,此例为之后，之前把after替换成before
    jieqi_times = 0
    while jieqi_times != 2:
        day = day.after(1) if clockwise else day.before(1)
        if day.hasJieQi():
            # print('节气：%s' % jqmc[day.getJieQi()])
            jd = day.getJieQiJD()
            t = sxtwl.JD2DD(jd)
            # print("节气时间:%d-%d-%d %d:%d:%d" % (t.Y, t.M, t.D, t.h, t.m, round(t.s)))
            jieqi_times += 1
    # 排大运
    jieqi = datetime(int(t.Y), int(t.M), int(t.D), int(t.h), int(t.m))
    # 时间差 三天等于365天 则1天等于 365/3
    gap = jieqi - born_time
    jieqi_gap = (gap.seconds + gap.days * (24 * 60 * 60)) * 365 / 3
    # 起运年份是 一年是 365*24*60*60秒
    gap_years = jieqi_gap // (365 * 24 * 60 * 60)
    gap_month = (jieqi_gap - gap_years * 365 * 24 * 60 * 60) // (30 * 24 * 60 * 60)
    gap_days = (jieqi_gap - gap_years * (365 * 24 * 60 * 60) - gap_month * (30 * 24 * 60 * 60)) // (24 * 60 * 60)
    print("出生后%s年%s月%s日起运" % (gap_years, gap_month, gap_days))
    dayun_list = []
    # 排8个大运
    if clockwise:
        index_increase = 1
    else:
        index_increase = -1
    tg_index = mTG.tg
    dz_index = mTG.dz
    for _ in range(8):
        tg_index = tg_index + index_increase
        dz_index = dz_index + index_increase
        tg_index = (tg_index) % 10
        dz_index = (dz_index) % 12
        dayun_list.append(Gan[tg_index] + Zhi[dz_index])

    # 开始排流年 排流月
    # 排流月
    # 甲己(0,5) 丙(2)
    # 乙庚(1,6) 戊(4)
    # 丙辛(2,7) 庚(6)
    # 丁壬(3,8) 壬(8)
    # 戊癸(4,9) 甲(0)
    print(dayun_list)
    liunian_list = []
    for i in range(0, 90):
        ytg_index = (yTG.tg + i) % 10
        ydz_index = (yTG.dz + i) % 12
        ygz = Gan[ytg_index] + Zhi[ydz_index]
        liuyue_list = []
        mtg_index = (ydz_index * 2 + 2) % 10
        for mdz_index in range(2, 14):
            mgz = Gan[(mtg_index + mdz_index) % 10] + Zhi[mdz_index % 12]
            # print("mgz",mgz)
            liuyue_list.append(mgz)
        ymgz = {
            ygz: liuyue_list
        }
        liunian_list.append({born_time.year + i: ymgz})
    for item in liunian_list:
        print(item)
    #   天干合冲
    #   甲（0）己（5）合化土；乙（1）庚（6）合化金；丙辛（2,7）合化水；丁壬（3,8）合化木；戊癸（4,9）合化火 隔5相合
    #   甲0庚6相冲，乙1辛7相冲，壬8丙2相冲，癸9丁3相冲 隔6相冲

    #   地支合冲
    #   寅卯辰三会木（234） 巳午未三会火（567） 申酉戌三会金（89，10） 亥子丑三会水（11，0，1）
    #   寅2午6戌10合火,亥11卯3未7合木,申8子0辰4合水,巳5酉9丑1合金
    #   寅(2)、巳(5)、申(8) 三刑
    #   丑(1)、未(7)、戌(10) 三刑
    #   子(0)卯(3)刑
    #   辰辰(4)，午午(5)，酉酉(9)，亥亥(11)自刑
    #   子(0)午(6)相冲，丑(1)未(7)相冲，寅(2)申(8)相冲，卯(3)酉(9)相冲，辰(4)戌(10)相冲，巳(5)亥(11)相冲 隔6相冲
    #   子(0)丑(1)相合，寅(2)亥(11)相合，卯(3)戌(10)相合，辰(4)酉(9)相合，巳(5)申(8)相合，午(6)未(7)相合 合起来等于13
    #   子(0)未(7)相害，丑(1)午(6)相害，寅(2)巳(5)相害，卯(3)辰(4)相害，申(8)亥(11)相害，酉(9)戌(10)相害
    #   子(0)酉(9)、卯(3)午(6)、辰(4)丑(1)、戌(10)未(7)、寅(2)亥(11)、巳(5)申(8) 相破 隔3或者9
    data_dict = {}
    data_dict["data"] = {
        "born_gz": {
            "yg": yTG.tg,
            "yz": yTG.dz,
            "mg": mTG.tg,
            "mz": mTG.dz,
            "dg": dTG.tg,
            "dz": dTG.dz,
            "hg": hTG.tg,
            "hz": hTG.dz
        },
        "born_info": {
            "name": chart_person.name,
            "gender": chart_person.gender,
            "born_time": chart_person.born_time,
            "born_country": born_location.country,
            "born_city": born_location.city,
            "born_province": born_location.province
        },
        "dayun_list": dayun_list,
        "liunian_list": liunian_list,
        "data_rate": chart_person.born_data_rate,
    }
    return data_dict
