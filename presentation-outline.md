# ShieldAgent - Presentation Deck
## Scoop AI Hackathon Tokyo Bowl | Jan 31, 2026

---

## SLIDE 1: Title Slide

**ShieldAgent**
AI-Powered Legal Shield for Migrant Workers in Japan

*AI Agent x Web3 for Labor Rights Protection*

Team: [Your Name]
Scoop AI Hackathon Tokyo Bowl | January 31, 2026

---

## SLIDE 2: The Problem (Emotional Hook)

**"I signed a contract I couldn't read. I lost 2 years of wages."**

- 2.05 million foreign workers in Japan — record high
- 9,006 TITP trainees went missing in 2022 alone (proxy for exploitation)
- Average wage theft per worker: 300,000 - 500,000 yen
- Only 30% of violations are ever reported

**Root cause: Language barriers + legal ignorance + fear of deportation**

> Speaker note: Open with Linh's story. "Imagine you're 24, you've moved
> to a country where you can't read the language, and someone hands you a
> 20-page contract to sign. You have no idea what you're agreeing to.
> This is the reality for hundreds of thousands of workers in Japan."

---

## SLIDE 3: Who Is Affected?

| Nationality | Workers | Japanese Literacy | Support Available |
|---|---|---|---|
| Vietnamese | 520,000 | Very Low | Limited |
| Chinese | 400,000 | Moderate | Some |
| Filipino | 230,000 | Low | Some NGO |
| Indonesian | 120,000 | Very Low | Minimal |
| Myanmar | 70,000 | Very Low | Almost None |
| Nepali | 150,000 | Very Low | Minimal |

**The most vulnerable workers have the least support.**

Japan plans to accept 820,000 more SSW workers by 2028.
The problem is growing, not shrinking.

> Speaker note: Emphasize that this is a structural issue, not individual
> bad actors. Japan needs these workers, but the system fails to protect them.

---

## SLIDE 4: Why Current Solutions Fail

| Solution | Limitation |
|---|---|
| OTIT Hotline | Limited hours, limited languages |
| FRESC Center | In-person only (Shinjuku), Japanese-heavy |
| Labor Inspection Office | Requires formal complaint, intimidating |
| NGOs | Overwhelmed, underfunded |
| Google Translate + ChatGPT | No legal context, hallucination risk, no evidence preservation |

**No existing solution provides:**
- 24/7 multilingual legal analysis
- Immutable evidence preservation
- Anonymous, safe reporting
- Transparent employer accountability

---

## SLIDE 5: Introducing ShieldAgent

**ShieldAgent** = AI Agent system that protects migrant workers through:

1. **Contract Guardian** — Analyzes employment contracts against Japanese law
2. **Violation Reporter** — Anonymous, immutable violation reporting
3. **Rights Navigator** — 24/7 multilingual legal Q&A

Built on **SpoonOS** + **Neo blockchain**

> Speaker note: "ShieldAgent is a system of three AI agents that work
> together to give migrant workers what they've never had: an always-available,
> multilingual legal advisor that preserves evidence they control."

---

## SLIDE 6: Agent 1 — Contract Guardian (Core Feature)

**Flow:**
1. Worker photographs their Japanese employment contract
2. SHISA.AI translates to worker's native language
3. AI Agent analyzes every clause against Japanese labor law via RAG
4. Flags violations with specific law article citations
5. Generates multilingual risk report
6. Stores contract + analysis on NeoFS (immutable, worker-controlled)

**What it checks:**
- Wage vs. prefectural minimum wage
- Working hours vs. legal limits (Labor Standards Act Art. 32)
- Overtime rates (125%/135%/150%)
- Illegal deductions
- Insurance enrollment
- Prohibited clauses (passport confiscation, penalty for quitting)

**Output: Clear, actionable report in the worker's language**

---

## SLIDE 7: Contract Guardian — Example Output

```
CONTRACT ANALYSIS REPORT
========================
Worker: [Anonymous ID via DID]
Employer: ABC Manufacturing Co., Ltd.
Prefecture: Aichi | Visa Type: TITP

CLAUSE 3 - WAGES                          [VIOLATION]
  Contract states: 950 yen/hour
  Legal minimum (Aichi 2026): 1,077 yen/hour
  Reference: Minimum Wage Act, Art. 4
  Underpayment: ~127 yen/hour = ~203,200 yen/year

CLAUSE 7 - HOUSING DEDUCTION              [WARNING]
  Contract states: Flat 50,000 yen/month deduction
  Legal requirement: Actual cost only, must be itemized
  Reference: Labor Standards Act, Art. 24
  Action: Request itemized cost breakdown from employer

CLAUSE 12 - PASSPORT STORAGE              [CRITICAL]
  Contract states: "Company will store passport for safety"
  This is ILLEGAL under Immigration Control Act
  Reference: TITP Act, Art. 48(1)
  Action: Immediately contact OTIT: 0120-250-168

OVERALL RISK: HIGH (3 issues found)
```

> Speaker note: Walk through this example. The power is in the specificity —
> not "this might be wrong" but "this violates Article 4 of the Minimum
> Wage Act and you're losing 203,200 yen per year."

---

## SLIDE 8: Agent 2 — Violation Reporter

**Problem:** Evidence disappears. Employers delete messages, alter timesheets.
Workers have no proof.

**Solution: Immutable, anonymous reporting on NeoFS**

Flow:
1. AI Agent guides worker through structured questions (native language)
2. Classifies severity: CRITICAL / SERIOUS / CONCERNING
3. Evidence (photos, messages, pay stubs) encrypted and stored on NeoFS
4. Blockchain hash = timestamped proof that cannot be altered
5. Worker controls access via DID — not employer, not platform, not government
6. Anonymized data feeds employer reputation score

**Critical cases** (passport confiscation, trafficking indicators) →
immediate routing to police + OTIT + NGOs

---

## SLIDE 9: Agent 3 — Rights Navigator

**24/7 multilingual legal Q&A with persistent memory**

The agent remembers the worker's context across conversations:
- Visa type, employer, prefecture, contract dates
- Previous issues discussed
- Upcoming deadlines (visa renewal, contract end)

**Example:**
> Worker: "My boss says I can't change jobs."
>
> Agent: "Under your TITP visa, job changes are currently restricted
> except in cases of employer abuse or bankruptcy. However, Japan is
> transitioning to the 'Ikusei Shuro' system in 2027 which will allow
> transfers after 1-2 years. Your current options are:
> 1. If you're experiencing abuse → you CAN transfer (contact OTIT)
> 2. If your contract ends → you can switch to SSW-1 visa
> 3. Would you like me to assess if your situation qualifies?"

Built with SpoonOS Memory mixin for persistent context.

---

## SLIDE 10: Why Web3? (Critical Slide)

| Without Blockchain | With Neo + NeoFS |
|---|---|
| Evidence can be deleted | Immutable, timestamped proof |
| Workers depend on platforms | Workers own their data via DID |
| Employer reputation is opaque | Transparent, tamper-proof scores |
| Funding for NGOs is opaque | x402 micropayments, outcome-based |
| Identity tied to employer | Portable DID across jobs & countries |

**Web3 is not optional here — it solves the trust problem.**

Workers don't trust employers. Workers don't trust platforms.
Workers don't trust governments.

**They need a system where trust is enforced by math, not institutions.**

> Speaker note: This is the most important slide for judges. Be ready to
> defend why blockchain is necessary. The key argument: evidence immutability
> and worker data sovereignty. These aren't possible with traditional infra.

---

## SLIDE 11: Technical Architecture

```
                    ShieldAgent System
    ┌───────────────────────────────────────────┐
    │                                           │
    │  Contract     Violation     Rights        │
    │  Guardian     Reporter      Navigator     │
    │  (ReAct)      (Graph)       (ReAct+Mem)   │
    │      │            │             │         │
    │      └────────────┼─────────────┘         │
    │                   │                       │
    │           SpoonOS Core Layer              │
    │    ┌──────┬───────┬────────┬────────┐    │
    │    │ LLM  │  RAG  │  MCP   │ Memory │    │
    │    └──┬───┘───┬───┘───┬────┘───┬────┘    │
    └───────┼───────┼───────┼────────┼──────────┘
            │       │       │        │
     ┌──────┴──┐ ┌──┴──┐ ┌─┴──────┐ ┌┴────────┐
     │ LLM API │ │NeoFS│ │SHISA.AI│ │   Neo   │
     │(via Spn)│ │     │ │Trans.  │ │Blockchain│
     └─────────┘ └─────┘ └────────┘ └──────────┘
```

**SpoonOS Integration:**
- LLM invocation: Agent → SpoonOS → OpenAI/Claude (required flow)
- RAG: Japanese labor law knowledge base (Spoon RAG tools)
- MCP: SHISA.AI translation API integration
- NeoFS Tools: Immutable document storage
- Memory: Persistent worker context
- x402: Payment rails for NGO funding
- DID: Portable worker identity

---

## SLIDE 12: SpoonOS Deep Integration

| SpoonOS Feature | ShieldAgent Usage |
|---|---|
| **ReAct Agent** | Contract analysis reasoning loop — multi-step legal checking |
| **Graph Agent** | Violation reporting workflow with state management |
| **RAG Pipeline** | Ingest Japanese labor law, immigration regulations, TITP rules |
| **NeoFS Tools** | Store contracts, reports, evidence — immutable & encrypted |
| **Memory Mixin** | Remember worker profile, visa dates, past conversations |
| **MCP Protocol** | Connect SHISA.AI translation, external legal databases |
| **x402 Payments** | Transparent micro-donations to legal aid organizations |
| **DID (ERC-8004)** | Portable worker identity across employers and borders |

**We use 8 SpoonOS features — this isn't a wrapper, it's a deep integration.**

---

## SLIDE 13: Sponsor Technology Usage

| Sponsor | How We Use It |
|---|---|
| **SpoonOS** | Core agent framework — all 3 agents built on SCDF |
| **Neo** | Blockchain for evidence hashing, DID, employer reputation |
| **SHISA.AI** | Translation API for contract analysis + multilingual chat |
| **Zilliz** | Vector DB backend for RAG legal knowledge base |
| **Supabase** | User session management and API layer |
| **Lovable** | Rapid UI prototyping for demo interface |

---

## SLIDE 14: Impact & Scale

**Direct Impact (Year 1 target):**
- 10,000 contracts analyzed
- 2,000 violations identified
- est. 800 million yen in wage theft flagged
- 500 workers connected to legal aid

**Systemic Impact:**
- Public employer reputation data → market pressure for compliance
- Aggregated violation data → policy recommendations to MHLW
- Reduced TITP disappearances through early intervention

**Moonshot:**
> "If 10% of TITP trainees (35,000 workers) use Contract Guardian
> and we find the average wage theft of 400,000 yen —
> that's **14 billion yen** in identified stolen wages."

---

## SLIDE 15: Business Model

| Phase | Model | Revenue |
|---|---|---|
| **Phase 1 (Now)** | Free for workers, grant-funded | 0 (social impact) |
| **Phase 2 (Scale)** | Employer Compliance Certification | 50,000-100,000 yen/employer/year |
| **Phase 3 (Ecosystem)** | Gov contracts + insurance integration | 10B+ yen addressable market |

**Key insight:** The same AI that protects workers can help *good* employers
prove compliance. Employers who pass get an on-chain "ShieldAgent Certified"
badge — recruitment agencies prefer certified employers.

**200,000 host companies x 50,000 yen = 10 billion yen market**

---

## SLIDE 16: Roadmap

**Today:** Contract Guardian agent demo (SpoonOS + SHISA.AI + RAG)

**Q2 2026:** Violation Reporter + NeoFS integration

**Q3 2026:** Rights Navigator with Memory + NGO partnerships

**Q4 2026:** Employer Certification pilot program

**2027:** Multi-country expansion (aligned with Ikusei Shuro launch)

---

## SLIDE 17: Team & Why Us

[Add your team info here]

- Passion for social impact
- Technical expertise in AI + Web3
- Understanding of Japan's migrant worker challenges

---

## SLIDE 18: Closing Slide

**ShieldAgent**
*Because no one should sign away their rights in a language they can't read.*

- AI Agents that understand law
- Web3 that preserves truth
- Technology that protects the vulnerable

**Built on SpoonOS x Neo**

---

## APPENDIX: Presentation Tips

1. **Open with emotion** (Slides 2-3): Tell Linh's story. Make judges FEEL the problem.
2. **Show the gap** (Slide 4): Current solutions are failing.
3. **Solution with specifics** (Slides 5-9): The contract analysis example output is your strongest moment. Walk through it line by line.
4. **Defend Web3** (Slide 10): Be ready for "why blockchain?" — evidence immutability and data sovereignty.
5. **Show technical depth** (Slides 11-12): Demonstrate you understand SpoonOS deeply.
6. **End with impact** (Slides 14-15): The 14 billion yen number is memorable.
7. **Close emotionally** (Slide 18): Bring it back to the human impact.

**Time allocation (assuming 5 min presentation):**
- Problem: 1 min (slides 2-4)
- Solution: 2 min (slides 5-9, focus on contract guardian example)
- Why Web3 + Tech: 1 min (slides 10-12)
- Impact + Close: 1 min (slides 14-18)
