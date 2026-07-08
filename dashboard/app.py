"""
Data Weaver Dashboard - Streamlit App
Interactive dashboard showing weather vs food ordering patterns
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Data Weaver - Weather vs Food Orders",
    page_icon="🌦️🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """Load the merged dataset"""
    import os
    # Resolve path relative to this file's location, so it works regardless of cwd
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data', 'merged_data.csv')
    try:
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        st.error("Merged data file not found. Please run data_processor.py first!")
        return None

def create_kpi_cards(df):
    """Create KPI cards for key metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate KPIs
    rainy_orders = df[df['is_rainy']]['order_count'].mean()
    non_rainy_orders = df[~df['is_rainy']]['order_count'].mean()
    total_orders = df['order_count'].sum()
    avg_temp = df['temperature'].mean()
    
    with col1:
        st.metric(
            label="🌧️ Avg Orders (Rainy Days)",
            value=f"{rainy_orders:.0f}",
            delta=f"{((rainy_orders - non_rainy_orders) / non_rainy_orders * 100):+.1f}%"
        )
    
    with col2:
        st.metric(
            label="☀️ Avg Orders (Clear Days)",
            value=f"{non_rainy_orders:.0f}"
        )
    
    with col3:
        st.metric(
            label="📊 Total Orders",
            value=f"{total_orders:,}"
        )
    
    with col4:
        st.metric(
            label="🌡️ Avg Temperature",
            value=f"{avg_temp:.1f}°C"
        )

def create_weather_orders_chart(df):
    """Create bar chart showing orders by weather condition"""
    weather_summary = df.groupby('weather_condition').agg({
        'order_count': ['mean', 'sum'],
        'total_amount': 'mean'
    }).round(1)
    
    weather_summary.columns = ['Avg Orders', 'Total Orders', 'Avg Revenue']
    weather_summary = weather_summary.reset_index()
    
    fig = px.bar(
        weather_summary,
        x='weather_condition',
        y='Avg Orders',
        color='weather_condition',
        title="Average Orders by Weather Condition",
        color_discrete_map={
            'Rainy': '#1f77b4',
            'Clear': '#ff7f0e',
            'Sunny': '#2ca02c',
            'Cloudy': '#d62728'
        }
    )
    
    fig.update_layout(
        xaxis_title="Weather Condition",
        yaxis_title="Average Orders per Day",
        showlegend=False
    )
    
    return fig

def create_temperature_orders_scatter(df):
    """Create scatter plot showing relationship between temperature and orders"""
    fig = px.scatter(
        df,
        x='temperature',
        y='order_count',
        color='weather_condition',
        size='total_amount',
        hover_data=['date', 'rainfall'],
        title="Orders vs Temperature (Size = Revenue)",
        color_discrete_map={
            'Rainy': '#1f77b4',
            'Clear': '#ff7f0e',
            'Sunny': '#2ca02c',
            'Cloudy': '#d62728'
        }
    )
    
    # Add trend line
    z = np.polyfit(df['temperature'], df['order_count'], 1)
    p = np.poly1d(z)
    fig.add_traces(go.Scatter(
        x=df['temperature'],
        y=p(df['temperature']),
        mode='lines',
        name='Trend Line',
        line=dict(color='red', dash='dash')
    ))
    
    fig.update_layout(
        xaxis_title="Temperature (°C)",
        yaxis_title="Total Orders"
    )
    
    return fig

def create_time_pattern_chart(df):
    """Create chart showing ordering patterns by time and weather"""
    # Create time categories
    df['time_category'] = df['avg_order_hour'].apply(lambda x: 
        'Morning (6-12)' if 6 <= x < 12 else
        'Afternoon (12-17)' if 12 <= x < 17 else
        'Evening (17-22)' if 17 <= x < 22 else
        'Night (22-6)'
    )
    
    time_weather = df.groupby(['time_category', 'weather_condition'])['order_count'].mean().reset_index()
    
    fig = px.bar(
        time_weather,
        x='time_category',
        y='order_count',
        color='weather_condition',
        barmode='group',
        title="Average Orders by Time Period and Weather",
        color_discrete_map={
            'Rainy': '#1f77b4',
            'Clear': '#ff7f0e',
            'Sunny': '#2ca02c',
            'Cloudy': '#d62728'
        }
    )
    
    fig.update_layout(
        xaxis_title="Time Period",
        yaxis_title="Average Orders"
    )
    
    return fig

def create_daily_trend_chart(df):
    """Create line chart showing daily trends"""
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Daily Orders', 'Daily Temperature & Rainfall'),
        specs=[[{"secondary_y": False}],
               [{"secondary_y": True}]]
    )
    
    # Orders trend
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['order_count'],
            mode='lines+markers',
            name='Orders',
            line=dict(color='blue')
        ),
        row=1, col=1
    )
    
    # Temperature trend
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['temperature'],
            mode='lines',
            name='Temperature (°C)',
            line=dict(color='red')
        ),
        row=2, col=1
    )
    
    # Rainfall bars
    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['rainfall'],
            name='Rainfall (mm)',
            opacity=0.6,
            marker_color='lightblue'
        ),
        row=2, col=1, secondary_y=True
    )
    
    fig.update_layout(
        title="Daily Trends: Orders, Temperature, and Rainfall",
        height=600
    )
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Orders", row=1, col=1)
    fig.update_yaxes(title_text="Temperature (°C)", row=2, col=1)
    fig.update_yaxes(title_text="Rainfall (mm)", row=2, col=1, secondary_y=True)
    
    return fig

def create_insights_section(df):
    """Create insights section with key findings"""
    st.subheader("🔍 Key Insights")
    
    # Calculate insights
    rainy_orders = df[df['is_rainy']]['order_count'].mean()
    non_rainy_orders = df[~df['is_rainy']]['order_count'].mean()
    temp_correlation = df['temperature'].corr(df['order_count'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Weather Impact on Orders:**
        - Rainy days see {((rainy_orders - non_rainy_orders) / non_rainy_orders * 100):+.1f}% more orders
        - Average {rainy_orders:.0f} orders on rainy days vs {non_rainy_orders:.0f} on clear days
        - People prefer ordering food when it's raining! 🌧️
        """)
        
        st.success(f"""
        **Temperature Correlation:**
        - Correlation coefficient: {temp_correlation:.3f}
        - {'Positive' if temp_correlation > 0 else 'Negative'} relationship between temperature and orders
        - {'Higher' if temp_correlation > 0 else 'Lower'} temperatures tend to increase orders
        """)
    
    with col2:
        # Peak hours analysis
        rainy_peak = df[df['is_rainy']]['avg_order_hour'].mean()
        clear_peak = df[~df['is_rainy']]['avg_order_hour'].mean()
        
        st.warning(f"""
        **Peak Ordering Times:**
        - Rainy days: {rainy_peak:.1f}:00 (avg peak hour)
        - Clear days: {clear_peak:.1f}:00 (avg peak hour)
        - Weather affects when people order food! ⏰
        """)
        
        # Revenue insights
        rainy_revenue = df[df['is_rainy']]['total_amount'].mean()
        clear_revenue = df[~df['is_rainy']]['total_amount'].mean()
        
        st.info(f"""
        **Revenue Insights:**
        - Rainy days: ₹{rainy_revenue:,.0f} average daily revenue
        - Clear days: ₹{clear_revenue:,.0f} average daily revenue
        - {((rainy_revenue - clear_revenue) / clear_revenue * 100):+.1f}% revenue difference on rainy days
        """)

def main():
    """Main dashboard function"""
    st.title("🌦️🍕 Data Weaver Dashboard")
    st.markdown("### Weather vs Food Ordering Patterns Analysis")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar filters
    st.sidebar.header("📊 Dashboard Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(df['date'].min(), df['date'].max()),
        min_value=df['date'].min(),
        max_value=df['date'].max()
    )
    
    # Weather condition filter
    weather_conditions = st.sidebar.multiselect(
        "Select Weather Conditions",
        options=df['weather_condition'].unique(),
        default=df['weather_condition'].unique()
    )
    
    # Filter data
    if len(date_range) == 2:
        df_filtered = df[
            (df['date'] >= pd.to_datetime(date_range[0])) &
            (df['date'] <= pd.to_datetime(date_range[1])) &
            (df['weather_condition'].isin(weather_conditions))
        ]
    else:
        df_filtered = df[df['weather_condition'].isin(weather_conditions)]
    
    # Display KPIs
    create_kpi_cards(df_filtered)
    
    st.markdown("---")
    
    # Main charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_weather_orders_chart(df_filtered), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_temperature_orders_scatter(df_filtered), use_container_width=True)
    
    # Time pattern chart
    st.plotly_chart(create_time_pattern_chart(df_filtered), use_container_width=True)
    
    # Daily trends
    st.plotly_chart(create_daily_trend_chart(df_filtered), use_container_width=True)
    
    # Insights section
    create_insights_section(df_filtered)
    
    # Data table
    with st.expander("📋 View Raw Data"):
        st.dataframe(df_filtered)
    
    # Footer
    st.markdown("---")
    st.markdown("**Built with ❤️ using Streamlit | Data Weaver Project**")

if __name__ == "__main__":
    main()