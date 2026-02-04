# GitHub Marketplace Actions Catalog for CNOT-Agent Orchestration

## Overview

This catalog documents GitHub Marketplace actions and apps that can be orchestrated as CNOT-gate agents in the AEROSPACEMODEL lifecycle simulation architecture. Each entry provides automation, AI inference, policy control, security scanning, provenance, or summarization capabilities for lifecycle governance and digital twins.

## Selection Criteria

Actions were selected based on:
- **Automation capabilities** for CI/CD integration
- **AI/LLM integration** for reasoning and summarization
- **Policy enforcement** and compliance gating
- **Security scanning** and vulnerability detection
- **SBOM generation** and provenance tracking
- **Lifecycle governance** support

---

## Actions Catalog

### 1. AI Inference Action
**Category:** AI Reasoning  
**Source:** `actions/ai-inference@v1` (verified)  
**License:** MIT (Official GitHub action)

**Description:**  
Calls models from GitHub Models (OpenAI, GPT-4, etc.) with a prompt or `.prompt.yml` file. Outputs AI responses as workflow outputs, enabling easy integration into CI/CD pipelines.

**Integration Points:**
- Direct workflow integration via GitHub Actions
- Supports prompt files and inline prompts
- Output as workflow variables for downstream steps

**Strengths:**
- ✅ Simplifies LLM invocation inside workflows
- ✅ Deterministic if prompt is fixed
- ✅ Official GitHub action with reliable support
- ✅ Integrated with GitHub Models subscription

**Risks:**
- ⚠️ Limited model choice (GitHub Models only)
- ⚠️ Cost implications for high-volume usage
- ⚠️ Must handle API secrets securely

**Compliance Notes:**
- Requires GitHub Models subscription
- Abide by GitHub Models usage policies
- Data handling governed by GitHub terms

**CNOT-Agent Use Cases:**
- AI-powered code summarization
- Natural language requirement extraction
- Automated documentation generation
- Decision support for lifecycle transitions

---

### 2. OpenHands AI Action
**Category:** AI Task Execution  
**Source:** `xinbenlv/openhands-ai-action`  
**License:** Apache-2.0

**Description:**  
Runs tasks using natural-language prompts via OpenHands framework. Supports different LLMs (default Claude-3 Sonnet) with logging and secure Docker-based execution.

**Integration Points:**
- Natural language task specification
- Multiple LLM backend support (OpenAI, Anthropic)
- Docker-based sandboxed execution
- Comprehensive logging

**Strengths:**
- ✅ Flexible model choice
- ✅ Good logging and traceability
- ✅ Secure execution environment
- ✅ Task-oriented interface

**Risks:**
- ⚠️ External API costs
- ⚠️ Complex secret management
- ⚠️ Tasks must be correctly specified

**Compliance Notes:**
- Apache-2.0 license
- Requires OpenAI or Anthropic API keys via secrets
- Ensure compliance with data-handling policies

**CNOT-Agent Use Cases:**
- Multi-step task automation
- Code generation and refactoring
- Test case generation
- Documentation updates

---

### 3. AI Code Reviewer
**Category:** Code Quality  
**Source:** `gaurav-nelson/github-actions-ai-code-reviewer`  
**License:** MIT

**Description:**  
Uses GPT-4 to review pull requests, offering suggestions and feedback. Filters files and posts comments directly in PRs.

**Integration Points:**
- Automatic PR review on push
- File filtering capabilities
- Direct PR comment integration

**Strengths:**
- ✅ Automates code review process
- ✅ Early issue detection
- ✅ Configurable file patterns

**Risks:**
- ⚠️ Potential false positives
- ⚠️ Sensitive code exposure to external API
- ⚠️ May require human review override

**Compliance Notes:**
- MIT license
- Requires OpenAI API key
- Data privacy governed by OpenAI API terms

**CNOT-Agent Use Cases:**
- Automated code quality gates
- Pre-certification code review
- Safety-critical code analysis
- Compliance checking

---

### 4. GHAS Policy as Code
**Category:** Policy Enforcement  
**Source:** `advanced-security/action-policy-as-code` (verified)  
**License:** Proprietary/OSS mix

**Description:**  
Runs policy files (YAML) to check risk thresholds across code scanning, secret scanning, dependency checks, and license validation. Returns results for gating releases.

**Integration Points:**
- GitHub Advanced Security (GHAS) integration
- YAML-based policy definitions
- Release gate enforcement
- Multi-scan aggregation

**Strengths:**
- ✅ Strong compliance gate mechanism
- ✅ Native GitHub integration
- ✅ Comprehensive security coverage
- ✅ Policy-as-code approach

**Risks:**
- ⚠️ Limited to GHAS customers
- ⚠️ Requires GHAS licensing

**Compliance Notes:**
- Proprietary GitHub Advanced Security features
- Consider GHAS licensing and entitlements
- Subject to GitHub enterprise agreements

**CNOT-Agent Use Cases:**
- Security compliance gates
- Vulnerability threshold enforcement
- License compliance validation
- Release approval automation

---

### 5. Setup OPA
**Category:** Policy Engine  
**Source:** `open-policy-agent/setup-opa`  
**License:** Apache-2.0

**Description:**  
Installs the Open Policy Agent (OPA) CLI and allows running Rego policy tests in workflows. Enables custom policy-as-code checks.

**Integration Points:**
- OPA CLI installation
- Rego policy execution
- Custom policy development
- Multi-resource policy queries

**Strengths:**
- ✅ Flexible policy engine
- ✅ Complex rule support
- ✅ Multi-resource queries
- ✅ Industry-standard policy language

**Risks:**
- ⚠️ Complexity in writing policies
- ⚠️ Requires Rego expertise

**Compliance Notes:**
- Apache-2.0 license
- Users must maintain their own policy code
- Open source and vendor-neutral

**CNOT-Agent Use Cases:**
- Custom governance rules
- Multi-stakeholder approval policies
- Configuration validation
- Compliance boundary enforcement

---

### 6. Anchore SBOM Action
**Category:** Supply Chain Security  
**Source:** `anchore/sbom-action` (verified)  
**License:** Apache-2.0

**Description:**  
Uses Syft to scan source code and container images, generating SBOMs in SPDX/CycloneDX formats. Uploads as workflow artifacts or release assets.

**Integration Points:**
- Source code scanning
- Container image scanning
- SPDX/CycloneDX format support
- Artifact upload integration

**Strengths:**
- ✅ Detailed software bill of materials
- ✅ Supply-chain transparency
- ✅ Multiple output formats
- ✅ Widely adopted standard

**Risks:**
- ⚠️ Scanning can increase build time
- ⚠️ Large artifacts for complex projects

**Compliance Notes:**
- Apache-2.0 license
- Sensitive to open source licensing
- Check export restrictions for certain components

**CNOT-Agent Use Cases:**
- Component provenance tracking
- License compliance validation
- Vulnerability assessment input
- Certification artifact generation

---

### 7. SBOM.sh Create
**Category:** Supply Chain Security  
**Source:** `codenotary/sbom.sh-create`  
**License:** Proprietary service

**Description:**  
Generates SBOMs via sbom.sh using tools like Trivy, Grype, Syft. Uploads SBOMs with shareable URL and optional vulnerability scanning.

**Integration Points:**
- Multiple scanner support (Trivy, Grype, Syft)
- Shareable SBOM URLs
- Integrated vulnerability scoring
- Third-party service integration

**Strengths:**
- ✅ Multiple scanner backends
- ✅ Vulnerability scoring
- ✅ Easy sharing via URLs

**Risks:**
- ⚠️ Depends on third-party service (sbom.sh)
- ⚠️ API costs and service availability

**Compliance Notes:**
- Proprietary service
- Check data handling agreements
- API costs may apply

**CNOT-Agent Use Cases:**
- Multi-tool SBOM generation
- Vulnerability tracking
- Component lifecycle management
- Supply chain attestation

---

### 8. GitHub Actions Usage Audit
**Category:** Audit & Tracking  
**Source:** GitHub community action  
**License:** MIT

**Description:**  
Audits workflow usage and prints minutes, budgets, repository and workflow metrics.

**Integration Points:**
- GitHub API integration
- Workflow metrics collection
- Budget tracking
- Usage reporting

**Strengths:**
- ✅ Cost tracking
- ✅ Audit trail generation
- ✅ Resource monitoring

**Risks:**
- ⚠️ Does not produce SBOM or security info
- ⚠️ Limited to usage metrics

**Compliance Notes:**
- MIT license
- Uses GitHub API
- No additional service dependencies

**CNOT-Agent Use Cases:**
- Agent execution cost tracking
- Workflow audit trails
- Resource optimization
- Budget compliance

---

### 9. AI GitHub Action
**Category:** Multi-Agent Orchestration  
**Source:** `aguirreibarra/ai-github-actions`  
**License:** MIT

**Description:**  
Uses OpenAI Agents framework to automate PR reviews, issue analysis, code scanning with custom instructions and traceable outputs.

**Integration Points:**
- OpenAI Agents framework
- Multi-step task automation
- Custom instruction support
- Traceable output generation

**Strengths:**
- ✅ Multi-step task support
- ✅ Tracing capabilities
- ✅ Complex agent workflows
- ✅ Customizable instructions

**Risks:**
- ⚠️ Depends on OpenAI API
- ⚠️ Experimental features
- ⚠️ May require significant tuning

**Compliance Notes:**
- MIT license
- Abide by OpenAI usage terms
- Experimental - use with caution

**CNOT-Agent Use Cases:**
- Complex lifecycle orchestration
- Multi-stage validation workflows
- Intelligent decision support
- Automated governance workflows

---

### 10. Action Policy
**Category:** Action Governance  
**Source:** `rob-derosa/action-policy`  
**License:** MIT

**Description:**  
Enforces allowed/prohibited actions in workflow YAML. Generates violations JSON output for prohibited actions, with optional follow-up scripts.

**Integration Points:**
- Workflow YAML scanning
- Policy file configuration
- JSON violation reports
- Script trigger support

**Strengths:**
- ✅ Controls marketplace action usage
- ✅ Structured violation output
- ✅ Automated enforcement

**Risks:**
- ⚠️ Policy list must be maintained
- ⚠️ May block legitimate actions

**Compliance Notes:**
- MIT license
- No external dependencies
- Local enforcement only

**CNOT-Agent Use Cases:**
- Agent authorization control
- Marketplace action governance
- Compliance boundary enforcement
- Security policy validation

---

### 11. SLSA Build Provenance Action
**Category:** Provenance & Attestation  
**Source:** `philips-labs/slsa-provenance-action`  
**License:** Apache-2.0

**Description:**  
Implements SLSA Level-1 provenance generation for release assets or build artifacts using in-toto attestations. Generates provenance.json during release.

**Integration Points:**
- SLSA framework integration
- in-toto attestation format
- Release asset attachment
- Build artifact linking

**Strengths:**
- ✅ Supply-chain security enhancement
- ✅ Auditability improvement
- ✅ Signed JSON provenance
- ✅ Industry standard format

**Risks:**
- ⚠️ Limited to SLSA Level-1
- ⚠️ May require additional steps for higher levels

**Compliance Notes:**
- Apache-2.0 license
- Follows SLSA specification
- Compatible with NIST guidance

**CNOT-Agent Use Cases:**
- Build artifact attestation
- Provenance vector generation
- Certification evidence
- Supply chain verification

---

### 12. ShiftLeft Security Multi-Scanner
**Category:** Security Scanning  
**Source:** ShiftLeft (maintenance mode)  
**License:** Apache-2.0

**Description:**  
Runs multi-scanner (credential scanning, SAST for multiple languages, open source dependency analysis) and generates HTML report. Project is in maintenance mode.

**Integration Points:**
- Multi-language SAST
- Credential scanning
- Dependency analysis
- HTML report generation
- PR status checks

**Strengths:**
- ✅ Comprehensive scanning
- ✅ License audit included
- ✅ PR integration

**Risks:**
- ⚠️ No longer actively developed
- ⚠️ May have false positives
- ⚠️ Limited support

**Compliance Notes:**
- Apache-2.0 license
- Maintenance mode means limited support
- Consider migration path

**CNOT-Agent Use Cases:**
- Legacy system scanning
- Multi-language projects
- Quick security assessment
- License compliance checking

---

### 13. AI Security Scanner
**Category:** AI-Powered Security  
**Source:** `scottman625/security-scanner-action`  
**License:** MIT

**Description:**  
Uses OpenAI (GPT-4) to detect security vulnerabilities in code, outputting SARIF reports integrated with GitHub code scanning.

**Integration Points:**
- GitHub code scanning integration
- SARIF report format
- OpenAI GPT-4 analysis
- Security tab visibility

**Strengths:**
- ✅ LLM-powered vulnerability detection
- ✅ Native GitHub integration
- ✅ SARIF standard format

**Risks:**
- ⚠️ Accuracy depends on LLM
- ⚠️ Requires OpenAI API key
- ⚠️ May produce false positives/negatives

**Compliance Notes:**
- MIT license
- Abide by OpenAI terms
- API costs apply

**CNOT-Agent Use Cases:**
- AI-powered security validation
- Vulnerability pre-screening
- Code quality gates
- Safety-critical code analysis

---

### 14. Black Duck Security Scan
**Category:** Enterprise Security  
**Source:** `blackduck-inc/blackduck-security`  
**License:** Proprietary (Synopsys)

**Description:**  
Runs SAST and Software Composition Analysis via Black Duck Bridge-CLI. Integrates multiple security products into GitHub workflows.

**Integration Points:**
- Black Duck Bridge-CLI
- SAST integration
- SCA integration
- Policy enforcement
- Enterprise reporting

**Strengths:**
- ✅ Industry-grade scanning
- ✅ Multi-language support
- ✅ Policy enforcement
- ✅ Enterprise features

**Risks:**
- ⚠️ Requires subscription
- ⚠️ Complex configuration
- ⚠️ Cost considerations

**Compliance Notes:**
- Proprietary Synopsys licensing
- Enterprise subscription required
- Commercial support available

**CNOT-Agent Use Cases:**
- Enterprise security compliance
- Advanced vulnerability detection
- License management
- Regulatory compliance

---

### 15. PR Summarizing using AI
**Category:** PR Summarization  
**Source:** `behrouz-rad/ai-pr-summarizer`  
**License:** MIT

**Description:**  
Generates concise summaries of PR changes using LLMs. Caches results and can upload summary artifacts. Uses Ollama for local model execution.

**Integration Points:**
- PR diff extraction
- Ollama integration
- Artifact upload
- Comment posting
- Caching support

**Strengths:**
- ✅ Improves review efficiency
- ✅ Customizable prompts
- ✅ Caching for performance

**Risks:**
- ⚠️ Summarization accuracy
- ⚠️ API/model costs
- ⚠️ Requires proper configuration

**Compliance Notes:**
- MIT license
- Uses OpenAI or local models via Ollama
- Abide by model provider terms

**CNOT-Agent Use Cases:**
- Automated change documentation
- Review acceleration
- Audit trail generation
- Stakeholder communication

---

### 16. SummarAIzeHub
**Category:** Issue Summarization  
**Source:** `zerebom/SummarAIzeHub`  
**License:** MIT

**Description:**  
Summarizes long GitHub issues when comment includes `/summarize-issue`. Requires OpenAI API key and PAT. Allows custom prompt templates.

**Integration Points:**
- Issue comment triggers
- OpenAI integration
- Custom prompt templates
- GitHub PAT authentication

**Strengths:**
- ✅ Helps manage large issues
- ✅ Command-based activation
- ✅ Template customization

**Risks:**
- ⚠️ External API usage
- ⚠️ Requires PAT management
- ⚠️ Cost per summarization

**Compliance Notes:**
- MIT license
- Abide by OpenAI and GitHub API terms
- PAT security considerations

**CNOT-Agent Use Cases:**
- Issue triage automation
- Requirements extraction
- Stakeholder communication
- Documentation generation

---

### 17. AI Commit Summary
**Category:** Commit Summarization  
**Source:** `dirtycajunrice/ai-commit-summary`  
**License:** MIT

**Description:**  
Generates commit-level and overall PR summaries using OpenAI gpt-4o-mini. Posts comments on PRs with structured summaries.

**Integration Points:**
- Commit analysis
- PR comment posting
- GPT-4o-mini integration
- Structured output

**Strengths:**
- ✅ Improves commit comprehension
- ✅ Cost-effective model
- ✅ Automated documentation

**Risks:**
- ⚠️ Model cost considerations
- ⚠️ Summarization quality
- ⚠️ May miss context

**Compliance Notes:**
- MIT license
- OpenAI API terms apply
- Cost per PR analysis

**CNOT-Agent Use Cases:**
- Commit documentation
- Change tracking
- Audit trail enhancement
- Review support

---

### 18. OpenAI Completions
**Category:** General LLM Integration  
**Source:** `Just-Moh-it/openai`  
**License:** Apache-2.0

**Description:**  
Provides wrapper around OpenAI's NodeJS SDK for chat/completions. Accepts openai-mode and openai-params JSON string for prompts and returns responses.

**Integration Points:**
- OpenAI NodeJS SDK wrapper
- JSON parameter passing
- Workflow output variables
- Generic completion support

**Strengths:**
- ✅ Simplifies LLM integration
- ✅ Flexible parameter support
- ✅ Generic use cases

**Risks:**
- ⚠️ Insecure parameter formatting possible
- ⚠️ Not domain-specific
- ⚠️ Requires careful configuration

**Compliance Notes:**
- Apache-2.0 license
- Abide by OpenAI terms
- JSON injection risks

**CNOT-Agent Use Cases:**
- Custom LLM workflows
- Generic AI tasks
- Prototyping
- Experimentation

---

## Category Summary

### AI Reasoning and Summarization
**Actions:** 1, 2, 3, 10, 15, 16, 17, 18  
**Use Cases:** Natural language reasoning, code/commit/issue summarization, classification, structured output generation for digital twin simulation or human review.

### Policy Gating and Compliance
**Actions:** 4, 5, 10  
**Use Cases:** Policy enforcement via GHAS or OPA, governance rule validation, compliance boundary enforcement.

### Supply Chain & Provenance
**Actions:** 6, 7, 11  
**Use Cases:** SBOM generation, provenance attestation, supply-chain transparency, certification evidence.

### Security Scanning
**Actions:** 12, 13, 14  
**Use Cases:** Vulnerability detection, SAST, SCA, credential scanning, license audit.

### Audit & Tracking
**Actions:** 8, 9  
**Use Cases:** Usage audit, workflow metrics, cost tracking, multi-agent orchestration.

---

## Integration with CNOT Gates

Each marketplace action can be integrated as a CNOT-gate agent at specific lifecycle transitions:

### Design → Verification
- **AI Code Reviewer** (action 3) for code quality gates
- **Setup OPA** (action 5) for design policy validation
- **AI Security Scanner** (action 13) for early vulnerability detection

### Verification → Certification
- **GHAS Policy as Code** (action 4) for compliance gating
- **Anchore SBOM Action** (action 6) for certification artifacts
- **SLSA Provenance** (action 11) for attestation generation

### Certification → Production
- **Black Duck Security Scan** (action 14) for final security validation
- **SBOM.sh Create** (action 7) for production SBOM
- **Action Policy** (action 10) for deployment governance

### Production → Operation → Maintenance
- **GitHub Actions Usage Audit** (action 8) for operational metrics
- **AI GitHub Action** (action 9) for incident analysis
- **SummarAIzeHub** (action 16) for issue triage

---

## Security and Compliance Considerations

### Secret Management
All actions requiring API keys must use GitHub Secrets:
```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Data Privacy
- Review data handling policies for all external APIs
- Consider data residency requirements
- Implement data minimization principles

### Cost Management
- Monitor API usage and costs
- Set budget alerts
- Use GitHub Actions Usage Audit (action 8)

### Licensing Compliance
- Verify license compatibility for all actions
- Document license obligations
- Maintain action inventory

---

## References

1. [GitHub Models](https://github.com/marketplace/actions/ai-inference)
2. [OpenHands AI](https://github.com/marketplace/actions/openhands-ai-action)
3. [AI Code Reviewer](https://github.com/marketplace/actions/ai-code-reviewer)
4. [GHAS Policy as Code](https://github.com/marketplace/actions/policy-as-code)
5. [Setup OPA](https://github.com/marketplace/actions/setup-opa)
6. [Anchore SBOM Action](https://github.com/marketplace/actions/sbom-action)
7. [SBOM.sh Create](https://github.com/marketplace/actions/sbom-sh-create)
8. [GitHub Actions Usage Audit](https://github.com/marketplace)
9. [AI GitHub Action](https://github.com/marketplace)
10. [Action Policy](https://github.com/marketplace)
11. [SLSA Provenance](https://github.com/philips-labs/slsa-provenance-action)
12. [ShiftLeft Security](https://github.com/marketplace)
13. [AI Security Scanner](https://github.com/marketplace)
14. [Black Duck Security](https://github.com/marketplace/actions/blackduck-security-scan)
15. [PR Summarizer](https://github.com/marketplace)
16. [SummarAIzeHub](https://github.com/zerebom/SummarAIzeHub)
17. [AI Commit Summary](https://github.com/marketplace)
18. [OpenAI Completions](https://github.com/Just-Moh-it/openai)

---

## Conclusion

This catalog provides a comprehensive inventory of GitHub Marketplace actions suitable for CNOT-agent orchestration in aerospace lifecycle management. Each action has been evaluated for its integration potential, compliance requirements, and security considerations.

For implementation guidance, see `CNOT_AGENT_LIFECYCLE_ARCHITECTURE.md`.
