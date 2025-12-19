import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="상식 퀴즈",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS 스타일
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        text-align: center;
        color: #a0a0a0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .stButton > button {
        width: 100%;
        padding: 1.2rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        border: none;
        border-radius: 15px;
        margin: 5px 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    }
    
    .quiz-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .question-text {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 600;
        line-height: 1.6;
        text-align: center;
    }
    
    .progress-info {
        display: flex;
        justify-content: space-between;
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .progress-text { color: #48dbfb; font-weight: 600; }
    .score-text { color: #feca57; font-weight: 600; }
    
    .result-card {
        background: linear-gradient(135deg, rgba(72, 219, 251, 0.2) 0%, rgba(255, 159, 243, 0.2) 100%);
        border-radius: 25px;
        padding: 3rem;
        text-align: center;
        border: 2px solid rgba(255, 255, 255, 0.3);
        margin: 2rem 0;
    }
    
    .result-score {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #feca57, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .result-message { color: #ffffff; font-size: 1.5rem; font-weight: 600; }
    .result-category { color: #48dbfb; font-size: 1.2rem; }
    .percentage { color: #55efc4; font-size: 2rem; font-weight: 700; text-align: center; }
    .stars { text-align: center; font-size: 2rem; margin: 1rem 0; }
    
    h1, h2, h3 { color: #ffffff !important; }
    p { color: #e0e0e0; }
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    }
</style>
""", unsafe_allow_html=True)

# 퀴즈 데이터 - 각 카테고리 30문제
quiz_data = {
    "🎨 문화예술": [
        {"question": "빈센트 반 고흐의 대표작 '별이 빛나는 밤'은 어느 나라에서 그려졌을까요?", "options": ["네덜란드", "프랑스", "이탈리아", "스페인", "영국"], "answer": "프랑스", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/300px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg"},
        {"question": "세계 3대 박물관에 포함되지 않는 것은?", "options": ["루브르 박물관", "대영 박물관", "메트로폴리탄 박물관", "바티칸 박물관", "에르미타주 박물관"], "answer": "바티칸 박물관", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Louvre_Museum_Wikimedia_Commons.jpg/300px-Louvre_Museum_Wikimedia_Commons.jpg"},
        {"question": "베토벤의 교향곡 중 '운명'이라 불리는 곡은 몇 번일까요?", "options": ["3번", "5번", "7번", "9번", "6번"], "answer": "5번", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Beethoven.jpg/220px-Beethoven.jpg"},
        {"question": "레오나르도 다빈치의 '모나리자'가 소장된 박물관은?", "options": ["우피치 미술관", "루브르 박물관", "프라도 미술관", "대영 박물관", "메트로폴리탄 미술관"], "answer": "루브르 박물관", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg/220px-Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg"},
        {"question": "발레 '백조의 호수'를 작곡한 음악가는?", "options": ["모차르트", "바흐", "차이콥스키", "브람스", "슈베르트"], "answer": "차이콥스키", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Tchaikovsky_by_Reutlinger_%28cropped%29.jpg/220px-Tchaikovsky_by_Reutlinger_%28cropped%29.jpg"},
        {"question": "피카소가 창시한 미술 사조는?", "options": ["인상주의", "입체주의", "초현실주의", "표현주의", "다다이즘"], "answer": "입체주의", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Pablo_picasso_1.jpg/220px-Pablo_picasso_1.jpg"},
        {"question": "셰익스피어의 4대 비극에 포함되지 않는 작품은?", "options": ["햄릿", "오셀로", "리어왕", "맥베스", "로미오와 줄리엣"], "answer": "로미오와 줄리엣", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Shakespeare.jpg/220px-Shakespeare.jpg"},
        {"question": "오페라 '카르멘'을 작곡한 사람은?", "options": ["베르디", "푸치니", "비제", "로시니", "도니체티"], "answer": "비제", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Georges_Bizet.jpg/220px-Georges_Bizet.jpg"},
        {"question": "'진주 귀걸이를 한 소녀'를 그린 화가는?", "options": ["렘브란트", "베르메르", "루벤스", "반 다이크", "할스"], "answer": "베르메르", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/1665_Girl_with_a_Pearl_Earring.jpg/220px-1665_Girl_with_a_Pearl_Earring.jpg"},
        {"question": "뮤지컬 '오페라의 유령'의 작곡가는?", "options": ["스티븐 손드하임", "앤드루 로이드 웨버", "클로드 미셸 쇤베르크", "레너드 번스타인", "콜 포터"], "answer": "앤드루 로이드 웨버", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Andrew_Lloyd_Webber%2C_2017.jpg/220px-Andrew_Lloyd_Webber%2C_2017.jpg"},
        {"question": "고흐가 자신의 귀를 자른 도시는?", "options": ["파리", "암스테르담", "아를", "오베르", "생레미"], "answer": "아를", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project.jpg/220px-Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project.jpg"},
        {"question": "르네상스 미술의 3대 거장이 아닌 사람은?", "options": ["레오나르도 다빈치", "미켈란젤로", "라파엘로", "보티첼리", "도나텔로"], "answer": "보티첼리", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Sandro_Botticelli_-_La_nascita_di_Venere_-_Google_Art_Project_-_edited.jpg/300px-Sandro_Botticelli_-_La_nascita_di_Venere_-_Google_Art_Project_-_edited.jpg"},
        {"question": "'절규'를 그린 노르웨이 화가는?", "options": ["뭉크", "고갱", "세잔", "마네", "르누아르"], "answer": "뭉크", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg/220px-Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg"},
        {"question": "모차르트가 태어난 도시는?", "options": ["빈", "잘츠부르크", "뮌헨", "프라하", "베를린"], "answer": "잘츠부르크", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Wolfgang-amadeus-mozart_1.jpg/220px-Wolfgang-amadeus-mozart_1.jpg"},
        {"question": "'게르니카'를 그린 화가는?", "options": ["달리", "피카소", "미로", "고야", "벨라스케스"], "answer": "피카소", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Mural_del_Gernika.jpg/300px-Mural_del_Gernika.jpg"},
        {"question": "인상주의 화가가 아닌 사람은?", "options": ["모네", "르누아르", "드가", "반 고흐", "피카소"], "answer": "피카소", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Claude_Monet_-_Water_Lilies_-_1906%2C_Ryerson.jpg/300px-Claude_Monet_-_Water_Lilies_-_1906%2C_Ryerson.jpg"},
        {"question": "바흐의 출생 국가는?", "options": ["오스트리아", "독일", "이탈리아", "프랑스", "영국"], "answer": "독일", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Johann_Sebastian_Bach.jpg/220px-Johann_Sebastian_Bach.jpg"},
        {"question": "'최후의 심판'을 그린 화가는?", "options": ["레오나르도 다빈치", "미켈란젤로", "라파엘로", "보티첼리", "티치아노"], "answer": "미켈란젤로", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Creaci%C3%B3n_de_Ad%C3%A1n_%28Miguel_%C3%81ngel%29.jpg/300px-Creaci%C3%B3n_de_Ad%C3%A1n_%28Miguel_%C3%81ngel%29.jpg"},
        {"question": "비발디의 대표곡 '사계'는 몇 개의 협주곡으로 구성되어 있나요?", "options": ["2개", "4개", "6개", "8개", "12개"], "answer": "4개", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Vivaldi.jpg/220px-Vivaldi.jpg"},
        {"question": "뮤지컬 '레미제라블'의 원작 소설 작가는?", "options": ["찰스 디킨스", "빅토르 위고", "에밀 졸라", "알렉상드르 뒤마", "발자크"], "answer": "빅토르 위고", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Victor_Hugo_by_%C3%89tienne_Carjat_1876_-_full.jpg/220px-Victor_Hugo_by_%C3%89tienne_Carjat_1876_-_full.jpg"},
        {"question": "'키스'로 유명한 오스트리아 화가는?", "options": ["클림트", "실레", "코코슈카", "훈데르트바서", "뭉크"], "answer": "클림트", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Klimt_-_Der_Kuss.jpeg/220px-Klimt_-_Der_Kuss.jpeg"},
        {"question": "판소리 다섯 마당에 포함되지 않는 것은?", "options": ["춘향가", "심청가", "흥부가", "수궁가", "배비장전"], "answer": "배비장전", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Korean_pansori_singer.jpg/220px-Korean_pansori_singer.jpg"},
        {"question": "쇼팽의 출생 국가는?", "options": ["프랑스", "폴란드", "독일", "러시아", "오스트리아"], "answer": "폴란드", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Frederic_Chopin_photo.jpeg/220px-Frederic_Chopin_photo.jpeg"},
        {"question": "'시스티나 성당'의 천장화를 그린 화가는?", "options": ["레오나르도 다빈치", "미켈란젤로", "라파엘로", "카라바조", "베르니니"], "answer": "미켈란젤로", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Sistine_Chapel_ceiling_photo_2.jpg/300px-Sistine_Chapel_ceiling_photo_2.jpg"},
        {"question": "발레 '호두까기 인형'의 작곡가는?", "options": ["차이콥스키", "스트라빈스키", "프로코피예프", "라흐마니노프", "림스키코르사코프"], "answer": "차이콥스키", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Nutcracker_-_Scene_from_Act_II.jpg/300px-Nutcracker_-_Scene_from_Act_II.jpg"},
        {"question": "'해바라기' 연작으로 유명한 화가는?", "options": ["모네", "고흐", "세잔", "르누아르", "고갱"], "answer": "고흐", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Vincent_Willem_van_Gogh_127.jpg/220px-Vincent_Willem_van_Gogh_127.jpg"},
        {"question": "오페라 '투란도트'의 작곡가는?", "options": ["베르디", "푸치니", "로시니", "도니체티", "벨리니"], "answer": "푸치니", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Giacomo_Puccini_cropped.jpg/220px-Giacomo_Puccini_cropped.jpg"},
        {"question": "'아비뇽의 처녀들'을 그린 화가는?", "options": ["피카소", "달리", "마티스", "브라크", "레제"], "answer": "피카소", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Pablo_picasso_1.jpg/220px-Pablo_picasso_1.jpg"},
        {"question": "베토벤의 유일한 오페라 작품은?", "options": ["피가로의 결혼", "마술피리", "피델리오", "돈 조반니", "아이다"], "answer": "피델리오", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Beethoven.jpg/220px-Beethoven.jpg"},
        {"question": "'생각하는 사람'을 조각한 예술가는?", "options": ["미켈란젤로", "로댕", "베르니니", "도나텔로", "브랑쿠시"], "answer": "로댕", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Mus%C3%A9e_Rodin_1.jpg/220px-Mus%C3%A9e_Rodin_1.jpg"}
    ],
    "💰 경제": [
        {"question": "GDP는 무엇의 약자일까요?", "options": ["Gross Domestic Product", "General Development Plan", "Global Distribution Price", "Growth Domestic Percentage", "Grand Deposit Program"], "answer": "Gross Domestic Product", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Gdp_real_growth_rate_2007_CIA_Factbook.PNG/300px-Gdp_real_growth_rate_2007_CIA_Factbook.PNG"},
        {"question": "세계 최초의 주식회사는?", "options": ["영국 동인도회사", "네덜란드 동인도회사", "허드슨베이 회사", "스웨덴 동인도회사", "덴마크 동인도회사"], "answer": "네덜란드 동인도회사", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/VOC_Amsterdam.jpg/300px-VOC_Amsterdam.jpg"},
        {"question": "화폐 단위 '파운드'를 사용하는 나라는?", "options": ["독일", "프랑스", "영국", "이탈리아", "스페인"], "answer": "영국", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Bank_of_England_note.jpg/300px-Bank_of_England_note.jpg"},
        {"question": "인플레이션의 반대 개념은?", "options": ["스태그플레이션", "디플레이션", "리플레이션", "하이퍼인플레이션", "슬럼프플레이션"], "answer": "디플레이션", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/US_Inflation.png/300px-US_Inflation.png"},
        {"question": "비트코인을 만든 것으로 알려진 가명은?", "options": ["빌 게이츠", "일론 머스크", "사토시 나카모토", "스티브 잡스", "마크 저커버그"], "answer": "사토시 나카모토", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/225px-Bitcoin.svg.png"},
        {"question": "뉴욕 증권거래소가 위치한 거리 이름은?", "options": ["브로드웨이", "5번가", "월스트리트", "매디슨 애비뉴", "파크 애비뉴"], "answer": "월스트리트", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Wall_Street_Sign.jpg/220px-Wall_Street_Sign.jpg"},
        {"question": "FTA는 무엇의 약자일까요?", "options": ["Free Trade Agreement", "Foreign Trade Association", "Federal Tax Authority", "Financial Trading Act", "Future Trade Alliance"], "answer": "Free Trade Agreement", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/2010_World_Trade_Organization_Ministerial_Conference.jpg/300px-2010_World_Trade_Organization_Ministerial_Conference.jpg"},
        {"question": "경제 용어 '블랙스완'이 의미하는 것은?", "options": ["주가 폭락", "예측 불가능한 사건", "인플레이션", "경기 침체", "버블 경제"], "answer": "예측 불가능한 사건", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Cygnus_atratus_1.jpg/300px-Cygnus_atratus_1.jpg"},
        {"question": "한국은행이 설립된 연도는?", "options": ["1945년", "1948년", "1950년", "1953년", "1960년"], "answer": "1950년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Seal_of_the_Bank_of_Korea.svg/220px-Seal_of_the_Bank_of_Korea.svg.png"},
        {"question": "세계 3대 신용평가사가 아닌 것은?", "options": ["무디스", "S&P", "피치", "블룸버그", "모두 신용평가사"], "answer": "블룸버그", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Moody%27s_Corporation_logo.svg/250px-Moody%27s_Corporation_logo.svg.png"},
        {"question": "달러($) 기호의 기원이 된 통화는?", "options": ["영국 파운드", "독일 마르크", "스페인 페소", "프랑스 프랑", "네덜란드 길더"], "answer": "스페인 페소", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Dollar_sign.svg/150px-Dollar_sign.svg.png"},
        {"question": "IMF는 무엇의 약자인가요?", "options": ["International Monetary Fund", "International Market Finance", "Internal Money Flow", "Investment Management Fund", "International Money Federation"], "answer": "International Monetary Fund", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/International_Monetary_Fund_logo.svg/220px-International_Monetary_Fund_logo.svg.png"},
        {"question": "KOSPI는 어느 나라의 주가지수인가요?", "options": ["일본", "중국", "한국", "대만", "홍콩"], "answer": "한국", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Korea_Exchange_in_Seoul.jpg/300px-Korea_Exchange_in_Seoul.jpg"},
        {"question": "세계 최초의 중앙은행은?", "options": ["영란은행", "스웨덴 릭스방크", "미국 연방준비제도", "프랑스은행", "네덜란드은행"], "answer": "스웨덴 릭스방크", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Riksbankshuset.jpg/300px-Riksbankshuset.jpg"},
        {"question": "'보이지 않는 손'이라는 개념을 제시한 경제학자는?", "options": ["존 케인스", "애덤 스미스", "칼 마르크스", "밀턴 프리드먼", "데이비드 리카도"], "answer": "애덤 스미스", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/AdamSmith.jpg/220px-AdamSmith.jpg"},
        {"question": "OPEC은 무엇을 조절하는 기구인가요?", "options": ["금 가격", "원유 생산량", "환율", "금리", "곡물 가격"], "answer": "원유 생산량", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/OPEC_Logo.svg/220px-OPEC_Logo.svg.png"},
        {"question": "나스닥(NASDAQ)은 어느 나라의 주식시장인가요?", "options": ["영국", "일본", "미국", "독일", "중국"], "answer": "미국", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/NASDAQ_stock_market_display.jpg/300px-NASDAQ_stock_market_display.jpg"},
        {"question": "경기가 침체되고 물가가 오르는 현상을 무엇이라 하나요?", "options": ["인플레이션", "디플레이션", "스태그플레이션", "리세션", "디프레션"], "answer": "스태그플레이션", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/US_Inflation.png/300px-US_Inflation.png"},
        {"question": "세계은행(World Bank)의 본부 소재지는?", "options": ["뉴욕", "워싱턴 D.C.", "제네바", "런던", "파리"], "answer": "워싱턴 D.C.", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/World_Bank_building_at_Washington.jpg/300px-World_Bank_building_at_Washington.jpg"},
        {"question": "금본위제를 폐지한 미국 대통령은?", "options": ["루스벨트", "케네디", "닉슨", "레이건", "클린턴"], "answer": "닉슨", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Richard_Nixon_presidential_portrait_%281%29.jpg/220px-Richard_Nixon_presidential_portrait_%281%29.jpg"},
        {"question": "공급이 수요보다 많을 때 나타나는 현상은?", "options": ["가격 상승", "가격 하락", "가격 유지", "거래 중단", "인플레이션"], "answer": "가격 하락", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Supply-and-demand.svg/220px-Supply-and-demand.svg.png"},
        {"question": "한국의 기준금리를 결정하는 기관은?", "options": ["기획재정부", "금융위원회", "한국은행", "국회", "대통령"], "answer": "한국은행", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Seal_of_the_Bank_of_Korea.svg/220px-Seal_of_the_Bank_of_Korea.svg.png"},
        {"question": "주식 시장에서 '베어마켓'이란?", "options": ["상승장", "하락장", "횡보장", "급등장", "폭락장"], "answer": "하락장", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Charging_Bull_statue.jpg/300px-Charging_Bull_statue.jpg"},
        {"question": "경제 대공황이 시작된 연도는?", "options": ["1919년", "1929년", "1939년", "1949년", "1959년"], "answer": "1929년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Crowd_outside_nyse.jpg/300px-Crowd_outside_nyse.jpg"},
        {"question": "WTO의 본부 소재지는?", "options": ["뉴욕", "워싱턴 D.C.", "제네바", "브뤼셀", "파리"], "answer": "제네바", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/WTO_members_and_observers.svg/300px-WTO_members_and_observers.svg.png"},
        {"question": "유로화를 사용하지 않는 EU 회원국은?", "options": ["독일", "프랑스", "스웨덴", "이탈리아", "스페인"], "answer": "스웨덴", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Euro_banknotes_2002.png/300px-Euro_banknotes_2002.png"},
        {"question": "주식시장에서 PER은 무엇을 의미하나요?", "options": ["주가수익비율", "주가순자산비율", "자기자본이익률", "부채비율", "배당수익률"], "answer": "주가수익비율", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/NYSE_floor.jpg/300px-NYSE_floor.jpg"},
        {"question": "케인스 경제학의 핵심 주장은?", "options": ["자유방임", "정부 개입", "금본위제", "통화량 조절", "공급 중시"], "answer": "정부 개입", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/John_Maynard_Keynes.jpg/220px-John_Maynard_Keynes.jpg"},
        {"question": "1997년 한국 외환위기 당시 IMF 구제금융 규모는?", "options": ["약 100억 달러", "약 300억 달러", "약 550억 달러", "약 800억 달러", "약 1000억 달러"], "answer": "약 550억 달러", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/International_Monetary_Fund_logo.svg/220px-International_Monetary_Fund_logo.svg.png"},
        {"question": "애플이 주식 시장에 상장된 연도는?", "options": ["1976년", "1980년", "1984년", "1990년", "1995년"], "answer": "1980년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/195px-Apple_logo_black.svg.png"}
    ],
    "👤 인물": [
        {"question": "상대성 이론을 발표한 과학자는?", "options": ["아이작 뉴턴", "알베르트 아인슈타인", "닐스 보어", "막스 플랑크", "베르너 하이젠베르크"], "answer": "알베르트 아인슈타인", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Albert_Einstein_Head.jpg/220px-Albert_Einstein_Head.jpg"},
        {"question": "마이크로소프트의 창업자는?", "options": ["스티브 잡스", "빌 게이츠", "마크 저커버그", "제프 베조스", "일론 머스크"], "answer": "빌 게이츠", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Bill_Gates_2017_%28cropped%29.jpg/220px-Bill_Gates_2017_%28cropped%29.jpg"},
        {"question": "만유인력의 법칙을 발견한 과학자는?", "options": ["갈릴레오 갈릴레이", "아이작 뉴턴", "니콜라우스 코페르니쿠스", "요하네스 케플러", "티코 브라헤"], "answer": "아이작 뉴턴", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Portrait_of_Sir_Isaac_Newton%2C_1689.jpg/220px-Portrait_of_Sir_Isaac_Newton%2C_1689.jpg"},
        {"question": "'I have a dream' 연설로 유명한 인물은?", "options": ["넬슨 만델라", "마틴 루터 킹", "말콤 X", "버락 오바마", "로자 파크스"], "answer": "마틴 루터 킹", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Martin_Luther_King%2C_Jr..jpg/220px-Martin_Luther_King%2C_Jr..jpg"},
        {"question": "페이스북(메타)의 창업자는?", "options": ["잭 도시", "마크 저커버그", "에반 스피겔", "케빈 시스트롬", "잰 쿰"], "answer": "마크 저커버그", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Mark_Zuckerberg_F8_2019_Keynote_%2832830578717%29_%28cropped%29.jpg/220px-Mark_Zuckerberg_F8_2019_Keynote_%2832830578717%29_%28cropped%29.jpg"},
        {"question": "전구를 발명한 발명가는?", "options": ["니콜라 테슬라", "토마스 에디슨", "알렉산더 그레이엄 벨", "제임스 와트", "마이클 패러데이"], "answer": "토마스 에디슨", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Thomas_Edison2.jpg/220px-Thomas_Edison2.jpg"},
        {"question": "진화론을 주장한 과학자는?", "options": ["그레고어 멘델", "찰스 다윈", "루이 파스퇴르", "로버트 훅", "칼 린네"], "answer": "찰스 다윈", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Charles_Darwin_seated_crop.jpg/220px-Charles_Darwin_seated_crop.jpg"},
        {"question": "테슬라와 스페이스X의 CEO는?", "options": ["제프 베조스", "팀 쿡", "일론 머스크", "순다르 피차이", "사티아 나델라"], "answer": "일론 머스크", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Elon_Musk_Royal_Society_%28crop2%29.jpg/220px-Elon_Musk_Royal_Society_%28crop2%29.jpg"},
        {"question": "대한민국 초대 대통령은?", "options": ["김구", "이승만", "박정희", "윤보선", "장면"], "answer": "이승만", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Rhee_Syng-Man_in_1956.jpg/220px-Rhee_Syng-Man_in_1956.jpg"},
        {"question": "세종대왕이 창제한 것은?", "options": ["향찰", "이두", "구결", "훈민정음", "향가"], "answer": "훈민정음", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/King_Sejong_the_Great.jpg/220px-King_Sejong_the_Great.jpg"},
        {"question": "노벨상을 만든 알프레드 노벨이 발명한 것은?", "options": ["전화기", "다이너마이트", "라디오", "전구", "자동차"], "answer": "다이너마이트", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Alfred_Nobel_adjusted.jpg/220px-Alfred_Nobel_adjusted.jpg"},
        {"question": "인류 최초로 달에 발을 디딘 우주비행사는?", "options": ["버즈 올드린", "닐 암스트롱", "유리 가가린", "존 글렌", "앨런 셰퍼드"], "answer": "닐 암스트롱", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Neil_Armstrong_pose.jpg/220px-Neil_Armstrong_pose.jpg"},
        {"question": "페니실린을 발견한 과학자는?", "options": ["루이 파스퇴르", "알렉산더 플레밍", "로버트 코흐", "에드워드 제너", "조지프 리스터"], "answer": "알렉산더 플레밍", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Alexander_Fleming.jpg/220px-Alexander_Fleming.jpg"},
        {"question": "아마존의 창업자는?", "options": ["제프 베조스", "일론 머스크", "빌 게이츠", "마크 저커버그", "래리 페이지"], "answer": "제프 베조스", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Jeff_Bezos_visits_LAAFB_SMC_%283908618%29_%28cropped%29.jpeg/220px-Jeff_Bezos_visits_LAAFB_SMC_%283908618%29_%28cropped%29.jpeg"},
        {"question": "라듐을 발견한 여성 과학자는?", "options": ["마리 퀴리", "로잘린드 프랭클린", "도로시 호지킨", "리제 마이트너", "바버라 매클린톡"], "answer": "마리 퀴리", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Marie_Curie_c._1920s.jpg/220px-Marie_Curie_c._1920s.jpg"},
        {"question": "조선을 건국한 인물은?", "options": ["이성계", "이방원", "정도전", "이순신", "세종"], "answer": "이성계", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/King_Taejo_of_Joseon.jpg/220px-King_Taejo_of_Joseon.jpg"},
        {"question": "'국부론'의 저자는?", "options": ["존 로크", "애덤 스미스", "칼 마르크스", "존 케인스", "데이비드 흄"], "answer": "애덤 스미스", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/AdamSmith.jpg/220px-AdamSmith.jpg"},
        {"question": "구글의 공동 창업자가 아닌 사람은?", "options": ["래리 페이지", "세르게이 브린", "에릭 슈미트", "모두 창업자", "선다르 피차이"], "answer": "선다르 피차이", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Google_logo.svg/300px-Google_logo.svg.png"},
        {"question": "임진왜란 때 거북선을 만든 장군은?", "options": ["권율", "이순신", "원균", "이억기", "곽재우"], "answer": "이순신", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Yi_Sun-sin.jpg/220px-Yi_Sun-sin.jpg"},
        {"question": "지동설을 주장한 천문학자는?", "options": ["프톨레마이오스", "코페르니쿠스", "아리스토텔레스", "탈레스", "피타고라스"], "answer": "코페르니쿠스", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Nikolaus_Kopernikus.jpg/220px-Nikolaus_Kopernikus.jpg"},
        {"question": "전화기를 발명한 사람은?", "options": ["토마스 에디슨", "알렉산더 그레이엄 벨", "니콜라 테슬라", "구글리엘모 마르코니", "새뮤얼 모스"], "answer": "알렉산더 그레이엄 벨", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Alexander_Graham_Bell.jpg/220px-Alexander_Graham_Bell.jpg"},
        {"question": "현대그룹의 창업자는?", "options": ["이병철", "정주영", "구인회", "신격호", "조중훈"], "answer": "정주영", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Hyundai_logo.svg/220px-Hyundai_logo.svg.png"},
        {"question": "미국 독립선언서를 작성한 주요 인물은?", "options": ["조지 워싱턴", "토머스 제퍼슨", "벤자민 프랭클린", "존 애덤스", "제임스 매디슨"], "answer": "토머스 제퍼슨", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Official_Presidential_portrait_of_Thomas_Jefferson_%28by_Rembrandt_Peale%2C_1800%29%28cropped%29.jpg/220px-Official_Presidential_portrait_of_Thomas_Jefferson_%28by_Rembrandt_Peale%2C_1800%29%28cropped%29.jpg"},
        {"question": "정신분석학의 창시자는?", "options": ["칼 융", "지그문트 프로이트", "알프레드 아들러", "카렌 호나이", "에리히 프롬"], "answer": "지그문트 프로이트", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Sigmund_Freud%2C_by_Max_Halberstadt_%28cropped%29.jpg/220px-Sigmund_Freud%2C_by_Max_Halberstadt_%28cropped%29.jpg"},
        {"question": "삼성그룹의 창업자는?", "options": ["정주영", "이병철", "구인회", "최종건", "신격호"], "answer": "이병철", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Samsung_Logo.svg/220px-Samsung_Logo.svg.png"},
        {"question": "DNA 이중나선 구조를 발견한 과학자가 아닌 사람은?", "options": ["왓슨", "크릭", "프랭클린", "다윈", "윌킨스"], "answer": "다윈", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/DNA_Structure%2BKey%2BLabelled.pn_NoBB.png/220px-DNA_Structure%2BKey%2BLabelled.pn_NoBB.png"},
        {"question": "프랑스 황제가 된 군인은?", "options": ["루이 14세", "나폴레옹 보나파르트", "샤를마뉴", "잔 다르크", "드골"], "answer": "나폴레옹 보나파르트", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Jacques-Louis_David_-_The_Emperor_Napoleon_in_His_Study_at_the_Tuileries_-_Google_Art_Project.jpg/220px-Jacques-Louis_David_-_The_Emperor_Napoleon_in_His_Study_at_the_Tuileries_-_Google_Art_Project.jpg"},
        {"question": "간디가 이끈 비폭력 저항 운동은 어느 나라에서 일어났나요?", "options": ["파키스탄", "인도", "방글라데시", "스리랑카", "네팔"], "answer": "인도", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Portrait_Gandhi.jpg/220px-Portrait_Gandhi.jpg"},
        {"question": "인터넷(WWW)을 발명한 사람은?", "options": ["빌 게이츠", "스티브 잡스", "팀 버너스 리", "빈트 서프", "래리 페이지"], "answer": "팀 버너스 리", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Sir_Tim_Berners-Lee_%28cropped%29.jpg/220px-Sir_Tim_Berners-Lee_%28cropped%29.jpg"},
        {"question": "고려를 건국한 인물은?", "options": ["왕건", "궁예", "견훤", "장보고", "김유신"], "answer": "왕건", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Taejo_of_Goryeo.jpg/220px-Taejo_of_Goryeo.jpg"}
    ],
    "📚 역사": [
        {"question": "제2차 세계대전이 끝난 연도는?", "options": ["1943년", "1944년", "1945년", "1946년", "1947년"], "answer": "1945년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Bundesarchiv_Bild_183-H27798%2C_Warschau%2C_Parade_vor_Adolf_Hitler.jpg/300px-Bundesarchiv_Bild_183-H27798%2C_Warschau%2C_Parade_vor_Adolf_Hitler.jpg"},
        {"question": "프랑스 대혁명이 일어난 연도는?", "options": ["1776년", "1789년", "1799년", "1804년", "1815년"], "answer": "1789년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Eug%C3%A8ne_Delacroix_-_La_libert%C3%A9_guidant_le_peuple.jpg/300px-Eug%C3%A8ne_Delacroix_-_La_libert%C3%A9_guidant_le_peuple.jpg"},
        {"question": "고조선을 건국한 인물은?", "options": ["주몽", "단군왕검", "박혁거세", "온조", "김수로"], "answer": "단군왕검", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Dangun.jpg/220px-Dangun.jpg"},
        {"question": "베를린 장벽이 무너진 연도는?", "options": ["1987년", "1988년", "1989년", "1990년", "1991년"], "answer": "1989년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/West_and_East_Germans_at_the_Brandenburg_Gate_in_1989.jpg/300px-West_and_East_Germans_at_the_Brandenburg_Gate_in_1989.jpg"},
        {"question": "임진왜란이 일어난 연도는?", "options": ["1590년", "1592년", "1594년", "1596년", "1598년"], "answer": "1592년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Yi_Sun-sin.jpg/220px-Yi_Sun-sin.jpg"},
        {"question": "이집트 피라미드 중 가장 큰 것은?", "options": ["카프레 피라미드", "쿠푸 피라미드", "멘카우레 피라미드", "조세르 피라미드", "붉은 피라미드"], "answer": "쿠푸 피라미드", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Kheops-Pyramid.jpg/300px-Kheops-Pyramid.jpg"},
        {"question": "한국전쟁이 발발한 연도는?", "options": ["1948년", "1949년", "1950년", "1951년", "1952년"], "answer": "1950년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Korean_War_Montage_2.png/300px-Korean_War_Montage_2.png"},
        {"question": "로마 제국이 멸망한 연도는?", "options": ["376년", "410년", "455년", "476년", "500년"], "answer": "476년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Colosseum_in_Rome-April_2007-1-_copie_2B.jpg/300px-Colosseum_in_Rome-April_2007-1-_copie_2B.jpg"},
        {"question": "3.1 운동이 일어난 연도는?", "options": ["1910년", "1915년", "1919년", "1920년", "1945년"], "answer": "1919년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/March_1st_movement.jpg/300px-March_1st_movement.jpg"},
        {"question": "콜럼버스가 아메리카 대륙에 도착한 연도는?", "options": ["1490년", "1492년", "1494년", "1498년", "1500년"], "answer": "1492년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Christopher_Columbus.PNG/220px-Christopher_Columbus.PNG"},
        {"question": "동학농민운동이 일어난 연도는?", "options": ["1884년", "1889년", "1894년", "1896년", "1900년"], "answer": "1894년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Donghak_Peasant_Revolution.jpg/300px-Donghak_Peasant_Revolution.jpg"},
        {"question": "제1차 세계대전의 발단이 된 사건은?", "options": ["진주만 공습", "사라예보 사건", "베르사유 조약", "삼국동맹", "모로코 위기"], "answer": "사라예보 사건", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/DC-1914-27-d-Sarajevo-cropped.jpg/300px-DC-1914-27-d-Sarajevo-cropped.jpg"},
        {"question": "조선이 건국된 연도는?", "options": ["1388년", "1392년", "1398년", "1400년", "1405년"], "answer": "1392년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/King_Taejo_of_Joseon.jpg/220px-King_Taejo_of_Joseon.jpg"},
        {"question": "광복절은 몇 월 며칠인가요?", "options": ["3월 1일", "6월 6일", "8월 15일", "10월 3일", "10월 9일"], "answer": "8월 15일", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Flag_of_South_Korea.svg/300px-Flag_of_South_Korea.svg.png"},
        {"question": "고려가 건국된 연도는?", "options": ["892년", "900년", "918년", "935년", "940년"], "answer": "918년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Taejo_of_Goryeo.jpg/220px-Taejo_of_Goryeo.jpg"},
        {"question": "미국 남북전쟁이 끝난 연도는?", "options": ["1861년", "1863년", "1865년", "1867년", "1870년"], "answer": "1865년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Ulysses_S._Grant_1870-1880.jpg/220px-Ulysses_S._Grant_1870-1880.jpg"},
        {"question": "중국의 마지막 왕조는?", "options": ["명", "청", "송", "원", "당"], "answer": "청", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Flag_of_China_%281889%E2%80%931912%29.svg/300px-Flag_of_China_%281889%E2%80%931912%29.svg.png"},
        {"question": "일본의 진주만 공습이 일어난 연도는?", "options": ["1939년", "1940년", "1941년", "1942년", "1943년"], "answer": "1941년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/The_USS_Arizona_%28BB-39%29_burning_after_the_Japanese_attack_on_Pearl_Harbor_-_NARA_195617_-_Edit.jpg/300px-The_USS_Arizona_%28BB-39%29_burning_after_the_Japanese_attack_on_Pearl_Harbor_-_NARA_195617_-_Edit.jpg"},
        {"question": "인도가 영국에서 독립한 연도는?", "options": ["1945년", "1947년", "1949년", "1950년", "1952년"], "answer": "1947년", "image": "https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Flag_of_India.svg/300px-Flag_of_India.svg.png"},
        {"question": "십자군 전쟁이 시작된 연도는?", "options": ["1066년", "1096년", "1100년", "1150년", "1200년"], "answer": "1096년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Armoiries_de_J%C3%A9rusalem.svg/220px-Armoiries_de_J%C3%A9rusalem.svg.png"},
        {"question": "백제를 멸망시킨 나라는?", "options": ["고구려", "신라", "당", "신라와 당 연합군", "발해"], "answer": "신라와 당 연합군", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Baekje-monarchs%27_graves.jpg/300px-Baekje-monarchs%27-graves.jpg"},
        {"question": "을사조약이 체결된 연도는?", "options": ["1904년", "1905년", "1906년", "1907년", "1910년"], "answer": "1905년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/1905_Eulsa.jpg/300px-1905_Eulsa.jpg"},
        {"question": "명량대첩이 일어난 연도는?", "options": ["1592년", "1593년", "1597년", "1598년", "1600년"], "answer": "1597년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Yi_Sun-sin.jpg/220px-Yi_Sun-sin.jpg"},
        {"question": "미국 독립선언이 발표된 연도는?", "options": ["1774년", "1775년", "1776년", "1777년", "1778년"], "answer": "1776년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Declaration_of_Independence_%281819%29%2C_by_John_Trumbull.jpg/300px-Declaration_of_Independence_%281819%29%2C_by_John_Trumbull.jpg"},
        {"question": "러시아 혁명이 일어난 연도는?", "options": ["1905년", "1914년", "1917년", "1919년", "1921년"], "answer": "1917년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/300px-Flag_of_the_Soviet_Union.svg.png"},
        {"question": "통일신라가 삼국을 통일한 연도는?", "options": ["660년", "668년", "676년", "680년", "698년"], "answer": "676년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/National_museum_of_korea_silla_crown.jpg/220px-National_museum_of_korea_silla_crown.jpg"},
        {"question": "흑사병이 유럽에서 가장 크게 유행한 시기는?", "options": ["12세기", "13세기", "14세기", "15세기", "16세기"], "answer": "14세기", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Plague_in_Ashod.jpg/300px-Plague_in_Ashod.jpg"},
        {"question": "독일 통일이 이루어진 연도는?", "options": ["1988년", "1989년", "1990년", "1991년", "1992년"], "answer": "1990년", "image": "https://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Flag_of_Germany.svg/300px-Flag_of_Germany.svg.png"},
        {"question": "신라가 건국된 연도는?", "options": ["기원전 37년", "기원전 18년", "기원전 57년", "기원후 42년", "기원전 108년"], "answer": "기원전 57년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/National_museum_of_korea_silla_crown.jpg/220px-National_museum_of_korea_silla_crown.jpg"},
        {"question": "소련이 해체된 연도는?", "options": ["1989년", "1990년", "1991년", "1992년", "1993년"], "answer": "1991년", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/300px-Flag_of_the_Soviet_Union.svg.png"}
    ],
    "😜 넌센스": [
        {"question": "세상에서 가장 추운 바다는?", "options": ["북극해", "남극해", "썰렁해", "태평양", "대서양"], "answer": "썰렁해", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Frosty_Leaf.jpg/300px-Frosty_Leaf.jpg"},
        {"question": "미국에서 빨간 모자를 쓰면?", "options": ["예의바름", "멋짐", "미국빨간모자", "아메리카노", "레드캡"], "answer": "미국빨간모자", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Red_cap.svg/200px-Red_cap.svg.png"},
        {"question": "소금의 유통기한은?", "options": ["1년", "5년", "천일(1000일)", "무제한", "3년"], "answer": "천일(1000일)", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Salt_shaker_on_white_background.jpg/220px-Salt_shaker_on_white_background.jpg"},
        {"question": "아몬드가 죽으면?", "options": ["땅콩", "호두", "다이아몬드", "피스타치오", "캐슈넛"], "answer": "다이아몬드", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Almonds.jpg/250px-Almonds.jpg"},
        {"question": "세상에서 가장 빠른 닭은?", "options": ["번개닭", "로켓닭", "후라이드 치킨", "치타닭", "광속닭"], "answer": "후라이드 치킨", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good-Food-Display_-_NCI_Visuals_Online.jpg/250px-Good-Food-Display_-_NCI_Visuals_Online.jpg"},
        {"question": "반성문을 영어로 하면?", "options": ["Sorry Paper", "Apology Letter", "글로벌", "Regret Note", "Reflection Paper"], "answer": "글로벌", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Earth_Western_Hemisphere_transparent_background.png/220px-Earth_Western_Hemisphere_transparent_background.png"},
        {"question": "왕이 넘어지면?", "options": ["킹콩", "퀸", "킹받네", "왕실 추락", "킹덤"], "answer": "킹콩", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/King_Kong_Fay_Wray_1933.jpg/220px-King_Kong_Fay_Wray_1933.jpg"},
        {"question": "세상에서 가장 똑똑한 포유류는?", "options": ["돌고래", "침팬지", "포유류는 다 똑같음", "인간", "백수(100점짜리 짐승)"], "answer": "백수(100점짜리 짐승)", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg/250px-Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg"},
        {"question": "도둑이 가장 싫어하는 아이스크림은?", "options": ["초코", "바닐라", "딸기", "녹차", "누가바"], "answer": "누가바", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Ice_Cream_dessert_02.jpg/250px-Ice_Cream_dessert_02.jpg"},
        {"question": "네 살짜리 아이 대여섯 명은 몇 살?", "options": ["20살", "24살", "30살", "대여섯(5~6)살", "60살"], "answer": "대여섯(5~6)살", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Kids_playing_on_a_trampoline.jpg/250px-Kids_playing_on_a_trampoline.jpg"},
        {"question": "신데렐라가 물에 빠지면?", "options": ["젖데렐라", "수영렐라", "물데렐라", "익사렐라", "디즈니"], "answer": "젖데렐라", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Glass_slipper.png/200px-Glass_slipper.png"},
        {"question": "가장 듣기 싫은 말은?", "options": ["싫어", "꺼져", "당나귀", "못생겼어", "바보"], "answer": "당나귀", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Donkey_in_Clovelly%2C_North_Devon%2C_England.jpg/250px-Donkey_in_Clovelly%2C_North_Devon%2C_England.jpg"},
        {"question": "세상에서 가장 게으른 왕은?", "options": ["영국 왕", "잠자는 숲속의 왕", "누워있는 왕", "잠만 자는 왕", "슬리핑"], "answer": "슬리핑", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Smiley.svg/220px-Smiley.svg.png"},
        {"question": "공을 던지면 항상 돌아오는 이유는?", "options": ["바람", "중력", "공을 안 놓아서", "마법", "고무줄"], "answer": "공을 안 놓아서", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/250px-Good_Food_Display_-_NCI_Visuals_Online.jpg"},
        {"question": "바다에서 가장 힘센 생물은?", "options": ["고래", "상어", "문어", "오징어", "씰"], "answer": "씰", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/201408_seal.png/220px-201408_seal.png"},
        {"question": "개가 사람을 가르치면?", "options": ["강사", "견사", "훈련사", "독선생", "개같은 선생"], "answer": "독선생", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Husky_dog.jpg/250px-Husky_dog.jpg"},
        {"question": "세상에서 가장 맛있는 집은?", "options": ["한옥", "양옥", "초가집", "빌라", "맛있는 집"], "answer": "초가집", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Smiley.svg/220px-Smiley.svg.png"},
        {"question": "귤이 걸으면?", "options": ["귤러가다", "오렌지 워킹", "과일 산책", "감귤", "밀감"], "answer": "귤러가다", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Hapjeong-9.jpg/250px-Hapjeong-9.jpg"},
        {"question": "토끼가 비타민을 먹으면?", "options": ["건강토끼", "비타토끼", "토비타민", "타조", "영양토끼"], "answer": "타조", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Common_Ostrich.jpg/220px-Common_Ostrich.jpg"},
        {"question": "가수가 잠을 자면?", "options": ["꿀잠", "휴식", "잠자리", "잠", "레스토랑"], "answer": "레스토랑", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Smiley.svg/220px-Smiley.svg.png"},
        {"question": "닭이 알을 많이 낳으면?", "options": ["슈퍼닭", "산란기", "다산", "난계", "알부자"], "answer": "알부자", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Chicken_near_Akola_Rd_Aurangabad.jpg/250px-Chicken_near_Akola_Rd_Aurangabad.jpg"},
        {"question": "세상에서 제일 뜨거운 과일은?", "options": ["사과", "딸기", "파인애플", "망고", "천도복숭아"], "answer": "천도복숭아", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Autumn_Red_peaches.jpg/250px-Autumn_Red_peaches.jpg"},
        {"question": "오리가 얼면?", "options": ["오리콘", "얼음오리", "언오리", "꽁오리", "냉동오리"], "answer": "언오리", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Bucephala-clangula-010.jpg/250px-Bucephala-clangula-010.jpg"},
        {"question": "소나무가 죽으면?", "options": ["고사목", "죽은나무", "다이소나무", "관목", "묘목"], "answer": "다이소나무", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Japanese_Black_Pine.jpg/250px-Japanese_Black_Pine.jpg"},
        {"question": "세계에서 가장 억울한 사람은?", "options": ["무고한 사람", "피해자", "오해받는 사람", "억", "누명 쓴 사람"], "answer": "억", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Smiley.svg/220px-Smiley.svg.png"},
        {"question": "세상에서 가장 쉬운 숫자는?", "options": ["1", "0", "팔", "구", "영"], "answer": "팔", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Smiley.svg/220px-Smiley.svg.png"},
        {"question": "사슴이 뿔이 없으면?", "options": ["무뿔사슴", "암사슴", "사수", "사쁨", "노루"], "answer": "사쁨", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Red_deer_in_velvet.jpg/250px-Red_deer_in_velvet.jpg"},
        {"question": "세상에서 가장 힘센 피자는?", "options": ["페퍼로니", "하와이안", "불고기피자", "피자헛", "피자"], "answer": "피자", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/250px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
        {"question": "세상에서 가장 지루한 새는?", "options": ["비둘기", "참새", "지빠귀", "까치", "까마귀"], "answer": "지빠귀", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Camponotus_flavomarginatus_ant.jpg/250px-Camponotus_flavomarginatus_ant.jpg"},
        {"question": "빵이 넘어지면?", "options": ["빵야", "아프다", "부서진다", "식빵", "빵꾸러지다"], "answer": "빵꾸러지다", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_bread_05.jpg/250px-Fresh_made_bread_05.jpg"}
    ]
}

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'category' not in st.session_state:
    st.session_state.category = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None
if 'questions' not in st.session_state:
    st.session_state.questions = []

# 홈 페이지
def show_home():
    st.markdown('<h1 class="main-title">🧠 상식 퀴즈</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">당신의 상식을 테스트해보세요!</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="quiz-card">
        <p style="text-align: center; color: #ffffff;">
            📌 각 카테고리 <strong style="color: #feca57;">30문제</strong> 중 <strong style="color: #ff6b6b;">12문제</strong> 랜덤 출제 |
            📌 <strong style="color: #48dbfb;">5지선다</strong> 형식
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 카테고리 선택")
    
    for category in quiz_data.keys():
        if st.button(category, key=f"cat_{category}", use_container_width=True):
            st.session_state.category = category
            # 30문제 중 12문제 랜덤 선택
            all_questions = quiz_data[category].copy()
            random.shuffle(all_questions)
            st.session_state.questions = all_questions[:12]
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.page = 'quiz'
            st.rerun()

# 퀴즈 페이지
def show_quiz():
    category = st.session_state.category
    questions = st.session_state.questions
    current_q = st.session_state.current_question
    question_data = questions[current_q]
    
    st.markdown(f"### {category}")
    
    st.markdown(f"""
    <div class="progress-info">
        <span class="progress-text">📝 문제 {current_q + 1} / 12</span>
        <span class="score-text">⭐ 점수: {st.session_state.score}점</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress((current_q + 1) / 12)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image(question_data["image"], use_container_width=True)
        except:
            st.info("🖼️ 이미지를 불러올 수 없습니다.")
    
    st.markdown(f'<p class="question-text">Q{current_q + 1}. {question_data["question"]}</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if not st.session_state.answered:
        for i, option in enumerate(question_data["options"]):
            if st.button(f"{i+1}. {option}", key=f"opt_{i}", use_container_width=True):
                st.session_state.selected_answer = option
                st.session_state.answered = True
                if option == question_data["answer"]:
                    st.session_state.score += 1
                st.rerun()
    else:
        for i, option in enumerate(question_data["options"]):
            if option == question_data["answer"]:
                st.success(f"✅ {i+1}. {option} (정답)")
            elif option == st.session_state.selected_answer:
                st.error(f"❌ {i+1}. {option} (선택)")
            else:
                st.write(f"⬜ {i+1}. {option}")
        
        if st.session_state.selected_answer == question_data["answer"]:
            st.balloons()
            st.success("🎉 정답입니다!")
        else:
            st.error(f"😅 오답! 정답: {question_data['answer']}")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if current_q < 11:
                if st.button("다음 문제 ▶", use_container_width=True):
                    st.session_state.current_question += 1
                    st.session_state.answered = False
                    st.session_state.selected_answer = None
                    st.rerun()
            else:
                if st.button("🏆 결과 보기", use_container_width=True):
                    st.session_state.page = 'result'
                    st.rerun()
        
        with col2:
            if st.button("🏠 홈으로", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()

# 결과 페이지
def show_result():
    score = st.session_state.score
    category = st.session_state.category
    percentage = (score / 12) * 100
    
    if score == 12:
        message, stars = "완벽해요! 상식왕! 👑", "⭐⭐⭐⭐⭐"
        st.balloons()
    elif score >= 10:
        message, stars = "훌륭해요! 🌟", "⭐⭐⭐⭐"
    elif score >= 7:
        message, stars = "잘했어요! 👏", "⭐⭐⭐"
    elif score >= 4:
        message, stars = "괜찮아요! 💪", "⭐⭐"
    else:
        message, stars = "다시 도전! 📚", "⭐"
    
    st.markdown('<h1 class="main-title">🏆 퀴즈 완료!</h1>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="result-card">
        <p class="result-category">{category}</p>
        <p class="stars">{stars}</p>
        <p class="result-score">{score} / 12</p>
        <p class="result-message">{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<p class="percentage">📊 정답률: {percentage:.1f}%</p>', unsafe_allow_html=True)
    st.progress(score / 12)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 도전", use_container_width=True):
            # 다시 30문제 중 12문제 랜덤 선택
            all_questions = quiz_data[category].copy()
            random.shuffle(all_questions)
            st.session_state.questions = all_questions[:12]
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.page = 'quiz'
            st.rerun()
    with col2:
        if st.button("🏠 홈으로", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

# 메인
if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'quiz':
    show_quiz()
elif st.session_state.page == 'result':
    show_result()