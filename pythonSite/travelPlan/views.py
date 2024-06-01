import os  # OS 모듈은 운영 체제와 상호작용을 위해 사용됩니다.
import pandas as pd  # Pandas는 데이터 조작 및 분석을 위한 라이브러리입니다.
from django.shortcuts import render  # Django의 render 함수는 템플릿을 렌더링하기 위해 사용됩니다.
from django.conf import settings  # Django 설정을 가져오기 위해 사용됩니다.
from catboost import CatBoostRegressor  # CatBoostRegressor는 CatBoost 라이브러리의 회귀 모델입니다.

# 모델 경로 설정
model_path = os.path.join(settings.BASE_DIR, 'travelPlan/models/my_model.cbm')  # 모델 파일 경로
data_path = os.path.join(settings.BASE_DIR, 'travelPlan/models/df_filter.csv')  # 데이터 파일 경로

# 모델 로드
model = CatBoostRegressor()  # CatBoost 회귀 모델 객체 생성
model.load_model(model_path)  # 모델 파일 로드

# 데이터 로드
df = pd.read_csv(data_path)  # CSV 파일을 데이터프레임으로 로드
area_names = df['VISIT_AREA_NM'].unique().tolist()  # 고유한 방문지 이름 목록 생성

# 메인 페이지 뷰
def index(request):
    return render(request, 'travelPlan/index.html')  # index.html 템플릿을 렌더링하여 응답 반환

# 여행지 추천 뷰
def recommend_destinations(request):
    if request.method == 'POST':  # POST 요청인지 확인
        user_inputs = []  # 사용자 입력 값을 저장할 리스트
        user_inputs.append(request.POST.get('gender'))  # 성별
        user_inputs.append(float(request.POST.get('age')))  # 나이
        for i in range(1, 9):  # 여행 스타일
            user_inputs.append(int(request.POST.get(f'travel_style{i}')))
        user_inputs.extend([8, 0.0, 3])  # 추가 고정값들

        # 사용자 입력 값을 딕셔너리로 변환
        traveler = {
            'GENDER': user_inputs[0],
            'AGE_GRP': user_inputs[1],
            'TRAVEL_STYL_1': user_inputs[2],
            'TRAVEL_STYL_2': user_inputs[3],
            'TRAVEL_STYL_3': user_inputs[4],
            'TRAVEL_STYL_4': user_inputs[5],
            'TRAVEL_STYL_5': user_inputs[6],
            'TRAVEL_STYL_6': user_inputs[7],
            'TRAVEL_STYL_7': user_inputs[8],
            'TRAVEL_STYL_8': user_inputs[9],
            'TRAVEL_MOTIVE_1': 8,
            'TRAVEL_COMPANIONS_NUM': 0.0,
            'TRAVEL_MISSION_INT': 3,
        }

        results = pd.DataFrame([], columns=['AREA', 'SCORE'])  # 결과를 저장할 데이터프레임 초기화

        for area in area_names:  # 각 방문지에 대해 예측 수행
            input_data = list(traveler.values())  # 사용자 입력 값 리스트로 변환
            input_data.append(area)  # 방문지 이름 추가

            score = model.predict([input_data])[0]  # 모델 예측 수행

            results = pd.concat([results, pd.DataFrame([[area, score]], columns=['AREA', 'SCORE'])])  # 결과 데이터프레임에 추가

        results = results.sort_values('SCORE', ascending=False).reset_index(drop=True)  # 점수 기준으로 정렬

        # 상위 10개의 결과만 반환 (전체 다 반환하고 싶으면 아래 코드 주석처리 하면 됨)
        top_10_results = results.head(10)  # 상위 10개 결과 추출

        return render(request, 'travelPlan/recommendations.html', {'results': top_10_results})  # recommendations.html 템플릿을 렌더링하여 응답 반환

    return render(request, 'travelPlan/user_input.html')  # GET 요청 시 user_input.html 템플릿을 렌더링하여 응답 반환
