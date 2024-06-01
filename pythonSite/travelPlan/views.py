import os
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from catboost import CatBoostRegressor

# 모델 경로 설정
model_path = os.path.join(settings.BASE_DIR, 'travelPlan/models/my_model.cbm')
data_path = os.path.join(settings.BASE_DIR, 'travelPlan/models/df_filter.csv')

# 모델 로드
model = CatBoostRegressor()
model.load_model(model_path)

# 데이터 로드
df = pd.read_csv(data_path)
area_names = df['VISIT_AREA_NM'].unique().tolist()

def index(request):
    return render(request, 'travelPlan/index.html')

def recommend_destinations(request):
    if request.method == 'POST':
        user_inputs = []
        user_inputs.append(request.POST.get('gender'))
        user_inputs.append(float(request.POST.get('age')))
        for i in range(1, 9):
            user_inputs.append(int(request.POST.get(f'travel_style{i}')))
        user_inputs.extend([8, 0.0, 3])

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

        results = pd.DataFrame([], columns=['AREA', 'SCORE'])

        for area in area_names:
            input_data = list(traveler.values())
            input_data.append(area)

            score = model.predict([input_data])[0]

            results = pd.concat([results, pd.DataFrame([[area, score]], columns=['AREA', 'SCORE'])])

        results = results.sort_values('SCORE', ascending=False).reset_index(drop=True)

        # 상위 10개의 결과만 반환 (전체 다 반환하고 싶으면 아래 코드 주석처리 하면 됨)
        top_10_results = results.head(10)

        return render(request, 'travelPlan/recommendations.html', {'results': top_10_results})

    return render(request, 'travelPlan/user_input.html')
