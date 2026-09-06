import time
import statistics

from src.rag import ask_question

questions = [
    "How many vacation days do employees receive?",
    "How many paid sick days do employees receive?",
    "Can unused vacation days be carried over?",
    "Do I need to use a VPN for remote work?",
    "Is MFA required when using the VPN?",
    "What holidays are paid?",
    "What expenses are eligible for reimbursement?",
    "When must expenses be submitted?",
    "How long must a password be?",
    "Can employees reuse passwords?",
    "What are the working hours?",
    "Can employees work remotely?",
    "Can I use a personal device for company work?",
    "How quickly must security incidents be reported?",
    "What class of flight is allowed for trips under six hours?",
]

times = []

for question in questions:
    start = time.perf_counter()
    ask_question(question)
    elapsed = time.perf_counter() - start
    times.append(elapsed)
    print(f"{elapsed:.3f}s - {question}")

times_sorted = sorted(times)

p50 = statistics.median(times)

index = max(0, int(0.95 * len(times_sorted)) - 1)
p95 = times_sorted[index]

print("\n" + "=" * 50)
print("LATENCY EVALUATION")
print("=" * 50)
print(f"Queries : {len(times)}")
print(f"Average : {statistics.mean(times):.3f}s")
print(f"P50     : {p50:.3f}s")
print(f"P95     : {p95:.3f}s")
print(f"Min     : {min(times):.3f}s")
print(f"Max     : {max(times):.3f}s")