source('data.R')
library(shiny)
library(bslib)

ui <- page_sidebar(
  title = "Sales Performance Dashboard",
  theme = bs_theme(bootswatch = "lumen"),
  
  sidebar = sidebar(
    selectInput("region", "Select Region:",
                choices = c("All", "North", "South", "East", "West")),
    dateRangeInput("date_range", "Date Range:",
                   start = min(sales_data$date),
                   end = max(sales_data$date))
  ),
  
  layout_column_wrap(
    width = 1/2,
    value_box(
      title = "Total Sales",
      value = textOutput("total_sales"),
      theme = "primary"
    ),
    value_box(
      title = "Total Units",
      value = textOutput("total_units"),
      theme = "secondary"
    ),
    value_box(
      title = "Average Sale Value",
      value = textOutput("avg_sale"),
      theme = "success"
    ),
    value_box(
      title = "Best Performing Region",
      value = textOutput("best_region"),
      theme = "warning"
    )
  ),
  
  layout_column_wrap(
    width = 1,
    card(
      full_screen = TRUE,
      card_header("Sales Trend"),
      plotOutput("sales_trend")
    )
  ),
  
  layout_column_wrap(
    width = 1/2,
    card(
      full_screen = TRUE,
      card_header("Sales by Region"),
      plotOutput("sales_by_region")
    ),
    card(
      full_screen = TRUE,
      card_header("Daily Sales Distribution"),
      plotOutput("sales_dist")
    )
  )
)