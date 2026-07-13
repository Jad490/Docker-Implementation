import requests
import json
import time
from typing import List, Dict

class SentimentAnalysisClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    def health_check(self) -> Dict:
        """Check if the API is healthy and model is loaded"""
        try:
            response = requests.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Health check failed: {e}")
            return None
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Send text for sentiment analysis"""
        try:
            payload = {"text": text}
            response = requests.post(
                f"{self.base_url}/analyze",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Sentiment analysis failed: {e}")
            return None
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Analyze multiple texts"""
        results = []
        for text in texts:
            result = self.analyze_sentiment(text)
            if result:
                results.append(result)
            time.sleep(0.1)  # Small delay between requests
        return results

def test_api():
    """Main test function"""
    print("🚀 Starting FastAPI Sentiment Analysis Client Test")
    print("=" * 60)
    
    # Initialize client
    client = SentimentAnalysisClient()
    
    # Test 1: Health check
    print("1. Testing health check...")
    health = client.health_check()
    if health:
        print(f"✅ API is healthy! Device: {health.get('device', 'unknown')}")
    else:
        print("❌ API health check failed! Make sure the server is running.")
        return
    
    print("\n" + "=" * 60)
    
    # Test 2: Single sentiment analysis (your example)
    print("2. Testing single sentiment analysis...")
    test_text = "I love this movie! It's absolutely fantastic."
    result = client.analyze_sentiment(test_text)
    
    if result:
        print(f"✅ Success!")
        print(f"   Text: {result['text']}")
        print(f"   Sentiment: {result['sentiment']}")
        print(f"   Confidence: {result['confidence']}")
    else:
        print("❌ Single sentiment analysis failed!")
    
    print("\n" + "=" * 60)
    
    # Test 3: Multiple test cases
    print("3. Testing multiple examples...")
    test_cases = [
        "I hate this movie. It's terrible!",
        "This product is amazing! I highly recommend it.",
        "The weather is okay today.",
        "I'm feeling sad and disappointed.",
        "What a wonderful day to be alive!",
        "The service was slow but the food was decent.",
        "This is the worst experience ever!",
        "I'm neutral about this topic."
    ]
    
    results = client.batch_analyze(test_cases)
    
    print(f"✅ Analyzed {len(results)} texts:")
    print(f"{'Text':<50} {'Sentiment':<10} {'Confidence':<10}")
    print("-" * 70)
    
    for result in results:
        text_preview = (result['text'][:47] + "...") if len(result['text']) > 50 else result['text']
        print(f"{text_preview:<50} {result['sentiment']:<10} {result['confidence']:<10.3f}")
    
    print("\n" + "=" * 60)
    
    # Test 4: Edge cases
    print("4. Testing edge cases...")
    edge_cases = [
        "",  # Empty string
        "   ",  # Only whitespace
        "A" * 600,  # Very long text
        "😊😊😊",  # Only emojis
        "12345",  # Only numbers
    ]
    
    for i, text in enumerate(edge_cases):
        print(f"   Test {i+1}: ", end="")
        if text == "":
            print("Empty string - ", end="")
        elif text.strip() == "":
            print("Whitespace only - ", end="")
        elif len(text) > 100:
            print("Very long text - ", end="")
        elif text == "😊😊😊":
            print("Only emojis - ", end="")
        elif text == "12345":
            print("Only numbers - ", end="")
        
        result = client.analyze_sentiment(text)
        if result:
            print(f"✅ {result['sentiment']} ({result['confidence']:.3f})")
        else:
            print("❌ Failed (expected for some edge cases)")
    
    print("\n" + "=" * 60)
    
    # Test 5: Performance test
    print("5. Performance test...")
    start_time = time.time()
    
    performance_texts = [
        "This is great!",
        "This is terrible!",
        "I'm not sure about this.",
    ] * 10  # 30 requests total
    
    performance_results = client.batch_analyze(performance_texts)
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = total_time / len(performance_results) if performance_results else 0
    
    print(f"✅ Processed {len(performance_results)} requests in {total_time:.2f} seconds")
    print(f"   Average time per request: {avg_time:.3f} seconds")
    
    print("\n" + "🎉 Test completed!")

def interactive_mode():
    """Interactive mode for manual testing"""
    print("\n" + "=" * 60)
    print("🔧 Interactive Mode - Type your own text to analyze!")
    print("(Type 'quit' to exit)")
    print("=" * 60)
    
    client = SentimentAnalysisClient()
    
    # Check if API is available
    if not client.health_check():
        print("❌ API is not available. Please start the server first.")
        return
    
    while True:
        user_input = input("\nEnter text to analyze: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not user_input:
            print("⚠️  Please enter some text.")
            continue
        
        result = client.analyze_sentiment(user_input)
        if result:
            print(f"📊 Sentiment: {result['sentiment']} (Confidence: {result['confidence']:.3f})")
        else:
            print("❌ Analysis failed. Please try again.")

if __name__ == "__main__":
    print("FastAPI Sentiment Analysis - Client Test Script")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print()
    
    try:
        # Run automatic tests
        test_api()
        
        # Ask if user wants interactive mode
        response = input("\nWould you like to try interactive mode? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_mode()
            
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")