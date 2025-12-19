import streamlit as st
import random
import time

st.set_page_config(page_title="상식 퀴즈", page_icon="🧠", layout="centered", initial_sidebar_state="expanded")

# 세션 상태 초기화
defaults = {'page': 'home', 'category': None, 'current_question': 0, 'score': 0, 'answered': False,
            'selected_answer': None, 'questions': [], 'dark_mode': True, 'hints_remaining': 3,
            'hint_used': False, 'hidden_options': [], 'start_time': None, 'time_up': False,
            'timer_enabled': True, 'time_limit': 15,
            'stats': {"🎨 문화예술": {"correct": 0, "total": 0}, "💰 경제": {"correct": 0, "total": 0},
                     "👤 인물": {"correct": 0, "total": 0}, "📚 역사": {"correct": 0, "total": 0},
                     "😜 넌센스": {"correct": 0, "total": 0}}}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# CSS
dark_css = """<style>
.stApp{background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460)}
.main-title{text-align:center;font-size:3rem;font-weight:800;background:linear-gradient(90deg,#ff6b6b,#feca57,#48dbfb,#ff9ff3);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.stButton>button{background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:15px;padding:1rem;font-size:1.1rem;font-weight:600}
.question-text{color:#fff;font-size:1.2rem;font-weight:600;text-align:center}
h1,h2,h3,p{color:#fff!important}
.timer-safe{background:linear-gradient(135deg,#00b894,#55efc4);padding:1rem;border-radius:10px;text-align:center;color:white;font-size:1.3rem;font-weight:bold}
.timer-warning{background:linear-gradient(135deg,#fdcb6e,#f39c12);padding:1rem;border-radius:10px;text-align:center;color:white;font-size:1.3rem;font-weight:bold}
.timer-danger{background:linear-gradient(135deg,#ff6b6b,#ee5a24);padding:1rem;border-radius:10px;text-align:center;color:white;font-size:1.3rem;font-weight:bold}
.explanation-box{background:linear-gradient(135deg,rgba(116,185,255,0.3),rgba(162,155,254,0.3));border-radius:15px;padding:1.5rem;margin:1rem 0;border-left:4px solid #74b9ff}
.result-score{font-size:3.5rem;font-weight:800;background:linear-gradient(90deg,#feca57,#ff6b6b);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
</style>"""

light_css = """<style>
.stApp{background:linear-gradient(135deg,#f5f7fa,#c3cfe2)}
.main-title{text-align:center;font-size:3rem;font-weight:800;background:linear-gradient(90deg,#e74c3c,#f39c12,#3498db,#9b59b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.stButton>button{background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:15px;padding:1rem;font-size:1.1rem;font-weight:600}
.question-text{color:#2c3e50;font-size:1.2rem;font-weight:600;text-align:center}
h1,h2,h3{color:#2c3e50!important}p{color:#555!important}
.timer-safe{background:linear-gradient(135deg,#00b894,#55efc4);padding:1rem;border-radius:10px;text-align:center;color:white;font-size:1.3rem;font-weight:bold}
.timer-warning{background:linear-gradient(135deg,#fdcb6e,#f39c12);padding:1rem;border-radius:10px;text-align:center;color:white;font-size:1.3rem;font-weight:bold}
.timer-danger{background:linear-gradient(135deg,#ff6b6b,#ee5a24);padding:1rem;border-radius:10px;text-align:center;color:white;font-size:1.3rem;font-weight:bold}
.explanation-box{background:linear-gradient(135deg,rgba(116,185,255,0.4),rgba(162,155,254,0.4));border-radius:15px;padding:1.5rem;margin:1rem 0;border-left:4px solid #3498db}
.result-score{font-size:3.5rem;font-weight:800;background:linear-gradient(90deg,#f39c12,#e74c3c);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
</style>"""

st.markdown(dark_css if st.session_state.dark_mode else light_css, unsafe_allow_html=True)

# 퀴즈 데이터 (해설 포함)
quiz_data = {
    "🎨 문화예술": [
        {"question": "빈센트 반 고흐의 '별이 빛나는 밤'은 어느 나라에서 그려졌나요?", "options": ["네덜란드", "프랑스", "이탈리아", "스페인", "영국"], "answer": "프랑스", "explanation": "고흐는 네덜란드 출신이지만, 이 작품(1889)은 프랑스 남부 생레미드프로방스의 정신병원에서 그렸습니다."},
        {"question": "세계 3대 박물관에 포함되지 않는 것은?", "options": ["루브르 박물관", "대영 박물관", "메트로폴리탄 박물관", "바티칸 박물관", "에르미타주 박물관"], "answer": "바티칸 박물관", "explanation": "세계 3대 박물관은 프랑스 루브르, 영국 대영 박물관, 미국 메트로폴리탄입니다."},
        {"question": "베토벤의 교향곡 중 '운명'이라 불리는 곡은?", "options": ["3번", "5번", "7번", "9번", "6번"], "answer": "5번", "explanation": "유명한 '빠빠빠빰' 도입부에 대해 베토벤이 '운명은 이렇게 문을 두드린다'고 말했다는 일화가 있어요."},
        {"question": "레오나르도 다빈치의 '모나리자'가 소장된 박물관은?", "options": ["우피치 미술관", "루브르 박물관", "프라도 미술관", "대영 박물관", "메트로폴리탄"], "answer": "루브르 박물관", "explanation": "다빈치가 프랑스 왕의 초청으로 가져간 후 프랑스 소유가 되어 파리 루브르에 있습니다."},
        {"question": "발레 '백조의 호수'를 작곡한 음악가는?", "options": ["모차르트", "바흐", "차이콥스키", "브람스", "슈베르트"], "answer": "차이콥스키", "explanation": "차이콥스키는 '백조의 호수', '호두까기 인형', '잠자는 숲속의 미녀' 3대 발레 음악을 모두 작곡했습니다."},
        {"question": "피카소가 창시한 미술 사조는?", "options": ["인상주의", "입체주의", "초현실주의", "표현주의", "다다이즘"], "answer": "입체주의", "explanation": "1907년경 조르주 브라크와 함께 입체주의(큐비즘)를 창시했습니다. 여러 각도에서 본 모습을 한 화면에 표현해요."},
        {"question": "셰익스피어의 4대 비극에 포함되지 않는 작품은?", "options": ["햄릿", "오셀로", "리어왕", "맥베스", "로미오와 줄리엣"], "answer": "로미오와 줄리엣", "explanation": "4대 비극은 햄릿, 오셀로, 리어왕, 맥베스입니다. 로미오와 줄리엣은 '비극적 로맨스'로 분류돼요."},
        {"question": "오페라 '카르멘'을 작곡한 사람은?", "options": ["베르디", "푸치니", "비제", "로시니", "도니체티"], "answer": "비제", "explanation": "프랑스 작곡가 조르주 비제가 1875년에 작곡했습니다. 현재 가장 많이 공연되는 오페라 중 하나예요."},
        {"question": "'진주 귀걸이를 한 소녀'를 그린 화가는?", "options": ["렘브란트", "베르메르", "루벤스", "반 다이크", "할스"], "answer": "베르메르", "explanation": "요하네스 베르메르의 1665년경 작품으로, '북유럽의 모나리자'라 불립니다."},
        {"question": "뮤지컬 '오페라의 유령'의 작곡가는?", "options": ["손드하임", "앤드루 로이드 웨버", "쇤베르크", "번스타인", "콜 포터"], "answer": "앤드루 로이드 웨버", "explanation": "1986년 초연 이후 브로드웨이 역사상 최장기 공연 기록을 세웠습니다."},
        {"question": "고흐가 자신의 귀를 자른 도시는?", "options": ["파리", "암스테르담", "아를", "오베르", "생레미"], "answer": "아를", "explanation": "1888년 프랑스 남부 아를에서 고갱과의 갈등 후 정신적 발작을 일으켜 귀 일부를 잘랐습니다."},
        {"question": "르네상스 3대 거장이 아닌 사람은?", "options": ["다빈치", "미켈란젤로", "라파엘로", "보티첼리", "도나텔로"], "answer": "보티첼리", "explanation": "3대 거장은 다빈치, 미켈란젤로, 라파엘로입니다. 보티첼리도 위대하지만 이 세 명의 영향력에는 미치지 못했어요."},
        {"question": "'절규'를 그린 노르웨이 화가는?", "options": ["뭉크", "고갱", "세잔", "마네", "르누아르"], "answer": "뭉크", "explanation": "에드바르 뭉크의 1893년 작품으로, 현대인의 불안과 공포를 상징합니다."},
        {"question": "모차르트가 태어난 도시는?", "options": ["빈", "잘츠부르크", "뮌헨", "프라하", "베를린"], "answer": "잘츠부르크", "explanation": "1756년 오스트리아 잘츠부르크에서 태어났습니다. 현재 그의 생가는 박물관이에요."},
        {"question": "'게르니카'를 그린 화가는?", "options": ["달리", "피카소", "미로", "고야", "벨라스케스"], "answer": "피카소", "explanation": "1937년 스페인 내전 중 나치 독일의 게르니카 폭격을 고발한 반전 그림입니다."},
        {"question": "인상주의 화가가 아닌 사람은?", "options": ["모네", "르누아르", "드가", "반 고흐", "피카소"], "answer": "피카소", "explanation": "피카소는 입체주의 화가입니다. 모네, 르누아르, 드가는 인상주의 대표 화가들이에요."},
        {"question": "바흐의 출생 국가는?", "options": ["오스트리아", "독일", "이탈리아", "프랑스", "영국"], "answer": "독일", "explanation": "1685년 독일 아이제나흐에서 태어났습니다. '음악의 아버지'로 불리며 바로크 음악을 완성했어요."},
        {"question": "'최후의 심판'을 그린 화가는?", "options": ["다빈치", "미켈란젤로", "라파엘로", "보티첼리", "티치아노"], "answer": "미켈란젤로", "explanation": "바티칸 시스티나 성당 제단 벽면에 그린 대작(1536-1541)으로, 300명 이상의 인물이 담겨 있어요."},
        {"question": "비발디의 '사계'는 몇 개의 협주곡으로 구성?", "options": ["2개", "4개", "6개", "8개", "12개"], "answer": "4개", "explanation": "봄, 여름, 가을, 겨울 4개의 바이올린 협주곡으로 구성됩니다."},
        {"question": "뮤지컬 '레미제라블' 원작 소설 작가는?", "options": ["디킨스", "빅토르 위고", "에밀 졸라", "뒤마", "발자크"], "answer": "빅토르 위고", "explanation": "1862년 출간된 프랑스 소설로, 장발장의 구원과 프랑스 혁명기 민중의 삶을 그렸습니다."},
        {"question": "'키스'로 유명한 오스트리아 화가는?", "options": ["클림트", "실레", "코코슈카", "훈데르트바서", "뭉크"], "answer": "클림트", "explanation": "구스타프 클림트의 1907-1908년 작품으로, 금박을 사용한 화려한 장식이 특징입니다."},
        {"question": "판소리 다섯 마당에 포함되지 않는 것은?", "options": ["춘향가", "심청가", "흥부가", "수궁가", "배비장전"], "answer": "배비장전", "explanation": "다섯 마당은 춘향가, 심청가, 흥부가, 수궁가(토끼전), 적벽가입니다."},
        {"question": "쇼팽의 출생 국가는?", "options": ["프랑스", "폴란드", "독일", "러시아", "오스트리아"], "answer": "폴란드", "explanation": "1810년 폴란드에서 태어났습니다. '피아노의 시인'으로 불리며, 20세 이후 주로 파리에서 활동했어요."},
        {"question": "시스티나 성당 천장화를 그린 화가는?", "options": ["다빈치", "미켈란젤로", "라파엘로", "카라바조", "베르니니"], "answer": "미켈란젤로", "explanation": "1508-1512년 4년에 걸쳐 완성했습니다. '아담의 창조' 등 성경 이야기를 담았어요."},
        {"question": "발레 '호두까기 인형' 작곡가는?", "options": ["차이콥스키", "스트라빈스키", "프로코피예프", "라흐마니노프", "림스키코르사코프"], "answer": "차이콥스키", "explanation": "1892년 초연된 크리스마스 발레의 정수입니다. '꽃의 왈츠'가 특히 유명해요."},
        {"question": "'해바라기' 연작으로 유명한 화가는?", "options": ["모네", "고흐", "세잔", "르누아르", "고갱"], "answer": "고흐", "explanation": "1888년 아를에서 고갱을 맞이하기 위해 그린 연작입니다. 노란색의 강렬한 표현이 특징이에요."},
        {"question": "오페라 '투란도트' 작곡가는?", "options": ["베르디", "푸치니", "로시니", "도니체티", "벨리니"], "answer": "푸치니", "explanation": "푸치니의 마지막 오페라로, 'Nessun Dorma(공주는 잠 못 이루고)'가 유명합니다."},
        {"question": "'아비뇽의 처녀들'을 그린 화가는?", "options": ["피카소", "달리", "마티스", "브라크", "레제"], "answer": "피카소", "explanation": "1907년 작품으로 입체주의의 시작을 알린 혁명적 그림입니다."},
        {"question": "베토벤의 유일한 오페라 작품은?", "options": ["피가로의 결혼", "마술피리", "피델리오", "돈 조반니", "아이다"], "answer": "피델리오", "explanation": "자유와 정의를 주제로, 부당하게 투옥된 남편을 구하는 아내의 이야기입니다."},
        {"question": "'생각하는 사람'을 조각한 예술가는?", "options": ["미켈란젤로", "로댕", "베르니니", "도나텔로", "브랑쿠시"], "answer": "로댕", "explanation": "오귀스트 로댕의 1880년대 작품으로, 인간의 사색과 고뇌를 표현한 근대 조각의 상징이에요."}
    ],
    "💰 경제": [
        {"question": "GDP는 무엇의 약자일까요?", "options": ["Gross Domestic Product", "General Development Plan", "Global Distribution Price", "Growth Domestic Percentage", "Grand Deposit Program"], "answer": "Gross Domestic Product", "explanation": "국내총생산으로, 한 나라 안에서 일정 기간 생산된 모든 재화와 서비스의 시장 가치 합계입니다."},
        {"question": "세계 최초의 주식회사는?", "options": ["영국 동인도회사", "네덜란드 동인도회사", "허드슨베이 회사", "스웨덴 동인도회사", "덴마크 동인도회사"], "answer": "네덜란드 동인도회사", "explanation": "1602년 설립된 VOC가 최초의 주식회사입니다. 주식 발행, 배당금 지급 등 현대 주식회사의 원형을 만들었어요."},
        {"question": "화폐 단위 '파운드'를 사용하는 나라는?", "options": ["독일", "프랑스", "영국", "이탈리아", "스페인"], "answer": "영국", "explanation": "영국 파운드(£)는 세계에서 가장 오래된 통화 중 하나로, EU 탈퇴 후에도 유로화를 채택하지 않았어요."},
        {"question": "인플레이션의 반대 개념은?", "options": ["스태그플레이션", "디플레이션", "리플레이션", "하이퍼인플레이션", "슬럼프플레이션"], "answer": "디플레이션", "explanation": "디플레이션은 물가가 지속적으로 하락하는 현상입니다. 일본의 '잃어버린 30년'이 대표적 사례예요."},
        {"question": "비트코인을 만든 것으로 알려진 가명은?", "options": ["빌 게이츠", "일론 머스크", "사토시 나카모토", "스티브 잡스", "마크 저커버그"], "answer": "사토시 나카모토", "explanation": "2008년 비트코인 백서를 발표한 인물의 가명입니다. 실제 정체는 아직 밝혀지지 않았어요."},
        {"question": "뉴욕 증권거래소가 위치한 거리는?", "options": ["브로드웨이", "5번가", "월스트리트", "매디슨 애비뉴", "파크 애비뉴"], "answer": "월스트리트", "explanation": "세계 금융의 중심지로, 17세기 네덜란드 식민지 시절 세운 방벽(wall)에서 이름이 유래했어요."},
        {"question": "FTA는 무엇의 약자일까요?", "options": ["Free Trade Agreement", "Foreign Trade Association", "Federal Tax Authority", "Financial Trading Act", "Future Trade Alliance"], "answer": "Free Trade Agreement", "explanation": "자유무역협정으로, 국가 간 관세와 무역 장벽을 줄이는 협정입니다."},
        {"question": "경제 용어 '블랙스완'이 의미하는 것은?", "options": ["주가 폭락", "예측 불가능한 사건", "인플레이션", "경기 침체", "버블 경제"], "answer": "예측 불가능한 사건", "explanation": "발생 가능성은 낮지만 일어나면 엄청난 충격을 주는 사건입니다. 2008년 금융위기가 대표적 예시예요."},
        {"question": "한국은행이 설립된 연도는?", "options": ["1945년", "1948년", "1950년", "1953년", "1960년"], "answer": "1950년", "explanation": "1950년 6월 12일 설립되었습니다. 물가 안정과 금융 안정을 담당하는 중앙은행이에요."},
        {"question": "세계 3대 신용평가사가 아닌 것은?", "options": ["무디스", "S&P", "피치", "블룸버그", "모두 신용평가사"], "answer": "블룸버그", "explanation": "무디스, S&P, 피치가 3대 신용평가사입니다. 블룸버그는 금융 정보 서비스 회사예요."},
        {"question": "달러($) 기호의 기원이 된 통화는?", "options": ["영국 파운드", "독일 마르크", "스페인 페소", "프랑스 프랑", "네덜란드 길더"], "answer": "스페인 페소", "explanation": "스페인 페소(peso)의 약자 PS가 겹쳐 쓰여 $가 되었다는 설이 유력합니다."},
        {"question": "IMF는 무엇의 약자인가요?", "options": ["International Monetary Fund", "International Market Finance", "Internal Money Flow", "Investment Management Fund", "International Money Federation"], "answer": "International Monetary Fund", "explanation": "국제통화기금으로, 회원국의 금융 위기 시 자금을 지원하는 역할을 합니다."},
        {"question": "KOSPI는 어느 나라의 주가지수?", "options": ["일본", "중국", "한국", "대만", "홍콩"], "answer": "한국", "explanation": "Korea Composite Stock Price Index의 약자로, 한국 유가증권시장의 대표 주가지수입니다."},
        {"question": "세계 최초의 중앙은행은?", "options": ["영란은행", "스웨덴 릭스방크", "미국 연방준비제도", "프랑스은행", "네덜란드은행"], "answer": "스웨덴 릭스방크", "explanation": "1668년 설립된 스웨덴 릭스방크가 세계 최초입니다. 노벨 경제학상도 릭스방크가 제정했어요."},
        {"question": "'보이지 않는 손' 개념을 제시한 경제학자는?", "options": ["존 케인스", "애덤 스미스", "칼 마르크스", "밀턴 프리드먼", "데이비드 리카도"], "answer": "애덤 스미스", "explanation": "1776년 '국부론'에서 제시한 자유시장경제의 핵심 원리입니다."},
        {"question": "OPEC은 무엇을 조절하는 기구?", "options": ["금 가격", "원유 생산량", "환율", "금리", "곡물 가격"], "answer": "원유 생산량", "explanation": "석유수출국기구로, 1960년 설립되어 원유 생산량을 조절해 국제 유가에 영향을 미칩니다."},
        {"question": "나스닥(NASDAQ)은 어느 나라의 주식시장?", "options": ["영국", "일본", "미국", "독일", "중국"], "answer": "미국", "explanation": "미국의 기술주 중심 주식시장으로, 애플, 마이크로소프트 등 빅테크 기업들이 상장되어 있어요."},
        {"question": "경기 침체+물가 상승 현상을 무엇이라 하나요?", "options": ["인플레이션", "디플레이션", "스태그플레이션", "리세션", "디프레션"], "answer": "스태그플레이션", "explanation": "경기침체(stagnation)+인플레이션(inflation)의 합성어로, 해결하기 가장 어려운 경제 상황이에요."},
        {"question": "세계은행의 본부 소재지는?", "options": ["뉴욕", "워싱턴 D.C.", "제네바", "런던", "파리"], "answer": "워싱턴 D.C.", "explanation": "1944년 설립된 국제 금융기구로, 개발도상국의 경제 발전을 지원합니다."},
        {"question": "금본위제를 폐지한 미국 대통령은?", "options": ["루스벨트", "케네디", "닉슨", "레이건", "클린턴"], "answer": "닉슨", "explanation": "1971년 달러-금 태환을 중지하며 금본위제가 종료되었습니다. '닉슨 쇼크'라 불려요."},
        {"question": "공급이 수요보다 많을 때 나타나는 현상은?", "options": ["가격 상승", "가격 하락", "가격 유지", "거래 중단", "인플레이션"], "answer": "가격 하락", "explanation": "수요-공급 법칙의 기본으로, 공급 과잉 시 판매자들이 경쟁적으로 가격을 낮춥니다."},
        {"question": "한국의 기준금리를 결정하는 기관은?", "options": ["기획재정부", "금융위원회", "한국은행", "국회", "대통령"], "answer": "한국은행", "explanation": "한국은행 금융통화위원회가 연 8회 기준금리를 결정합니다."},
        {"question": "주식 시장에서 '베어마켓'이란?", "options": ["상승장", "하락장", "횡보장", "급등장", "폭락장"], "answer": "하락장", "explanation": "곰(bear)이 앞발로 아래로 내리치는 모습에서 유래했습니다. 반대는 '불마켓'이에요."},
        {"question": "경제 대공황이 시작된 연도는?", "options": ["1919년", "1929년", "1939년", "1949년", "1959년"], "answer": "1929년", "explanation": "1929년 10월 미국 주식시장 폭락(검은 목요일)으로 시작된 세계적 경제 위기입니다."},
        {"question": "WTO의 본부 소재지는?", "options": ["뉴욕", "워싱턴 D.C.", "제네바", "브뤼셀", "파리"], "answer": "제네바", "explanation": "세계무역기구는 1995년 설립되어 스위스 제네바에 본부를 두고 있습니다."},
        {"question": "유로화를 사용하지 않는 EU 회원국은?", "options": ["독일", "프랑스", "스웨덴", "이탈리아", "스페인"], "answer": "스웨덴", "explanation": "스웨덴은 2003년 국민투표로 유로화 도입을 거부하고 자국 통화 크로나를 유지하고 있어요."},
        {"question": "주식시장에서 PER은 무엇을 의미?", "options": ["주가수익비율", "주가순자산비율", "자기자본이익률", "부채비율", "배당수익률"], "answer": "주가수익비율", "explanation": "Price Earnings Ratio의 약자로, 기업의 수익성 대비 주가가 적정한지 판단하는 지표예요."},
        {"question": "케인스 경제학의 핵심 주장은?", "options": ["자유방임", "정부 개입", "금본위제", "통화량 조절", "공급 중시"], "answer": "정부 개입", "explanation": "대공황 시기에 정부의 적극적인 재정정책으로 유효수요를 창출해야 한다고 주장했습니다."},
        {"question": "1997년 한국 IMF 구제금융 규모는?", "options": ["약 100억 달러", "약 300억 달러", "약 550억 달러", "약 800억 달러", "약 1000억 달러"], "answer": "약 550억 달러", "explanation": "1997년 12월 약 550억 달러를 받았고, 2001년 8월 조기 상환을 완료했어요."},
        {"question": "애플이 주식 시장에 상장된 연도는?", "options": ["1976년", "1980년", "1984년", "1990년", "1995년"], "answer": "1980년", "explanation": "1980년 12월 나스닥에 상장되어 역사상 가장 성공적인 IPO 중 하나가 되었습니다."}
    ],
    "👤 인물": [
        {"question": "상대성 이론을 발표한 과학자는?", "options": ["뉴턴", "아인슈타인", "닐스 보어", "막스 플랑크", "하이젠베르크"], "answer": "아인슈타인", "explanation": "1905년 특수상대성이론, 1915년 일반상대성이론을 발표했습니다. E=mc²로 유명해요."},
        {"question": "마이크로소프트의 창업자는?", "options": ["스티브 잡스", "빌 게이츠", "마크 저커버그", "제프 베조스", "일론 머스크"], "answer": "빌 게이츠", "explanation": "1975년 폴 앨런과 함께 창업했습니다. Windows와 Office로 개인용 컴퓨터 시대를 열었어요."},
        {"question": "만유인력의 법칙을 발견한 과학자는?", "options": ["갈릴레이", "뉴턴", "코페르니쿠스", "케플러", "티코 브라헤"], "answer": "뉴턴", "explanation": "전설에 따르면 사과가 떨어지는 것을 보고 영감을 얻었다고 해요."},
        {"question": "'I have a dream' 연설로 유명한 인물은?", "options": ["만델라", "마틴 루터 킹", "말콤 X", "오바마", "로자 파크스"], "answer": "마틴 루터 킹", "explanation": "1963년 워싱턴 행진에서 한 연설입니다. 비폭력 저항으로 미국 흑인 인권 운동을 이끌었어요."},
        {"question": "페이스북(메타)의 창업자는?", "options": ["잭 도시", "마크 저커버그", "에반 스피겔", "케빈 시스트롬", "잰 쿰"], "answer": "마크 저커버그", "explanation": "2004년 하버드대 재학 중 창업해 세계 최연소 억만장자가 되었습니다."},
        {"question": "전구를 발명한 발명가는?", "options": ["니콜라 테슬라", "토마스 에디슨", "벨", "제임스 와트", "패러데이"], "answer": "토마스 에디슨", "explanation": "1879년 실용적인 백열전구를 발명했습니다. 1,000개 이상의 특허를 보유한 '발명왕'이에요."},
        {"question": "진화론을 주장한 과학자는?", "options": ["멘델", "찰스 다윈", "파스퇴르", "로버트 훅", "칼 린네"], "answer": "찰스 다윈", "explanation": "1859년 '종의 기원'에서 자연선택에 의한 진화론을 발표했습니다."},
        {"question": "테슬라와 스페이스X의 CEO는?", "options": ["제프 베조스", "팀 쿡", "일론 머스크", "순다르 피차이", "사티아 나델라"], "answer": "일론 머스크", "explanation": "남아공 출신으로 전기차, 우주개발, 뇌-컴퓨터 인터페이스 등 다양한 사업을 이끌고 있어요."},
        {"question": "대한민국 초대 대통령은?", "options": ["김구", "이승만", "박정희", "윤보선", "장면"], "answer": "이승만", "explanation": "1948년 제헌국회에서 선출되어 1960년까지 재임했습니다. 독립운동가 출신이에요."},
        {"question": "세종대왕이 창제한 것은?", "options": ["향찰", "이두", "구결", "훈민정음", "향가"], "answer": "훈민정음", "explanation": "1443년 창제, 1446년 반포되었습니다. '백성을 가르치는 바른 소리'라는 뜻이에요."},
        {"question": "노벨상을 만든 알프레드 노벨이 발명한 것은?", "options": ["전화기", "다이너마이트", "라디오", "전구", "자동차"], "answer": "다이너마이트", "explanation": "1867년 발명해 부를 쌓았지만, 전쟁에 사용되는 것에 회의를 느껴 노벨상을 제정했어요."},
        {"question": "인류 최초로 달에 발을 디딘 우주비행사는?", "options": ["버즈 올드린", "닐 암스트롱", "유리 가가린", "존 글렌", "앨런 셰퍼드"], "answer": "닐 암스트롱", "explanation": "1969년 7월 20일 '한 인간에게는 작은 발걸음이지만, 인류에게는 거대한 도약'이라고 말했어요."},
        {"question": "페니실린을 발견한 과학자는?", "options": ["파스퇴르", "알렉산더 플레밍", "로버트 코흐", "에드워드 제너", "리스터"], "answer": "알렉산더 플레밍", "explanation": "1928년 우연히 곰팡이가 세균을 죽이는 것을 발견해 항생제 시대를 열었습니다."},
        {"question": "아마존의 창업자는?", "options": ["제프 베조스", "일론 머스크", "빌 게이츠", "마크 저커버그", "래리 페이지"], "answer": "제프 베조스", "explanation": "1994년 온라인 서점으로 시작해 세계 최대 전자상거래 기업으로 성장시켰습니다."},
        {"question": "라듐을 발견한 여성 과학자는?", "options": ["마리 퀴리", "로잘린드 프랭클린", "도로시 호지킨", "리제 마이트너", "매클린톡"], "answer": "마리 퀴리", "explanation": "노벨 물리학상(1903)과 화학상(1911)을 모두 받은 최초의 인물입니다."},
        {"question": "조선을 건국한 인물은?", "options": ["이성계", "이방원", "정도전", "이순신", "세종"], "answer": "이성계", "explanation": "1392년 고려를 멸하고 조선을 건국했습니다. 위화도 회군으로 권력을 잡았어요."},
        {"question": "'국부론'의 저자는?", "options": ["존 로크", "애덤 스미스", "칼 마르크스", "존 케인스", "데이비드 흄"], "answer": "애덤 스미스", "explanation": "1776년 출간해 '경제학의 아버지'로 불립니다. 자유시장경제를 주장했어요."},
        {"question": "구글의 공동 창업자가 아닌 사람은?", "options": ["래리 페이지", "세르게이 브린", "에릭 슈미트", "모두 창업자", "선다르 피차이"], "answer": "선다르 피차이", "explanation": "1998년 래리 페이지와 세르게이 브린이 스탠퍼드대 재학 중 창업했습니다."},
        {"question": "임진왜란 때 거북선을 만든 장군은?", "options": ["권율", "이순신", "원균", "이억기", "곽재우"], "answer": "이순신", "explanation": "23전 23승을 거둔 명장입니다. 거북선을 활용한 해전으로 일본 수군을 격파했어요."},
        {"question": "지동설을 주장한 천문학자는?", "options": ["프톨레마이오스", "코페르니쿠스", "아리스토텔레스", "탈레스", "피타고라스"], "answer": "코페르니쿠스", "explanation": "1543년 지구가 태양 주위를 돈다는 지동설을 발표해 과학 혁명의 시작이 되었어요."},
        {"question": "전화기를 발명한 사람은?", "options": ["에디슨", "알렉산더 그레이엄 벨", "테슬라", "마르코니", "새뮤얼 모스"], "answer": "알렉산더 그레이엄 벨", "explanation": "1876년 전화기 특허를 획득했습니다. 청각 장애인 교육자로도 활동했어요."},
        {"question": "현대그룹의 창업자는?", "options": ["이병철", "정주영", "구인회", "신격호", "조중훈"], "answer": "정주영", "explanation": "1946년 현대토건으로 시작했습니다. '이봐, 해봤어?' 정신으로 유명해요."},
        {"question": "미국 독립선언서를 작성한 주요 인물은?", "options": ["조지 워싱턴", "토머스 제퍼슨", "벤자민 프랭클린", "존 애덤스", "매디슨"], "answer": "토머스 제퍼슨", "explanation": "1776년 초안을 작성했고, 제3대 대통령이 되었습니다."},
        {"question": "정신분석학의 창시자는?", "options": ["칼 융", "지그문트 프로이트", "아들러", "카렌 호나이", "에리히 프롬"], "answer": "지그문트 프로이트", "explanation": "무의식, 꿈의 해석, 오이디푸스 콤플렉스 등의 개념을 제시했습니다."},
        {"question": "삼성그룹의 창업자는?", "options": ["정주영", "이병철", "구인회", "최종건", "신격호"], "answer": "이병철", "explanation": "1938년 삼성상회로 시작했습니다. '호암'이라는 호를 사용했어요."},
        {"question": "DNA 이중나선 발견과 관계없는 사람은?", "options": ["왓슨", "크릭", "프랭클린", "다윈", "윌킨스"], "answer": "다윈", "explanation": "1953년 왓슨과 크릭이 발표했습니다. 로잘린드 프랭클린의 X선 사진이 결정적 역할을 했어요."},
        {"question": "프랑스 황제가 된 군인은?", "options": ["루이 14세", "나폴레옹", "샤를마뉴", "잔 다르크", "드골"], "answer": "나폴레옹", "explanation": "코르시카 출신 군인으로, 1804년 황제에 즉위해 유럽 대부분을 정복했습니다."},
        {"question": "간디의 비폭력 운동은 어느 나라에서?", "options": ["파키스탄", "인도", "방글라데시", "스리랑카", "네팔"], "answer": "인도", "explanation": "비폭력·불복종 운동으로 영국 식민 지배에 저항해 1947년 인도 독립을 이끌어냈어요."},
        {"question": "월드와이드웹(WWW)을 발명한 사람은?", "options": ["빌 게이츠", "스티브 잡스", "팀 버너스 리", "빈트 서프", "래리 페이지"], "answer": "팀 버너스 리", "explanation": "1989년 CERN에서 WWW를 개발했습니다. HTTP, HTML, URL 등을 만들고 특허 없이 공개했어요."},
        {"question": "고려를 건국한 인물은?", "options": ["왕건", "궁예", "견훤", "장보고", "김유신"], "answer": "왕건", "explanation": "918년 궁예를 몰아내고 고려를 건국했습니다. 후삼국을 통일했어요."}
    ],
    "📚 역사": [
        {"question": "제2차 세계대전이 끝난 연도는?", "options": ["1943년", "1944년", "1945년", "1946년", "1947년"], "answer": "1945년", "explanation": "1945년 5월 독일 항복, 8월 일본 항복으로 끝났습니다. 히로시마·나가사키 원폭 투하 후였어요."},
        {"question": "프랑스 대혁명이 일어난 연도는?", "options": ["1776년", "1789년", "1799년", "1804년", "1815년"], "answer": "1789년", "explanation": "1789년 7월 14일 바스티유 감옥 습격으로 시작되었습니다. '자유, 평등, 박애' 이념의 시작이에요."},
        {"question": "고조선을 건국한 인물은?", "options": ["주몽", "단군왕검", "박혁거세", "온조", "김수로"], "answer": "단군왕검", "explanation": "기원전 2333년 건국했다고 전해집니다. 이 날이 개천절(10월 3일)이에요."},
        {"question": "베를린 장벽이 무너진 연도는?", "options": ["1987년", "1988년", "1989년", "1990년", "1991년"], "answer": "1989년", "explanation": "1989년 11월 9일 동독 정부의 여행 자유화 발표 후 시민들이 장벽을 허물었습니다. 냉전 종식의 상징이에요."},
        {"question": "임진왜란이 일어난 연도는?", "options": ["1590년", "1592년", "1594년", "1596년", "1598년"], "answer": "1592년", "explanation": "1592년 일본의 도요토미 히데요시가 조선을 침략했습니다. 7년 만에 격퇴했어요."},
        {"question": "이집트 피라미드 중 가장 큰 것은?", "options": ["카프레", "쿠푸", "멘카우레", "조세르", "붉은 피라미드"], "answer": "쿠푸", "explanation": "기자의 대피라미드로, 높이 146m, 230만 개의 석재 블록으로 이루어진 세계 7대 불가사의예요."},
        {"question": "한국전쟁이 발발한 연도는?", "options": ["1948년", "1949년", "1950년", "1951년", "1952년"], "answer": "1950년", "explanation": "1950년 6월 25일 북한의 남침으로 시작되었습니다. 1953년 휴전협정이 체결되었어요."},
        {"question": "로마 제국이 멸망한 연도는?", "options": ["376년", "410년", "455년", "476년", "500년"], "answer": "476년", "explanation": "476년 게르만 용병대장 오도아케르가 서로마 황제를 폐위시켰습니다."},
        {"question": "3.1 운동이 일어난 연도는?", "options": ["1910년", "1915년", "1919년", "1920년", "1945년"], "answer": "1919년", "explanation": "1919년 3월 1일 일제 강점기에 일어난 대규모 독립운동입니다. 200만 명 이상이 참여했어요."},
        {"question": "콜럼버스가 아메리카에 도착한 연도는?", "options": ["1490년", "1492년", "1494년", "1498년", "1500년"], "answer": "1492년", "explanation": "1492년 10월 12일 바하마 제도에 도착했습니다. 인도로 가는 서쪽 항로를 찾다가 발견했어요."},
        {"question": "동학농민운동이 일어난 연도는?", "options": ["1884년", "1889년", "1894년", "1896년", "1900년"], "answer": "1894년", "explanation": "1894년 전봉준을 중심으로 일어난 농민 봉기입니다. 반봉건·반외세를 외쳤어요."},
        {"question": "제1차 세계대전의 발단이 된 사건은?", "options": ["진주만 공습", "사라예보 사건", "베르사유 조약", "삼국동맹", "모로코 위기"], "answer": "사라예보 사건", "explanation": "1914년 오스트리아-헝가리 황태자 부부가 세르비아계 청년에게 암살당했습니다."},
        {"question": "조선이 건국된 연도는?", "options": ["1388년", "1392년", "1398년", "1400년", "1405년"], "answer": "1392년", "explanation": "1392년 이성계가 고려를 멸하고 조선을 건국했습니다. 505년간 존속했어요."},
        {"question": "광복절은 몇 월 며칠인가요?", "options": ["3월 1일", "6월 6일", "8월 15일", "10월 3일", "10월 9일"], "answer": "8월 15일", "explanation": "1945년 8월 15일 일본이 항복하면서 한국이 독립했습니다. '빛을 되찾은 날'이에요."},
        {"question": "고려가 건국된 연도는?", "options": ["892년", "900년", "918년", "935년", "940년"], "answer": "918년", "explanation": "918년 왕건이 궁예를 몰아내고 고려를 건국했습니다. 약 470년간 지속되었어요."},
        {"question": "미국 남북전쟁이 끝난 연도는?", "options": ["1861년", "1863년", "1865년", "1867년", "1870년"], "answer": "1865년", "explanation": "1865년 남부 연합군의 항복으로 끝났습니다. 노예제 폐지를 둘러싼 전쟁이었어요."},
        {"question": "중국의 마지막 왕조는?", "options": ["명", "청", "송", "원", "당"], "answer": "청", "explanation": "1644년부터 1912년까지 존속한 만주족의 왕조입니다. 신해혁명으로 막을 내렸어요."},
        {"question": "일본의 진주만 공습이 일어난 연도는?", "options": ["1939년", "1940년", "1941년", "1942년", "1943년"], "answer": "1941년", "explanation": "1941년 12월 7일 일본이 하와이 진주만을 기습 공격해 미국이 2차 대전에 참전했습니다."},
        {"question": "인도가 영국에서 독립한 연도는?", "options": ["1945년", "1947년", "1949년", "1950년", "1952년"], "answer": "1947년", "explanation": "1947년 8월 15일 독립했습니다. 동시에 파키스탄과 분리되어 종교 분쟁이 일어났어요."},
        {"question": "십자군 전쟁이 시작된 연도는?", "options": ["1066년", "1096년", "1100년", "1150년", "1200년"], "answer": "1096년", "explanation": "1096년 교황 우르바노 2세의 호소로 시작된 종교 전쟁입니다. 약 200년간 8차례 진행되었어요."},
        {"question": "백제를 멸망시킨 나라는?", "options": ["고구려", "신라", "당", "신라와 당 연합군", "발해"], "answer": "신라와 당 연합군", "explanation": "660년 나당 연합군이 백제를 멸망시켰습니다. 의자왕이 항복했어요."},
        {"question": "을사조약이 체결된 연도는?", "options": ["1904년", "1905년", "1906년", "1907년", "1910년"], "answer": "1905년", "explanation": "1905년 일본이 강압적으로 체결한 조약으로, 대한제국의 외교권을 박탈했습니다."},
        {"question": "명량대첩이 일어난 연도는?", "options": ["1592년", "1593년", "1597년", "1598년", "1600년"], "answer": "1597년", "explanation": "1597년 이순신 장군이 13척의 배로 일본 함대 133척을 격파한 해전입니다."},
        {"question": "미국 독립선언이 발표된 연도는?", "options": ["1774년", "1775년", "1776년", "1777년", "1778년"], "answer": "1776년", "explanation": "1776년 7월 4일 영국으로부터의 독립을 선언했습니다. 미국 독립기념일이에요."},
        {"question": "러시아 혁명이 일어난 연도는?", "options": ["1905년", "1914년", "1917년", "1919년", "1921년"], "answer": "1917년", "explanation": "1917년 볼셰비키 혁명으로 로마노프 왕조가 무너지고 세계 최초 사회주의 국가가 탄생했어요."},
        {"question": "통일신라가 삼국을 통일한 연도는?", "options": ["660년", "668년", "676년", "680년", "698년"], "answer": "676년", "explanation": "676년 신라가 당나라 세력을 한반도에서 축출하며 삼국 통일을 완성했습니다."},
        {"question": "흑사병이 유럽에서 가장 크게 유행한 시기는?", "options": ["12세기", "13세기", "14세기", "15세기", "16세기"], "answer": "14세기", "explanation": "1347-1351년 유럽 인구의 30-60%가 사망했습니다. 중세 유럽 사회를 변화시킨 대재앙이에요."},
        {"question": "독일 통일이 이루어진 연도는?", "options": ["1988년", "1989년", "1990년", "1991년", "1992년"], "answer": "1990년", "explanation": "1990년 10월 3일 동독이 서독에 편입되며 통일되었습니다. 베를린 장벽 붕괴 후 1년 만이에요."},
        {"question": "신라가 건국된 연도는?", "options": ["기원전 37년", "기원전 18년", "기원전 57년", "기원후 42년", "기원전 108년"], "answer": "기원전 57년", "explanation": "기원전 57년 박혁거세가 건국했다고 전해집니다. 992년간 존속한 가장 오래된 왕조예요."},
        {"question": "소련이 해체된 연도는?", "options": ["1989년", "1990년", "1991년", "1992년", "1993년"], "answer": "1991년", "explanation": "1991년 12월 25일 소련이 공식 해체되며 냉전이 종식되었습니다. 15개 공화국이 독립했어요."}
    ],
    "😜 넌센스": [
        {"question": "세상에서 가장 추운 바다는?", "options": ["북극해", "남극해", "썰렁해", "태평양", "대서양"], "answer": "썰렁해", "explanation": "'썰렁하다'의 '썰렁'과 바다 '해(海)'를 합친 말장난이에요! 😄"},
        {"question": "미국에서 빨간 모자를 쓰면?", "options": ["예의바름", "멋짐", "미국빨간모자", "아메리카노", "레드캡"], "answer": "미국빨간모자", "explanation": "'아메리카(미국) + 빨간모자'를 합친 말장난! 동화 '빨간 모자'가 생각나죠? 🎩"},
        {"question": "소금의 유통기한은?", "options": ["1년", "5년", "천일(1000일)", "무제한", "3년"], "answer": "천일(1000일)", "explanation": "'천일염(千日鹽)'에서 따온 말장난! 실제 소금은 거의 무제한 보관 가능해요. 🧂"},
        {"question": "아몬드가 죽으면?", "options": ["땅콩", "호두", "다이아몬드", "피스타치오", "캐슈넛"], "answer": "다이아몬드", "explanation": "'다이(die, 죽다) + 아몬드'로 다이아몬드! 영어와 한글을 섞은 말장난이에요. 💎"},
        {"question": "세상에서 가장 빠른 닭은?", "options": ["번개닭", "로켓닭", "후라이드 치킨", "치타닭", "광속닭"], "answer": "후라이드 치킨", "explanation": "'훨훨 날아간다(fly)'와 '치킨'을 합친 Fried Chicken! 🍗"},
        {"question": "반성문을 영어로 하면?", "options": ["Sorry Paper", "Apology Letter", "글로벌", "Regret Note", "Reflection Paper"], "answer": "글로벌", "explanation": "'글로 벌(罰)받는다'는 뜻의 말장난! 반성문은 글로 벌을 받는 거니까요. 📝"},
        {"question": "왕이 넘어지면?", "options": ["킹콩", "퀸", "킹받네", "왕실 추락", "킹덤"], "answer": "킹콩", "explanation": "'King(왕) + 쿵(넘어지는 소리)'으로 킹콩! 🦍"},
        {"question": "세상에서 가장 똑똒한 포유류는?", "options": ["돌고래", "침팬지", "다 똑같음", "인간", "백수"], "answer": "백수", "explanation": "'백점(100점) + 짐승 = 백수!' 시험 만점과 연결한 말장난이에요. 🦁"},
        {"question": "도둑이 가장 싫어하는 아이스크림은?", "options": ["초코", "바닐라", "딸기", "녹차", "누가바"], "answer": "누가바", "explanation": "'누가 봐(누군가 본다)'와 발음이 같아요. 도둑은 누가 보는 걸 제일 싫어하죠! 🍦"},
        {"question": "네 살짜리 아이 대여섯 명은 몇 살?", "options": ["20살", "24살", "30살", "대여섯살", "60살"], "answer": "대여섯살", "explanation": "함정 문제! '대여섯'은 5~6을 뜻하는 말이에요. 네 살이 아니라 대여섯 살인 아이들! 👶"},
        {"question": "신데렐라가 물에 빠지면?", "options": ["젖데렐라", "수영렐라", "물데렐라", "익사렐라", "디즈니"], "answer": "젖데렐라", "explanation": "'신(新, 새로운) → 젖(젖은)'으로 바꾼 말장난! 물에 빠지면 젖으니까요. 👗"},
        {"question": "가장 듣기 싫은 말은?", "options": ["싫어", "꺼져", "당나귀", "못생겼어", "바보"], "answer": "당나귀", "explanation": "'당나 귀(당신의 귀)'처럼 들려요. 듣기 싫은 '귀'라는 말장난! 🫏"},
        {"question": "세상에서 가장 게으른 왕은?", "options": ["영국 왕", "잠자는 왕", "누워있는 왕", "잠만 자는 왕", "슬리핑"], "answer": "슬리핑", "explanation": "'Sleeping(자는) + King(왕)'을 합쳐 읽으면 슬리핑! 😴"},
        {"question": "바다에서 가장 힘센 생물은?", "options": ["고래", "상어", "문어", "오징어", "씰"], "answer": "씰", "explanation": "'Seal(물개)'이 영어로 '확정하다'라는 뜻도 있어요. '딜 확정(Seal the deal)'처럼요! 🦭"},
        {"question": "개가 사람을 가르치면?", "options": ["강사", "견사", "훈련사", "독선생", "개같은 선생"], "answer": "독선생", "explanation": "'犬(견, 개) = Dog = 독'이에요. 개 선생님은 독선생! 🐕"},
        {"question": "세상에서 가장 맛있는 집은?", "options": ["한옥", "양옥", "초가집", "빌라", "맛있는 집"], "answer": "초가집", "explanation": "'초가(草家)'집이 '초콜릿 가게 집'처럼 들려요. 초코집은 맛있겠죠? 🏠"},
        {"question": "귤이 걸으면?", "options": ["귤러가다", "오렌지 워킹", "과일 산책", "감귤", "밀감"], "answer": "귤러가다", "explanation": "'귤 + 걸어가다 = 귤러가다!' 발음이 비슷한 말장난이에요. 🍊"},
        {"question": "토끼가 비타민을 먹으면?", "options": ["건강토끼", "비타토끼", "토비타민", "타조", "영양토끼"], "answer": "타조", "explanation": "'토(끼가) + 비타(민 먹으면) = 토비타 → 타조!' 🐰➡️🦃"},
        {"question": "가수가 잠을 자면?", "options": ["꿀잠", "휴식", "잠자리", "잠", "레스토랑"], "answer": "레스토랑", "explanation": "'Rest(쉬다) + 오랑(오래)'으로 레스토랑! 🎤"},
        {"question": "닭이 알을 많이 낳으면?", "options": ["슈퍼닭", "산란기", "다산", "난계", "알부자"], "answer": "알부자", "explanation": "'알 + 부자(많이 가진 사람)'로 알부자! 🥚"},
        {"question": "세상에서 제일 뜨거운 과일은?", "options": ["사과", "딸기", "파인애플", "망고", "천도복숭아"], "answer": "천도복숭아", "explanation": "'천도(千度, 1000도) + 복숭아'로 천도복숭아! 🍑"},
        {"question": "오리가 얼면?", "options": ["오리콘", "얼음오리", "언오리", "꽁오리", "냉동오리"], "answer": "언오리", "explanation": "'언(frozen) + 오리'로 언오리! '얼다'의 관형사 '언'을 사용했어요. 🦆"},
        {"question": "소나무가 죽으면?", "options": ["고사목", "죽은나무", "다이소나무", "관목", "묘목"], "answer": "다이소나무", "explanation": "'Die(죽다) + 소나무'로 다이소나무! 🌲"},
        {"question": "세계에서 가장 억울한 사람은?", "options": ["무고한 사람", "피해자", "오해받는 사람", "억", "누명 쓴 사람"], "answer": "억", "explanation": "'억울하다'에서 '억'만 남기면 억(億, 1억)! 😤"},
        {"question": "세상에서 가장 쉬운 숫자는?", "options": ["1", "0", "팔", "구", "영"], "answer": "팔", "explanation": "'팔(8)'이 '쉽다'의 방언과 비슷해요. 또는 팔짱 끼면 쉬우니까! 💪"},
        {"question": "사슴이 뿔이 없으면?", "options": ["무뿔사슴", "암사슴", "사수", "사쁨", "노루"], "answer": "사쁨", "explanation": "'사슴 - 뿔 = 사쁨!' 글자에서 뿔을 빼면 사쁨이 돼요. 😊"},
        {"question": "세상에서 가장 지루한 새는?", "options": ["비둘기", "참새", "지빠귀", "까치", "까마귀"], "answer": "지빠귀", "explanation": "'지루하다'와 '빠귀(새)'를 합친 말장난이에요! 🐦"},
        {"question": "빵이 넘어지면?", "options": ["빵야", "아프다", "부서진다", "식빵", "빵꾸러지다"], "answer": "빵꾸러지다", "explanation": "'빵 + 꾸러지다(넘어지다)'로 빵꾸러지다! 🍞"},
        {"question": "자동차가 빵꾸나면?", "options": ["펑크", "고장", "카스테라", "타이어", "수리"], "answer": "카스테라", "explanation": "'카(car) + 스테라(찢어진)'로 카스테라! 🚗"},
        {"question": "세상에서 가장 빠른 감은?", "options": ["단감", "홍시", "곶감", "번개감", "탐감"], "answer": "탐감", "explanation": "'탐(Tom, 톰과 제리) + 감'으로 탐감! 또는 탐나는 감이라 빨리 사라져요! 🍊"}
    ]
}

# 사이드바
with st.sidebar:
    st.markdown("## ⚙️ 설정")
    if st.button("🌙 다크 모드" if st.session_state.dark_mode else "☀️ 라이트 모드", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    st.markdown("---")
    st.markdown("### ⏱️ 타이머")
    st.session_state.timer_enabled = st.checkbox("타이머 사용", value=st.session_state.timer_enabled)
    if st.session_state.timer_enabled:
        st.session_state.time_limit = st.slider("제한 시간", 5, 30, st.session_state.time_limit)
    st.markdown("---")
    st.markdown("### 📊 정답률")
    for cat, stat in st.session_state.stats.items():
        rate = (stat["correct"] / stat["total"] * 100) if stat["total"] > 0 else 0
        st.write(f"{cat}: **{rate:.0f}%** ({stat['correct']}/{stat['total']})" if stat["total"] > 0 else f"{cat}: -")
    if st.button("🗑️ 통계 초기화", use_container_width=True):
        for cat in st.session_state.stats:
            st.session_state.stats[cat] = {"correct": 0, "total": 0}
        st.rerun()

def show_home():
    st.markdown('<h1 class="main-title">🧠 상식 퀴즈</h1>', unsafe_allow_html=True)
    st.markdown(f"**📌 30문제 중 12문제 랜덤 출제 | 💡 힌트 3회 | ⏱️ {st.session_state.time_limit}초**")
    st.markdown("### 🎯 카테고리 선택")
    for cat in quiz_data.keys():
        if st.button(cat, key=f"cat_{cat}", use_container_width=True):
            st.session_state.category = cat
            q = quiz_data[cat].copy()
            random.shuffle(q)
            st.session_state.questions = q[:12]
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.hints_remaining = 3
            st.session_state.hint_used = False
            st.session_state.hidden_options = []
            st.session_state.start_time = time.time()
            st.session_state.time_up = False
            st.session_state.page = 'quiz'
            st.rerun()

def show_quiz():
    cat = st.session_state.category
    q_num = st.session_state.current_question
    q = st.session_state.questions[q_num]
    
    st.markdown(f"### {cat}")
    
    # 타이머
    if st.session_state.timer_enabled and not st.session_state.answered:
        remaining = max(0, st.session_state.time_limit - int(time.time() - st.session_state.start_time))
        cls = "timer-safe" if remaining > 10 else ("timer-warning" if remaining > 5 else "timer-danger")
        st.markdown(f'<div class="{cls}">⏱️ {remaining}초</div>', unsafe_allow_html=True)
        if remaining == 0 and not st.session_state.time_up:
            st.session_state.time_up = True
            st.session_state.answered = True
            st.session_state.stats[cat]["total"] += 1
            st.rerun()
    
    st.markdown(f"**문제 {q_num+1}/12** | ⭐ {st.session_state.score}점 | 💡 {st.session_state.hints_remaining}회")
    st.progress((q_num + 1) / 12)
    st.markdown(f'<p class="question-text">Q{q_num+1}. {q["question"]}</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 힌트
    if not st.session_state.answered and st.session_state.hints_remaining > 0 and not st.session_state.hint_used:
        if st.button(f"💡 힌트 ({st.session_state.hints_remaining}회)"):
            wrong = [o for o in q["options"] if o != q["answer"]]
            st.session_state.hidden_options = random.sample(wrong, 2)
            st.session_state.hints_remaining -= 1
            st.session_state.hint_used = True
            st.rerun()
    
    # 선택지
    if not st.session_state.answered:
        for i, opt in enumerate(q["options"]):
            if opt in st.session_state.hidden_options:
                st.button(f"~~{i+1}. {opt}~~ ❌", key=f"o{i}", disabled=True, use_container_width=True)
            elif st.button(f"{i+1}. {opt}", key=f"o{i}", use_container_width=True):
                st.session_state.selected_answer = opt
                st.session_state.answered = True
                st.session_state.stats[cat]["total"] += 1
                if opt == q["answer"]:
                    st.session_state.score += 1
                    st.session_state.stats[cat]["correct"] += 1
                st.rerun()
    else:
        if st.session_state.time_up:
            st.error("⏰ 시간 초과!")
        for i, opt in enumerate(q["options"]):
            if opt == q["answer"]:
                st.success(f"✅ {i+1}. {opt} (정답)")
            elif opt == st.session_state.selected_answer:
                st.error(f"❌ {i+1}. {opt}")
            else:
                st.write(f"⬜ {i+1}. {opt}")
        
        if st.session_state.selected_answer == q["answer"]:
            st.balloons()
            st.success("🎉 정답!")
        elif st.session_state.selected_answer:
            st.error(f"오답! 정답: {q['answer']}")
        
        # 해설 표시
        st.markdown(f"""<div class="explanation-box">
        <div style="font-weight:bold;color:#74b9ff;margin-bottom:0.5rem;">📚 해설</div>
        <div>{q["explanation"]}</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            if q_num < 11:
                if st.button("다음 ▶", use_container_width=True):
                    st.session_state.current_question += 1
                    st.session_state.answered = False
                    st.session_state.selected_answer = None
                    st.session_state.hint_used = False
                    st.session_state.hidden_options = []
                    st.session_state.start_time = time.time()
                    st.session_state.time_up = False
                    st.rerun()
            else:
                if st.button("🏆 결과", use_container_width=True):
                    st.session_state.page = 'result'
                    st.rerun()
        with c2:
            if st.button("🏠 홈", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
    
    if st.session_state.timer_enabled and not st.session_state.answered:
        time.sleep(1)
        st.rerun()

def show_result():
    score = st.session_state.score
    cat = st.session_state.category
    pct = score / 12 * 100
    msg = "완벽! 👑" if score == 12 else "훌륭해요! 🌟" if score >= 10 else "잘했어요! 👏" if score >= 7 else "괜찮아요! 💪" if score >= 4 else "다시 도전! 📚"
    stars = "⭐" * min(5, (score // 2) + 1)
    
    if score >= 10:
        st.balloons()
    
    st.markdown('<h1 class="main-title">🏆 퀴즈 완료!</h1>', unsafe_allow_html=True)
    st.markdown(f"### {cat}")
    st.markdown(f"<p style='text-align:center;font-size:2rem;'>{stars}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='result-score' style='text-align:center;'>{score} / 12</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;font-size:1.5rem;'>{msg}</p>", unsafe_allow_html=True)
    st.markdown(f"### 정답률: {pct:.0f}%")
    st.progress(score / 12)
    
    stat = st.session_state.stats[cat]
    if stat["total"] > 0:
        st.info(f"📈 {cat} 누적: {stat['correct']/stat['total']*100:.0f}% ({stat['correct']}/{stat['total']})")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 다시", use_container_width=True):
            q = quiz_data[cat].copy()
            random.shuffle(q)
            st.session_state.questions = q[:12]
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.hints_remaining = 3
            st.session_state.hint_used = False
            st.session_state.hidden_options = []
            st.session_state.start_time = time.time()
            st.session_state.time_up = False
            st.session_state.page = 'quiz'
            st.rerun()
    with c2:
        if st.button("🏠 홈", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

# 메인
if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'quiz':
    show_quiz()
elif st.session_state.page == 'result':
    show_result()
