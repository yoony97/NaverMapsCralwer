import argparse
from crawler import NaverMapsCrawler

def main():
    # 명령행 인수를 처리하는 argparse 객체 생성
    parser = argparse.ArgumentParser(description="Naver Maps Crawler")
    
    # 검색어 인수
    parser.add_argument(
        'keyword', 
        type=str, 
        help="검색할 키워드"
    )
    
    # ChromeDriver 경로 인수
    parser.add_argument(
        'chromedriver_path', 
        type=str, 
        help="ChromeDriver 경로"
    )
    
    # 설정 파일 경로 인수
    parser.add_argument(
        '--config', 
        type=str, 
        default='./config.json', 
        help="설정 파일 경로 (기본값: ./config.json)"
    )
    
    # 헤드리스 모드 인수
    parser.add_argument(
        '--headless', 
        action='store_true', 
        help="헤드리스 모드로 실행"
    )
    
    # 출력 파일명 인수
    parser.add_argument(
        '--output', 
        type=str, 
        default='results.json', 
        help="결과를 저장할 파일명 (기본값: results.json)"
    )
    
    # 인수 파싱
    args = parser.parse_args()
    
    # 크롤러 실행
    crawler = NaverMapsCrawler(
        args.keyword, 
        args.chromedriver_path, 
        config_path=args.config, 
        headless=args.headless
    )
    crawler.crawling()
    crawler.save_results(filename=args.output)
    crawler.close()

if __name__ == '__main__':
    main()
