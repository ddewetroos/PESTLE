import numpy as np
import streamlit as st

# Define the range for all subcriteria
universe = np.arange(1, 101, 1)


# Membership function definitions
def trimf(x, a, b, c):
    """Triangular membership function with safeguards against zero division."""
    if a >= b or b >= c:
        raise ValueError(f"Invalid parameters for trimf: a={a}, b={b}, c={c}. Ensure a < b < c.")
    return np.maximum(
        np.minimum((x - a) / max(b - a, 1e-6), (c - x) / max(c - b, 1e-6)), 0
    )


# Define fuzzy membership functions
def membership_low(x):
    return trimf(x, 1, 25, 50)  # Adjusted a=1, b=25, c=50 to satisfy a < b < c


def membership_medium(x):
    return trimf(x, 25, 50, 75)  # a=25, b=50, c=75 (no changes needed)


def membership_high(x):
    return trimf(x, 50, 75, 100)  # Adjusted a=50, b=75, c=100 to satisfy a < b < c


# Define a simple rule evaluation
def evaluate_risk(value):
    """Evaluate risk based on fuzzy rules."""
    low = membership_low(value)
    medium = membership_medium(value)
    high = membership_high(value)

    # Debugging output for membership values
    st.write(f"Membership values for input {value}:")
    st.write(f"  Low: {low:.2f}, Medium: {medium:.2f}, High: {high:.2f}")

    # Weighted average defuzzification
    numerator = (low * 25) + (medium * 50) + (high * 75)
    denominator = low + medium + high

    # Safeguard for division by zero
    if denominator == 0:
        return 0  # Default risk value when no membership is triggered
    return numerator / denominator


# Streamlit interface
st.title("PESTEL Analysis Risk Evaluation")
st.write("Use the sliders below to input values for the sub-criteria:")

# PESTEL Subcriteria
subcriteria = {
    'POLITICAL': ['European Union Relations', 'Regional Relations', 'Democratization Process',
                  'North Africa and Middle East', 'Political Stability'],
    'ECONOMIC': ['National Income', 'Investment Incentives', 'Monetary Policy', 'Fiscal Policy', 'Foreign Investment',
                 'Current Deficit', 'Energy Cost', 'Foreign Debt', 'Unemployment'],
    'SOCIAL': ['Life Style', 'Education Level', 'Awareness of Citizenship', 'Rule of Law',
               'Willingness of Population to Work', 'Democratic Culture'],
    'TECHNOLOGICAL': ['Government Attitude', 'New Patents', 'R&D Activities Supported by Government',
                      'Adoption of New Technology', 'Rate of Change in Technology'],
    'ENVIRONMENTAL': ['Transportation Infrastructure', 'Traffic Safety', 'Public Health', 'Level of Urbanization',
                      'Disaster Management Infrastructure', 'Green Issues'],
    'LEGISLATIVE FRAMEWORK': ['Competition Laws', 'Judicial System', 'Consumer Rights', 'Implementation of Legislation',
                              'International Treaties']
}

# User inputs via sliders for each subcriterion
pestel_values = {}
for factor, subcriterion_list in subcriteria.items():
    st.header(f"{factor} Factors")
    for subcriterion in subcriterion_list:
        pestel_values[subcriterion] = st.slider(
            f"{subcriterion}",
            min_value=1, max_value=100, value=50, step=1
        )

# Calculate the risk score for each subcriterion
risk_scores = {}
for subcriterion, value in pestel_values.items():
    risk_scores[subcriterion] = evaluate_risk(value)
    st.write(f"Risk score for {subcriterion} (Value: {value}): {risk_scores[subcriterion]:.2f}")

# Calculate the overall risk by averaging the risk scores of all sub-criteria
overall_risk = np.mean(list(risk_scores.values()))
st.subheader(f"Overall risk based on PESTEL analysis: {overall_risk:.2f}")

