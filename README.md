# KSC2021
- 논문 제목 : 서버리스 앙상블 추론 시스템

### 고안한 시스템 구성도
<img src='assets/structure.png' width="600" />

### AWS Step Function을 이용해 구성
<img src='assets/step_function.png' width="600" />
- 각 폴더는 Step Function의 람다 Dockerfile로 build 할 수 있는 코드
