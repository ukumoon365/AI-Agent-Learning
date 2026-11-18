## Machine_Learning
```text
ML (기계학습)

데이터로부터 패턴을 학습하여 예측, 판단 규칙을 스스로 찾아가는 방법
    


ML 시스템의 구성 요소
✔️ Target 
    지능의 목표 / 모델이 학습을 통해 수행 하고자 하는 기능
    - Target에 따라 Data set 설정

✔️ Dataset 
    기능을 학습하기 위해 사용하는 데이터 집합
    - 학습에 적절한 dataset 필요
    ✔️ Sample
        ○ 많을수록 정확성 🔝
        ○ 편중된 결과값 방지를 위해 개수는 동일하게
        ○ 일반화를 위해 다양한 data값 필요 (중복 ❌)
    ✅  Featrue(특징)의 개수
        -  입력값과 비례
        
✔️ Model
    데이터를 받아 학습, 패턴을 담아가는 수학적 구조

✔️Trained Model 
    학습을 통해 얻은 패턴과 규칙(Parameter)를 담고 있는 구조
    
⚠️  학습 데이터와 모델의 품질에 따라 성능 차이 발생 / data에 의존
```
# Learning (학습 방법)
```text
✔️ Supervised Learning (지도 학습)
    ✅ Label (정답)를 이용해 학습
    - Label이 포함된 데이터 사용
    - 입력, 출력의 관계 학습
    - 회귀: ( -∞ ~ +∞)
    - 분류: {A, B, C}

✔️Unsupervised Learning (비지도 학습)
    ✅ Label ❌ 패턴을 학습
    - Label 없이 데이터 구조 탐색
    - 숨겨진 패턴이나 그룹 발견
    - 군집: Group A, Group B ...
    - 연관: 우유(~), 빵(~)

✔️ Reinforcement Learning (강화학습)
    ✅Reward(보상)를 이용한 행동 전략 학습
    - 에이전트가 환경과 상호작용
    - 보상 최대화의 행동 전략 학습
    - 많은 시도, 경우의 수 필요 -> 시뮬레이션
정확한 목표가 있을 때 사용 / 여러 방법이 있을 경우에도 사용
```