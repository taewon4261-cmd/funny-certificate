import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 페이지 기본 설정 (웹브라우저 탭 이름 등)
st.set_page_config(
    page_title="대국민 쓸데없는 자격증 발급소",
    page_icon="🎖️",
    layout="centered"
)

# ==========================================
# [설정 영역] - 수정해주신 내용 적용 완료!
# ==========================================
# 0. [신규] 상단 '자격증' 제목 위치 및 크기 (궁서체 예정)
HEADER_X, HEADER_Y = 400, 160  # '자격증' 글자 중앙 위치 (배경에 따라 조정 필요)
FONT_SIZE_HEADER = 80          # 가장 크고 웅장하게!

# 1. 위치 좌표
NAME_X, NAME_Y = 150, 280
TITLE_X, TITLE_Y = 150, 400
DESC_X, DESC_Y = 150, 525

# 2. [중요] 가로 한계선
MAX_WIDTH = 450

# 3. 하단 문구 및 도장
FOOTER_X, FOOTER_Y = 120, 800
STAMP_X, STAMP_Y = 400, 650
STAMP_SIZE = (250, 250)
STAMP_TEXT_X_OFFSET = 250   # 도장 텍스트 위치 미세조정
STAMP_TEXT_Y_OFFSET = 65

# 4. 기본 글자 크기
FONT_SIZE_NAME = 55
FONT_SIZE_TITLE_DEFAULT = 50
FONT_SIZE_DESC = 30
FONT_SIZE_FOOTER = 40
FONT_SIZE_STAMP = 45

# 5. 폰트 파일 경로 (💡 중요: 이 파일이 궁서체여야 합니다!)
FONT_PATH = "font.ttf"

# 6. 색상
TEXT_COLOR = (0, 0, 0)
STAMP_COLOR = (230, 0, 0, 220)
# ==========================================

# 📜 [데이터베이스]
CERT_DB = {
    "협곡의 지배자 1급": {
        "desc": "위 사람은 '오빠 갱 안와?'를 시전하며 남 탓하기의 달인이고, 키보드 샷건 치기의 장인이기에 임명함.",
        "footer": "전국 키보드 워리어 협회",
        "stamp_text": "남탓 장인"
    },
    "프로 먹방러 1급": {
        "desc": "위 사람은 치킨 뼈를 보았을 때 양념인지 후라이드인지 구분하며, '맛있으면 0칼로리'를 과학적으로 증명했기에 임명함.",
        "footer": "배달의 민족 VVIP",
        "stamp_text": "돼지 보스"
    },
    "3대 500 헬창 1급": {
        "desc": "위 사람은 근손실을 세상에서 제일 무서워하며, 닭가슴살 쉐이크를 주식으로 삼는 쇠질 중독자이기에 임명함.",
        "footer": "국제 프로틴 연구소",
        "stamp_text": "근육 돼지"
    },
    "집 밖은 위험해 1급": {
        "desc": "위 사람은 약속이 취소되면 희열을 느끼며, 전기장판 위에서 귤 까먹는 스킬이 타의 추종을 불허하기에 임명함.",
        "footer": "전국 집순이 집돌이 연합",
        "stamp_text": "이불 밖 위험"
    },
    "알콜 마스터 1급": {
        "desc": "위 사람은 간 해독 능력이 타의 추종을 불허하며, '막차 끊겼다'를 핑계로 아침 해를 보고야 마는 인재이기에 임명함.",
        "footer": "국제 알콜 감별사 협회",
        "stamp_text": "알콜 요정"
    },
    "월급 로그아웃 1급": {
        "desc": "위 사람은 월급이 통장에 들어오자마자 0.1초 만에 카드값으로 퍼가요 당하는 마술을 보였기에 임명함.",
        "footer": "사이버 머니 수집가",
        "stamp_text": "텅장 주인"
    },
    "카페인 중독 1급": {
        "desc": "위 사람은 혈관에 피 대신 아이스 아메리카노가 흐르며, 커피 없이는 인성질을 부리는 금단현상이 있기에 임명함.",
        "footer": "전국 얼죽아 협회",
        "stamp_text": "커피 수혈"
    },
    "민트초코 1급": {
        "desc": "위 사람은 치약 맛이라고 놀림받아도 굴하지 않으며, 밥 비벼 먹을 기세로 민초를 찬양하는 굳건한 미각을 가졌기에 임명함.",
        "footer": "민초단 우수 회원",
        "stamp_text": "민초가 세상을"
    },
    "프로 눕방러 1급": {
        "desc": "위 사람은 숨쉬기 운동 외에는 일절 움직이지 않으며, 등과 바닥의 물아일체 경지에 올랐기에 임명함.",
        "footer": "전세계 눕방 협회장 김눕방",
        "stamp_text": "눕방 장인"
    },
    "야근 요정 1급": {
        "desc": "위 사람은 남들 퇴근할 때 모니터와 대화하며, 회사의 전기를 수호하였기에 임명함.",
        "footer": "대한민국 야근 수호대",
        "stamp_text": "야근 노예"
    },
    "아가리어터 1급": {
        "desc": "위 사람은 '다이어트는 내일부터'라는 명언을 매일 실천하며, 운동 등록만 하고 기부천사가 되었기에 임명함.",
        "footer": "전국 작심삼일 연합회",
        "stamp_text": "입만 살음"
    },
    "스마트폰 중독 1급": {
        "desc": "위 사람은 화장실 갈 때 폰이 없으면 변비에 걸리며, 배터리 20% 미만 시 손을 떠는 금단현상을 보였기에 임명함.",
        "footer": "도파민의 노예들",
        "stamp_text": "도파민 중독"
    },
    "직접 입력": {
        "desc": "직접 입력해주세요.",
        "footer": "직접 입력해주세요.",
        "stamp_text": "내가 일짱"
    }
}


# --- 🛠️ 헬퍼 함수들 ---
def wrap_text(text, font, max_width, draw):
    lines = []
    paragraphs = text.split('\n')
    for paragraph in paragraphs:
        current_line = []
        for char in paragraph:
            current_line.append(char)
            test_line = "".join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            if width > max_width:
                current_line.pop()
                lines.append("".join(current_line))
                current_line = [char]
        if current_line:
            lines.append("".join(current_line))
    return "\n".join(lines)

def get_fitted_title_font(text, max_width, draw, font_path, start_size, min_size=20):
    current_size = start_size
    try:
        font = ImageFont.truetype(font_path, current_size)
    except:
        return ImageFont.load_default()
    while current_size > min_size:
        font = ImageFont.truetype(font_path, current_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width <= max_width:
            return font
        current_size -= 2
    return ImageFont.truetype(font_path, min_size)


# ==========================================
# [메인 로직 시작]
# ==========================================

# 1. 사이드바 메뉴 구성 및 안내문
with st.sidebar:
    st.header("📂 메뉴 선택")
    # 추후 확장을 대비한 메뉴 구조
    menu = st.radio(
        "이동할 서비스를 선택하세요:",
        ["🏆 자격증 발급소", "🔮 심리테스트 (준비중)", "🤖 AI 캐릭터 (준비중)"]
    )
    
    st.markdown("---")
    st.header("☕ 개발자 응원하기")
    st.markdown("재밌게 즐기셨다면 100원만..🙇‍♂️")
    st.code("1000-4564-3898", language="text")
    st.caption("토스/카뱅 복사용")

# 2. [⭐ 중요] 메인 화면 최상단 안내 문구 추가
st.info("👈 **왼쪽 상단의 화살표(>)**를 눌러 정보 입력창을 열어주세요!")


# 3. 메뉴별 화면 보여주기
if menu == "🏆 자격증 발급소":
    st.title("🎖️ 대국민 쓸데없는 자격증 발급소")
    st.caption("오늘 당신의 잉여력을 증명하세요!")

    # --- 자격증 입력 폼 ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("📝 자격증 정보 입력")
    user_name = st.sidebar.text_input("이름", value="홍길동")
    selected_cert = st.sidebar.selectbox("자격증 종류", list(CERT_DB.keys()))

    if selected_cert == "직접 입력":
        cert_title_input = st.sidebar.text_input("자격증 이름", value="코딩 천재 1급")
        cert_desc_input = st.sidebar.text_area("내용", value="내용을 입력하세요.")
        footer_text = st.sidebar.text_input("발급 기관", value="코딩 협회")
        stamp_text_input = st.sidebar.text_input("도장 문구", value="참 잘했어요")
    else:
        cert_title_input = selected_cert
        cert_desc_input = CERT_DB[selected_cert]["desc"]
        footer_text = CERT_DB[selected_cert]["footer"]
        stamp_text_input = CERT_DB[selected_cert]["stamp_text"]

    # --- 발급 버튼 및 로직 ---
    if st.button("자격증 발급하기 🖨️", type="primary"):
        try:
            bg_image = Image.open("certificate_bg.png")
            draw = ImageDraw.Draw(bg_image)
            
            # 폰트 로드 (font.ttf 파일이 궁서체여야 합니다!)
            try:
                font_header = ImageFont.truetype(FONT_PATH, FONT_SIZE_HEADER) # [신규] 상단 제목용
                font_desc = ImageFont.truetype(FONT_PATH, FONT_SIZE_DESC)
                font_footer = ImageFont.truetype(FONT_PATH, FONT_SIZE_FOOTER)
                font_stamp = ImageFont.truetype(FONT_PATH, FONT_SIZE_STAMP)
            except:
                st.error("🚨 'font.ttf' 파일을 찾을 수 없습니다! 기본 폰트로 대체됩니다.")
                font_header = ImageFont.load_default()
                font_desc = ImageFont.load_default()
                font_footer = ImageFont.load_default()
                font_stamp = ImageFont.load_default()

            # 0. [신규] 상단에 '자 격 증' 글자 그리기 (궁서체)
            # anchor="mm"은 좌표를 글자의 정중앙으로 설정하는 옵션입니다.
            draw.text((HEADER_X, HEADER_Y), "자 격 증", fill=TEXT_COLOR, font=font_header, anchor="mm")

            # 1. 이름 쓰기
            full_name = f"성 명 : {user_name}"
            fitted_name_font = get_fitted_title_font(full_name, MAX_WIDTH, draw, FONT_PATH, FONT_SIZE_NAME)
            draw.text((NAME_X, NAME_Y), full_name, fill=TEXT_COLOR, font=fitted_name_font)
            
            # 2. 제목 쓰기
            full_title = f"자 격 : {cert_title_input}"
            fitted_title_font = get_fitted_title_font(full_title, MAX_WIDTH, draw, FONT_PATH, FONT_SIZE_TITLE_DEFAULT)
            draw.text((TITLE_X, TITLE_Y), full_title, fill=TEXT_COLOR, font=fitted_title_font)
            
            # 3. 본문 쓰기
            wrapped_desc = wrap_text(cert_desc_input, font_desc, MAX_WIDTH, draw)
            draw.text((DESC_X, DESC_Y), wrapped_desc, fill=TEXT_COLOR, font=font_desc, spacing=15)
            
            # 4. 하단 문구
            draw.text((FOOTER_X, FOOTER_Y), footer_text, fill=TEXT_COLOR, font=font_footer)

            # 5. 도장 찍기
            try:
                stamp_image = Image.open("stamp_frame.png").convert("RGBA")
                stamp_draw = ImageDraw.Draw(stamp_image)
                final_stamp_text = stamp_text_input.replace(" ", "\n")
                stamp_w, stamp_h = stamp_image.size
                left, top, right, bottom = stamp_draw.multiline_textbbox((0, 0), final_stamp_text, font=font_stamp, spacing=10, align='center')
                text_w, text_h = right - left, bottom - top
                text_x = (stamp_w - text_w) / 2 + STAMP_TEXT_X_OFFSET
                text_y = (stamp_h - text_h) / 2 + STAMP_TEXT_Y_OFFSET
                stamp_draw.multiline_text((text_x, text_y), final_stamp_text, fill=STAMP_COLOR, font=font_stamp, spacing=10, align='center')
                stamp_image = stamp_image.resize(STAMP_SIZE)
                bg_image.paste(stamp_image, (STAMP_X, STAMP_Y), stamp_image)
            except Exception as e:
                st.warning(f"도장 오류: {e}")

            # 결과 출력
            st.image(bg_image, caption="완성된 자격증", use_container_width=True)
            
            # 다운로드 버튼
            buf = io.BytesIO()
            bg_image.save(buf, format="PNG")
            st.download_button("이미지 저장 📥", buf.getvalue(), f"{user_name}_자격증.png", "image/png")
            
        except Exception as e:
            st.error(f"오류 발생: {e}")
            st.info("폴더에 'certificate_bg.png', 'stamp_frame.png', 'font.ttf' 파일이 있는지 확인해주세요.")

elif menu == "🔮 심리테스트 (준비중)":
    st.title("🔮 나의 숨겨진 성격 테스트")
    st.info("이 기능은 곧 오픈됩니다! 조금만 기다려주세요.")

elif menu == "🤖 AI 캐릭터 (준비중)":
    st.title("🤖 AI 캐릭터 만들기")
    st.warning("개발자가 열심히 코딩 중입니다... 💦")