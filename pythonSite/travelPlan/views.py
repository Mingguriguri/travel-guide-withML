import os
import pandas as pd
import tensorflow as tf
from django.shortcuts import render
from django.conf import settings

# BASE_DIR을 이용하여 절대 경로 설정
model_path = os.path.join(settings.BASE_DIR, 'travelPlan/models/my_model.h5')
data_path = os.path.join(settings.BASE_DIR, 'travelPlan/models/df_filter.csv')

# 모델 로드
model = tf.keras.models.load_model(model_path)

# 전처리된 데이터셋 로드
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
        user_inputs.append(8)  # TRAVEL_MOTIVE_1 고정값
        user_inputs.append(0.0)  # TRAVEL_COMPANIONS_NUM 고정값
        user_inputs.append(3)  # TRAVEL_MISSION_INT 고정값

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

            # 예측
            score = predict(model, input_data)

            results = pd.concat([results, pd.DataFrame([[area, score]], columns=['AREA', 'SCORE'])])

        results = results.sort_values('SCORE', ascending=False).reset_index(drop=True)

        return render(request, 'travelPlan/recommendations.html', {'results': results})

    return render(request, 'travelPlan/user_input.html')

# 예측 함수 정의
def predict(model, input_data):
    input_tensor = tf.convert_to_tensor([input_data], dtype=tf.float32)
    prediction = model.predict(input_tensor)
    return prediction[0][0]
