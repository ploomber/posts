# Generate sample sales data
set.seed(123)
n_days <- 365

sales_data <- data.frame(
  date = seq.Date(from = Sys.Date() - n_days, by = "day", length.out = n_days),
  sales = runif(n_days, 1000, 5000),
  units = round(runif(n_days, 50, 200)),
  region = sample(c("North", "South", "East", "West"), n_days, replace = TRUE)
)

# Add some seasonality and trend
sales_data$sales <- sales_data$sales * (1 + 0.3 * sin(2 * pi * (as.numeric(sales_data$date) / 365))) +
  as.numeric(sales_data$date - min(sales_data$date)) * 2

# Calculate metrics
total_sales <- sum(sales_data$sales)
total_units <- sum(sales_data$units)
avg_sale_value <- mean(sales_data$sales)
best_region <- names(sort(tapply(sales_data$sales, sales_data$region, sum), decreasing = TRUE)[1])