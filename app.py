"""Module Readiness Advisor, web demo.

Run locally:   py -m streamlit run app.py
Online:        deployed on Streamlit Community Cloud from this repository.
The Gemini key comes from Streamlit secrets or the GEMINI_API_KEY
environment variable, never from the code.
"""

import os

import streamlit as st
from google import genai
from google.genai import errors

from advisor import SPLIT_THRESHOLD, assess, load
from ask import match_request

st.set_page_config(page_title="Module Readiness Advisor", page_icon="🧩")

st.title("Module Readiness Advisor")
st.write(
    "Describe the infrastructure an application team needs, in plain English. "
    "AI matches it to a capability in the catalogue, then fixed rules work out "
    "what already exists, what must be built, what blocks it, and whether it is "
    "ready for the next sprint."
)
st.caption("Built on public cloud modules and synthetic data only.")

capabilities = load("catalog.yaml")["capabilities"]
existing = {item["id"] for item in load("inventory.yaml")["existing_resources"]}

examples = [
    "Our support team wants a chatbot that answers customer questions",
    "We need somewhere private and encrypted to keep our application logs",
    "Files land in a bucket every hour and need loading into our warehouse",
    "Something for our new application",
]
choice = st.selectbox("Try an example, or write your own below", [""] + examples)
request = st.text_area("Request", value=choice, height=80)

def get_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.environ.get("GEMINI_API_KEY")

if st.button("Assess readiness", type="primary") and request.strip():
    key = get_key()
    if not key:
        st.error("No Gemini API key is configured for this demo.")
        st.stop()

    with st.spinner("Matching the request to a capability..."):
        try:
            chosen, question = match_request(genai.Client(api_key=key), request, capabilities)
        except errors.APIError as error:
            st.warning(f"The AI service is busy right now (error {error.code}). Please try again in a minute.")
            st.stop()

    if chosen is None:
        st.info(f"**The request is not clear enough to assess.**\n\nQuestion back to the team: {question}")
        st.stop()

    capability = next(c for c in capabilities if c["id"] == chosen)
    reuse, build, dependencies, readiness = assess(capability, existing)

    st.subheader(capability["name"])
    colour = {"Ready": "green", "Blocked": "red", "Needs decision": "orange"}[readiness]
    st.markdown(f"**Readiness:** :{colour}[{readiness}]")

    stories = sorted({part["story"] for part in build})
    if len(build) > SPLIT_THRESHOLD:
        st.markdown(f"**Sprint fit:** Needs splitting. {len(build)} new pieces across {len(stories)} stories.")
    else:
        st.markdown(f"**Sprint fit:** OK, {len(build)} new pieces.")

    left, right = st.columns(2)
    with left:
        st.markdown("**Already exists, reuse**")
        for item in sorted(reuse) or ["nothing"]:
            st.markdown(f"- {item}")
        st.markdown("**To build, grouped by story**")
        for story in stories:
            parts = ", ".join(p["id"] for p in build if p["story"] == story)
            st.markdown(f"- **{story}**: {parts}")
    with right:
        st.markdown("**Dependencies**")
        for d in dependencies:
            st.markdown(f"- `{d['type']}` {d['need']}")
        if not dependencies:
            st.markdown("- none")

    if capability.get("note"):
        st.caption(capability["note"])

st.divider()
st.caption(
    "Readiness rules: approval or unconfirmed demand means Needs decision; "
    "a missing module, networking, IAM or existing repository dependency means Blocked; "
    "otherwise Ready. Platform APIs are reported but do not block."
)
