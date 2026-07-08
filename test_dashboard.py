"""
Simple test script to verify data processing and basic functionality
Run this if Streamlit is not available
"""

import pandas as pd

def test_data_loading():
    """Test if merged data loads correctly"""
    try:
        df = pd.read_csv('data/merged_data.csv')
        print(f"✅ Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def basic_analysis(df):
    """Perform basic analysis without advanced plotting"""
    print("\n=== BASIC ANALYSIS ===")
    
    # Weather condition summary
    print("\n📊 Orders by Weather Condition:")
    weather_summary = df.groupby('weather_condition')['order_count'].agg(['mean', 'sum']).round(1)
    print(weather_summary)
    
    # Rainy vs non-rainy comparison
    rainy_orders = df[df['is_rainy']]['order_count'].mean()
    non_rainy_orders = df[~df['is_rainy']]['order_count'].mean()
    
    print(f"\n🌧️ Rainy Days Average Orders: {rainy_orders:.1f}")
    print(f"☀️ Non-Rainy Days Average Orders: {non_rainy_orders:.1f}")
    print(f"📈 Difference: {((rainy_orders - non_rainy_orders) / non_rainy_orders * 100):+.1f}%")
    
    # Temperature correlation
    temp_corr = df['temperature'].corr(df['order_count'])
    print(f"\n🌡️ Temperature-Orders Correlation: {temp_corr:.3f}")
    
    # Revenue analysis
    rainy_revenue = df[df['is_rainy']]['total_amount'].mean()
    non_rainy_revenue = df[~df['is_rainy']]['total_amount'].mean()
    
    print(f"\n💰 Revenue Analysis:")
    print(f"   Rainy days: ₹{rainy_revenue:,.0f}")
    print(f"   Non-rainy days: ₹{non_rainy_revenue:,.0f}")
    print(f"   Difference: {((rainy_revenue - non_rainy_revenue) / non_rainy_revenue * 100):+.1f}%")

def show_data_sample(df):
    """Show sample data and structure"""
    print("\n📋 Data Sample (First 5 rows):")
    print(df.head().to_string())
    
    print(f"\n📊 Data Types:")
    print(df.dtypes.to_string())
    
    print(f"\n📈 Summary Statistics:")
    print(df.describe().round(2).to_string())

def main():
    print("🧪 Testing Data Weaver Project...")
    
    # Test data loading
    df = test_data_loading()
    if df is None:
        return
    
    # Show basic info
    print(f"\n📋 Dataset Info:")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"   Weather conditions: {', '.join(df['weather_condition'].unique())}")
    print(f"   Temperature range: {df['temperature'].min():.1f}°C to {df['temperature'].max():.1f}°C")
    
    # Perform analysis
    basic_analysis(df)
    
    # Show data sample
    show_data_sample(df)
    
    print("\n✅ Test completed successfully!")
    print("\n📝 Next steps:")
    print("   1. Install Streamlit: py -m pip install streamlit plotly")
    print("   2. Run dashboard: streamlit run dashboard/app.py")
    print("   3. Open browser to http://localhost:8501")

if __name__ == "__main__":
    main()