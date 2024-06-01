# 투어스(To us;Tours)

## 📌서비스 소개
> **기존에 경험하지 못한 새로운 여행지 추천 시스템, 고민만 하던 여행 계획을 투어스를 통해 여행지 추천을 받아보세요!**
- 여행을 가고 싶은데 어딜 가야 할지 모르겠나요? 여행 계획만 세워봤지 어디로 가야 할지 결정하기 어려운가요? 투어스는 사용자의 선호도에 따라 맞춤형 여행지를 추천해주는 시스템입니다. 간단한 몇 가지 질문에 답하면, 당신에게 딱 맞는 여행지를 추천해드립니다.
- 투어스는 여행 스타일, 성별, 연령대 등의 정보를 바탕으로 개별 맞춤형 여행지를 제공합니다. 이제 더 이상 고민하지 말고 투어스를 통해 새로운 여행지를 발견해보세요!
 
## 🌱제작 동기
2024년 1학기 파이썬 응용 소프트웨어 수업에서 가상의 서비스 소프트웨어를 구상하고 프로토타입을 만드는 과제를 수행했습니다. 이 과정에서 사용자에게 유익한 서비스를 고민한 끝에, 국내 여행지를 추천해주는 시스템을 개발하기로 결정했습니다.

사용자마다 선호도가 다르기 때문에, 빅데이터 전처리 과정을 거쳐 사용자 맞춤형 여행지 추천 시스템을 고안했습니다. 이 시스템은 사용자의 성별, 연령대, 여행 스타일에 따라 최적의 여행지를 추천해줍니다.

여행 스타일은 다음과 같은 항목으로 구분됩니다:

- 자연 vs 도시
- 숙박 vs 당일치기
- 새로운 지역 vs 익숙한 지역
- 편하지만 비싼 숙소 vs 불편하지만 저렴한 숙소
- 휴양/휴식 vs 체험활동
- 유명하지 않은 방문지 vs 유명한 방문지
- 계획 여행 vs 즉흥 여행
- 사진 촬영 중요 vs 중요하지 않음

이를 통해 사용자는 개인 맞춤형 여행지 추천을 받아 보다 만족스러운 여행 계획을 세울 수 있습니다.



## 📁데이터 수집
> 여행, 여행객, 방문자 데이터
- [여행 데이터](https://raw.githubusercontent.com/kairess/toy-datasets/master/tn_travel_%E1%84%8B%E1%85%A7%E1%84%92%E1%85%A2%E1%86%BC_A.csv)
- [여행객 마스터 데이터](https://raw.githubusercontent.com/kairess/toy-datasets/master/tn_traveller_master_%E1%84%8B%E1%85%A7%E1%84%92%E1%85%A2%E1%86%BC%E1%84%80%E1%85%A2%E1%86%A8%20Master_A.csv)
- [방문지 정보 데이터](https://raw.githubusercontent.com/kairess/toy-datasets/master/tn_visit_area_info_%E1%84%87%E1%85%A1%E1%86%BC%E1%84%86%E1%85%AE%E1%86%AB%E1%84%8C%E1%85%B5%E1%84%8C%E1%85%A5%E1%86%BC%E1%84%87%E1%85%A9_A.csv)


## 📖학습 과정
본 프로젝트에서는 CatBoost 회귀 모델을 사용하여 여행지 추천 시스템을 구축했습니다. 다음은 데이터 전처리 및 모델 학습 과정입니다:

1. 데이터를 병합하여 하나의 데이터프레임으로 구성했습니다.
2. 필요 없는 열을 제거하고, 결측값을 처리했습니다.
3. 범주형 데이터를 인코딩하고, 데이터를 학습 및 테스트 세트로 분할했습니다.
4. CatBoost 회귀 모델을 사용하여 학습을 수행했습니다.
5. 학습된 모델을 저장하고, Django 뷰에서 불러와 사용했습니다.

## 👫팀 구성원 역할

- 김민정: 머신러닝 모델을 백엔드에 연결 및 프론트엔드 화면 구성
- 박진서: 데이터 전처리 및 머신러닝 모델 학습 

## ⚡️실행 방법:
1. 프로젝트를 클론합니다:
    ```shell
    git clone https://github.com/Mingguriguri/travel-guide-withML.git
    cd travel-guide-withML/pythonSite
    ```

2. 가상 환경을 설정하고 활성화합니다:
    ```shell
    python -m venv venv
    source venv/bin/activate  # Windows에서는 `venv\Scripts\activate`
    ```

3. 필요한 패키지를 설치합니다:
    ```shell
    pip install -r requirements.txt
    ```

4. Django 서버를 실행합니다:
    ```shell
    python manage.py runserver
    ```
5. 웹 브라우저에서 `http://127.0.0.1:8000`을 엽니다.



## 🏋️‍♀️주요 파일 설명
### `views.py`
- **모듈 임포트**: 필요한 파이썬 및 Django 모듈과 라이브러리를 불러옵니다.
- **경로 설정**: 모델과 데이터를 불러오기 위한 경로를 설정합니다.
- **모델 로드**: CatBoost 회귀 모델을 불러옵니다.
- **데이터 로드**: CSV 파일에서 데이터를 읽어옵니다.
- **index 뷰**: 메인 페이지를 렌더링합니다.
- **recommend_destinations 뷰**: 여행지 추천을 위한 사용자 입력을 받아 모델을 통해 예측하고 결과를 반환합니다.

### `index.html`
<img width="1822" alt="python-1" src="https://github.com/Mingguriguri/travel-guide-withML/assets/101111603/14442a8b-3b6b-4ad9-bec4-3a9480203709">

- **헤더**: 웹 페이지의 제목과 간단한 설명을 포함합니다.
- **메인 컨텐츠**: 여행지 추천 시스템에 대한 설명과 버튼을 포함한 히어로 섹션을 구성합니다.
- **푸터**: 저작권 정보와 프로젝트 정보를 포함합니다.
  
### `user_input.html`
<img width="1822" alt="python-2" src="https://github.com/Mingguriguri/travel-guide-withML/assets/101111603/2bdde1b8-6d7d-4726-9500-3e8dfd0bcf52">
<img width="1822" alt="python-3" src="https://github.com/Mingguriguri/travel-guide-withML/assets/101111603/958088ba-3e8c-423a-8c31-e30d6b84765a">

- **폼**: 사용자로부터 성별, 연령대, 여행 스타일 등을 입력받는 폼을 구성합니다.


### `recommendations.html`
<img width="1822" alt="python-4" src="https://github.com/Mingguriguri/travel-guide-withML/assets/101111603/2e9b96e3-ee88-47fa-8e60-25fe331b78b3">

- **결과 목록**: 추천된 여행지와 점수를 카드 형태로 표시합니다.
- **처음으로 돌아가기 버튼**: 메인 페이지로 돌아가는 링크를 포함합니다.



