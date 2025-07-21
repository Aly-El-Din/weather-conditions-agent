
# import requests
# from typing import TypedDict

# class WeatherAgentState(TypedDict):
#     messages: str
#     location: str

# def weather_api(location: str) -> str:
#     url = f"https://wttr.in/{location}?format=j1"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return f"Failed to fetch weather data for {location}."

#     data = response.json()
#     forecast = data.get("weather", [])
#     result = f"Weather forecast for {location}:\n"
#     for day in forecast:
#         date = day["date"]
#         avg_temp = day["avgtempC"]
#         desc = day["hourly"][4]["weatherDesc"][0]["value"]
#         result += f"- {date}: {desc}, Avg Temp: {avg_temp}°C\n"
#     return result.strip()

from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

# %%
GOOGLE_API_KEY = "AIzaSyA9fKC9uXhHOrgg2-Sk2557XzxYQM-Bayg"

# %%
class WeatherAgentState(TypedDict):
    messages: str
    location: str

# %%
llm = ChatGoogleGenerativeAI(
    model = "models/gemini-2.5-pro",
    temperature = 0.0,
    google_api_key = GOOGLE_API_KEY
)

# %%
def setup_node(state:WeatherAgentState) -> WeatherAgentState:
    print("Calling setup node...")
    return state

# %%
def is_weather_query(message: str) -> bool:
    determine_weather_prompt_message = f"Determine if this message:{message} is a prompt asking for weather conditions in a specific location or not, if yes return the word yes else return the word no"
    is_weather = llm.invoke(determine_weather_prompt_message).content.strip().lower()
    print("Calling is weather query...")
    print(f"llm response to is weather query:{is_weather}")
    return is_weather == "yes"

# %%
def router(state):
    print("calling router...")
    return "weather" if is_weather_query(state["messages"]) else "llm"

# %%
def call_weather_api_node(state:WeatherAgentState) -> WeatherAgentState:
    result = weather_api.invoke(state["location"])
    print("calling weather api node...")
    print(f"result of the api: {result}")
    return {
        "messages": result,
        "location": state["location"]
    }

# %%
def get_weather_location_node(state:WeatherAgentState) -> WeatherAgentState:
    get_location_message = f"get location from this message: {state['messages']}, make the response contains the location only not anything more than the location, if there is no location return the word None."
    response = llm.invoke(get_location_message)
    state["location"] = response.content.strip()
    print("calling get weather location node...")
    print(f"Location extracted: {response.content}")
    return state

# %%
@tool
def weather_api(location: str) -> str:
    """
    Get the weather forecast for the current week using wttr.in.
    """
    print(f"in weather api, the location received is: {location}")
    import requests
    # wttr.in automatically shows a 3-day forecast by default; adding &format=j1 gives JSON
    url = f"https://wttr.in/{location}?format=j1"  # JSON format
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to fetch weather data for {location}."
    
    data = response.json()
    forecast = data.get("weather", [])  # list of daily forecasts
    result = f"Weather forecast for {location}:\n"
    
    for day in forecast:
        date = day["date"]
        avg_temp = day["avgtempC"]
        description = day["hourly"][4]["weatherDesc"][0]["value"]  # Approx midday
        result += f"- {date}: {description}, Avg Temp: {avg_temp}°C\n"

    return result.strip()

# %%
def run_llm_node(state: WeatherAgentState) -> WeatherAgentState:
    response = llm.invoke(state["messages"])
    print("running llm node...")
    print(f"response of the llm {response.content}")
    return {"messages":response.content}

# %%
def format_csv_node(state: WeatherAgentState) -> WeatherAgentState:
    location = state.get("location", "Unknown")
    response = state["messages"]
    formatted = f'"{location}","{response}"'
    print("formating csv node")
    return {"messages": formatted}


# %%
def location_decider(state: WeatherAgentState):
    loc = state["location"].strip().lower()
    print(f"location decider response:{loc}")
    return "has_location" if loc and loc != "none" else "no_location"