from datetime import datetime
import pandas as pd
import numpy as np
import copy
import csv
import os

# from merge_line_dto import MergeLineDTO
# from k_line_dto import KLineDTO
# from sql_lite_util import *
__author__ = 'pwg2'


# K线DTO
class KLineDTO(object):
    day = datetime.now()
    begin_time = datetime.now()
    end_time = datetime.now()
    open = 0.0
    high = 0.0
    low = 0.0
    close = 0.0

    def __init__(self, day, begin_time, end_time, open, high, low, close):
        self.day = day
        self.begin_time = begin_time
        self.end_time = end_time
        self.open = open
        self.high = high
        self.low = low
        self.close = close

    def __str__(self):
        return "(" + self.day.strftime('%Y-%m-%d %H:%M:%S') + ", " \
               + self.begin_time.strftime('%Y-%m-%d %H:%M:%S') + ", " \
               + self.end_time.strftime('%Y-%m-%d %H:%M:%S') + ")"


# --------------------------------

# 合并后的K线DTO
class MergeLineDTO(object):
    memberList = []
    stick_num = 0
    begin_time = datetime.now()
    end_time = datetime.now()
    high = 0.0
    low = 0.0
    is_peak = 'N'
    is_bottom = 'N'
    member_list = []  # KLineDTO[]

    def __init__(self, stick_num, begin_time, end_time, high, low, is_peak, is_bottom):
        self.stick_num = stick_num
        self.begin_time = begin_time
        self.end_time = end_time
        self.high = high
        self.low = low
        self.is_peak = is_peak
        self.is_bottom = is_bottom

    def __str__(self):
        return "(" + self.begin_time.strftime('%Y-%m-%d %H:%M:%S') + ", " \
               + self.end_time.strftime('%Y-%m-%d %H:%M:%S') + ")"

class ZhongshuDTO(object):
    begin_time = datetime.now()
    end_time = datetime.now()
    high = 0.0
    low = 0.0
    highrange = 0.0
    lowrange = 0.0
    member_list = []

    def __init__(self, begin_time, end_time, high, low, highrange, lowrange):
        self.begin_time = begin_time
        self.end_time = end_time
        self.high = high
        self.low = low 
        self.highrange = highrange
        self.lowrange = lowrange

    def __str__(self):
        return "(" + self.begin_time.strftime('%Y-%m-%d %H:%M:%S') + ", " \
               + self.end_time.strftime('%Y-%m-%d %H:%M:%S') + ")"

# --------------------------------

def set_peak_and_bottom_flag(merge_line_list):
    #  标记顶和底
    #  []MergeLineDTO

    if len(merge_line_list) < 3:
        return

    #  顶和底,暂不考虑是否公用k线

    i = 1
    while i < len(merge_line_list) - 1:
        first_dto = merge_line_list[i - 1]
        middle_dto = merge_line_list[i]
        last_dto = merge_line_list[i + 1]
        if middle_dto.high > max(first_dto.high, last_dto.high) \
                and middle_dto.low > max(first_dto.low, last_dto.low):
            middle_dto.is_peak = 'Y'

        if middle_dto.high < min(first_dto.high, last_dto.high) \
                and middle_dto.low < min(first_dto.low, last_dto.low):
            middle_dto.is_bottom = 'Y'

        i += 1


def is_inclusive(merge_line_dto, high_price, low_price):
    #  判断是否存在包含关系
    #  MergeLineDTO, float, float
    if (merge_line_dto.high >= high_price and merge_line_dto.low <= low_price) \
            or (merge_line_dto.high <= high_price and merge_line_dto.low >= low_price):
        return True
    return False


def is_down(merge_line_dto, high_price, low_price):
    #  是否方向向下
    #  MergeLineDTO, float, float
    if merge_line_dto.high > high_price and merge_line_dto.low > low_price:
        return True
    return False


def is_up(merge_line_dto, high_price, low_price):
    #   是否方向向上
    #  MergeLineDTO, float, float
    if merge_line_dto.high < high_price and merge_line_dto.low < low_price:
        return True
    return False


def merge_k_line(merge_line_dto, k_line_dto, trend):
    #  合并K线
    #  MergeLineDTO, KLineDTO, string
    if trend == 'up':
        merge_line_dto.high = max(merge_line_dto.high, k_line_dto.high)
        merge_line_dto.low = max(merge_line_dto.low, k_line_dto.low)
        merge_line_dto.end_time = k_line_dto.end_time
    if trend == 'down':
        merge_line_dto.high = min(merge_line_dto.high, k_line_dto.high)
        merge_line_dto.low = min(merge_line_dto.low, k_line_dto.low)
        merge_line_dto.end_time = k_line_dto.end_time
    merge_line_dto.end_time = k_line_dto.end_time
    merge_line_dto.member_list.append(k_line_dto)
    merge_line_dto.stick_num += 1


def find_peak_and_bottom(k_line_list, begin_trend):  # []KLineDTO
    #  寻找真正的顶和底
    #  []KLineDTO, string
    k_line_dto = k_line_list[0]

    merge_line_dto = MergeLineDTO(1, k_line_dto.begin_time, k_line_dto.end_time,
                                  k_line_dto.high, k_line_dto.low, 'N', 'N')

    merge_line_list = [merge_line_dto]
    trend = begin_trend

    i = 1
    while i < len(k_line_list):

        today_k_line_dto = k_line_list[i]
        last_m_line_dto = merge_line_list[len(merge_line_list) - 1]
        if is_inclusive(last_m_line_dto, today_k_line_dto.high, today_k_line_dto.low):
            #  假如存在包含关系,合并K线
            merge_k_line(last_m_line_dto, today_k_line_dto, trend)
        else:
            if is_up(last_m_line_dto, today_k_line_dto.high, today_k_line_dto.low):
                trend = "up"
            elif is_down(last_m_line_dto, today_k_line_dto.high, today_k_line_dto.low):
                trend = "down"

            this_mline_dto = MergeLineDTO(1, today_k_line_dto.begin_time, today_k_line_dto.end_time,
                                          today_k_line_dto.high, today_k_line_dto.low, 'N', 'N')
            this_mline_dto.member_list = []
            this_mline_dto.member_list.append(today_k_line_dto)
            merge_line_list.append(this_mline_dto)

        #  处理顶底分型
        set_peak_and_bottom_flag(merge_line_list)
        i += 1

    # print(merge_line_list)
    #  输出检查
    '''
    for m_line_dto in merge_line_list:
        print(m_line_dto.begin_time.strftime('%Y-%m-%d %H:%M:%S') + " -- " +
              m_line_dto.end_time.strftime('%Y-%m-%d %H:%M:%S') + "**" +
              m_line_dto.is_peak + "**" + m_line_dto.is_bottom + "**" +
              str(m_line_dto.stick_num))
    '''
    return merge_line_list


def fen_bi(merge_line_list):
    #  分笔
    #  MergeLineDTO[]
    point_flag_list = [False] * len(merge_line_list)
    # print(str(point_flag_list[0])+" " + str(point_flag_list[4]))

    #  1.预处理，处理后相邻的都是非同一种分型
    last_point_m_line_dto = None

    for index in range(len(merge_line_list)):
        this_m_line_dto = merge_line_list[index]
        if this_m_line_dto.is_peak == 'N' \
                and this_m_line_dto.is_bottom == 'N':
            continue

        if last_point_m_line_dto is None:
            last_point_m_line_dto = this_m_line_dto
            point_flag_list[index] = True
            continue

        if last_point_m_line_dto.is_peak == 'Y' and this_m_line_dto.is_peak == 'Y':
            #  同为顶，取最高的
            if this_m_line_dto.high >= last_point_m_line_dto.high:
                last_point_m_line_dto = this_m_line_dto
                point_flag_list[index] = True
        elif last_point_m_line_dto.is_bottom == 'Y' and this_m_line_dto.is_bottom == 'Y':
            #  同为底，取最低的
            if this_m_line_dto.low <= last_point_m_line_dto.low:
                last_point_m_line_dto = this_m_line_dto
                point_flag_list[index] = True
        else:
            last_point_m_line_dto = this_m_line_dto
            point_flag_list[index] = True
    #  2.动态规划，找出任意[k,k+i]是否能成一笔
    point_index_list = []
    for index in range(len(point_flag_list)):
        if point_flag_list[index]:
            point_index_list.append(index)

    point_index_matrix = [[False] * len(point_index_list) for i in range(len(point_index_list))]
    # print(str(point_index_matrix[0][0]) + " " +
    #       str(point_index_matrix[len(point_index_list)-1][len(point_index_list)-1]))

    find_valid_point_by_dp(merge_line_list, point_index_list, point_index_matrix)

    #  3.根据上一步得到的结果，得出最后合理的分型
    result_array = [False] * len(point_index_list)
    has_result = False
    index = len(point_index_list) - 1
    while index > 0:
        for result in result_array:
            result = False

        has_result = check_final_fen_bi(merge_line_list, point_index_list,
                                        point_index_matrix, result_array, index)

        if has_result:
            break

        index -= 1

    #  4.输出分笔结果
    print("分笔结果 : " + str(has_result))
    if not has_result:
        print("按照目前的划分规则，没有找到分笔的结果.")
    
    fenbi_list = []
    for i in range(len(result_array)):
        if result_array[i]:
            m_line_dto = merge_line_list[point_index_list[i]]
            if m_line_dto.is_peak == 'Y':
                fenbi_list.append(m_line_dto)
#                 print(m_line_dto.begin_time + "\t" +
#                       m_line_dto.end_time + "\t" +
#                       "合并[" + str(m_line_dto.stick_num) + "]条K线" + "\t" +
#                       "顶[" + str(m_line_dto.low) + "][" + str(m_line_dto.high) + "]")
            if m_line_dto.is_bottom == 'Y':
                fenbi_list.append(m_line_dto)
#                 print(m_line_dto.begin_time + "\t" +
#                       m_line_dto.end_time+ "\t" +
#                       "合并[" + str(m_line_dto.stick_num) + "]条K线" + "\t" +

    return fenbi_list

 
def xianduan(fenbi_list):
    xianduan_list = []
    last_direction = []
    fenbi = copy.deepcopy(fenbi_list)
    while fenbi:
        if len(fenbi) < 4 and not xianduan_list:
            print('线段必须至少4个点')
            return xianduan_list
        if len(fenbi) < 4 and xianduan_list:
            print('线段是否可以延伸')
            if len(fenbi) == 3:
                if fenbi[0].high > fenbi[1].high and last_direction[-1] == -1:
                    xianduan_list[-1] = fenbi[1]
                    if fenbi[1].high > fenbi[2].high:
                        xianduan_list[-1] = fenbi[2]
                if fenbi[0].high < fenbi[1].high and last_direction[-1] == 1:
                    xianduan_list[-1] = fenbi[1]
                    if fenbi[1].high < fenbi[1].high:
                        xianduan_list[-1] = fenbi[2] 
            elif len(fenbi) == 2:
                if fenbi[0].high > fenbi[1].high and last_direction[-1] == -1:
                    xianduan_list[-1] = fenbi[1]
                if fenbi[0].high < fenbi[1].high and last_direction[-1] == 1:
                    xianduan_list[-1] = fenbi[1] 
            else:
                pass
            return xianduan_list
        is_xianduan(last_direction, xianduan_list, fenbi[0:4])
        if not xianduan_list:
            fenbi.pop(0)
        else:
            fenbi.pop(0)
            fenbi.pop(0)
            fenbi.pop(0)
    return xianduan_list
        
def is_xianduan(last_direction, xianduan_list, fenbi):
    if fenbi[0].high < fenbi[1].high and fenbi[1].high < fenbi[3].high:
        direction = 1
        if not xianduan_list:
            xianduan_list.append(fenbi[0])
            xianduan_list.append(fenbi[3])
        else:
            if last_direction[-1] == direction:
                xianduan_list[-1] = fenbi[3]
            else:
                xianduan_list.append(fenbi[3])
        last_direction.append(direction)
    elif fenbi[0].low > fenbi[1].low and fenbi[1].low > fenbi[3].low:
        direction = -1
        if not xianduan_list:
            xianduan_list.append(fenbi[0])
            xianduan_list.append(fenbi[3])
        else:
            if last_direction[-1] == direction:
                xianduan_list[-1] = fenbi[3]
            else:
                xianduan_list.append(fenbi[3])
        last_direction.append(direction)
    else:
        if xianduan_list:
            xianduan_list[-1] = fenbi[3]
        else:
            return
        print('线段延伸') 
 
def check_final_fen_bi(merge_line_list, point_index_list,
                       point_index_matrix, result_array, end_index):
    #  查看最终正确的笔划分
    #  MergeLineDTO[], boolean[], boolean[][],boolean[],integer
    search_result = False
    i = 0
    while i < end_index and not search_result:
        search_result = search_final_fen_bi(merge_line_list, point_index_list,
                                   point_index_matrix, result_array,
                                   i, end_index)
        i += 1
    return search_result

def search_final_fen_bi(merge_line_list, point_index_list,
                        point_index_matrix, result_array, index, end_index):
    #  递归查找查看最终正确的笔划分
    #  MergeLineDTO[], boolean[], boolean[][],boolean[],integer,integer
    if index == end_index:
        return True
    else:
        i = index + 1
        while i <= end_index:
            if point_index_matrix[index][i]:
                result_array[index] = True
                result_array[i] = True
                if search_final_fen_bi(merge_line_list, point_index_list,
                                       point_index_matrix, result_array,
                                       i, end_index):
                    return True
                else:
                    result_array[index] = False
                    result_array[i] = False
            i+=1
    return False


def find_valid_point_by_dp(merge_line_list, point_index_list, point_index_matrix):
    #  通过动态规划寻找有效的分型
    #  通过动态规划，查找局部解，结果在pointIndexMatrix中
    #  MergeLineDTO[], boolean[], boolean[][]
    distance = 1
    while distance < len(point_index_list):
        #  取奇数，经过之前第一阶段的预处理，间隔为偶数的都是同类分型
        process_by_distance(merge_line_list, point_index_list, point_index_matrix, distance)
        distance += 2


def process_by_distance(merge_line_list, point_index_list, point_index_matrix, distance):
    #  处理间隔为dist的分型组合，是否能成一笔
    #  MergeLineDTO[], boolean[], boolean[][], integer
    index = 0
    while index < len(point_index_list) - distance:
        check_result = check_2point_is_multi_line(merge_line_list,
                                                  point_index_list,
                                                  point_index_matrix,
                                                  index, index + distance)

        if check_result:
            point_index_matrix[index][index + distance] = False
        else:
            if validate_peak_and_bottom(merge_line_list,
                                        point_index_list[index],
                                        point_index_list[index + distance]):
                point_index_matrix[index][index + distance] = True
            else:
                point_index_matrix[index][index + distance] = False
        index += 1


def check_2point_is_multi_line(merge_line_list, point_index_list,
                               point_index_matrix, start_index, end_index):
    #  递归处理，逐步检查[startIndex，endIndex]是否能划分成多笔
    #  MergeLineDTO[], boolean[], boolean[][], integer, integer
    if start_index == end_index:
        return True
    else:
        index = start_index + 1
        while index <= end_index:
            if point_index_matrix[start_index][index]:
                boolean_result = check_2point_is_multi_line(merge_line_list,
                                                            point_index_list,
                                                            point_index_matrix,
                                                            index, end_index)
                if boolean_result:
                    return True
            index += 1
    return False


def validate_peak_and_bottom(merge_line_list, start_index, end_index):
    #  校验是否满足一笔
    #  MergeLineDTO[], integer, integer
    start_m_line_dto = merge_line_list[start_index]
    end_m_line_dto = merge_line_list[end_index]

    #  1.不满足顶必须接着底、或底必须接着顶
    if start_index == 0:
        if end_m_line_dto.is_peak == 'N' and end_m_line_dto.is_bottom != 'N':
            return False
    elif (start_m_line_dto.is_peak == 'Y' and end_m_line_dto.is_peak == 'Y') \
            or (start_m_line_dto.is_bottom == 'Y' and end_m_line_dto.is_bottom == 'Y'):
        return False

    #  2.顶分型与底分型经过包含处理后，不允许共用K线
    if end_index - start_index < 3:
        return False

    #  3.顶分型中最高K线和底分型的最低K线之间（不包括这两K线），不考虑包含关系，至少有3根（包括3根）以上K线
    k_line_number = 0
    for index in range(len(start_m_line_dto.member_list)):
        k_line_dto = start_m_line_dto.member_list[index]
        if start_m_line_dto.is_peak == 'Y' and start_m_line_dto.high == k_line_dto.high:
            #  顶，并且是顶元素
            k_line_number += (len(start_m_line_dto.member_list) - index - 1)
            break
        elif start_m_line_dto.is_bottom == 'Y' and start_m_line_dto.low == k_line_dto.low:
            #  底，并且是底元素
            k_line_number += (len(start_m_line_dto.member_list) - index - 1)
            break

    for index in range(len(end_m_line_dto.member_list)):
        k_line_dto = end_m_line_dto.member_list[index]
        if end_m_line_dto.is_bottom == 'Y' and end_m_line_dto.low == k_line_dto.low:
            k_line_number += index
            break
        elif end_m_line_dto.is_peak == 'Y' and end_m_line_dto.high == k_line_dto.high:
            k_line_number += index
            break
    #  分型中间元素的k线合计
    index = start_index + 1
    while index < end_index:
        m_line_dto = merge_line_list[index]
        k_line_number += m_line_dto.stick_num
        index += 1

    if k_line_number < 3:
        return False

    #  4.顶底分别是笔中(包括组成分型的元素)的最高和最低
    peak_dto = None
    bottom_dto = None
    if start_m_line_dto.is_peak == 'Y':
        peak_dto = start_m_line_dto
        bottom_dto = end_m_line_dto
    else:
        peak_dto = end_m_line_dto
        bottom_dto = start_m_line_dto

    index = 0 if start_index == 0 else start_index - 1
    while index <= end_index + 1:
        m_line_dto = merge_line_list[index]

        #  存在更高的点位
        if m_line_dto.high > peak_dto.high \
                and m_line_dto.begin_time != peak_dto.begin_time:
            return False

        if m_line_dto.low < bottom_dto.low \
                and m_line_dto.begin_time != bottom_dto.begin_time:
            return False

        index += 1

    #  5.不允许中间有其他的顶和底
    #  6.或许还需要判断顶底的区间是否不能重叠
    return True

def zhongshu(xianduan_list):
    zhongshu = []
    xianduan = copy.deepcopy(xianduan_list) 
    while xianduan:
        mline = xianduan[0]
        if not zhongshu:
            if len(xianduan) > 3:
                    if (xianduan[0].low < xianduan[1].high and xianduan[2].high < xianduan[3].high) \
                    or (xianduan[0].high > xianduan[1].low and xianduan[2].high > xianduan[3].high):
                        begin_time = xianduan[0].begin_time
                        end_time = xianduan[3].end_time
                        temp_xianduan_high = [xianduan[0].high, xianduan[1].high, xianduan[2].high, xianduan[3].high]
                        highrange = max(temp_xianduan_high)
                        temp_xianduan_high.remove(max(temp_xianduan_high))
                        high = max(temp_xianduan_high)
                        temp_xianduan_low = [xianduan[0].low, xianduan[1].low, xianduan[2].low, xianduan[3].low]
                        lowrange = min(temp_xianduan_low)
                        temp_xianduan_low.remove(min(temp_xianduan_low))
                        low = min(temp_xianduan_low)
                        if xianduan[2].high > xianduan[1].high and xianduan[1].low == low and xianduan[2].high == high:
                            xianduan.pop(0)
                            continue
                        if xianduan[2].high < xianduan[1].high and xianduan[1].high == high and xianduan[2].low == low:
                            xianduan.pop(0)
                            continue
                        zhongshudto = ZhongshuDTO(begin_time, end_time, high, low, highrange, lowrange)
                        zhongshudto.member_list.append(xianduan[0])
                        zhongshudto.member_list.append(xianduan[1])
                        zhongshudto.member_list.append(xianduan[2])
                        zhongshudto.member_list.append(xianduan[3])
                        zhongshu.append(zhongshudto)
                        xianduan.pop(0)
                        xianduan.pop(0)
                        xianduan.pop(0)
                        xianduan.pop(0)  
                        continue
                    else:
                        xianduan.pop(0)
                        continue
            else:
                print('不能构成中枢')
                return zhongshu
        if mline.high < zhongshu[-1].high and mline.low > zhongshu[-1].low:
            zhongshu[-1].end_time = mline.end_time
            zhongshu[-1].highrange = zhongshu[-1].highrange if mline.high < zhongshu[-1].highrange else mline.high
            zhongshu[-1].lowrange = zhongshu[-1].lowrange if mline.low > zhongshu[-1].lowrange else mline.low
            xianduan.pop(0)
            continue
        else:
            # 向后看最多3条线段  
            index = xianduan.index(mline)
            if len(xianduan) > index+1:
                after_1 = xianduan[index+1]
                if after_1.high <= zhongshu[-1].high and after_1.low >= zhongshu[-1].low:
                    zhongshu[-1].end_time = after_1.end_time
                    zhongshu[-1].highrange = zhongshu[-1].highrange if after_1.high < zhongshu[-1].highrange else after_1.high
                    zhongshu[-1].lowrange = zhongshu[-1].lowrange if after_1.low > zhongshu[-1].lowrange else after_1.low
                    #zhongshu[-1].high = mline.high
                    xianduan.pop(0)
                    xianduan.pop(0)
                    continue
                else:
                    pass
            if len(xianduan) > index+2:
                after_2 = xianduan[index+2]
                if after_2.high <= zhongshu[-1].high and after_2.low >= zhongshu[-1].low:
                    zhongshu[-1].end_time = after_2.end_time
                    zhongshu[-1].highrange = zhongshu[-1].highrange if after_2.high < zhongshu[-1].highrange else after_2.high
                    zhongshu[-1].lowrange = zhongshu[-1].lowrange if after_2.low > zhongshu[-1].lowrange else after_2.low
                    #zhongshu[-1].high = mline.high
                    xianduan.pop(0)
                    xianduan.pop(0)
                    xianduan.pop(0)
                    continue
                else:
                    pass
            if len(xianduan) > index+3:
                after_3 = xianduan[index+3]
                if after_3.high <= zhongshu[-1].high and after_3.low >= zhongshu[-1].low:
                    zhongshu[-1].end_time = after_3.end_time
                    zhongshu[-1].highrange = zhongshu[-1].highrange if after_3.high < zhongshu[-1].highrange else after_3.high
                    zhongshu[-1].lowrange = zhongshu[-1].lowrange if after_3.low > zhongshu[-1].lowrange else after_3.low
                    #zhongshu[-1].high = mline.high
                    xianduan.pop(0)
                    xianduan.pop(0)
                    xianduan.pop(0)
                    xianduan.pop(0)
                    continue
                else:
                    if (mline.low < after_1.high and after_1.high < after_3.high) \
                    or (mline.high > after_1.low and after_1.high > after_3.high):
                        begin_time = mline.begin_time
                        end_time = after_3.end_time
                        temp_xianduan_high = [mline.high, after_1.high, after_2.high, after_3.high]
                        highrange = max(temp_xianduan_high)
                        temp_xianduan_high.remove(max(temp_xianduan_high))
                        high = max(temp_xianduan_high)
                        temp_xianduan_low = [mline.low, after_1.low, after_2.low, after_3.low]
                        lowrange = min(temp_xianduan_low)
                        temp_xianduan_low.remove(min(temp_xianduan_low))
                        low = min(temp_xianduan_low)
                        if after_2.high > after_1.high and after_1.low == low and after_2.high == high:
                            xianduan.pop(0)
                            continue
                        if after_2.high < after_1.high and after_1.high == high and after_2.low == low:
                            xianduan.pop(0)
                            continue
                        zhongshudto = ZhongshuDTO(begin_time, end_time, high, low, highrange, lowrange)
                        zhongshudto.member_list.append(mline)
                        zhongshudto.member_list.append(after_1)
                        zhongshudto.member_list.append(after_2)
                        zhongshudto.member_list.append(after_3)
                        zhongshu.append(zhongshudto)
                        xianduan.pop(0)
                        xianduan.pop(0)
                        xianduan.pop(0)
                        xianduan.pop(0)
                        continue
                    else:
                        xianduan.pop(0)
                        continue
            xianduan.pop(0)
                        
    return zhongshu

def readstkData(filepaths, interval):
    dfs = []
    for rootpath in filepaths:
        file_list = os.listdir(rootpath)
        for file in file_list:
            if file.endswith(interval+'.csv'):
                file_path = os.path.join(rootpath, file)
                df = pd.read_csv(file_path, skiprows=1) 
                dfs.append(df)
    df = [] 
    df = pd.concat(dfs)
    df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'])
    df.sort_values('candle_begin_time', inplace=True)
    #df = df[0:2500]
    return df



def run_test():
    #  测试
    #  取原始数据
    exchange = 'bitfinex'
    symbol = 'ETHUSD'
    interval = '30T'
    time_period = ['2018-09','2018-10']
    absdir = os.path.dirname(os.path.abspath(__file__))
    filepaths = []
    for period in time_period:
        daylinefilepath = os.path.join(absdir,exchange,symbol,period)
        filepaths.append(daylinefilepath)
    df = readstkData(filepaths,interval)
    df = df[:2800]
    '''
    df = pd.read_csv('bitfinex_hour.csv')
    df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'])
    df.sort_values('candle_begin_time', inplace=True)
    mask = (df['candle_begin_time'] > '2018-06-01') & (df['candle_begin_time'] <= '2018-06-30')
    df = df.loc[mask]
    '''
    day = '2018-01-31 00:00:00'
    end_time = '2018-01-31 23:59:59'
    k_line_list = []
    for row in df.itertuples():
        begin_time = row.candle_begin_time 
        end_time = row.candle_begin_time 
        Open = row.open 
        high = row.high
        low = row.low
        close = row.close
        kline = KLineDTO(day, begin_time, end_time, Open, high, low, close)
        k_line_list.append(kline)
    print(len(k_line_list))
    # k_line_list = get_stock_30min_data_by_time("999999", "2015-03-10", "2015-05-16")

    print("---------------------------")
    #  分型
    merge_line_list = find_peak_and_bottom(k_line_list, "down")
    m_line_dto = merge_line_list[0]
    m_line_dto.is_peak = 'Y'
    
    fenbi_list =  fen_bi(merge_line_list)
    #fenbi_csv = 'fenbi.csv'
    fenbi_csv = 'fenbi'+str(time_period)+'.csv'
    with open(fenbi_csv, 'w') as fenbicsv:
        csv_writer = csv.writer(fenbicsv)
        csv_writer.writerow(['candle_begin_time', 'high', 'low','is_peak', 'is_low'])
        for fenbi in fenbi_list:
            csv_writer.writerow([fenbi.begin_time, fenbi.high, fenbi.low, fenbi.is_peak, fenbi.is_bottom])
    xianduan_list = xianduan(fenbi_list)
    print(xianduan_list)
    #xianduan_csv = 'xianduan.csv'
    xianduan_csv = 'xianduan'+str(time_period)+'.csv'
    with open(xianduan_csv, 'w') as xianduan_csv:
        csv_writer = csv.writer(xianduan_csv)
        csv_writer.writerow(['candle_begin_time', 'high', 'low','is_peak', 'is_low'])
        for xd in xianduan_list:
            csv_writer.writerow([xd.begin_time, xd.high, xd.low, xd.is_peak, xd.is_bottom])
    zhongshu_list = zhongshu(xianduan_list)
    #zhongshu_csv = 'zhongshu.csv'
    zhongshu_csv = 'zhongshu'+str(time_period)+'.csv'
    with open(zhongshu_csv, 'w') as zhongshu_csv:
        csv_writer = csv.writer(zhongshu_csv)
        csv_writer.writerow(['begin_time', 'end_time', 'high', 'low'])
        for zs in zhongshu_list:
            csv_writer.writerow([zs.begin_time, zs.end_time, zs.high, zs.low])
run_test()
