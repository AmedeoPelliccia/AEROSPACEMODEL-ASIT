#!/usr/bin/env python3
import argparse
import math
import sys
import yaml
from typing import Dict, Any, List


DOMAIN_KEYS = [
    "D1_verificability",
    "D2_transparency",
    "D3_privacy",
    "D4_security",
    "D5_governance",
    "D6_interop",
    "D7_identity",
    "D8_sustainability",
    "D9_antimisinf",
]


def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def clamp_score(x: Any) -> int:
    if not isinstance(x, (int, float)):
        raise ValueError(f"Score inválido (no numérico): {x}")
    # Reject non-integer floats (except integral floats like 3.0)
    if isinstance(x, float) and x != int(x):
        raise ValueError(f"Score debe ser entero, no flotante: {x}")
    xi = int(x)
    if xi < 0 or xi > 5:
        raise ValueError(f"Score fuera de rango 0..5: {x}")
    return xi


def maturity_from_total(total: int, levels: List[Dict[str, Any]]) -> str:
    for lv in levels:
        if lv["min"] <= total <= lv["max"]:
            return lv["id"]
    return "L1"


def evaluate(policy: Dict[str, Any], assessment: Dict[str, Any]) -> Dict[str, Any]:
    root = assessment.get("ngi_autoassessment", {})
    domains = root.get("domains", {})

    # Validate domains presence
    for d in DOMAIN_KEYS:
        if d not in domains:
            raise ValueError(f"Falta dominio requerido: {d}")

    # Validate evidence minimum items
    policy_domains = policy["policy"]["domains"]
    for d in DOMAIN_KEYS:
        min_items = policy_domains[d].get("required_evidence_min_items", 0)
        evidence = domains[d].get("evidence", [])
        if len(evidence) < min_items:
            raise ValueError(f"Dominio {d} requiere al menos {min_items} evidencias, tiene {len(evidence)}")

    # Weighted score
    total = 0.0
    for d in DOMAIN_KEYS:
        score = clamp_score(domains[d].get("score", 0))
        weight = policy_domains[d]["weight"]
        total += (score / 5.0) * weight

    # deterministic rounding (half up)
    total_int = int(math.floor(total + 0.5))

    # Read hard gates from policy
    s = {d: clamp_score(domains[d].get("score", 0)) for d in DOMAIN_KEYS}
    hard_gates = policy["policy"]["gates"]["hard"]
    hard_ok = True
    for gate in hard_gates:
        # Parse rule like "D1_verificability.score >= 3"
        rule = gate["rule"]
        if ".score >=" in rule:
            domain = rule.split(".score")[0]
            threshold = int(rule.split(">=")[1].strip())
            if s.get(domain, 0) < threshold:
                hard_ok = False
                break

    # Read soft gates from policy
    soft_gates = policy["policy"]["gates"]["soft"]
    soft_total_ok = True
    soft_min_domain_ok = True
    for gate in soft_gates:
        rule = gate["rule"]
        if gate["id"] == "SOFT_TOTAL":
            # Extract threshold from rule like "computed.total_score_0_100 >= 70"
            threshold = int(rule.split(">=")[1].strip())
            soft_total_ok = total_int >= threshold
        elif gate["id"] == "SOFT_MIN_DOMAIN":
            # Extract threshold from rule like "all_domain_scores >= 2"
            threshold = int(rule.split(">=")[1].strip())
            soft_min_domain_ok = all(v >= threshold for v in s.values())

    soft_ok = soft_total_ok and soft_min_domain_ok

    # Decision logic from policy
    if (not hard_ok) or (not soft_min_domain_ok):
        decision = "BLOCK"
    elif hard_ok and (not soft_total_ok):
        decision = "WARN"
    else:
        decision = "PASS"

    maturity = maturity_from_total(total_int, policy["policy"]["maturity_levels"])

    # Ensure computed block
    root.setdefault("computed", {})
    root["computed"]["total_score_0_100"] = total_int
    root["computed"]["maturity_level"] = maturity
    root["computed"]["hard_gates_passed"] = bool(hard_ok)
    root["computed"]["soft_gates_passed"] = bool(soft_ok)
    root["computed"]["publish_decision"] = decision

    # Default remediation if empty
    root.setdefault("remediation", [])
    if decision != "PASS" and not root["remediation"]:
        root["remediation"] = [
            "Improve failed hard gates first (D1/D3/D4/D7 >= 3).",
            "Raise any domain below 2 to at least 2.",
            "Increase total score to >= 70."
        ]

    return {"ngi_autoassessment": root}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", required=True)
    parser.add_argument("--assessment", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    policy = load_yaml(args.policy)
    assessment = load_yaml(args.assessment)
    result = evaluate(policy, assessment)

    with open(args.out, "w", encoding="utf-8") as f:
        yaml.safe_dump(result, f, sort_keys=False, allow_unicode=True)

    decision = result["ngi_autoassessment"]["computed"]["publish_decision"]
    print(f"NGI decision: {decision}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[NGI_EVAL_ERROR] {e}", file=sys.stderr)
        sys.exit(2)
