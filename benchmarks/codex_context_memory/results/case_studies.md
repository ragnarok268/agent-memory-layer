# Qualitative Case Studies

## memory_challenge_b

Baseline:
- Detected random or UUID-style identifiers despite the deterministic ID decision.
- Intent violations: 2
- Architecture regression: True
- Rediscovery required: None

AML:
- Preserved the relevant prior decision according to the scoring receipt.
- Prior decision preserved: True
- Memory artifact consulted: True
- Architecture regression: False

Outcome:
- Prior architectural knowledge was reused in the AML condition.

## memory_challenge_c

Baseline:
- Preserved the relevant prior decision according to the scoring receipt.
- Intent violations: 0
- Architecture regression: False
- Rediscovery required: None

AML:
- Preserved the relevant prior decision according to the scoring receipt.
- Prior decision preserved: True
- Memory artifact consulted: True
- Architecture regression: False

Outcome:
- Both conditions preserved the relevant decision; no material AML-only benefit is shown by this pair.
