(references/api/guardrails)=

# Guardrails

Built-in, language-agnostic guardrails — PII, prompt-injection, and
wrong-language — that register on an agent like any hand-written
guardrail.

## Factories

- `philharmonica.adk.guardrails.pii_guardrail`
- `philharmonica.adk.guardrails.injection_scan_guardrail`
- `philharmonica.adk.guardrails.semantic_scan_guardrail`
- `philharmonica.adk.guardrails.wrong_language_guardrail`

## Scanners

- `philharmonica.adk.guardrails.PatternScanner`
- `philharmonica.adk.guardrails.SemanticScanner`
- `philharmonica.adk.guardrails.SemanticMatch`

## Helpers

- `philharmonica.adk.guardrails.mask_pii_spans`
- `philharmonica.adk.guardrails.fence_untrusted_text`
- `philharmonica.adk.guardrails.detect_wrong_language`

## Defaults

- `philharmonica.adk.guardrails.DEFAULT_PII_MASK`
- `philharmonica.adk.guardrails.DEFAULT_INJECTION_EXEMPLARS`

Three further defaults, spelled out because their content is the
interesting part:

- `DEFAULT_PII_PATTERNS` — cheap, deterministic regex markers for the
  common injected identifiers: email addresses (ASCII and
  internationalized), URLs, and phone numbers. Override via the
  `patterns` argument of `pii_guardrail`.
- `DEFAULT_INJECTION_PATTERNS` — high-confidence injection markers:
  broad English phrases plus the classic "ignore the previous
  instructions" signature across FR/DE/ES/PT/RU/ZH/JA/HI/AR. Override
  via the `patterns` argument of `injection_scan_guardrail`.
- `DEFAULT_LANGUAGE_CODES` — target-language name to ISO 639-1 code,
  spanning every language the detector supports. Override via the
  `language_codes` argument of `wrong_language_guardrail`.

Agent-level guardrail configuration is documented under the
[Guardrails guide](../../guardrails/guardrail_hub.md).
