"""
ShieldAgent — Streamlit Web Demo
AI-Powered Legal Shield for Migrant Workers in Japan
Built on SpoonOS × Neo | Scoop AI Hackathon Tokyo Bowl
"""

import streamlit as st
import asyncio
import os

# Page config
st.set_page_config(
    page_title="ShieldAgent - Contract Guardian",
    page_icon="🛡️",
    layout="wide",
)

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
    "Ibaraki", "Niigata", "Nagano", "Gifu", "Gunma", "Tochigi",
    "Other",
]

VISA_TYPES = [
    "TITP (Technical Intern Training)",
    "SSW-1 (Specified Skilled Worker No. 1)",
    "SSW-2 (Specified Skilled Worker No. 2)",
    "Student Visa (Part-time work)",
    "Other",
]


# ============================================================
# Async helpers
# ============================================================
def run_async(coro):
    """Run async function in Streamlit context."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


async def translate_text(text: str) -> str:
    """Translate Japanese text to English."""
    import anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY") or st.session_state.get("anthropic_key", "")
    if not api_key:
        return "Error: No API key configured"
    client = anthropic.AsyncAnthropic(api_key=api_key)
    resp = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system="You are a professional Japanese-English legal translator. Translate preserving clause numbering. No commentary.",
        messages=[{"role": "user", "content": text}],
        temperature=0.1,
    )
    return resp.content[0].text


async def analyze_contract(translated: str, prefecture: str, visa_type: str) -> str:
    """Analyze contract against labor law."""
    import anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY") or st.session_state.get("anthropic_key", "")
    if not api_key:
        return "Error: No API key configured"
    client = anthropic.AsyncAnthropic(api_key=api_key)

    prompt = f"""Analyze this employment contract clause by clause against Japanese labor law.

CONTRACT:
{translated}

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
    return resp.content[0].text


async def answer_question(question: str) -> str:
    """Answer a labor rights question."""
    import anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY") or st.session_state.get("anthropic_key", "")
    if not api_key:
        return "Error: No API key configured"
    client = anthropic.AsyncAnthropic(api_key=api_key)
    resp = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=(
            "You are ShieldAgent Rights Navigator. Help foreign workers in Japan "
            "understand their legal rights.\n\n"
            f"{LABOR_LAW_REFERENCE}\n\n"
            "Always cite specific law articles. Be empathetic but factual. "
            "If something is a violation, say so clearly. "
            "End every response with relevant contact numbers."
        ),
        messages=[{"role": "user", "content": question}],
        temperature=0.2,
    )
    return resp.content[0].text


# ============================================================
# UI
# ============================================================
def main():
    # Header
    st.markdown("""
    # ShieldAgent
    ### AI-Powered Legal Shield for Migrant Workers in Japan
    **Built on SpoonOS x Neo** | Scoop AI Hackathon Tokyo Bowl 2026
    """)

    # Sidebar - API key config
    with st.sidebar:
        st.markdown("## Settings")
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            value=os.getenv("ANTHROPIC_API_KEY", ""),
            help="Required for contract analysis",
        )
        if api_key:
            st.session_state["anthropic_key"] = api_key
            os.environ["ANTHROPIC_API_KEY"] = api_key

        st.markdown("---")
        st.markdown("## How It Works")
        st.markdown("""
        1. Upload/paste a Japanese employment contract
        2. ShieldAgent translates and analyzes it
        3. Get a detailed violation report
        4. Know your rights, take action
        """)
        st.markdown("---")
        st.markdown("## Tech Stack")
        st.markdown("""
        - **SpoonOS** - AI Agent Framework
        - **Neo Blockchain** - Immutable evidence
        - **Anthropic Claude** - LLM Analysis
        - **SHISA.AI** - JA/EN Translation
        """)
        st.markdown("---")
        st.markdown("""
        **Emergency Contacts:**
        - OTIT: 0120-250-168
        - FRESC: 0120-76-2029
        - Legal Aid: 0570-078377
        """)

    # Main tabs
    tab1, tab2, tab3 = st.tabs([
        "Contract Analysis",
        "Rights Q&A",
        "About",
    ])

    # ---- Tab 1: Contract Analysis ----
    with tab1:
        st.markdown("## Contract Guardian")
        st.markdown("Upload or paste a Japanese employment contract to check for legal violations.")

        col1, col2 = st.columns(2)

        with col1:
            prefecture = st.selectbox("Worker's Prefecture", PREFECTURES, index=3)  # Default: Aichi
            visa_type = st.selectbox("Visa Type", VISA_TYPES, index=0)  # Default: TITP

        with col2:
            use_sample = st.checkbox("Use sample contract (demo)", value=True)

        if use_sample:
            contract_text = st.text_area(
                "Japanese Contract Text",
                value=SAMPLE_CONTRACT,
                height=300,
            )
        else:
            uploaded = st.file_uploader("Upload contract file (.txt)", type=["txt"])
            if uploaded:
                contract_text = uploaded.read().decode("utf-8")
                st.text_area("Contract Preview", value=contract_text, height=300)
            else:
                contract_text = st.text_area(
                    "Or paste Japanese contract text here",
                    height=300,
                    placeholder="雇用契約書\n\n甲（使用者）：...",
                )

        if st.button("Analyze Contract", type="primary", use_container_width=True):
            if not contract_text.strip():
                st.error("Please provide a contract to analyze.")
            elif not (os.getenv("ANTHROPIC_API_KEY") or st.session_state.get("anthropic_key")):
                st.error("Please enter your Anthropic API key in the sidebar.")
            else:
                # Step 1: Translate
                with st.status("Analyzing contract...", expanded=True) as status:
                    st.write("Step 1: Translating contract from Japanese to English...")
                    translation = run_async(translate_text(contract_text))

                    st.write("Step 2: Analyzing each clause against Japanese labor law...")
                    analysis = run_async(analyze_contract(translation, prefecture, visa_type))

                    status.update(label="Analysis complete!", state="complete")

                # Show results
                st.markdown("---")

                # Translation
                with st.expander("View English Translation", expanded=False):
                    st.markdown(translation)

                # Analysis Report
                st.markdown("## Analysis Report")
                st.markdown(analysis)

                # Action items
                st.markdown("---")
                st.error("""
                **Recommended Actions:**
                1. OTIT Hotline: **0120-250-168** (Vietnamese, Chinese, Filipino, Indonesian)
                2. FRESC: **0120-76-2029** (14 languages)
                3. Legal Aid (Houterasu): **0570-078377**
                4. Keep a copy of this report as evidence
                """)

                st.caption("Disclaimer: This analysis is AI-generated for informational purposes only. Consult a qualified legal professional.")

    # ---- Tab 2: Rights Q&A ----
    with tab2:
        st.markdown("## Rights Navigator")
        st.markdown("Ask any question about your labor rights in Japan.")

        # Example questions
        st.markdown("**Example questions:**")
        example_cols = st.columns(3)
        examples = [
            "Can my employer take my passport?",
            "What is minimum wage in Tokyo?",
            "Can I change employers on TITP visa?",
        ]
        for i, ex in enumerate(examples):
            if example_cols[i].button(ex, key=f"ex_{i}"):
                st.session_state["qa_input"] = ex

        question = st.text_input(
            "Your question:",
            value=st.session_state.get("qa_input", ""),
            placeholder="Type your question about labor rights in Japan...",
        )

        if st.button("Ask ShieldAgent", type="primary") and question:
            if not (os.getenv("ANTHROPIC_API_KEY") or st.session_state.get("anthropic_key")):
                st.error("Please enter your Anthropic API key in the sidebar.")
            else:
                with st.spinner("Searching labor law database..."):
                    answer = run_async(answer_question(question))
                st.markdown("### Answer")
                st.markdown(answer)

    # ---- Tab 3: About ----
    with tab3:
        st.markdown("""
        ## About ShieldAgent

        **ShieldAgent** is an AI agent system that protects migrant workers in Japan
        by analyzing their employment contracts against Japanese labor law and identifying
        violations.

        ### The Problem

        - **2.05 million** foreign workers in Japan (record high)
        - **9,006** TITP trainees went missing in 2022 (proxy for exploitation)
        - Average wage theft: **300,000 - 500,000 yen** per worker
        - Only **~30%** of violations are ever reported
        - **Root cause:** Language barriers + legal ignorance + fear of deportation

        ### Our Solution: Three AI Agents

        | Agent | Purpose |
        |---|---|
        | **Contract Guardian** | Translates and analyzes contracts clause-by-clause |
        | **Violation Reporter** | Anonymous, immutable violation reporting on NeoFS |
        | **Rights Navigator** | 24/7 multilingual legal Q&A |

        ### Why Web3?

        | Problem | Web3 Solution |
        |---|---|
        | Evidence gets destroyed | NeoFS: immutable, timestamped proof |
        | Workers don't own their data | DID: worker-controlled identity |
        | Employer reputation is opaque | On-chain transparent scoring |
        | NGO funding is opaque | x402 micropayments |

        ### Technical Architecture

        ```
        User -> ShieldAgent (SpoonOS ToolCallAgent)
                    |
                    +-> read_contract (BaseTool)
                    +-> translate_contract (SHISA.AI / Claude)
                    +-> analyze_contract (Claude + Labor Law RAG)
                    +-> lookup_labor_law (Legal Knowledge Base)
                    |
                    +-> SpoonOS -> LLM (Anthropic Claude)
                    +-> NeoFS (Immutable Storage)
                    +-> Neo Blockchain (Evidence Hashing)
        ```

        ### Impact Potential

        > If 10% of TITP trainees (35,000 workers) use Contract Guardian
        > and we find the average wage theft of 400,000 yen,
        > that's **14 billion yen** in identified stolen wages.

        ---

        **Built with:** SpoonOS, Neo Blockchain, Anthropic Claude, SHISA.AI, Streamlit

        **Hackathon:** Scoop AI Hackathon Tokyo Bowl | January 31, 2026
        """)


if __name__ == "__main__":
    main()
