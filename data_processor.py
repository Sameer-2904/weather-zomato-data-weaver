"""
Data Weaver - Data Processing Module
Cleans, preprocesses, and merges weather and Zomato order datasets
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_and_clean_weather_data(file_path):
    """
    Load and clean weather data
    - Handle missing values
    - Normalize date formats
    - Validate temperature and rainfall ranges
    """
    print("Loading weather data...")
    weather_df = pd.read_csv(file_path)
    
    # Convert date column to datetime
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    
    # Handle missing values
    weather_df['temperature'].fillna(weather_df['temperature'].mean(), inplace=True)
    weather_df['rainfall'].fillna(0, inplace=True)
    weather_df['weather_condition'].fillna('Clear', inplace=True)
    
    # Create binary rainy flag for easier analysis
    weather_df['is_rainy'] = weather_df['weather_condition'].isin(['Rainy'])
    
    print(f"Weather data loaded: {len(weather_df)} records")
    return weather_df

def load_and_clean_orders_data(file_path):
    """
    Load and clean Zomato orders data
    - Handle missing values
    - Normalize date and time formats
    - Aggregate orders by date
    """
    print("Loading orders data...")
    orders_df = pd.read_csv(file_path)
    
    # Convert date column to datetime
    orders_df['date'] = pd.to_datetime(orders_df['date'])
    
    # Extract hour from time for time-based analysis
    orders_df['hour'] = pd.to_datetime(orders_df['time'], format='%H:%M').dt.hour
    
    # Handle missing values
    orders_df['order_count'].fillna(0, inplace=True)
    orders_df['total_amount'].fillna(0, inplace=True)
    
    print(f"Orders data loaded: {len(orders_df)} records")
    return orders_df

def aggregate_orders_by_date(orders_df):
    """
    Aggregate order data by date for merging with weather data
    """
    print("Aggregating orders by date...")
    
    # Daily aggregations
    daily_orders = orders_df.groupby('date').agg({
        'order_count': 'sum',
        'total_amount': 'sum',
        'category': 'count'  # Count of different order entries per day
    }).reset_index()
    
    # Rename category count to total_orders
    daily_orders.rename(columns={'category': 'total_orders'}, inplace=True)
    
    # Calculate average order value
    daily_orders['avg_order_value'] = daily_orders['total_amount'] / daily_orders['order_count']
    
    # Peak hour analysis
    peak_hours = orders_df.groupby('date')['hour'].agg(['min', 'max', 'mean']).reset_index()
    peak_hours.columns = ['date', 'earliest_order_hour', 'latest_order_hour', 'avg_order_hour']
    
    # Merge daily orders with peak hours
    daily_orders = daily_orders.merge(peak_hours, on='date', how='left')
    
    print(f"Daily aggregated data: {len(daily_orders)} records")
    return daily_orders

def merge_datasets(weather_df, daily_orders_df):
    """
    Merge weather and orders datasets on date
    """
    print("Merging datasets...")
    
    # Merge on date
    merged_df = weather_df.merge(daily_orders_df, on='date', how='inner')
    
    # Add derived features for analysis
    merged_df['orders_per_degree'] = merged_df['order_count'] / merged_df['temperature']
    merged_df['rainfall_category'] = pd.cut(merged_df['rainfall'], 
                                          bins=[-0.1, 0, 10, 20, float('inf')], 
                                          labels=['No Rain', 'Light Rain', 'Moderate Rain', 'Heavy Rain'])
    
    print(f"Merged dataset: {len(merged_df)} records")
    return merged_df

def generate_insights(merged_df):
    """
    Generate key insights from the merged dataset
    """
    print("\nGenerating insights...")
    
    insights = {}
    
    # Insight 1: Orders on rainy vs non-rainy days
    rainy_orders = merged_df[merged_df['is_rainy']]['order_count'].mean()
    non_rainy_orders = merged_df[~merged_df['is_rainy']]['order_count'].mean()
    insights['rainy_vs_non_rainy'] = {
        'rainy_avg': rainy_orders,
        'non_rainy_avg': non_rainy_orders,
        'difference_pct': ((rainy_orders - non_rainy_orders) / non_rainy_orders) * 100
    }
    
    # Insight 2: Temperature correlation with orders
    temp_correlation = merged_df['temperature'].corr(merged_df['order_count'])
    insights['temperature_correlation'] = temp_correlation
    
    # Insight 3: Peak ordering times
    rainy_peak_hour = merged_df[merged_df['is_rainy']]['avg_order_hour'].mean()
    non_rainy_peak_hour = merged_df[~merged_df['is_rainy']]['avg_order_hour'].mean()
    insights['peak_hours'] = {
        'rainy_peak': rainy_peak_hour,
        'non_rainy_peak': non_rainy_peak_hour
    }
    
    # Insight 4: Revenue impact
    rainy_revenue = merged_df[merged_df['is_rainy']]['total_amount'].mean()
    non_rainy_revenue = merged_df[~merged_df['is_rainy']]['total_amount'].mean()
    insights['revenue_impact'] = {
        'rainy_avg_revenue': rainy_revenue,
        'non_rainy_avg_revenue': non_rainy_revenue,
        'revenue_difference_pct': ((rainy_revenue - non_rainy_revenue) / non_rainy_revenue) * 100
    }
    
    return insights

def main():
    """
    Main data processing pipeline
    """
    print("=== Data Weaver - Data Processing Pipeline ===\n")
    
    # Load and clean data
    weather_df = load_and_clean_weather_data('data/weather.csv')
    orders_df = load_and_clean_orders_data('data/zomato_orders.csv')
    
    # Aggregate orders by date
    daily_orders_df = aggregate_orders_by_date(orders_df)
    
    # Merge datasets
    merged_df = merge_datasets(weather_df, daily_orders_df)
    
    # Save merged dataset
    merged_df.to_csv('data/merged_data.csv', index=False)
    print("Merged dataset saved to 'data/merged_data.csv'")
    
    # Generate and display insights
    insights = generate_insights(merged_df)
    
    print("\n=== KEY INSIGHTS ===")
    print(f"1. Rainy Day Orders: {insights['rainy_vs_non_rainy']['rainy_avg']:.1f} vs Non-Rainy: {insights['rainy_vs_non_rainy']['non_rainy_avg']:.1f}")
    print(f"   Difference: {insights['rainy_vs_non_rainy']['difference_pct']:.1f}% more orders on rainy days")
    
    print(f"\n2. Temperature-Orders Correlation: {insights['temperature_correlation']:.3f}")
    
    print(f"\n3. Peak Ordering Hours:")
    print(f"   Rainy days: {insights['peak_hours']['rainy_peak']:.1f}:00")
    print(f"   Non-rainy days: {insights['peak_hours']['non_rainy_peak']:.1f}:00")
    
    print(f"\n4. Revenue Impact:")
    print(f"   Rainy days: ₹{insights['revenue_impact']['rainy_avg_revenue']:.0f}")
    print(f"   Non-rainy days: ₹{insights['revenue_impact']['non_rainy_avg_revenue']:.0f}")
    print(f"   Difference: {insights['revenue_impact']['revenue_difference_pct']:.1f}% more revenue on rainy days")
    
    print(f"\n=== Data Processing Complete ===")
    print(f"Final dataset shape: {merged_df.shape}")

if __name__ == "__main__":
    main()