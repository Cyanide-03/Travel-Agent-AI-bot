import streamlit as st

with st.sidebar:
    if not st.experimental_user.is_logged_in:
        st.button("Log in", on_click=st.login,args=("google",))
        st.stop()

    st.write("Log out",on_click=st.logout,args=("google",))


# Load Firebase credentials
# if not firebase_admin._apps:
#     cred = credentials.Certificate("firebase_credentials.json")
#     firebase_admin.initialize_app(cred)

# db = firestore.client()

# GOOGLE_CLIENT_ID = st.secrets["google_oauth"]["client_id"]
# GOOGLE_CLIENT_SECRET = st.secrets["google_oauth"]["client_secret"]
# REDIRECT_URI = st.secrets["google_oauth"]["redirect_uri"]

# def check_api_usage(user_email):
#     user_doc = db.collection("users").document(user_email).get()

#     if user_doc.exists:
#         user_data = user_doc.to_dict()
#         usage_count = user_data.get("usage_count", 0)
#         limit = user_data.get("limit", 100)
#         if usage_count >= limit:
#             return False  # User has exceeded their API limit
#         else:
#             # Increment usage count
#             db.collection("users").document(user_email).update({
#                 "usage_count": firestore.Increment(1)
#             })
#             return True
#     return False

# # Store user session
# if "user" not in st.session_state:
#     st.session_state.user = None

# def get_google_login_url():
#     params = {
#         "client_id": GOOGLE_CLIENT_ID,
#         "redirect_uri": REDIRECT_URI,
#         "response_type": "code",
#         "scope": "openid email profile",
#         "access_type": "offline",
#         "prompt": "consent",
#     }
#     return f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"

# def get_google_user_info(auth_code):
#     TOKEN_URL = "https://oauth2.googleapis.com/token"
#     USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
#     data = {
#         "client_id": GOOGLE_CLIENT_ID,
#         "client_secret": GOOGLE_CLIENT_SECRET,
#         "code": auth_code,
#         "redirect_uri": REDIRECT_URI,
#         "grant_type": "authorization_code",
#     }
#     response = requests.post(TOKEN_URL, data=data)
#     tokens = response.json()
    
#     if "access_token" in tokens:
#         headers = {"Authorization": f"Bearer {tokens['access_token']}"}
#         user_info = requests.get(USER_INFO_URL, headers=headers).json()

#         # Check if the user exists in Firestore
#         user_doc = db.collection("users").document(user_info["email"]).get()

#         if not user_doc.exists:
#             # Generate API keys for Mistral and SerpAPI
#             mistral_api_key = secrets.token_hex(16)
#             serp_api_key = secrets.token_hex(16)

#             # Store user info & API keys in Firestore
#             db.collection("users").document(user_info["email"]).set({
#                 "name": user_info["name"],
#                 "email": user_info["email"],
#                 "mistral_api_key": mistral_api_key,
#                 "serp_api_key": serp_api_key,
#                 "usage_count": 0,  # Track API usage
#                 "limit": 100  # Example: Limit to 100 queries
#             })

#             user_info["mistral_api_key"] = mistral_api_key
#             user_info["serp_api_key"] = serp_api_key
#         else:
#             user_info["mistral_api_key"] = user_doc.to_dict()["mistral_api_key"]
#             user_info["serp_api_key"] = user_doc.to_dict()["serp_api_key"]

#         return user_info

#     return None

# # Get query parameters from the URL (to check for auth code)
# query_params = st.query_params
# if "code" in query_params:
#     auth_code = query_params.get("code", [None])[0]
#     user_info = get_google_user_info(auth_code)
#     if user_info:
#         st.session_state.user = user_info  # Store user info in session
#         st.rerun()  # Refresh UI to show login status

# if st.session_state.user:
#     user_email = st.session_state.user["email"]
#     user_doc = db.collection("users").document(user_email).get()
#     if user_doc.exists:
#         user_data = user_doc.to_dict()
#         st.session_state.MISTRAL_API_KEY = user_data.get("mistral_api_key", "")
#         st.session_state.SERPAPI_KEY = user_data.get("serp_api_key", "")
# else:
#     st.markdown(f"[🔑 Sign in with Google]({get_google_login_url()})", unsafe_allow_html=True)