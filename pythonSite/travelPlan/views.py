import random
import pandas as pd
from django.shortcuts import render

# 더미 데이터 사용
dummy_areas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

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

        # 더미 데이터 사용하여 점수 생성
        results = pd.DataFrame(dummy_areas, columns=['AREA'])
        results['SCORE'] = [random.uniform(0, 1) for _ in range(len(dummy_areas))]
        results = results.sort_values('SCORE', ascending=False).reset_index(drop=True)

        return render(request, 'travelPlan/recommendations.html', {'results': results})

    return render(request, 'travelPlan/user_input.html')
