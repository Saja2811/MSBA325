import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Electricity-Lebanon-2023')

# Load the CSV directly from the file path
csv_file_path = 'C:/Users/User/Desktop/Data Vis/Plotly Hw-Saja/Electricity.csv'  
df = pd.read_csv(csv_file_path)

# Display the DataFrame
st.subheader('Raw data')
st.dataframe(df)


st.subheader('Exploratory Visualizations:')
# Chart 1: Bar Chart
st.subheader('Interactive Chart 1')

# Sidebar filters for user input
st.sidebar.header("Filter Options")

# Filter by existence of alternative energy
alternative_energy_filter = st.sidebar.selectbox(
    "Does alternative energy exist?",
    options=df['Existence of alternative energy - exists'].unique(),
    format_func=lambda x: "Yes" if x == 1 else "No"
)

# Filter data based on selection
filtered_df = df[df['Existence of alternative energy - exists'] == alternative_energy_filter]

# Plot selection
plot_option = st.sidebar.selectbox(
    "Choose data to visualize",
    ["State of the Power Grid", "State of the Lighting Network"]
)
# Plot the selected option
if plot_option == "State of the Power Grid":
    state_grid = filtered_df.groupby('State of the power grid - good')['Town'].count().reset_index()
    state_grid.columns = ['Power Grid Good', 'Number of Towns']
    fig = px.bar(state_grid, 
                 x='Power Grid Good', 
                 y='Number of Towns', 
                 title='Power Grid Status of Towns',
                 text_auto=True)
elif plot_option == "State of the Lighting Network":
    state_lighting = filtered_df.groupby('State of the lighting network - good')['Town'].count().reset_index()
    state_lighting.columns = ['Lighting Network Good', 'Number of Towns']
    fig = px.bar(state_lighting, 
                 x='Lighting Network Good', 
                 y='Number of Towns',
                 title='Lighting Network Status of Towns',
                 text_auto=True)

# Display the plot
st.plotly_chart(fig)



# Chart 2: Donut Chart
st.subheader('Interactive Chart 2')
st.subheader("Town-wise Alternative Energy Existence and Type")
# User selects a town from the dropdown
selected_town = st.selectbox("Select a Town", df['Town'].unique())

# Filter the data for the selected town
town_data = df[df['Town'] == selected_town]

# Check if alternative energy exists in the selected town
if town_data['Existence of alternative energy - exists'].values[0] == 1:
    st.write(f"In {selected_town}, alternative energy **exists**.")
    
    # Plot types of alternative energy used
    energy_types = {
        "Hydropower (Water Use)": town_data['Type of alternative energy used - hydropower (water use)'].values[0],
        "Solar Energy": town_data['Type of alternative energy used - solar energy'].values[0],
        "Wind Energy": town_data['Type of alternative energy used - wind energy'].values[0],
        "Other Energy": town_data['Type of alternative energy used - other'].values[0]
    }

 # Convert the dictionary to a DataFrame for plotting
    energy_df = pd.DataFrame(list(energy_types.items()), columns=["Energy Type", "Used"])
    
    # Filter to include only energy types that are used (value == 1)
    energy_df = energy_df[energy_df['Used'] == 1]

    # Create a donut chart to show which types of alternative energy are used
    if not energy_df.empty:
        fig = px.pie(energy_df, 
                     names='Energy Type',
                     values='Used',
                     hole=0.3, 
                     title=f"Types of Alternative Energy Used in {selected_town}",
                     color_discrete_sequence=['red'] )
        fig.update_layout(
    legend=dict(
        font=dict(size=20),   # Increase the font size of the legend
        orientation="h",      # Set legend horizontally if needed
        x=0.5,                # Position the legend in the middle
        xanchor='center',
        y=-0.2,               # Adjust position to move it below the chart
    )
)
        st.plotly_chart(fig)
    else:
        st.write(f"No specific types of alternative energy are used in {selected_town}.")
else:
    st.write(f"In {selected_town}, alternative energy **does not exist**.")




# Chart 3: Horizontal bar chart
st.subheader("Interactive Chart 3:")
st.subheader("Alternative Energy Distribution by Reference Area")

# User selects a reference area
selected_ref_area = st.selectbox("Select a Reference Area", df['refArea'].unique())

# Filter the data for the selected reference area
ref_area_data = df[df['refArea'] == selected_ref_area]

# Create a bar chart of alternative energy types
energy_type_counts = ref_area_data[['Type of alternative energy used - hydropower (water use)', 
                                    'Type of alternative energy used - solar energy', 
                                    'Type of alternative energy used - wind energy', 
                                    'Type of alternative energy used - other']].sum()

# Convert the counts into a DataFrame
energy_type_df = pd.DataFrame({'Energy Type': energy_type_counts.index, 'Count': energy_type_counts.values})

# Plot the bar chart
fig = px.bar(energy_type_df, x='Count', y='Energy Type',orientation='h', title=f"Energy Types in {selected_ref_area}", text_auto=True)
fig.update_traces(marker_color='green')
st.plotly_chart(fig)




#Chart 4 : Treemap
st.subheader("Interactive Chart 4 ")
st.subheader("Interactive Treemap: Alternative Energy by Towns and Reference Areas")

# Let the user select up to 3 refAreas
selected_ref_areas = st.multiselect("Select up to 3 Reference Areas", df['refArea'].unique(), max_selections=3)

# Check if the user selected any reference areas
if selected_ref_areas:
    # Filter the dataframe based on the selected refAreas
    filtered_df = df[df['refArea'].isin(selected_ref_areas)]
    
    # Add a 'Count' column to use for the Treemap size (since we need a numerical value)
    filtered_df['Count'] = 1

    # Create Treemap using Plotly
    fig = px.treemap(filtered_df, 
                     path=['refArea', 'Town'],  # Hierarchy levels: Reference Area -> Town
                     values='Count',  # Using the 'Count' column to represent the size of each rectangle
                     color='Existence of alternative energy - exists',  # Color by energy existence
                     color_discrete_map={'Exists': 'red', 'Does Not Exist': 'pink'},  # Custom color map (purple for exists, pink for does not exist)
                     title='Alternative Energy Usage by Towns and Reference Areas')

    # Customize the layout to make the chart larger
    fig.update_layout(
        width=1100,  # Width of the plot
        height=600  # Height of the plot
    )

    # Display the Treemap in Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Please select at least one Reference Area to visualize the Treemap.")








