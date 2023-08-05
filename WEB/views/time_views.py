from flask import Blueprint, render_template, request
from API import Odsay

bp = Blueprint('time', __name__, url_prefix='/time')

@bp.route('/')
def main():
    return render_template('main/time.html')

@bp.route('/', methods=['POST', 'GET'])
def result():
    
    start_station = request.form.get('start_station')
    end_station = request.form.get('end_station')
    
    SID, EID = Odsay.SID_EID(start_station, end_station) # SID, EID 구하는 함수
    df_stations, drive_info_df = Odsay.metrojson(SID, EID) # Odsay Data 구하는 함수
    
    # 시간 받는 거
    
    congestion_ls = [] # 재영님이 주실 것
    split_stations, split_congestion, split_minute, percent_ls, lane = Odsay.result_list(df_stations, drive_info_df, congestion_ls)
    
    cogestion_mapping = {}

    # < 결과 예시 >
    # split_stations = [['서울역', '회현', '명동', '충무로'], (환승) ['동대문역사문화공원', '신당', '상왕십리', '왕십리', '한양대']]
    # split_congestion = [[12, 34, 1, 99], (환승) [12, 34, 34, 24, 11]]
    # lane = ['4호선', '2호선']
    # travel_time_ls = [2, 4, 5, 7, 10, 12, 13, 15, 17] -> 이동 시간
    # split_minute = [[2, 4, 5, 7], (환승) [10, 12, 13, 15, 17]] -> 
    # percent_ls = [11.76470588235294, 11.76470588235294, 5.88235294117647, 11.76470588235294, 17.647058823529413, 11.76470588235294, 5.88235294117647, 11.76470588235294, 11.76470588235294]
    
    return render_template('main/time.html', 
                           split_stations=split_stations, split_congestion=split_congestion,
                           split_minute=split_minute, percent_ls=percent_ls, lane=lane)