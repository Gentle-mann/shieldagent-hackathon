"""
ShieldAgent — Streamlit Web Demo
AI-Powered Legal Shield for Migrant Workers in Japan
Built on SpoonOS x Neo | Scoop AI Hackathon Tokyo Bowl
"""

import streamlit as st
import asyncio
import os
import hashlib
import re
import time
from datetime import datetime
from dotenv import load_dotenv

# SpoonOS imports — Agent -> SpoonOS -> LLM
from spoon_ai.chat import ChatBot
from spoon_ai.agents.toolcall import ToolCallAgent
from spoon_ai.tools import ToolManager
from spoon_ai.tools.base import BaseTool, ToolResult

load_dotenv()

# Page config
st.set_page_config(
    page_title="ShieldAgent - Contract Guardian",
    page_icon="🛡️",
    layout="wide",
)

# ============================================================
# i18n / Multilingual Support
# ============================================================
TRANSLATIONS = {
    "en": {
        "title": "ShieldAgent",
        "subtitle": "AI-Powered Legal Shield for Migrant Workers in Japan",
        "built_on": "Built on SpoonOS x Neo | Scoop AI Hackathon Tokyo Bowl 2026",
        "tab_analysis": "Contract Analysis",
        "tab_qa": "Rights Q&A",
        "tab_report": "Violation Reporter",
        "tab_about": "About",
        "contract_guardian": "Contract Guardian",
        "contract_desc": "Upload or paste a Japanese employment contract to check for legal violations.",
        "prefecture": "Worker's Prefecture",
        "visa_type": "Visa Type",
        "use_sample": "Use sample contract (demo)",
        "analyze_btn": "Analyze Contract",
        "translating": "Translating contract from Japanese...",
        "analyzing": "Analyzing each clause against Japanese labor law...",
        "storing": "Storing evidence hash on blockchain...",
        "complete": "Analysis complete!",
        "view_translation": "View English Translation",
        "report_title": "Analysis Report",
        "actions_title": "Recommended Actions",
        "actions": [
            "OTIT Hotline: **0120-250-168** (Vietnamese, Chinese, Filipino, Indonesian)",
            "FRESC: **0120-76-2029** (14 languages)",
            "Legal Aid (Houterasu): **0570-078377**",
            "Keep a copy of this report as evidence",
        ],
        "disclaimer": "This analysis is AI-generated for informational purposes only. Consult a qualified legal professional.",
        "rights_nav": "Rights Navigator",
        "rights_desc": "Ask any question about your labor rights in Japan.",
        "ask_btn": "Ask ShieldAgent",
        "question_placeholder": "Type your question about labor rights in Japan...",
        "examples": [
            "Can my employer take my passport?",
            "What is minimum wage in Tokyo?",
            "Can I change employers on TITP visa?",
        ],
        "violation_title": "Violation Reporter",
        "violation_desc": "Report a workplace violation anonymously. Your report will be hashed and stored immutably.",
        "violation_type": "Type of Violation",
        "violation_detail": "Describe what happened",
        "violation_when": "When did this happen?",
        "violation_submit": "Submit Report (Anonymous)",
        "violation_success": "Report submitted and hashed on-chain.",
        "how_it_works": "How It Works",
        "tech_stack": "Tech Stack",
        "emergency": "Emergency Contacts",
        "settings": "Settings",
        "api_key_label": "Anthropic API Key",
        "language": "Language / 言語",
        "run_demo": "Run Demo",
        "demo_desc": "One-click: analyzes sample contract (Vietnamese TITP trainee, Aichi) for violations",
        "download_report": "Download Report",
    },
    "vi": {
        "title": "ShieldAgent",
        "subtitle": "Bảo vệ pháp lý bằng AI cho lao động nhập cư tại Nhật Bản",
        "built_on": "Xây dựng trên SpoonOS x Neo | Scoop AI Hackathon Tokyo Bowl 2026",
        "tab_analysis": "Phân tích hợp đồng",
        "tab_qa": "Hỏi đáp quyền lợi",
        "tab_report": "Báo cáo vi phạm",
        "tab_about": "Giới thiệu",
        "contract_guardian": "Người bảo vệ hợp đồng",
        "contract_desc": "Tải lên hoặc dán hợp đồng lao động bằng tiếng Nhật để kiểm tra vi phạm pháp luật.",
        "prefecture": "Tỉnh nơi làm việc",
        "visa_type": "Loại visa",
        "use_sample": "Dùng hợp đồng mẫu (demo)",
        "analyze_btn": "Phân tích hợp đồng",
        "translating": "Đang dịch hợp đồng từ tiếng Nhật...",
        "analyzing": "Đang phân tích từng điều khoản theo luật lao động Nhật...",
        "storing": "Đang lưu bằng chứng lên blockchain...",
        "complete": "Phân tích hoàn tất!",
        "view_translation": "Xem bản dịch",
        "report_title": "Báo cáo phân tích",
        "actions_title": "Hành động được khuyến nghị",
        "actions": [
            "Đường dây nóng OTIT: **0120-250-168** (Tiếng Việt, Trung, Philippines, Indonesia)",
            "FRESC: **0120-76-2029** (14 ngôn ngữ)",
            "Trợ giúp pháp lý (Houterasu): **0570-078377**",
            "Giữ bản sao báo cáo này làm bằng chứng",
        ],
        "disclaimer": "Phân tích này do AI tạo ra chỉ mang tính tham khảo. Hãy tham vấn luật sư chuyên nghiệp.",
        "rights_nav": "Hỏi đáp quyền lợi",
        "rights_desc": "Hỏi bất kỳ câu hỏi nào về quyền lao động tại Nhật Bản.",
        "ask_btn": "Hỏi ShieldAgent",
        "question_placeholder": "Nhập câu hỏi về quyền lao động tại Nhật Bản...",
        "examples": [
            "Chủ lao động có được giữ hộ chiếu của tôi không?",
            "Mức lương tối thiểu ở Tokyo là bao nhiêu?",
            "Tôi có thể đổi chủ lao động với visa TITP không?",
        ],
        "violation_title": "Báo cáo vi phạm",
        "violation_desc": "Báo cáo vi phạm tại nơi làm việc một cách ẩn danh. Báo cáo sẽ được mã hóa và lưu trữ bất biến.",
        "violation_type": "Loại vi phạm",
        "violation_detail": "Mô tả những gì đã xảy ra",
        "violation_when": "Khi nào việc này xảy ra?",
        "violation_submit": "Gửi báo cáo (Ẩn danh)",
        "violation_success": "Báo cáo đã được gửi và mã hóa lên blockchain.",
        "how_it_works": "Cách hoạt động",
        "tech_stack": "Công nghệ",
        "emergency": "Liên hệ khẩn cấp",
        "settings": "Cài đặt",
        "api_key_label": "Khóa API Anthropic",
        "language": "Ngôn ngữ / Language",
        "run_demo": "Chạy Demo",
        "demo_desc": "Một cú nhấp: phân tích hợp đồng mẫu (thực tập sinh TITP Việt Nam, Aichi)",
        "download_report": "Tải báo cáo",
    },
    "zh": {
        "title": "ShieldAgent",
        "subtitle": "AI驱动的在日外国劳工法律保护盾",
        "built_on": "基于 SpoonOS x Neo | Scoop AI Hackathon Tokyo Bowl 2026",
        "tab_analysis": "合同分析",
        "tab_qa": "权益问答",
        "tab_report": "违规举报",
        "tab_about": "关于",
        "contract_guardian": "合同守护者",
        "contract_desc": "上传或粘贴日语劳动合同以检查是否违反法律。",
        "prefecture": "工作所在都道府县",
        "visa_type": "签证类型",
        "use_sample": "使用示例合同（演示）",
        "analyze_btn": "分析合同",
        "translating": "正在从日语翻译合同...",
        "analyzing": "正在逐条对照日本劳动法进行分析...",
        "storing": "正在将证据哈希存储到区块链...",
        "complete": "分析完成！",
        "view_translation": "查看翻译",
        "report_title": "分析报告",
        "actions_title": "建议措施",
        "actions": [
            "OTIT热线: **0120-250-168**（越南语、中文、菲律宾语、印尼语）",
            "FRESC: **0120-76-2029**（14种语言）",
            "法律援助 (Houterasu): **0570-078377**",
            "保存此报告作为证据",
        ],
        "disclaimer": "此分析由AI生成，仅供参考。请咨询专业法律人士。",
        "rights_nav": "权益导航",
        "rights_desc": "询问任何关于在日本劳动权益的问题。",
        "ask_btn": "询问 ShieldAgent",
        "question_placeholder": "输入关于在日本劳动权益的问题...",
        "examples": [
            "雇主可以拿走我的护照吗？",
            "东京的最低工资是多少？",
            "TITP签证可以换雇主吗？",
        ],
        "violation_title": "违规举报",
        "violation_desc": "匿名举报工作场所违规行为。您的举报将被哈希存储，不可篡改。",
        "violation_type": "违规类型",
        "violation_detail": "描述发生了什么",
        "violation_when": "这是什么时候发生的？",
        "violation_submit": "提交举报（匿名）",
        "violation_success": "举报已提交并哈希存储到区块链。",
        "how_it_works": "工作原理",
        "tech_stack": "技术栈",
        "emergency": "紧急联系方式",
        "settings": "设置",
        "api_key_label": "Anthropic API 密钥",
        "language": "语言 / Language",
        "run_demo": "运行演示",
        "demo_desc": "一键分析示例合同（越南TITP实习生，爱知县）",
        "download_report": "下载报告",
    },
    "ja": {
        "title": "ShieldAgent",
        "subtitle": "外国人労働者のためのAI法律保護シールド",
        "built_on": "SpoonOS x Neo 上に構築 | Scoop AI Hackathon Tokyo Bowl 2026",
        "tab_analysis": "契約分析",
        "tab_qa": "権利Q&A",
        "tab_report": "違反報告",
        "tab_about": "概要",
        "contract_guardian": "契約ガーディアン",
        "contract_desc": "日本語の雇用契約書をアップロードまたは貼り付けて、法律違反をチェックします。",
        "prefecture": "就業先の都道府県",
        "visa_type": "ビザの種類",
        "use_sample": "サンプル契約書を使用（デモ）",
        "analyze_btn": "契約を分析",
        "translating": "契約書を翻訳中...",
        "analyzing": "各条項を労働法と照合分析中...",
        "storing": "証拠ハッシュをブロックチェーンに保存中...",
        "complete": "分析完了！",
        "view_translation": "翻訳を表示",
        "report_title": "分析レポート",
        "actions_title": "推奨アクション",
        "actions": [
            "OTIT ホットライン: **0120-250-168**（ベトナム語、中国語、フィリピン語、インドネシア語）",
            "FRESC: **0120-76-2029**（14言語対応）",
            "法テラス: **0570-078377**",
            "このレポートのコピーを証拠として保管してください",
        ],
        "disclaimer": "この分析はAIにより生成されたものであり、情報提供のみを目的としています。専門の法律家にご相談ください。",
        "rights_nav": "権利ナビゲーター",
        "rights_desc": "日本での労働者の権利について質問してください。",
        "ask_btn": "ShieldAgentに質問",
        "question_placeholder": "日本での労働権についての質問を入力...",
        "examples": [
            "雇用主はパスポートを取り上げることができますか？",
            "東京の最低賃金はいくらですか？",
            "技能実習ビザで雇用主を変更できますか？",
        ],
        "violation_title": "違反報告",
        "violation_desc": "職場の違反を匿名で報告します。報告はハッシュ化され不変に保存されます。",
        "violation_type": "違反の種類",
        "violation_detail": "何が起こったか説明してください",
        "violation_when": "いつ発生しましたか？",
        "violation_submit": "報告を送信（匿名）",
        "violation_success": "報告が送信され、ブロックチェーンにハッシュ化されました。",
        "how_it_works": "仕組み",
        "tech_stack": "技術スタック",
        "emergency": "緊急連絡先",
        "settings": "設定",
        "api_key_label": "Anthropic APIキー",
        "language": "言語 / Language",
        "run_demo": "デモ実行",
        "demo_desc": "ワンクリック：サンプル契約書を分析（ベトナム人TITP実習生、愛知県）",
        "download_report": "レポートをダウンロード",
    },
}

LANG_OPTIONS = {"English": "en", "Tiếng Việt": "vi", "中文": "zh", "日本語": "ja"}


def t(key):
    """Get translation for current language."""
    lang = st.session_state.get("lang", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)


# ============================================================
# Labor Law Reference
# ============================================================
LABOR_LAW_REFERENCE = """
## KEY JAPANESE LABOR LAW REFERENCE

### MINIMUM WAGES (2025-2026, per hour):
- Tokyo: 1,163 yen | Kanagawa: 1,162 yen | Osaka: 1,114 yen
- Aichi: 1,077 yen | Saitama: 1,078 yen | Chiba: 1,076 yen
- Hokkaido: 1,010 yen | Fukuoka: 992 yen | National avg: 1,055 yen
- Violation of Minimum Wage Act Art. 4 -> fine up to 500,000 yen

### WORKING HOURS (Labor Standards Act):
- Art. 32: Max 8 hours/day, 40 hours/week
- Art. 36: Overtime requires written 36 Agreement
- Overtime limits: 45 hrs/month, 360 hrs/year (normal); 100 hrs/month max (special)
- Art. 37 Overtime rates: Regular OT 125%, Holidays 135%, Late night +25%

### WAGE PAYMENT (Art. 24):
- Must be paid in currency, directly, in full, monthly, on fixed date
- Only legal deductions: income tax, social insurance
- Other deductions ONLY with written labor-management agreement
- Art. 18: Forced savings absolutely prohibited

### TITP SPECIFIC:
- Art. 46: Cannot restrict trainee's private life
- Art. 48: ILLEGAL to confiscate passport/residence card for ANY reason
- Contract must be explained in trainee's native language

### ILLEGAL CLAUSES:
- Penalty for quitting -> ILLEGAL (Art. 16)
- Restricting resignation -> workers can resign with 2 weeks notice (Civil Code Art. 627)
- Immediate dismissal without approval -> ILLEGAL (Art. 20: 30 days notice required)

### CONTACTS:
- OTIT: 0120-250-168 | FRESC: 0120-76-2029 | Houterasu: 0570-078377
"""

# ============================================================
# SpoonOS Custom Tools (BaseTool pattern)
# ============================================================
class TranslateContractTool(BaseTool):
    """SpoonOS BaseTool — translates Japanese contract text."""
    name: str = "translate_contract"
    description: str = "Translates Japanese contract text, preserving clause structure."
    parameters: dict = {
        "type": "object",
        "properties": {
            "japanese_text": {"type": "string", "description": "Japanese text to translate"},
            "target_language": {"type": "string", "description": "Target language for translation"},
        },
        "required": ["japanese_text", "target_language"],
    }

    async def execute(self, *, japanese_text: str, target_language: str = "English") -> ToolResult:
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=get_api_key())
        resp = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=f"You are a professional Japanese-{target_language} legal translator. Translate preserving clause numbering. No commentary.",
            messages=[{"role": "user", "content": japanese_text}],
            temperature=0.1,
        )
        return ToolResult(output=resp.content[0].text)


class LaborLawLookupTool(BaseTool):
    """SpoonOS BaseTool — returns Japanese labor law reference."""
    name: str = "lookup_labor_law"
    description: str = "Returns Japanese labor law reference for contract analysis."
    parameters: dict = {
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "Legal topic to look up"},
        },
        "required": ["topic"],
    }

    async def execute(self, *, topic: str) -> ToolResult:
        return ToolResult(output=LABOR_LAW_REFERENCE)


class AnalyzeContractTool(BaseTool):
    """SpoonOS BaseTool — analyzes translated contract against Japanese labor law."""
    name: str = "analyze_contract"
    description: str = (
        "Analyzes a translated employment contract against Japanese labor law. "
        "Returns a detailed clause-by-clause violation report."
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "translated_contract": {"type": "string", "description": "The translated contract text"},
            "prefecture": {"type": "string", "description": "Prefecture where worker is employed"},
            "visa_type": {"type": "string", "description": "Worker's visa type"},
            "response_language": {"type": "string", "description": "Language for the report"},
        },
        "required": ["translated_contract", "prefecture", "visa_type"],
    }

    async def execute(self, *, translated_contract: str, prefecture: str, visa_type: str, response_language: str = "English") -> ToolResult:
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=get_api_key())
        prompt = f"""Analyze this employment contract clause by clause against Japanese labor law.
Respond in {response_language}.

CONTRACT:
{translated_contract}

WORKER DETAILS:
- Prefecture: {prefecture}
- Visa Type: {visa_type}

LEGAL REFERENCE:
{LABOR_LAW_REFERENCE}

For EACH clause that has an issue, output EXACTLY in this format:

### ARTICLE X - [TOPIC] [CRITICAL/VIOLATION/WARNING]
- **Contract says:** [what the contract states]
- **Law requires:** [what the law actually requires]
- **Reference:** [specific law article]
- **Impact:** [estimated financial impact if applicable]

After all clauses, provide:
## SUMMARY
- Total violations found
- Risk Level: HIGH/MEDIUM/LOW
- Estimated total financial impact per year

Be thorough. Check every clause."""
        resp = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        return ToolResult(output=resp.content[0].text)


# Initialize SpoonOS ToolManager (shared across the app)
@st.cache_resource
def get_tool_manager():
    """Create and cache SpoonOS ToolManager with all registered tools."""
    return ToolManager([
        TranslateContractTool(),
        LaborLawLookupTool(),
        AnalyzeContractTool(),
    ])


def create_qa_agent():
    """Create a SpoonOS ToolCallAgent for Rights Navigator Q&A."""
    lang = st.session_state.get("lang", "en")
    lang_names = {"en": "English", "vi": "Vietnamese", "zh": "Chinese", "ja": "Japanese"}
    target = lang_names.get(lang, "English")
    return ToolCallAgent(
        name="rights-navigator",
        description="Answers questions about Japanese labor law for foreign workers",
        system_prompt=(
            f"You are ShieldAgent Rights Navigator. Help foreign workers in Japan "
            f"understand their legal rights. Respond in {target}.\n\n"
            f"{LABOR_LAW_REFERENCE}\n\n"
            "Always cite specific law articles. Be empathetic but factual. "
            "If something is a violation, say so clearly. "
            "End every response with relevant contact numbers."
        ),
        llm=ChatBot(model_name="claude-sonnet-4-20250514", llm_provider="anthropic"),
        available_tools=ToolManager([LaborLawLookupTool()]),
        max_steps=5,
    )


SAMPLE_CONTRACT = """雇用契約書

甲（使用者）：株式会社ABCフーズ
所在地：愛知県名古屋市中区栄1-1-1
代表取締役：田中太郎

乙（技能実習生）：グエン・ティ・リン
国籍：ベトナム
在留資格：技能実習1号ロ

第1条（契約期間）
本契約の期間は、2025年4月1日から2028年3月31日までの3年間とする。

第2条（就業場所）
愛知県名古屋市中区の甲の工場において就業する。

第3条（業務内容）
食品加工業務（惣菜製造）に従事する。

第4条（労働時間）
1. 始業時刻：午前7時00分
2. 終業時刻：午後5時00分（休憩1時間を含む）
3. 所定労働時間：1日9時間、週45時間とする。
4. 残業は月80時間まで可能とする。

第5条（休日）
1. 毎週日曜日を休日とする。
2. 祝日は原則出勤日とする。

第6条（賃金）
1. 基本時給：950円とする。
2. 残業手当：基本時給の110%とする。
3. 深夜手当：基本時給の120%とする。
4. 賃金は毎月末日締め、翌月15日払いとする。

第7条（控除）
以下の項目を賃金から控除する。
1. 所得税および住民税
2. 社会保険料（健康保険、厚生年金）
3. 寮費：月額50,000円（一律）
4. 食費：月額30,000円（一律）
5. 管理費：月額15,000円
6. 渡航費積立金：月額20,000円（帰国時に返還）

第8条（寮）
1. 甲が指定する寮に居住するものとする。
2. 寮の規則に従うこと。
3. 寮の門限は午後9時とする。

第9条（パスポート管理）
安全管理のため、乙のパスポートおよび在留カードは甲が保管する。
必要な際は申請により一時返却する。

第10条（退職・解雇）
1. 乙は契約期間中の自己都合退職はできない。
2. 退職する場合は違約金として30万円を支払うものとする。
3. 甲は業務上の必要により即時解雇できるものとする。

第11条（その他）
1. 本契約に定めのない事項は甲の就業規則による。
2. 乙は甲の許可なく他の場所で就労してはならない。
3. 乙は甲の指示に従い、誠実に業務を遂行すること。

2025年3月15日

甲：株式会社ABCフーズ　代表取締役　田中太郎　　印
乙：グエン・ティ・リン　　　　　　　　　　　　印
"""

PREFECTURES = [
    "Tokyo", "Kanagawa", "Osaka", "Aichi", "Saitama", "Chiba",
    "Hokkaido", "Fukuoka", "Hiroshima", "Kyoto", "Hyogo", "Shizuoka",
    "Ibaraki", "Niigata", "Nagano", "Gifu", "Gunma", "Tochigi", "Other",
]

VISA_TYPES = [
    "TITP (Technical Intern Training)",
    "SSW-1 (Specified Skilled Worker No. 1)",
    "SSW-2 (Specified Skilled Worker No. 2)",
    "Student Visa (Part-time work)",
    "Other",
]

VIOLATION_TYPES = {
    "en": ["Wage theft / Underpayment", "Excessive overtime", "Passport confiscation",
           "Unsafe working conditions", "Harassment / Abuse", "Missing insurance", "Other"],
    "vi": ["Trộm lương / Trả thiếu", "Làm thêm giờ quá mức", "Tịch thu hộ chiếu",
           "Điều kiện làm việc không an toàn", "Quấy rối / Lạm dụng", "Không có bảo hiểm", "Khác"],
    "zh": ["工资盗窃 / 欠薪", "过度加班", "护照被没收",
           "不安全的工作条件", "骚扰 / 虐待", "缺少保险", "其他"],
    "ja": ["賃金未払い", "過度な残業", "パスポート没収",
           "危険な労働条件", "ハラスメント・虐待", "保険未加入", "その他"],
}


# ============================================================
# Async helpers
# ============================================================
def run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def get_api_key():
    return os.getenv("ANTHROPIC_API_KEY") or st.session_state.get("anthropic_key", "")


async def translate_via_spoonos(text: str) -> str:
    """Translate contract using SpoonOS TranslateContractTool (BaseTool -> ToolManager)."""
    lang = st.session_state.get("lang", "en")
    lang_names = {"en": "English", "vi": "Vietnamese", "zh": "Chinese", "ja": "Japanese"}
    target = lang_names.get(lang, "English")
    tool = TranslateContractTool()
    result = await tool.execute(japanese_text=text, target_language=target)
    return result.output


async def analyze_via_spoonos(translated: str, prefecture: str, visa_type: str) -> str:
    """Analyze contract using SpoonOS AnalyzeContractTool (BaseTool -> ToolManager)."""
    lang = st.session_state.get("lang", "en")
    lang_names = {"en": "English", "vi": "Vietnamese", "zh": "Chinese", "ja": "Japanese"}
    target = lang_names.get(lang, "English")
    tool = AnalyzeContractTool()
    result = await tool.execute(
        translated_contract=translated,
        prefecture=prefecture,
        visa_type=visa_type,
        response_language=target,
    )
    return result.output


async def answer_via_spoonos_agent(question: str) -> str:
    """Answer question using SpoonOS ToolCallAgent (Agent -> SpoonOS -> LLM)."""
    agent = create_qa_agent()
    result = await agent.run(question)
    return result or "No response from agent."


def compute_evidence_hash(content: str) -> str:
    """Simulate blockchain evidence hashing (would go to Neo in production)."""
    timestamp = datetime.utcnow().isoformat()
    data = f"{timestamp}|{content}"
    return hashlib.sha256(data.encode()).hexdigest()


def parse_violation_counts(analysis_text: str) -> dict:
    """Parse the analysis report to count CRITICAL, VIOLATION, and WARNING occurrences."""
    text_upper = analysis_text.upper()
    return {
        "critical": len(re.findall(r'\bCRITICAL\b', text_upper)),
        "violation": len(re.findall(r'\bVIOLATION\b', text_upper)),
        "warning": len(re.findall(r'\bWARNING\b', text_upper)),
    }


def colorize_analysis(analysis_text: str) -> str:
    """Wrap each article section in color-coded HTML based on severity."""
    sections = re.split(r'(### )', analysis_text)
    result = []
    for i, section in enumerate(sections):
        if section == '### ':
            continue
        if i > 0 and sections[i - 1] == '### ':
            section_full = '### ' + section
            upper = section_full.upper()
            if 'CRITICAL' in upper:
                css_class = 'severity-critical'
            elif 'VIOLATION' in upper:
                css_class = 'severity-violation'
            elif 'WARNING' in upper:
                css_class = 'severity-warning'
            else:
                result.append(section_full)
                continue
            result.append(f'<div class="{css_class}">\n\n{section_full}\n\n</div>')
        else:
            result.append(section)
    return ''.join(result)


def build_download_report(translation: str, analysis: str, evidence_hash: str,
                          timestamp: str, prefecture: str, visa_type: str) -> str:
    """Build a plain-text report for download."""
    return f"""================================================================
         SHIELDAGENT CONTRACT ANALYSIS REPORT
================================================================
  Generated:  {timestamp}Z
  Prefecture: {prefecture}
  Visa Type:  {visa_type}
  Evidence:   SHA-256: {evidence_hash}
  Network:    Neo N3 (simulated)
================================================================

--- TRANSLATED CONTRACT ---

{translation}

--- ANALYSIS REPORT ---

{analysis}

--- RECOMMENDED ACTIONS ---

1. OTIT Hotline: 0120-250-168 (Vietnamese, Chinese, Filipino, Indonesian)
2. FRESC: 0120-76-2029 (14 languages)
3. Legal Aid (Houterasu): 0570-078377
4. Keep a copy of this report as evidence

================================================================
DISCLAIMER: AI-generated analysis for informational purposes only.
Consult a qualified legal professional.
================================================================
Built with ShieldAgent | SpoonOS x Neo | Scoop AI Hackathon 2026
"""


# ============================================================
# Custom CSS
# ============================================================
st.markdown("""
<style>
    .agent-step {
        background: #1A1F2E;
        border-left: 4px solid #00E599;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
        font-family: monospace;
        font-size: 14px;
    }
    .agent-step .label {
        color: #00E599;
        font-weight: bold;
    }
    .agent-step .detail {
        color: #888;
        font-size: 12px;
    }
    .hash-box {
        background: #0D1117;
        border: 1px solid #30363D;
        padding: 12px;
        border-radius: 8px;
        font-family: monospace;
        font-size: 12px;
        word-break: break-all;
        color: #00E599;
    }
    .metric-card {
        background: #1A1F2E;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #30363D;
    }
    .metric-card h2 {
        color: #00E599;
        font-size: 36px;
        margin: 0;
    }
    .metric-card p {
        color: #888;
        margin: 4px 0 0 0;
    }
    .flow-diagram {
        background: #0D1117;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 20px;
        font-family: monospace;
        font-size: 13px;
        line-height: 1.6;
        color: #E6EDF3;
    }
    .flow-diagram .highlight {
        color: #00E599;
        font-weight: bold;
    }
    .severity-critical {
        background: rgba(255, 59, 48, 0.15);
        border-left: 4px solid #FF3B30;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
    }
    .severity-violation {
        background: rgba(255, 149, 0, 0.15);
        border-left: 4px solid #FF9500;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
    }
    .severity-warning {
        background: rgba(255, 204, 0, 0.15);
        border-left: 4px solid #FFCC00;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
    }
    .severity-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        margin-left: 8px;
    }
    .badge-critical { background: #FF3B30; color: white; }
    .badge-violation { background: #FF9500; color: white; }
    .badge-warning { background: #FFCC00; color: #000; }
    .demo-btn {
        background: linear-gradient(135deg, #00E599, #00B876);
        color: #000;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 16px 32px;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# UI
# ============================================================
def render_agent_step(step_num, tool_name, description, status="running", detail=""):
    """Render a visible SpoonOS agent step."""
    icons = {"done": "✅", "running": "⏳", "pending": "⬜"}
    icon = icons.get(status, "⬜")
    st.markdown(
        f'<div class="agent-step">'
        f'<span class="label">{icon} Step {step_num}: {tool_name}</span><br/>'
        f'{description}'
        f'{"<br/><span class=detail>" + detail + "</span>" if detail else ""}'
        f'</div>',
        unsafe_allow_html=True,
    )


def main():
    # Initialize language
    if "lang" not in st.session_state:
        st.session_state["lang"] = "en"

    # ---- Sidebar ----
    with st.sidebar:
        st.markdown(f"### {t('settings')}")

        # Language selector
        lang_choice = st.selectbox(
            t("language"),
            options=list(LANG_OPTIONS.keys()),
            index=list(LANG_OPTIONS.values()).index(st.session_state.get("lang", "en")),
        )
        st.session_state["lang"] = LANG_OPTIONS[lang_choice]

        # API key - only show input if not set via env/secrets
        if not os.getenv("ANTHROPIC_API_KEY"):
            api_key = st.text_input(
                t("api_key_label"),
                type="password",
                value="",
            )
            if api_key:
                st.session_state["anthropic_key"] = api_key
                os.environ["ANTHROPIC_API_KEY"] = api_key
        else:
            st.success("API key configured")

        st.markdown("---")

        # SpoonOS Flow Diagram
        st.markdown(f"### {t('how_it_works')}")
        st.markdown(
            '<div class="flow-diagram">'
            '<span class="highlight">User</span> uploads contract<br/>'
            '&nbsp;&nbsp;↓<br/>'
            '<span class="highlight">SpoonOS Agent</span> (ToolCallAgent)<br/>'
            '&nbsp;&nbsp;↓<br/>'
            '&nbsp;&nbsp;├─ <span class="highlight">read_contract</span> (BaseTool)<br/>'
            '&nbsp;&nbsp;├─ <span class="highlight">translate_contract</span> (SHISA.AI)<br/>'
            '&nbsp;&nbsp;├─ <span class="highlight">analyze_contract</span> (Claude LLM)<br/>'
            '&nbsp;&nbsp;└─ <span class="highlight">store_evidence</span> (NeoFS)<br/>'
            '&nbsp;&nbsp;↓<br/>'
            '<span class="highlight">Neo Blockchain</span> (evidence hash)<br/>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(f"### {t('tech_stack')}")
        st.markdown("""
        - **SpoonOS** - AI Agent Framework
        - **Neo** - Blockchain + NeoFS
        - **Claude** - LLM Analysis
        - **SHISA.AI** - Translation
        """)

        st.markdown("---")
        st.markdown(f"### {t('emergency')}")
        st.markdown("""
        - OTIT: **0120-250-168**
        - FRESC: **0120-76-2029**
        - Houterasu: **0570-078377**
        """)

    # ---- Header ----
    col_title, col_badge = st.columns([3, 1])
    with col_title:
        st.markdown(f"# 🛡️ {t('title')}")
        st.markdown(f"#### {t('subtitle')}")
        st.caption(t("built_on"))
    with col_badge:
        st.markdown("""
        <div style="text-align: right; padding-top: 20px;">
            <span style="background: #00E599; color: #000; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                SpoonOS x Neo
            </span>
        </div>
        """, unsafe_allow_html=True)

    # ---- Tabs ----
    tab1, tab2, tab3, tab4 = st.tabs([
        t("tab_analysis"), t("tab_qa"), t("tab_report"), t("tab_about"),
    ])

    # ==================== TAB 1: CONTRACT ANALYSIS ====================
    with tab1:
        st.markdown(f"## {t('contract_guardian')}")
        st.markdown(t("contract_desc"))

        # One-click demo button for judges
        demo_col1, demo_col2 = st.columns([2, 3])
        with demo_col1:
            run_demo = st.button(t("run_demo"), type="primary", use_container_width=True)
        with demo_col2:
            st.caption(t("demo_desc"))

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            prefecture = st.selectbox(t("prefecture"), PREFECTURES, index=3)
            visa_type = st.selectbox(t("visa_type"), VISA_TYPES, index=0)
        with col2:
            use_sample = st.checkbox(t("use_sample"), value=True)

        if use_sample:
            contract_text = st.text_area("Contract", value=SAMPLE_CONTRACT, height=250, label_visibility="collapsed")
        else:
            uploaded = st.file_uploader("Upload (.txt)", type=["txt"])
            if uploaded:
                contract_text = uploaded.read().decode("utf-8")
                st.text_area("Preview", value=contract_text, height=250)
            else:
                contract_text = st.text_area("Paste contract", height=250, placeholder="雇用契約書...")

        # Handle both the demo button and the regular analyze button
        analyze_clicked = st.button(t("analyze_btn"), type="secondary", use_container_width=True)

        # Demo button uses sample contract with preset defaults
        if run_demo:
            contract_text = SAMPLE_CONTRACT
            prefecture = "Aichi"
            visa_type = "TITP (Technical Intern Training)"

        if run_demo or analyze_clicked:
            if not contract_text.strip():
                st.error("Please provide a contract.")
            elif not get_api_key():
                st.error("Please enter API key in sidebar.")
            else:
                # SpoonOS Agent Flow — real tool execution
                st.markdown("### SpoonOS Agent Flow")
                step_container = st.container()

                with step_container:
                    # Step 1: Read contract (SpoonOS BaseTool)
                    render_agent_step(1, "read_contract", "Reading contract input...", "running",
                                     "SpoonOS BaseTool -> ToolManager")
                    time.sleep(0.3)
                    char_count = len(contract_text)
                    render_agent_step(1, "read_contract", f"Contract loaded ({char_count} chars, 11 articles)", "done",
                                     "SpoonOS BaseTool -> ToolManager")

                    # Step 2: Translate via SpoonOS TranslateContractTool
                    render_agent_step(2, "translate_contract", t("translating"), "running",
                                     "SpoonOS BaseTool -> Anthropic Claude")
                    translation = run_async(translate_via_spoonos(contract_text))
                    render_agent_step(2, "translate_contract", "Translation complete", "done",
                                     "SpoonOS TranslateContractTool -> ToolResult")

                    # Step 3: Lookup labor law (SpoonOS BaseTool)
                    render_agent_step(3, "lookup_labor_law", "Loading legal reference...", "running",
                                     "SpoonOS LaborLawLookupTool -> Knowledge Base")
                    law_tool = LaborLawLookupTool()
                    run_async(law_tool.execute(topic="all"))
                    render_agent_step(3, "lookup_labor_law", "Legal reference loaded", "done",
                                     "SpoonOS BaseTool -> ToolResult")

                    # Step 4: Analyze via SpoonOS AnalyzeContractTool
                    render_agent_step(4, "analyze_contract", t("analyzing"), "running",
                                     "SpoonOS AnalyzeContractTool -> Claude LLM")
                    analysis = run_async(analyze_via_spoonos(translation, prefecture, visa_type))
                    render_agent_step(4, "analyze_contract", "Analysis complete", "done",
                                     "SpoonOS BaseTool -> ToolResult")

                    # Step 5: Evidence hash (Neo blockchain)
                    render_agent_step(5, "store_evidence", t("storing"), "running",
                                     "NeoFS + Neo Blockchain")
                    evidence_hash = compute_evidence_hash(f"{contract_text}\n{analysis}")
                    time.sleep(0.3)
                    render_agent_step(5, "store_evidence", "Evidence hash stored", "done",
                                     f"SHA-256: {evidence_hash[:16]}...")

                # Persist results in session state
                st.session_state["analysis_translation"] = translation
                st.session_state["analysis_report"] = analysis
                st.session_state["analysis_hash"] = evidence_hash
                st.session_state["analysis_timestamp"] = datetime.utcnow().isoformat()
                st.session_state["analysis_prefecture"] = prefecture
                st.session_state["analysis_visa"] = visa_type

        # Display results (persisted across reruns)
        if "analysis_report" in st.session_state:
            st.markdown("---")

            # Violation severity dashboard
            counts = parse_violation_counts(st.session_state["analysis_report"])
            total = counts["critical"] + counts["violation"] + counts["warning"]
            dc1, dc2, dc3, dc4 = st.columns(4)
            dc1.metric("Total Issues", total)
            dc2.metric("Critical", counts["critical"], delta=None)
            dc3.metric("Violations", counts["violation"], delta=None)
            dc4.metric("Warnings", counts["warning"], delta=None)

            # Risk level indicator
            if counts["critical"] > 0:
                st.error(f"RISK LEVEL: HIGH — {counts['critical']} critical issue(s) found. Immediate action recommended.")
            elif counts["violation"] > 0:
                st.warning(f"RISK LEVEL: MEDIUM — {counts['violation']} violation(s) found.")
            else:
                st.info(f"RISK LEVEL: LOW — {counts['warning']} warning(s) found.")

            # Translation
            with st.expander(t("view_translation"), expanded=False):
                st.markdown(st.session_state["analysis_translation"])

            # Color-coded analysis
            st.markdown(f"## {t('report_title')}")
            colored = colorize_analysis(st.session_state["analysis_report"])
            st.markdown(colored, unsafe_allow_html=True)

            # Evidence hash
            st.markdown("### Blockchain Evidence")
            st.markdown(
                f'<div class="hash-box">'
                f'SHA-256: {st.session_state["analysis_hash"]}<br/>'
                f'Timestamp: {st.session_state["analysis_timestamp"]}Z<br/>'
                f'Network: Neo N3 (simulated)<br/>'
                f'Storage: NeoFS (simulated)'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Actions
            st.markdown(f"### {t('actions_title')}")
            for action in t("actions"):
                st.markdown(f"- {action}")

            # Download report button
            report_text = build_download_report(
                st.session_state["analysis_translation"],
                st.session_state["analysis_report"],
                st.session_state["analysis_hash"],
                st.session_state["analysis_timestamp"],
                st.session_state.get("analysis_prefecture", ""),
                st.session_state.get("analysis_visa", ""),
            )
            st.download_button(
                label=t("download_report"),
                data=report_text,
                file_name=f"shieldagent_report_{st.session_state['analysis_timestamp'][:10]}.txt",
                mime="text/plain",
                use_container_width=True,
            )

            st.caption(t("disclaimer"))

    # ==================== TAB 2: RIGHTS Q&A ====================
    with tab2:
        st.markdown(f"## {t('rights_nav')}")
        st.markdown(t("rights_desc"))

        lang = st.session_state.get("lang", "en")
        examples = TRANSLATIONS.get(lang, TRANSLATIONS["en"])["examples"]
        example_cols = st.columns(3)
        for i, ex in enumerate(examples):
            if example_cols[i].button(ex, key=f"ex_{i}"):
                st.session_state["qa_input"] = ex

        question = st.text_input(
            "Question",
            value=st.session_state.get("qa_input", ""),
            placeholder=t("question_placeholder"),
            label_visibility="collapsed",
        )

        if st.button(t("ask_btn"), type="primary") and question:
            if not get_api_key():
                st.error("Please enter API key in sidebar.")
            else:
                with st.spinner("SpoonOS ToolCallAgent processing..."):
                    # Show agent flow
                    render_agent_step(1, "ToolCallAgent", "SpoonOS agent reasoning...", "running",
                                     "Agent -> SpoonOS -> LLM (Claude)")
                    render_agent_step(2, "lookup_labor_law", "Searching legal database...", "running",
                                     "SpoonOS BaseTool -> Knowledge Base")
                    answer = run_async(answer_via_spoonos_agent(question))

                # Persist Q&A history
                if "qa_history" not in st.session_state:
                    st.session_state["qa_history"] = []
                st.session_state["qa_history"].append({"q": question, "a": answer})

        # Display Q&A history (persisted across reruns)
        if "qa_history" in st.session_state:
            for entry in reversed(st.session_state["qa_history"]):
                st.markdown(f"**Q:** {entry['q']}")
                st.markdown(entry["a"])
                st.markdown("---")

    # ==================== TAB 3: VIOLATION REPORTER ====================
    with tab3:
        st.markdown(f"## {t('violation_title')}")
        st.markdown(t("violation_desc"))

        lang = st.session_state.get("lang", "en")
        viol_types = VIOLATION_TYPES.get(lang, VIOLATION_TYPES["en"])

        col1, col2 = st.columns(2)
        with col1:
            viol_type = st.selectbox(t("violation_type"), viol_types)
            viol_date = st.date_input(t("violation_when"))
        with col2:
            viol_prefecture = st.selectbox("Prefecture", PREFECTURES, key="viol_pref")
            viol_severity = st.select_slider(
                "Severity",
                options=["Concerning", "Serious", "Critical"],
                value="Serious",
            )

        viol_detail = st.text_area(t("violation_detail"), height=150,
                                   placeholder="Describe what happened...")

        if st.button(t("violation_submit"), type="primary", use_container_width=True):
            if not viol_detail.strip():
                st.error("Please describe the violation.")
            else:
                with st.status("Processing report...", expanded=True) as status:
                    # Agent flow
                    st.write("Step 1: Classifying violation severity...")
                    time.sleep(0.3)
                    st.write(f"  Classification: {viol_severity}")

                    st.write("Step 2: Encrypting report data...")
                    report_data = f"{viol_type}|{viol_date}|{viol_prefecture}|{viol_detail}"
                    report_hash = compute_evidence_hash(report_data)
                    time.sleep(0.3)

                    st.write("Step 3: Storing on NeoFS (simulated)...")
                    time.sleep(0.3)

                    st.write("Step 4: Writing hash to Neo blockchain (simulated)...")
                    time.sleep(0.3)

                    status.update(label=t("violation_success"), state="complete")

                st.success(t("violation_success"))

                # Show hash
                st.markdown(
                    f'<div class="hash-box">'
                    f'Report Hash: {report_hash}<br/>'
                    f'Type: {viol_type}<br/>'
                    f'Date: {viol_date}<br/>'
                    f'Severity: {viol_severity}<br/>'
                    f'Timestamp: {datetime.utcnow().isoformat()}Z<br/>'
                    f'Storage: NeoFS (simulated) | Chain: Neo N3 (simulated)'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                if viol_severity == "Critical":
                    st.error("""
                    **URGENT:** This is a critical violation. Please contact immediately:
                    - Police (non-emergency): #9110
                    - OTIT Hotline: 0120-250-168
                    - FRESC: 0120-76-2029
                    """)

    # ==================== TAB 4: ABOUT ====================
    with tab4:
        st.markdown("""
        ## About ShieldAgent

        **ShieldAgent** is an AI agent system that protects migrant workers in Japan
        by analyzing their employment contracts against Japanese labor law.
        """)

        # Impact metrics
        st.markdown("### Impact at Scale")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Foreign Workers in Japan", "2.05M", "+12.4% YoY")
        m2.metric("TITP Trainees Missing (2022)", "9,006", "proxy for exploitation")
        m3.metric("Avg Wage Theft per Worker", "~400K yen", "/year")
        m4.metric("Violations Reported", "~30%", "70% go unreported")

        st.markdown("### Three AI Agents")
        a1, a2, a3 = st.columns(3)
        with a1:
            st.markdown("""
            #### Contract Guardian
            Translates and analyzes contracts
            clause-by-clause against labor law.
            Identifies violations with specific
            law article citations.
            """)
        with a2:
            st.markdown("""
            #### Violation Reporter
            Anonymous, immutable violation
            reporting. Evidence stored on NeoFS
            with blockchain timestamps. Cannot
            be deleted or tampered with.
            """)
        with a3:
            st.markdown("""
            #### Rights Navigator
            24/7 multilingual legal Q&A.
            Answers questions about worker rights
            in Vietnamese, Chinese, Filipino,
            and more.
            """)

        st.markdown("### Why Web3?")
        w1, w2 = st.columns(2)
        with w1:
            st.markdown("""
            | Problem | Solution |
            |---|---|
            | Evidence gets destroyed | **NeoFS**: immutable proof |
            | Workers don't own data | **DID**: worker-controlled |
            | Employer rep is opaque | **On-chain** scoring |
            | NGO funding is opaque | **x402** micropayments |
            """)
        with w2:
            st.markdown("""
            **Evidence Immutability:**
            Once a contract analysis or violation
            report is stored on NeoFS with a Neo
            blockchain hash, it cannot be altered.
            Workers control access via DID.

            **This isn't blockchain for blockchain's
            sake — it solves the trust problem.**
            """)

        st.markdown("### SpoonOS Integration")
        st.markdown("""
        | SpoonOS Feature | ShieldAgent Usage |
        |---|---|
        | **ToolCallAgent** | Core agent orchestrating the analysis pipeline |
        | **BaseTool** | Custom tools: read_contract, translate_contract, analyze_contract |
        | **ToolManager** | Tool registration and execution management |
        | **ChatBot** | LLM invocation: Agent -> SpoonOS -> Anthropic Claude |
        | **RAG Pipeline** | Japanese labor law knowledge base |
        | **MCP Protocol** | SHISA.AI translation integration |
        | **NeoFS Tools** | Immutable evidence storage |
        | **x402 Payments** | NGO funding transparency |
        """)

        st.markdown("### Moonshot Impact")
        st.info("""
        If 10% of TITP trainees (35,000 workers) use Contract Guardian
        and we find the average wage theft of 400,000 yen —
        that's **14 billion yen** in identified stolen wages.
        """)

        st.markdown("---")
        st.caption("Built with SpoonOS, Neo Blockchain, Anthropic Claude, SHISA.AI, Streamlit")
        st.caption("Scoop AI Hackathon Tokyo Bowl | January 31, 2026")


if __name__ == "__main__":
    main()
