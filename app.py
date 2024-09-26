import streamlit as st
st.title("Hello World")

Chart 4
st.subheader("Interactive Chart 4")
st.subheader("Filter Towns by Criteria")

# User selects criteria for filtering
alternative_energy = st.selectbox("Does the town have alternative energy?", ['Both', 'Exists', 'Does Not Exist'])
power_grid = st.selectbox("State of the Power Grid - good", ['Both', 'Good', 'Bad'])
lighting_network = st.selectbox("State of the Lighting Network - good", ['Both', 'Good', 'Bad'])

# Apply filters to the dataframe
if alternative_energy != 'Both':
    df = df[df['Existence of alternative energy - exists'] == alternative_energy]
if power_grid != 'Both':
    df = df[df['State of the Power Grid - good'] == power_grid]
if lighting_network != 'Both':
    df = df[df['State of the Lighting Network - good'] == lighting_network]

# Show the filtered data
st.write(f"Showing {len(df)} towns that match the selected criteria:")
st.dataframe(df[['Town', 'Existence of alternative energy - exists', 'State of the Power Grid', 'State of the Lighting Network']])

