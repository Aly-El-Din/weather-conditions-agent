from graphBuilder import WeatherGraphBuilder

def test_app():
    app = WeatherGraphBuilder().compile_app()

    test_inputs = [
        {"messages": "What’s the weather like in Cairo today?"},
        {"messages": "Tell me a joke about cats."},
        {"messages": "How's the weather in Washington?"},
    ]

    for i, state in enumerate(test_inputs, 1):
        print(f"\nTest Case {i}")
        result = app.invoke(state)
        print(result["messages"])

if __name__ == "__main__":
    test_app()