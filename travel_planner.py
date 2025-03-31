import requests
import streamlit as st
from serpapi import GoogleSearch
import json

st.title("AI Travel Planner 🗺️")

# Store API keys in session state
if "api_keys_entered" not in st.session_state:
    st.session_state.api_keys_entered = False

# If API keys aren't entered, show the input fields
if not st.session_state.api_keys_entered:
    with st.sidebar:
        st.subheader("Enter your API keys to continue:")
        MISTRAL_API_KEY = st.text_input("Mistral API Key:", type="password")
        SERPAPI_KEY = st.text_input("SerpAPI Key:", type="password")

        if MISTRAL_API_KEY and SERPAPI_KEY:
            st.session_state.MISTRAL_API_KEY = MISTRAL_API_KEY
            st.session_state.SERPAPI_KEY = SERPAPI_KEY
            st.session_state.api_keys_entered = True
            st.success("API keys saved 🔥! Redirecting to the chatbot...")

            # Force rerun to refresh UI and show chatbot
            st.rerun()
        else:
            st.warning("🗝️ Please enter your own API keys to proceed.")
            st.stop()  # Stop execution until user enters API keys

# Function to call Mistral AI
def get_mistral_response(messages):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {st.session_state.MISTRAL_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "mistral-tiny", "messages": messages}

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# Function to extract travel details from user input
def extract_travel_details(chat_history):
    extraction_prompt = """
    Extract key travel details from the conversation. Return JSON with:
    - "destination": City or country name
    - "duration": Example: '5 days' or '2 weeks'
    - "interests": ["food", "adventure", "history"]
    - "budget": "budget", "mid-range", or "luxury"
    - "dietary": ["vegetarian", "vegan", "no preference"]
    - "mobility": "low", "moderate", or "high"
    - "accommodation": ["budget", "mid-range", "luxury", "central"]
    - "purpose": "relaxation", "adventure", "cultural immersion", etc.

    If details are unspecified, return: { "that field name": "unspecified" }
    """

    # Extract only user messages for better accuracy
    user_messages = [{"role": "system", "content": extraction_prompt}]
    user_messages += [msg for msg in chat_history if msg["role"] == "user"]

    response = get_mistral_response(user_messages)

    try:
        extracted_data = json.loads(response)
        if "error" in extracted_data:
            return None  # AI couldn't extract enough info
        return extracted_data
    except json.JSONDecodeError:
        return None

# Function to fetch top attractions using Google search
def web_search(destination, interests):
    query = f"Best places in {destination} for {', '.join(interests)} in 2025"
    
    params = {"engine": "google", "q": query, "api_key": st.session_state.SERPAPI_KEY}
    search = GoogleSearch(params)
    results = search.get_dict().get("organic_results", [])[:5]

    return [f"{res['title']} - {res['link']}" for res in results] if results else ["No results found."]

# Function to generate a structured travel itinerary
def generate_itinerary(user_data, attractions):
    duration = user_data["duration"]
    attraction_text = "\n".join(attractions) if attractions else "various local attractions"

    itinerary_prompt = f"""
    You are a friendly and knowledgeable AI travel planner. The user is planning a {duration} trip to {user_data['destination']}.
    Their interests include {", ".join(user_data['interests'])}. Budget is {user_data['budget']}.

    Suggested places to visit:
    {attraction_text}

    Generate a relaxed, fun day-by-day itinerary for the **entire** {duration}:
    - If the trip is shorter than 10 days, create a detailed daily itinerary.
    - If the trip is longer than 10 days, summarize every few days (e.g., "Days 11-13: Explore XYZ area").
    - **Morning:** Easy start, café suggestions, light sightseeing.
    - **Afternoon:** Key attractions, adventure or cultural activities.
    - **Evening:** Dining, local nightlife, or relaxation.

    Rules:
    - **Ensure the itinerary covers the full {duration}.**
    - **Make it flexible** – Don't make it feel like a strict schedule.
    - **Personalized tone** – Speak like a friend giving travel advice.
    - **Add breaks** – Recommend cozy cafés or relaxing spots.
    - **Offer options** – Suggest alternatives in case a place is too crowded.

    Format the response in a fun, engaging manner!
    """

    return get_mistral_response([{"role": "system", "content": itinerary_prompt}])

# Streamlit UI
def main():
    # st.title("AI Travel Planner 🗺️")

    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Hey there! 🌟 I'm your AI travel buddy. Ready to plan an amazing trip? Where are you dreaming of going?"
        }]
        st.session_state.travel_details = {}
        st.session_state.detail_progress = {
            "destination": False, "duration": False, "interests": False, "budget": False,
            "dietary": False, "mobility": False, "accommodation": False, "purpose": False
        }
        st.session_state.awaiting_detail = None
        st.session_state.itinerary_generated = False  # Ensures itinerary is generated only once

    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type your response...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        if st.session_state.awaiting_detail:
            # Save user response for the missing detail
            st.session_state.travel_details[st.session_state.awaiting_detail] = user_input
            st.session_state.detail_progress[st.session_state.awaiting_detail] = True
            st.session_state.awaiting_detail = None  # Reset

        else:
            # Extract details only if user input is long (initial input)
            if len(user_input) > 10:
                extracted_details = extract_travel_details(st.session_state.messages)

                if extracted_details:
                    # print("Extracted Details: ", extracted_details)
                    for key, value in extracted_details.items():
                        if value != "unspecified" and not st.session_state.detail_progress[key]:
                            st.session_state.travel_details[key] = value
                            st.session_state.detail_progress[key] = True

        # Find the first missing detail AFTER updating extracted details
        missing_detail = next((key for key, filled in st.session_state.detail_progress.items() if not filled), None)

        if missing_detail:
            questions = {
                "destination": "Hello buddy! Could you tell me the city or country you're thinking of? 🌍",
                "duration": "How long are you planning to stay? A weekend getaway or a longer adventure? 🏖️",
                "interests": "What kind of experiences are you looking for? Foodie adventures, historical tours, or something else? 🍽️🏛️",
                "budget": "What's your budget like? Are we going all out or keeping it chill? 💸",
                "dietary": "Do you have any dietary preferences? Vegetarian, Non-vegetarian, or no restrictions? 🍽️",
                "mobility": "How comfortable are you with walking? Low, moderate, or high? 🚶‍♂️",
                "accommodation": "What kind of accommodation do you prefer? Budget, mid-range, luxury, or central? 🏨",
                "purpose": "What's the purpose of your trip? Relaxation, adventure, cultural immersion, or something else? 🎯",
            }

            st.session_state.messages.append({"role": "assistant", "content": questions[missing_detail]})
            st.session_state.awaiting_detail = missing_detail  # Track which detail we're waiting for
            st.rerun()

    # Generate itinerary only when ALL details are collected
    if all(st.session_state.detail_progress.values()) and not st.session_state.itinerary_generated:
        destination = st.session_state.travel_details["destination"]
        interests = ', '.join(st.session_state.travel_details.get('interests', ['varied experiences']))

        # Fetch attractions
        attractions = web_search(destination, interests)

        # Generate itinerary
        itinerary = generate_itinerary(st.session_state.travel_details, attractions)

        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Here's your travel plan for {destination}:\n\n{itinerary}"
        })

        st.session_state.itinerary_generated = True  # Ensure itinerary is not generated again
        st.rerun()

if __name__ == "__main__":
    main()
