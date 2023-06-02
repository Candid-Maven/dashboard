import time
import revenue_fetch
import supplier_fetch
import utm_fetch

# Fetch all data
start_time = time.time()
print(f"batch starting fetch {start_time}")

revenue_fetch.fetch_data()
revenue_time = time.time()
print(f"batch finished revenue fetch {revenue_time}")

supplier_fetch.fetch_data()
supplier_time = time.time()
print(f"batch finished supplier fetch {supplier_time}")

utm_fetch.fetch_data()
utm_time = time.time()
print(f"batch finished utm fetch {utm_time}")

# Analyze all data
start_time = time.time()
print(f"batch starting clean {start_time}")

revenue_fetch.clean_data()
revenue_time = time.time()
print(f"batch finished revenue clean {revenue_time}")

supplier_fetch.clean_data()
supplier_time = time.time()
print(f"batch finished supplier clean {supplier_time}")

utm_fetch.clean_data()
utm_time = time.time()
print(f"batch finished utm clean {utm_time}")
