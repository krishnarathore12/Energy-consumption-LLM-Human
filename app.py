import streamlit as st
import nltk
from nltk.tokenize import word_tokenize

# Ensure necessary NLTK data is available
nltk.download('punkt', quiet=True)

# Function for energy comparison
def calculate_energy_comparison(text):
    """
    Calculates and compares the energy needed to generate a text by LLM and human,
    and the time for human writing.

    Args:
        text: The input text string.

    Returns:
        A dictionary containing the calculated values.
    """

    # --- Human Estimates ---
    human_words_per_hour = 250
    human_energy_per_hour_physiological_kwh = 0.12
    human_energy_per_hour_per_capita_kwh = 6  # Using the US electricity per person estimate

    # --- LLM Estimates ---
    llm_joules_per_token = 4
    words_per_token = 0.75
    joules_to_kwh = 2.77778e-7  # 1 Joule = 2.77778e-7 kWh

    # --- Calculations ---
    num_words = len(word_tokenize(text))
    num_tokens = num_words / words_per_token

    # Human Time
    human_writing_time_hours = num_words / human_words_per_hour

    # Human Energy
    human_energy_physiological_kwh = human_writing_time_hours * human_energy_per_hour_physiological_kwh
    human_energy_per_capita_kwh = human_writing_time_hours * human_energy_per_hour_per_capita_kwh

    # LLM Energy
    llm_energy_joules = num_tokens * llm_joules_per_token
    llm_energy_kwh = llm_energy_joules * joules_to_kwh

    return {
        "num_words": num_words,
        "human_writing_time_hours": human_writing_time_hours,
        "human_energy_physiological_kwh": human_energy_physiological_kwh,
        "human_energy_per_capita_kwh": human_energy_per_capita_kwh,
        "llm_energy_kwh": llm_energy_kwh
    }

# Streamlit app
st.title("Energy Comparison: Human vs. LLM Text Generation")
st.write("This app calculates and compares the energy required for text generation by humans and large language models (LLMs). Enter a text below to analyze.")

# Input text
input_text = st.text_area("Enter your text:", height=200)

if st.button("Analyze"):
    if input_text.strip():
        results = calculate_energy_comparison(input_text)

        st.subheader("Analysis Results")
        st.write(f"Number of words: {results['num_words']}")

        st.subheader("Human Effort")
        st.write(f"Estimated writing time: {results['human_writing_time_hours']:.2f} hours")
        st.write(f"Estimated energy consumption (physiological): {results['human_energy_physiological_kwh']:.4f} kWh")
        st.write(f"Estimated energy consumption (per capita US): {results['human_energy_per_capita_kwh']:.2f} kWh")

        st.subheader("LLM Effort")
        st.write(f"Estimated energy consumption: {results['llm_energy_kwh']:.6f} kWh")

        st.subheader("Comparison")
        if results['llm_energy_kwh'] < results['human_energy_physiological_kwh']:
            st.write("The LLM is estimated to use less energy than the human (physiological estimate) to generate this text.")
        else:
            st.write("The LLM is estimated to use more energy than the human (physiological estimate) to generate this text.")

        if results['llm_energy_kwh'] < results['human_energy_per_capita_kwh']:
            st.write("The LLM is estimated to use significantly less energy than the human (per capita US estimate) for this work.")
        else:
            st.write("The LLM is estimated to use more energy than the human (per capita US estimate) for this work.")

        st.write("\nNote: These are back-of-the-envelope calculations based on the provided estimates.")
    else:
        st.error("Please enter some text to analyze.")
