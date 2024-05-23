import random

from django.shortcuts import render
from django.http import HttpResponse

activities = {
    "휴양": ["해변에서 일광욕", "스파 및 마사지", "호숫가에서 피크닉"],
    "탐험": ["하이킹", "산악 자전거 타기", "동굴 탐험"],
    "역사 문화": ["박물관 방문", "역사적 유적지 탐방", "전통 공연 관람"],
    "미식": ["현지 음식점 탐방", "와인 시음", "시장 투어"],
    "쇼핑": ["쇼핑몰 방문", "현지 시장 방문", "기념품 가게 탐방"],
    "가족 여행": ["테마파크 방문", "동물원 방문", "어린이 박물관 탐방"],
    "로맨틱 여행": ["해변에서 일몰 감상", "로맨틱 디너", "커플 마사지"],
    "모험": ["번지 점프", "스카이다이빙", "래프팅"]
}

interests_activities = {
    "자연 경관": ["산책", "등산", "자연 보호 구역 탐방"],
    "박물관": ["미술관 방문", "역사 박물관 방문", "과학 박물관 탐방"],
    "역사적 장소": ["고대 유적지 탐방", "성 방문", "기념관 방문"],
    "테마파크": ["놀이공원 방문", "워터파크 방문", "동물 테마파크 방문"],
    "지역 음식점": ["현지 음식점 탐방", "스트리트 푸드 투어", "요리 교실 참여"],
    "시장": ["지역 시장 방문", "벼룩시장 탐방", "농산물 시장 방문"],
    "문화 행사": ["지역 축제 참여", "전통 공연 관람", "문화 워크샵 참여"],
    "스포츠 활동": ["축구 경기 관람", "자전거 타기", "해양 스포츠 참여"]
}

def index(request):
    return HttpResponse("Hello, world. You're at the travel index.")

def create_itinerary(request):
    if request.method == 'POST':
        travel_style = request.POST.get('travel_style')
        selected_interests = request.POST.getlist('selected_interests')
        travel_duration = int(request.POST.get('travel_duration'))

        itinerary = []
        for day in range(1, travel_duration + 1):
            day_plan = {
                "day": day,
                "morning": "카페에서 아침 식사",
                "forenoon": random.choice(activities[travel_style]),
                "lunch": "현지 유명 음식점에서 식사",
                "afternoon": random.choice(interests_activities[random.choice(selected_interests)] if len(selected_interests) > 0 else ["자유 시간"]),
                "evening": random.choice(interests_activities[random.choice(selected_interests)] if len(selected_interests) > 1 else ["자유 시간"]),
                "night": "숙소로 돌아오기"
            }
            itinerary.append(day_plan)
        
        return render(request, 'travelPlan/itinerary.html', {'itinerary': itinerary})

    travel_styles = ["휴양", "탐험", "역사 문화", "미식", "쇼핑", "가족 여행", "로맨틱 여행", "모험"]
    interests = ["자연 경관", "박물관", "역사적 장소", "테마파크", "지역 음식점", "시장", "문화 행사", "스포츠 활동"]

    return render(request, 'travelPlan/create_itinerary.html', {'travel_styles': travel_styles, 'interests': interests})