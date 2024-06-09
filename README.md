# NaverMaps Crawler

> 이 레포지토리는 상업적 목적이 아닌 인공지능 모델 개발을 위한 연구 목적으로 제작되었습니다. 문제가 될 경우, 삭제될 수 있습니다.

## 목차

- [개요](#개요)
- [기능](#기능)
- [설치](#설치)
  - [필수 요구 사항](#필수-요구-사항)
  - [설치 단계](#설치-단계)
- [사용법](#사용법)
- [구성 요소](#구성-요소)
- [기여](#기여)
- [라이선스](#라이선스)

## 개요

NaverMaps Crawler는 Naver Maps를 통해 전국의 관련 업체들의 주소/평점/리뷰를 수집하는 파이썬 기반 웹 크롤러입니다. 이 프로젝트는 상업적 목적이 아닌 인공지능 모델 학습용 데이터 수집을 위해 제작되었습니다.

## 기능

- **Naver Maps 데이터 크롤링**: 지정된 지역의 주차장 정보를 자동으로 수집합니다.
- **데이터 저장**: 수집된 데이터를 CSV 파일로 저장합니다.
- **로그 관리**: 크롤링 과정 중 발생하는 로그를 기록하여 문제를 추적할 수 있습니다.

## 설치

### 필수 요구 사항

- Python 3.8 이상
- Chrome 브라우저
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) (브라우저 버전에 맞는 버전 설치)

### 설치 단계

1. **리포지토리 클론**:

    ```bash
    git clone https://github.com/your-username/NaverMapsCrawler.git
    cd NaverMapsCrawler
    ```

2. **가상 환경 생성 및 활성화** (선택 사항):

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows에서는 venv\Scripts\activate
    ```

3. **필요한 패키지 설치**:

    ```bash
    pip install -r requirements.txt
    ```

## 사용법

1. **크롤러 설정**:

    `config.json` 파일을 수정하여 크롤러 설정을 사용자 정의합니다. 예를 들어, 네이버 맵의 CSS Selector를 수정할 수 있습니다.

    ```json
    {
        "search_input": "div.input_box > input.input_search",
        "shop_list": "li.VLTHu",
        "page_list": ".zRM9F> a",
        "shop_names": ".YwYLL",
        "shop_types": ".YzBgS",
        "etc": "..."
    }
  
    ```

2. **크롤러 실행**:
    명령행에서 main.py를 실행할 때 필요한 인수를 함께 제공하여 실행합니다. 기본적인 실행 예시는 아래와 같습니다.
    ```bash
        python main.py '검색어' '크롬드라이버 경로' --config '설정 파일 경로' --headless --output '출력 파일명'
    ```
    예를 들어, 인테리어 업체들을 수집하고 결과를 인테리어.json 파일에 저장하려면 다음과 같이 실행합니다:

    ```bash
    python main.py '인테리어' './chromedriver.exe' --config './config.json' --headless --output '인테리어.json'
    ```

3. **데이터 확인**:

    수집된 데이터는 `output` 폴더에 저장된 json 파일에서 확인할 수 있습니다.


## 구성 요소

- `main.py`: 크롤러 실행 스크립트로, 프로그램의 진입점입니다. 크롤링을 시작하고 종료하는 역할을 합니다.
- `crawler.py`: 크롤러의 주요 로직을 포함한 파일입니다. 크롤링 작업을 수행하는 함수들이 정의되어 있습니다.
- `config.json`: 크롤러 설정 파일입니다. 크롤링할 지역, 검색어, 최대 페이지 수 등을 설정할 수 있습니다.
- `requirements.txt`: 이 프로젝트에 필요한 파이썬 패키지 목록입니다. `pip install -r requirements.txt` 명령어로 설치할 수 있습니다.
- `output/`: 크롤러가 수집한 데이터를 저장하는 폴더입니다. json 파일 형식으로 저장됩니다.


## 기여

기여를 환영합니다! 기여 방법:

1. 이 리포지토리를 포크합니다.
2. 새로운 브랜치를 생성합니다. (`git checkout -b feature/your-feature`)
3. 변경 사항을 커밋합니다. (`git commit -am 'Add new feature'`)
4. 브랜치에 푸시합니다. (`git push origin feature/your-feature`)
5. 풀 리퀘스트를 생성합니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `md/LICENSE` 파일을 참조하세요.


## 개발 예정

1. 커스텀 DB 커넥터
2. 폴더 구조 변경
3. DockerFile 및 k8s용 yaml 추가
