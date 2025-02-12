import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils import (
    calculate_total_cost,
    estimate_property_values,
    calculate_roi_with_split,
    generate_monthly_projection,
    calculate_share_investment,
    calculate_dubai_fees
)

# Page configuration
st.set_page_config(
    page_title="Real Estate Investment Simulator - UAE",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .stProgress .st-bo {
        background-color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("Real Estate Investment Simulator - UAE")
st.markdown("---")

# Sidebar for input parameters
with st.sidebar:
    st.header("Investment Parameters")

    initial_investment = st.number_input(
        "Initial Property Value (AED)",
        min_value=200_000,
        max_value=50_000_000,
        value=1_000_000,
        step=100_000,
        help="Enter the current property value in AED"
    )

    square_feet = st.number_input(
        "Property Size (sq ft)",
        min_value=500,
        max_value=10000,
        value=1500,
        step=100
    )

    quality_level = st.selectbox(
        "Package Level",
        options=['basic', 'medium', 'luxury'],
        help="Choose the package level (Basic: 300 AED/sqft, Medium: 380 AED/sqft, Luxury: 780 AED/sqft)"
    )

    market_factor = st.slider(
        "Market Appreciation (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=5,
        help="Expected market value increase percentage"
    ) / 100  # Convert percentage to decimal

    holding_period = st.slider(
        "Holding Period (months)",
        min_value=1,
        max_value=60,
        value=12,
        step=1
    )

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Cost Breakdown")
    total_cost = calculate_total_cost(square_feet, quality_level)

    # Display costs
    st.metric(
        label="Total Package Cost",
        value=f"AED {total_cost:,.2f}"
    )

    # Cost per sqft
    st.info(f"Package rate: AED {total_cost/square_feet:.2f} per sq ft")

with col2:
    st.subheader("Estimated Sale Prices")
    property_values = estimate_property_values(
        initial_investment,
        total_cost,
        market_factor
    )

    # Add scenario selection
    selected_scenario = st.radio(
        "Select Price Scenario",
        options=['conservative', 'moderate', 'optimistic'],
        index=1,  # Default to moderate
        horizontal=True
    )

    # Display different price estimates
    for scenario, value in property_values.items():
        base_markup = 15 if scenario == 'conservative' else 25 if scenario == 'moderate' else 35
        total_markup = base_markup + (market_factor * 100)

        if scenario == selected_scenario:
            st.markdown(f'### **{scenario.title()} Estimate (+{total_markup:.1f}%)**')
            st.metric(
                label="Final Value",
                value=f"AED {value:,.2f}",
                delta=f"AED {value - initial_investment:,.2f}"
            )
        else:
            st.markdown(f'### {scenario.title()} Estimate (+{total_markup:.1f}%)')
            st.metric(
                label="Final Value",
                value=f"AED {value:,.2f}",
                delta=f"AED {value - initial_investment:,.2f}"
            )

# Dubai Property Fees
st.markdown("---")
st.header("Dubai Property Fees")
dubai_fees = calculate_dubai_fees(property_values[selected_scenario])

col9, col10, col11, col12 = st.columns(4)

with col9:
    st.metric(
        label="DLD Fee (4%)",
        value=f"AED {dubai_fees['dld_fee']:,.2f}"
    )

with col10:
    st.metric(
        label="Broker Fee (2%)",
        value=f"AED {dubai_fees['broker_fee']:,.2f}"
    )

with col11:
    st.metric(
        label="Title Deed Fee",
        value=f"AED {dubai_fees['title_deed_fee']:,.2f}"
    )

with col12:
    st.metric(
        label="Conveyance Fee",
        value=f"AED {dubai_fees['conveyance_fee']:,.2f}"
    )

st.info(f"Total Fees: AED {dubai_fees['total_fees']:,.2f}")

# ROI Analysis
st.markdown("---")
st.header("Investment Analysis")

# Calculate ROI for selected scenario
roi_data = calculate_roi_with_split(
    initial_investment,
    property_values[selected_scenario],
    total_cost,
    holding_period
)

col3, col4, col5 = st.columns(3)

with col3:
    st.metric(
        label="Investor's Profit (88%)",
        value=f"AED {roi_data['investor_profit']:,.2f}"
    )

with col4:
    st.metric(
        label="Company's Profit (12%)",
        value=f"AED {roi_data['company_profit']:,.2f}"
    )

with col5:
    st.metric(
        label="Annual ROI",
        value=f"{roi_data['annual_roi']:.2f}%"
    )

# Share Investment Section
st.markdown("---")
st.header("Share Investment Calculator")
st.markdown("Invest in shares of the project and earn 0.5% monthly returns until property sale")

total_investment = initial_investment + total_cost
share_amount = st.number_input(
    "Investment Amount (AED)",
    min_value=100_000,
    max_value=int(total_investment),
    value=int(total_investment),  # Start at 100%
    step=50_000,
    help="Enter the amount you want to invest in this project"
)

share_data = calculate_share_investment(total_investment, share_amount, holding_period)

col6, col7, col8 = st.columns(3)

with col6:
    st.metric(
        label="Project Share",
        value=f"{share_data['share_percentage']:.2f}%"
    )

with col7:
    st.metric(
        label="Monthly Returns",
        value=f"AED {share_data['monthly_returns']:,.2f}"
    )

with col8:
    st.metric(
        label="Total Returns (During Holding Period)",
        value=f"AED {share_data['total_returns']:,.2f}"
    )

st.info(f"Effective Annual Return Rate: {share_data['effective_annual_return']:.2f}%")

# Visualizations
st.markdown("---")
st.header("Investment Projections")

# Generate monthly projections for selected scenario
monthly_values = generate_monthly_projection(
    initial_investment,
    property_values[selected_scenario],
    holding_period
)
months = list(range(1, holding_period + 1))

# Line chart for value progression
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=months,
    y=monthly_values,
    mode='lines+markers',
    name='Property Value',
    line=dict(color='#1f77b4', width=3)
))

fig1.update_layout(
    title="Projected Property Value Over Time",
    xaxis_title="Month",
    yaxis_title="Property Value (AED)",
    hovermode='x',
    height=500
)

st.plotly_chart(fig1, use_container_width=True)

# Pie chart for investment breakdown
costs_data = pd.DataFrame({
    'Category': ['Initial Investment', 'Total Package Cost'],
    'Amount': [initial_investment, total_cost]
})

fig2 = px.pie(
    costs_data,
    values='Amount',
    names='Category',
    title='Investment Breakdown'
)
fig2.update_traces(
    textposition='inside',
    textinfo='percent+label'
)

st.plotly_chart(fig2, use_container_width=True)

# Disclaimer
st.markdown("---")
st.caption(
    "Disclaimer: This is a simulation tool. Actual results may vary. "
    "Please consult with real estate professionals before making investment decisions."
)