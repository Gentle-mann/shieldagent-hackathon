"""
ShieldAgent — AI-Powered Legal Shield for Migrant Workers in Japan
Scoop AI Hackathon Tokyo Bowl | Built on SpoonOS × Neo

Demo: Contract Guardian Agent
Analyzes Japanese employment contracts against labor law using:
- SpoonOS ToolCallAgent (Agent → SpoonOS → LLM)
- SpoonOS Tools (BaseTool, ToolManager)
- Custom Translation Tool (SHISA.AI / Anthropic Claude for JA→EN translation)
- Custom Legal Analysis Pipeline
"""

import asyncio
import os
from dotenv import load_dotenv

from spoon_ai.chat import ChatBot
from spoon_ai.agents.toolcall import ToolCallAgent
from spoon_ai.tools import ToolManager
from spoon_ai.tools.base import BaseTool, ToolResult

load_dotenv()

# ============================================================
# Japanese Labor Law Reference
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
- Art. 36: Overtime requires written 36 Agreement filed with Labor Standards Office
- Overtime limits: 45 hrs/month, 360 hrs/year (normal); 100 hrs/month max (special)
- Art. 37 Overtime rates:
  - Regular OT: 125% (1.25x)
  - Statutory holidays: 135% (1.35x)
  - Late night (22:00-05:00): +25% premium
  - OT + late night: 150% (1.50x)

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
- Forced savings -> ILLEGAL (Art. 18)
- Restricting resignation -> workers can resign with 2 weeks notice (Civil Code Art. 627)
- Immediate dismissal without approval -> ILLEGAL (Art. 20: 30 days notice required)
- Curfew on adults -> potential Art. 46 violation

### CONTACTS:
- OTIT: 0120-250-168 | FRESC: 0120-76-2029 | Houterasu: 0570-078377
"""


# ============================================================
# Custom Tools (SpoonOS BaseTool pattern)
# ============================================================
class ReadContractTool(BaseTool):
    name: str = "read_contract"
    description: str = "Reads a contract text file from disk and returns its contents."
    parameters: dict = {
        "type": "object",
        "properties": {
            "file_path": {"type": "string", "description": "Path to the contract file"},
        },
        "required": ["file_path"],
    }

    async def execute(self, *, file_path: str) -> ToolResult:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return ToolResult(output=f.read())
        except Exception as e:
            return ToolResult(output=f"Error: {e}")


class TranslateContractTool(BaseTool):
    name: str = "translate_contract"
    description: str = "Translates Japanese contract text to English, preserving clause structure."
    parameters: dict = {
        "type": "object",
        "properties": {
            "japanese_text": {"type": "string", "description": "Japanese text to translate"},
        },
        "required": ["japanese_text"],
    }

    async def execute(self, *, japanese_text: str) -> ToolResult:
        import anthropic
        shisa_key = os.getenv("SHISA_API_KEY")
        if shisa_key:
            import openai
            client = openai.AsyncOpenAI(
                api_key=shisa_key,
                base_url=os.getenv("SHISA_BASE_URL", "https://talk.shisa.ai/v1"),
            )
            resp = await client.chat.completions.create(
                model="shisa-v2.1-70b",
                messages=[
                    {"role": "system", "content": "You are a professional Japanese-English legal translator. Translate preserving clause numbering. No commentary."},
                    {"role": "user", "content": japanese_text},
                ],
                temperature=0.1,
            )
            return ToolResult(output=resp.choices[0].message.content)
        else:
            client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            resp = await client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system="You are a professional Japanese-English legal translator. Translate preserving clause numbering. No commentary.",
                messages=[{"role": "user", "content": japanese_text}],
                temperature=0.1,
            )
            return ToolResult(output=resp.content[0].text)


class LaborLawLookupTool(BaseTool):
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
    """The core analysis tool — sends contract + law to LLM for clause-by-clause analysis."""
    name: str = "analyze_contract"
    description: str = (
        "Analyzes a translated employment contract against Japanese labor law. "
        "Provide the English translation and the worker's details. "
        "Returns a detailed clause-by-clause violation report."
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "translated_contract": {"type": "string", "description": "The English translation of the contract"},
            "prefecture": {"type": "string", "description": "Prefecture where worker is employed"},
            "visa_type": {"type": "string", "description": "Worker's visa type (e.g., TITP, SSW-1)"},
        },
        "required": ["translated_contract", "prefecture", "visa_type"],
    }

    async def execute(self, *, translated_contract: str, prefecture: str, visa_type: str) -> ToolResult:
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        analysis_prompt = f"""Analyze this employment contract clause by clause against Japanese labor law.

CONTRACT:
{translated_contract}

WORKER DETAILS:
- Prefecture: {prefecture}
- Visa Type: {visa_type}

LEGAL REFERENCE:
{LABOR_LAW_REFERENCE}

For EACH clause that has an issue, output in this exact format:

ARTICLE X - [TOPIC]                    [CRITICAL/VIOLATION/WARNING]
  Contract says: [what the contract states]
  Law requires: [what the law actually requires]
  Reference: [specific law article]
  Impact: [estimated financial impact if applicable]

After all clauses, provide:
SUMMARY: X violations found, Y warnings
RISK LEVEL: HIGH/MEDIUM/LOW

Be thorough. Check every clause. This worker's rights depend on your analysis."""

        resp = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": analysis_prompt}],
            temperature=0.0,
        )
        return ToolResult(output=resp.content[0].text)


# ============================================================
# Main Demo — Pipeline Approach
# ============================================================
async def main():
    print("=" * 64)
    print("  ShieldAgent - Contract Guardian Demo")
    print("  AI Agent x Web3 for Migrant Worker Protection")
    print("  Built on SpoonOS | Scoop AI Hackathon Tokyo Bowl")
    print("=" * 64)
    print()

    # Initialize tools via SpoonOS ToolManager
    tools = ToolManager([
        ReadContractTool(),
        TranslateContractTool(),
        LaborLawLookupTool(),
        AnalyzeContractTool(),
    ])

    # Create SpoonOS agent
    agent = ToolCallAgent(
        name="shield_contract_guardian",
        description="Analyzes Japanese employment contracts for labor law violations",
        system_prompt=(
            "You are ShieldAgent Contract Guardian. You protect migrant workers "
            "by analyzing their employment contracts against Japanese labor law.\n\n"
            "Follow these steps IN ORDER:\n"
            "1. Use read_contract to read the file\n"
            "2. Use translate_contract to translate to English\n"
            "3. Use analyze_contract with the translation, prefecture, and visa type\n"
            "4. Return the analysis results to the user with a formatted header and footer\n\n"
            "You MUST call all three tools before responding."
        ),
        llm=ChatBot(model_name="claude-sonnet-4-20250514", llm_provider="anthropic"),
        available_tools=tools,
        max_steps=10,
    )

    contract_path = os.path.join(
        os.path.dirname(__file__), "sample_contracts", "sample_contract_ja.txt"
    )

    print(f"  Analyzing: {contract_path}")
    print(f"  Worker: Vietnamese TITP trainee, Aichi Prefecture")
    print(f"  Agent: SpoonOS ToolCallAgent -> Anthropic Claude")
    print(f"  Tools: read_contract, translate_contract, analyze_contract")
    print()
    print("-" * 64)

    result = await agent.run(
        f"Analyze the contract at {contract_path}. "
        f"The worker is a Vietnamese TITP trainee in Aichi prefecture. "
        f"Read it, translate it, then analyze it for violations."
    )

    # Print the report
    print()
    print("=" * 64)
    print("         SHIELDAGENT CONTRACT ANALYSIS REPORT")
    print("=" * 64)
    print(f"  Employer:    ABC Foods Co., Ltd. (Aichi)")
    print(f"  Worker:      TITP Trainee (Vietnam)")
    print(f"  Agent Flow:  Agent -> SpoonOS -> LLM")
    print("=" * 64)
    print()

    if result:
        print(result)
    else:
        print("[Agent returned no text — analysis was completed in tool steps above]")

    print()
    print("=" * 64)
    print("  RECOMMENDED ACTIONS")
    print("=" * 64)
    print("  1. OTIT Hotline: 0120-250-168 (VN, CN, PH, ID)")
    print("  2. FRESC: 0120-76-2029 (14 languages)")
    print("  3. Legal Aid (Houterasu): 0570-078377")
    print("  4. Keep this report as evidence")
    print("=" * 64)
    print()
    print("  DISCLAIMER: AI-generated analysis for informational")
    print("  purposes only. Consult a legal professional.")
    print("=" * 64)


# ============================================================
# Interactive Q&A Mode
# ============================================================
async def interactive():
    print("=" * 64)
    print("  ShieldAgent - Rights Navigator (Interactive)")
    print("  Ask questions about labor rights in Japan")
    print("  Type 'quit' to exit")
    print("=" * 64)
    print()

    navigator = ToolCallAgent(
        name="rights-navigator",
        description="Answers questions about Japanese labor law for foreign workers",
        system_prompt=(
            "You are ShieldAgent Rights Navigator. Help foreign workers in Japan "
            "understand their legal rights. Use lookup_labor_law when needed.\n\n"
            f"{LABOR_LAW_REFERENCE}\n\n"
            "Always cite specific law articles. Be empathetic but factual. "
            "If something is a violation, say so clearly. "
            "End every response with relevant contact numbers."
        ),
        llm=ChatBot(model_name="claude-sonnet-4-20250514", llm_provider="anthropic"),
        available_tools=ToolManager([LaborLawLookupTool()]),
        max_steps=5,
    )
    print("Ready. Ask any question about worker rights in Japan.\n")

    while True:
        try:
            question = input("Your question: ").strip()
            if question.lower() in ("quit", "exit", "q"):
                print("Goodbye! Remember: you have rights.")
                break
            if not question:
                continue
            print("\nAnalyzing...")
            answer = await navigator.run(question)
            print(f"\n{answer}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive())
    else:
        asyncio.run(main())
