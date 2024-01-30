# -*- coding: utf-8 -*-

'''
@Author : Jiangjie Chen
@Time   : 2024/01/29 12:15
@Contact: jjchen19@fudan.edu.cn
'''

import argparse 
from collections import defaultdict
import json



# keep updating
model_map_cost_per_1k = {
    'gpt-3.5-turbo-0301': [0.0015, 0.002],
    'gpt-3.5-turbo-0613': [0.0015, 0.002],
    'gpt-3.5-turbo-16k-0613': [0.003, 0.004],
    'gpt-3.5-turbo-1106': [0.001, 0.002],
    'gpt-3.5-turbo-instruct': [0.0015, 0.002],
    'gpt-3.5-turbo-0125': [0.0005, 0.0015],
    'gpt-4-0314': [0.03, 0.06],
    'gpt-4-0613': [0.03, 0.06],
    'gpt-4-1106-preview': [0.01, 0.03],
    'gpt-4-0125-preview': [0.01, 0.03],
}


def calculate_total_cost_per_user(data, cost_map):
    user_costs = defaultdict(lambda: defaultdict(float))

    for entry in data:
        if not entry.get('model'): continue
        model = entry["model"]

        if model not in cost_map:
            continue  # Skip if the model is not in the cost map

        context_token_cost, generated_token_cost = cost_map[model]

        # Calculate costs
        context_cost = (entry["n_context_tokens_total"] / 1000) * context_token_cost
        generated_cost = (entry["n_generated_tokens_total"] / 1000) * generated_token_cost
        total_cost = context_cost + generated_cost

        # Accumulate cost per user and model
        user = entry["user"]
        user_costs[user][model] += total_cost

    for user in user_costs:
        total = 0
        for m in user_costs[user]:
            total += user_costs[user][m]
        user_costs[user]['total'] = total
            
    return user_costs



def test():
    example = [
        {
            "operation": "completion",
            "n_context_tokens_total": 3380842,
            "n_generated_tokens_total": 71105,
            "api_key_id": None,
            "api_key_name": None,
            "api_key_redacted": None,
            "usage_type": "text",
            "model": "gpt-4-1106-preview",
            "timestamp": 1704067200,
            "user": "User 1",
            "num_requests": 526
        },
        {
            "operation": "completion",
            "n_context_tokens_total": 10664577,
            "n_generated_tokens_total": 76450,
            "api_key_id": None,
            "api_key_name": None,
            "api_key_redacted": None,
            "usage_type": "text",
            "model": "gpt-3.5-turbo-1106",
            "timestamp": 1704067200,
            "user": "User 1",
            "num_requests": 1346
        },
        {
            "operation": "completion",
            "n_context_tokens_total": 354,
            "n_generated_tokens_total": 736,
            "api_key_id": None,
            "api_key_name": None,
            "api_key_redacted": None,
            "usage_type": "text",
            "model": "gpt-3.5-turbo-0613",
            "timestamp": 1704067200,
            "user": "User 2",
            "num_requests": 3
        }
    ]
    result = calculate_total_cost_per_user(example, model_map_cost_per_1k)
    print(result)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', 
        help='File path to the exported activity log from OpenAI Playground (https://platform.openai.com/usage). ' \
             'Example: `activity-2024-01-01-2024-02-01.json`')
    parser.add_argument('--all', '-a', action='store_true', help='Print API cost per model')
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    result = calculate_total_cost_per_user(data['data'], model_map_cost_per_1k)

    all_cost = 0
    for user in result:
        total = result[user].pop('total')
        all_cost += total
        
        print('=================================')
        print(f'* {user}: ${total}')
        if args.all:
            for model in result[user]:
                print(f"  - {model}: ${round(result[user][model], 2)}")
            print('=================================')
            print('')

    print(f'- Team Total Cost: ${all_cost}')