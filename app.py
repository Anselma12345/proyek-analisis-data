import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === 1. GATHERING DATA ===
st.title("📊 E-commerce Data Analysis Dashboard")

dataset_folder = "C:/Users/ansel/OneDrive/Documents/DBS FONDATION/proyek_analisis_data/E-commerce-public-dataset/E-Commerce Public Dataset"

# Membaca dataset
df_orders = pd.read_csv(os.path.join(dataset_folder, "orders_dataset.csv"))
df_customers = pd.read_csv(os.path.join(dataset_folder, "customers_dataset.csv"))
df_order_items = pd.read_csv(os.path.join(dataset_folder, "order_items_dataset.csv"))
df_products = pd.read_csv(os.path.join(dataset_folder, "products_dataset.csv"))
df_sellers = pd.read_csv(os.path.join(dataset_folder, "sellers_dataset.csv"))
df_payments = pd.read_csv(os.path.join(dataset_folder, "order_payments_dataset.csv"))
df_reviews = pd.read_csv(os.path.join(dataset_folder, "order_reviews_dataset.csv"))

# === 2. ASSESSING DATA ===
st.header("📌 Dataset Overview")
st.write("Checking missing values and dataset structure:")
st.write(df_orders.info())

# === 3. CLEANING DATA ===
st.subheader("📌 Data Cleaning")

# Mengubah kolom tanggal menjadi datetime
for col in ["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]:
    df_orders[col] = pd.to_datetime(df_orders[col], errors='coerce')

# Hitung waktu pengiriman & keterlambatan
df_orders["delivery_time_days"] = (df_orders["order_delivered_customer_date"] - df_orders["order_purchase_timestamp"]).dt.days
df_orders["late_delivery_days"] = (df_orders["order_delivered_customer_date"] - df_orders["order_estimated_delivery_date"]).dt.days.fillna(0).apply(lambda x: x if x > 0 else 0)

# === 4. EXPLORATORY DATA ANALYSIS ===
st.header("📊 Exploratory Data Analysis")

# Statistik Deskriptif
st.subheader("Summary Statistics")
st.write(df_orders[['delivery_time_days', 'late_delivery_days']].describe())

# === 5. VISUALIZATION & EXPLANATORY ANALYSIS ===
st.header("📈 Visualizations")

# Distribusi Waktu Pengiriman
st.subheader("Distribution of Delivery Time")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df_orders["delivery_time_days"].dropna(), bins=30, kde=True, color="skyblue", ax=ax)
ax.axvline(df_orders["delivery_time_days"].mean(), color='red', linestyle='dashed', linewidth=2, label=f"Mean: {df_orders['delivery_time_days'].mean():.2f} days")
ax.set_xlabel("Delivery Time (days)")
ax.set_ylabel("Count")
ax.set_title("Distribution of Delivery Time")
ax.legend()
st.pyplot(fig)

# Persentase Keterlambatan
st.subheader("Late Deliveries Percentage")
delay_percentage = (df_orders["late_delivery_days"] > 0).mean() * 100
st.metric(label="Percentage of Late Deliveries", value=f"{delay_percentage:.2f}%")

# Metode Pembayaran
st.subheader("Total Payment Value by Payment Type")
df_merged = df_orders.merge(df_payments, on='order_id', how='left')
df_payment_analysis = df_merged.groupby("payment_type")["payment_value"].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='payment_type', y='payment_value', data=df_payment_analysis, palette='coolwarm', ax=ax)
ax.set_title("Total Payment Value by Payment Type")
ax.set_xlabel("Payment Type")
ax.set_ylabel("Total Payment Value")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

# Tren Jumlah Pesanan dari Waktu ke Waktu
st.subheader("Orders Trend Over Time")
df_orders['order_purchase_date'] = pd.to_datetime(df_orders['order_purchase_timestamp']).dt.date
df_orders_trend = df_orders.groupby('order_purchase_date').size().reset_index(name='order_count')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='order_purchase_date', y='order_count', data=df_orders_trend, ax=ax, color='blue')
ax.set_title("Daily Order Count Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Number of Orders")
st.pyplot(fig)

st.success("✅ Dashboard successfully loaded!")