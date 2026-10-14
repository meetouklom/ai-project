import urllib.request
import json
import time

def ask_agent_benchmark(model_name, prompt):
    url = "http://localhost:11434/api/chat"
    data = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            end_time = time.time()
            
            elapsed_time = end_time - start_time
            content = result.get('message', {}).get('content', '')
            return content, elapsed_time
    except Exception as e:
        end_time = time.time()
        return f"Error: {e}", end_time - start_time

if __name__ == "__main__":
    # กำหนดคำถามที่ต้องการทดสอบเปรียบเทียบ
    test_prompt = "แนะนำตัวเป็นภาษาไทยสั้นๆ 1 ประโยค"
    
    print("=" * 60)
    print(f"🎯 BENCHMARK PROMPT:\n\"{test_prompt}\"")
    print("=" * 60 + "\n")
    
    # 1. ทดสอบ Hermes3
    print("⏳ Testing Hermes3...")
    hermes_reply, hermes_time = ask_agent_benchmark("hermes3", test_prompt)
    print(f"👉 Hermes3 Result (Time: {hermes_time:.2f} seconds):")
    print(hermes_reply)
    print("-" * 60 + "\n")
    
    # 2. ทดสอบ Qwen2.5:3b
    print("⏳ Testing Qwen2.5:3b...")
    qwen_reply, qwen_time = ask_agent_benchmark("qwen2.5:3b", test_prompt)
    print(f"👉 Qwen2.5:3b Result (Time: {qwen_time:.2f} seconds):")
    print(qwen_reply)
    print("-" * 60)
    
    # สรุปผลความเร็ว
    print("\n📊 Summary Benchmark:")
    if hermes_time < qwen_time:
        print(f"⚡ Speed Winner: Hermes3 is faster by {abs(hermes_time - qwen_time):.2f}s")
    else:
        print(f"⚡ Speed Winner: Qwen2.5:3b is faster by {abs(hermes_time - qwen_time):.2f}s")