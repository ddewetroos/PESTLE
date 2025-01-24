import numpy as np
import sys
import importlib
import streamlit as st

# Implement the workaround for the 'imp' module
class DummyImp:
    @staticmethod
    def find_module(name, path=None):
        spec = importlib.util.find_spec(name, path)
        if spec is None:
            return None, None, None
        return spec.loader, spec.origin, ('', '', importlib.machinery.BYTECODE_SUFFIXES)

    @staticmethod
    def load_module(name, file=None, pathname=None, description=None):
        if name in sys.modules:
            return sys.modules[name]
        spec = importlib.util.find_spec(name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[name] = module
        return module

sys.modules['imp'] = DummyImp

import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define the range for all subcriteria
universe = np.arange(1, 101, 1)

# Initialize the subcriteria for each PESTEL factor
subcriteria = {
    'POLITICAL': ['European Union Relations', 'Regional Relations', 'Democratization Process', 'North Africa and Middle East', 'Political Stability'],
    'ECONOMIC': ['National Income', 'Investment Incentives', 'Monetary Policy', 'Fiscal Policy', 'Foreign Investment', 'Current Deficit', 'Energy Cost', 'Foreign Debt', 'Unemployment'],
    'SOCIAL': ['Life Style', 'Education Level', 'Awareness of Citizenship', 'Rule of Law', 'Willingness of Population to Work', 'Democratic Culture'],
    'TECHNOLOGICAL': ['Government Attitude', 'New Patents', 'r&D Activities Supported by Government', 'Adoption of new Technology', 'Rate of Change in Technology'],
    'ENVIRONMENTAL': ['Transportation Infrastructure', 'Traffic Safety', 'Public Health', 'Level of Urbanization', 'Disaster Management Infrastructure', 'Green Issues'],
    'LEGISLATIVE FRAMEWORK': ['Competition Laws', 'Judicial System', 'Consumer Rights', 'Implementation of Legislation', 'International Treaties']
}

# Define the fuzzy membership functions for each subcriterion
subcriterion_values = {}
risk_scores = {}

for factor, subcriterion_list in subcriteria.items():
    for subcriterion in subcriterion_list:
        subcriterion_values[subcriterion] = ctrl.Antecedent(universe, subcriterion)
        subcriterion_values[subcriterion]['low'] = fuzz.trimf(subcriterion_values[subcriterion].universe, [1, 1, 50])
        subcriterion_values[subcriterion]['medium'] = fuzz.trimf(subcriterion_values[subcriterion].universe, [25, 50, 75])
        subcriterion_values[subcriterion]['high'] = fuzz.trimf(subcriterion_values[subcriterion].universe, [50, 100, 100])

# Define the risk fuzzy variable
risk = ctrl.Consequent(universe, 'risk')
risk['low'] = fuzz.trimf(risk.universe, [1, 1, 50])
risk['medium'] = fuzz.trimf(risk.universe, [25, 50, 75])
risk['high'] = fuzz.trimf(risk.universe, [50, 100, 100])

# Function to create control system and evaluate risk based on PESTEL sub-criterion value
def evaluate_risk(value, subcriterion):
    # Create fuzzy rules for this specific subcriterion
    rule1 = ctrl.Rule(subcriterion_values[subcriterion]['low'], risk['low'])
    rule2 = ctrl.Rule(subcriterion_values[subcriterion]['medium'], risk['medium'])
    rule3 = ctrl.Rule(subcriterion_values[subcriterion]['high'], risk['high'])

    # Create the control system for this specific subcriterion
    risk_control_system = ctrl.ControlSystem([rule1, rule2, rule3])
    risk_simulation = ctrl.ControlSystemSimulation(risk_control_system)

    # Input the value and compute the risk
    risk_simulation.input[subcriterion] = value
    risk_simulation.compute()

    return risk_simulation.output['risk']

# Streamlit interface
st.title("PESTEL Analysis Risk Evaluation")
st.write("Use the sliders below to input values for the sub-criteria:")

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
for subcriterion, value in pestel_values.items():
    risk_scores[subcriterion] = evaluate_risk(value, subcriterion)
    st.write(f"Risk score for {subcriterion} (Value: {value}): {risk_scores[subcriterion]:.2f}")

# Calculate the overall risk by averaging the risk scores of all sub-criteria
overall_risk = np.mean(list(risk_scores.values()))
st.subheader(f"Overall risk based on PESTEL analysis: {overall_risk:.2f}")
