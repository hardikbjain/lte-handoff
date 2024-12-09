import streamlit as st
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

st.title('LTE Handover Region Visualization')

# Create sidebar sliders with AP input values
st.sidebar.header('Threshold Parameters')

# Function to format the label with both values
def format_label(value):
    ap_value = value + 140
    return f"{value} dBm (AP input: {ap_value})"

# Create columns in sidebar for each threshold
st.sidebar.header('Threshold Parameters')
A1 = st.sidebar.slider('A1 Threshold', -110, -60, -70, 
                      format=format_label)
A2 = st.sidebar.slider('A2 Threshold', -110, -60, -75, 
                      format=format_label)
A5_1 = st.sidebar.slider('A5-1 Threshold', -110, -60, -90, 
                        format=format_label)
A5_2 = st.sidebar.slider('A5-2 Threshold', -110, -60, -95, 
                        format=format_label)
hysteresis = st.sidebar.slider('Hysteresis (dB)', 0, 10, 3)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 8))

# Create power ranges
power_range = np.arange(-110, -75, 0.5)

# Plot handover region
ax.fill_between(power_range, 
                power_range + hysteresis, 
                -75,
                where=(power_range < A5_1),
                color='green', alpha=0.3,
                label=f'Handover Region\n(Neighbor > Serving + {hysteresis}dB\n'
                      f'AND Serving < A5-1\n'
                      f'AND Neighbor > A5-2)')

# Mask for neighbor threshold
ax.axhspan(-110, A5_2, color='white', alpha=1.0)

# Plot lines
ax.plot(power_range, power_range + hysteresis, 'k--', 
         label=f'Neighbor = Serving + {hysteresis}dB')
ax.plot(power_range, power_range, 'k--', label='Neighbor = Serving')

# Plot thresholds
ax.axvline(x=A1, color='g', linestyle='--', label='A1 threshold')
ax.text(A1+0.5, -77, f'A1 threshold\n({A1} dBm)', horizontalalignment='left')

ax.axvline(x=A2, color='y', linestyle='--', label='A2 threshold')
ax.text(A2+0.5, -77, f'A2 threshold\n({A2} dBm)', horizontalalignment='left')

ax.axvline(x=A5_1, color='r', linestyle='--', label='A5-1 threshold')
ax.text(A5_1+0.5, -77, f'A5-1 threshold\n({A5_1} dBm)', horizontalalignment='left')

ax.axhline(y=A5_2, color='orange', linestyle='--', label='A5-2 threshold')
ax.text(-108, A5_2+0.5, f'A5-2 threshold ({A5_2} dBm)', verticalalignment='bottom')

# Set labels and title
ax.set_xlabel('Serving Cell Power (dBm)')
ax.set_ylabel('Neighbor Cell Power (dBm)')
ax.set_title('LTE Handover Regions')
ax.grid(True)
ax.legend(loc='lower right', bbox_to_anchor=(0.98, 0.02))

# Set axis limits
ax.set_xlim(-110, -75)
ax.set_ylim(-110, -75)

# Display the plot in Streamlit
st.pyplot(fig)

# Add explanation
st.markdown("""
### How to use this visualization:
1. Use the sliders in the sidebar to adjust threshold values
2. The green region shows where handover will occur
3. Conditions for handover:
   - Neighbor power > Serving power + Hysteresis
   - Serving power < A5-1 threshold
   - Neighbor power > A5-2 threshold
""")