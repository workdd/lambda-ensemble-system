## KSC2021
### 논문 제목 : [서버리스 앙상블 추론 시스템](http://www.riss.or.kr/search/detail/DetailView.do?p_mat_type=1a0202e37d52c72d&control_no=77bd8480298a674ad18150b21a227875&keyword=)
딥러닝 모델을 앙상블 하는 것은 단일 모델을 추론할 때보다 높은 정확도를 얻을 수 있다. 하지만 기존 온디맨드 구조에서는 순차적으로 모델을 실행시키는 방식이 일반적이다.
서버리스 컴퓨팅의 병렬 처리 이점을 이용해 딥러닝 추론 모델을 병렬적으로 처리하는 시스템 구조를 만들어 제안했다.

### 고안한 시스템 구성도
<img src='assets/structure.png' width="600" />

### AWS Step Function을 이용해 구성
<img src='assets/stepfunction.png' width="600" />

### 결과
한국 정보 과학회주관 KSC2021 학회에 참여 및 [포스터 발표](https://user-images.githubusercontent.com/28581495/218098592-e9901327-af9d-440a-8438-e19817f9f7ca.png)를 진행하여 컴퓨터 시스템 부문 [우수논문발표상](http://www.kiise.or.kr/academy/board/academyNewsView.fa?MENU_ID=080100&sch_add_bd=%ED%95%99%ED%9A%8C%EC%86%8C%EC%8B%9D&NUM=2260)에 입상함

<img src='https://user-images.githubusercontent.com/28581495/218097695-b629a171-b707-4876-aa87-9439dd6b23d3.png' width="300" />
