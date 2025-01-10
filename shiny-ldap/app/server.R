library(magrittr)
source('data.R')
library(shiny)
library(dplyr)
library(ggplot2)

server <- function(input, output, session) {
  
  # Handle logout button click
  observeEvent(input$logout_btn, {
    session$sendCustomMessage("logout", "/logout")
  })
  
  # Reactive filtered dataset
  filtered_data <- reactive({
    data <- sales_data
    
    if (input$region != "All") {
      data <- data[data$region == input$region,]
    }
    
    data <- data[data$date >= input$date_range[1] & data$date <= input$date_range[2],]
    data
  })
  
  # Value boxes
  output$total_sales <- renderText({
    paste0("$", format(round(sum(filtered_data()$sales)), big.mark = ","))
  })
  
  output$total_units <- renderText({
    format(sum(filtered_data()$units), big.mark = ",")
  })
  
  output$avg_sale <- renderText({
    paste0("$", format(round(mean(filtered_data()$sales)), big.mark = ","))
  })
  
  output$best_region <- renderText({
    sales_by_region <- tapply(filtered_data()$sales, filtered_data()$region, sum)
    names(which.max(sales_by_region))
  })
  
  # Plots
  output$sales_trend <- renderPlot({
    ggplot(filtered_data(), aes(x = date, y = sales)) +
      geom_line(color = "#007bff") +
      geom_smooth(method = "loess", color = "#dc3545") +
      theme_minimal() +
      labs(x = "Date", y = "Sales ($)") +
      scale_y_continuous(labels = scales::dollar_format())
  })
  
  output$sales_by_region <- renderPlot({
    filtered_data() %>%
      group_by(region) %>%
      summarise(total_sales = sum(sales)) %>%
      ggplot(aes(x = reorder(region, -total_sales), y = total_sales, fill = region)) +
      geom_col() +
      theme_minimal() +
      labs(x = "Region", y = "Total Sales ($)") +
      scale_y_continuous(labels = scales::dollar_format()) +
      theme(legend.position = "none")
  })
  
  output$sales_dist <- renderPlot({
    ggplot(filtered_data(), aes(x = sales)) +
      geom_histogram(fill = "#17a2b8", bins = 30) +
      theme_minimal() +
      labs(x = "Sales ($)", y = "Count") +
      scale_x_continuous(labels = scales::dollar_format())
  })
}