import streamlit as st

def convertor(value, from_unit, to_unit):
    elements = {
        "meter": {
            "kilometer": 0.001,
            "centimeter": 100,
            "millimeter": 1000,
            "meter": 1
        },
        "Gram": {
            "kilogram": 0.001,
            "milligram": 1000,
            "pound": 0.00220462,
            "Gram": 1
        },
        "Area": {
            "hectare": 0.0001,
            "acre": 0.000247105,
            "square_meter": 1,
            "Area": 1
        }
    }

    # First convert to base unit (meter, Gram, or square_meter)
    if from_unit in elements["meter"]:
        base_value = value / elements["meter"][from_unit]
        return base_value * elements["meter"][to_unit]
    elif from_unit in elements["Gram"]:
        base_value = value / elements["Gram"][from_unit]
        return base_value * elements["Gram"][to_unit]
    elif from_unit in elements["Area"]:
        base_value = value / elements["Area"][from_unit]
        return base_value * elements["Area"][to_unit]
    else:
        return "Invalid conversion"

st.sidebar.title("Unit Converter")

value = st.sidebar.number_input("Enter Value")

unit_type = st.sidebar.selectbox("Unit Type", ["meter", "Gram", "Area"])

# Get available conversion options based on selected unit type
conversion_options = {
    "meter": ["kilometer", "centimeter", "millimeter", "meter"],
    "Gram": ["kilogram", "milligram", "pound", "Gram"],
    "Area": ["hectare", "acre", "square_meter", "Area"]
}

from_unit = st.radio("From Unit", options=conversion_options[unit_type])
to_unit = st.radio("To Unit", options=conversion_options[unit_type])

if st.button("Convert"):
    result = convertor(value, from_unit, to_unit)
    st.write(f"Converted value is: `{result}`")