
from langgraph.graph import StateGraph, END
from weatherAgent import WeatherAgentState, call_weather_api_node, weather_api, setup_node, router, get_weather_location_node, run_llm_node, format_csv_node, location_decider

class WeatherGraphBuilder:
    def __init__(self):
        self.graph = StateGraph(WeatherAgentState)
        self._build()

    def _build(self):
        self.graph.add_node("setup", setup_node)
        self.graph.add_node("determine_location", get_weather_location_node)
        self.graph.add_node("call_weather_api", call_weather_api_node)
        self.graph.add_node("run_llm", run_llm_node)
        self.graph.add_node("format_csv", format_csv_node)

        self.graph.set_entry_point("setup")

        self.graph.add_conditional_edges("setup", router, {
            "weather": "determine_location",
            "llm": "run_llm"
        })

        self.graph.add_conditional_edges("determine_location", location_decider, {
            "has_location": "call_weather_api",
            "no_location": "run_llm"
        })

        self.graph.add_edge("call_weather_api", "format_csv")
        self.graph.add_edge("run_llm", END)
        self.graph.add_edge("format_csv", END)

    def compile_app(self):
        return self.graph.compile()
