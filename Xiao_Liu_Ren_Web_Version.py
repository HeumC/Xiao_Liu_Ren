import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from lunar_python import Solar
from streamlit_javascript import st_javascript

# 页面基础配置
st.set_page_config(page_title="小六壬掌诀", page_icon="☯", layout="centered")

# 获取用户设备浏览器的本地时区（如 "Asia/Shanghai", "America/New_York" 等）
user_tz_str = st_javascript("Intl.DateTimeFormat().resolvedOptions().timeZone")

# 容错处理：若刚打开时 JS 尚未返回，默认使用上海时区
if not user_tz_str:
    user_tz = ZoneInfo("Asia/Shanghai")
    tz_display = "Asia/Shanghai (默认)"
else:
    try:
        user_tz = ZoneInfo(user_tz_str)
        tz_display = user_tz_str
    except (ZoneInfoNotFoundError, Exception):
        user_tz = ZoneInfo("Asia/Shanghai")
        tz_display = "Asia/Shanghai"

# 六神数据定义
XLR_DATA = {
    0: {"name": "大安", "symbol": "⭐", "speed": "安详平稳 · 缓中有吉", "action": "身不动时，五行属木。求谋可成，宜守常安泰，踏实积累，利于静止与扎根。"},
    1: {"name": "留连", "symbol": "❌", "speed": "拖延阻滞 · 需耐心周旋", "action": "卒未归时，五行属水。凡事有阻，宜守旧防滞，不可冒进，适合复盘与等待转机。"},
    2: {"name": "速喜", "symbol": "⭐⭐⭐", "speed": "喜庆迅速 · 即刻降临", "action": "人便至时，五行属火。诸事吉利，宜抓紧行动，正向反馈极快，乘势而上莫迟疑。"},
    3: {"name": "赤口", "symbol": "❌❌", "speed": "口舌纷争 · 凶事防疾", "action": "官事凶时，五行属金。易生言语摩擦，宜谨慎言辞，防小人与争执，低调不惹事。"},
    4: {"name": "小吉", "symbol": "⭐⭐", "speed": "和合吉利 · 渐入佳境", "action": "人来喜时，五行属木。万事和顺，多得贵人照拂，利于协同合作与日常微小进步。"},
    5: {"name": "空亡", "symbol": "❌❌❌", "speed": "虚耗落空 · 彻底清空", "action": "音信稀时，五行属土。谋事难成，宜闭门自省，不可强求，清空杂念等待下一轮起点。"}
}

st.title("小六壬 · 掌诀占候")
st.caption(f"以时起卦 · 当前识别设备时区：`{tz_display}`")

# 按钮触发计算
if st.button("以当前时辰排盘", type="primary", use_container_width=True):
    # 按照用户设备的本地时区取当前时刻
    now = datetime.now(user_tz)
    
    solar = Solar.fromYmdHms(now.year, now.month, now.day, now.hour, now.minute, now.second)
    lunar = solar.getLunar()

    month = abs(lunar.getMonth())
    day = lunar.getDay()
    zhi = lunar.getTimeZhi()
    zhi_idx = lunar.getTimeZhiIndex() + 1

    result_idx = (month + day + zhi_idx - 3) % 6
    info = XLR_DATA[result_idx]

    # 结果展示卡片
    with st.container(border=True):
        st.subheader(f"【 {info['name']} 】")
        st.write(f"**应验：** {info['symbol']} {info['speed']}")
        st.info(f"**断辞与指引：**\n\n{info['action']}")
        st.divider()
        st.caption(f"本地时间：{now.strftime('%Y-%m-%d %H:%M:%S')} ({tz_display})")
        st.caption(f"农历：{lunar.getMonthInChinese()}月{lunar.getDayInChinese()} · {zhi}时 (第{zhi_idx}时辰)")
else:
    st.info("凝神静气，心中默念所测之事，点击上方按钮起卦。")

st.caption("注：⭐/❌ 数量代表好运或阻滞降临的速度，并非吉凶程度。")
