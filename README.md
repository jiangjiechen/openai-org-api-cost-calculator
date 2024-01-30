# openai-org-api-cost-calculator
A simple script that summarizes the OpenAI API usage ($) per organization member.

## Workflow

1. Export activity log from OpenAI Playground (https://platform.openai.com/usage).
   1. Example: `activity-2024-01-01-2024-02-01.json`
2. Run `python3 calc_openai_cost.py -i YOUR_ACTIVITY_LOG`.
   1. Use `-a` to show the detailed cost per model.
3. Cry over your wallet.
