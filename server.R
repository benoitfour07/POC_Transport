library(shiny)
library(shinydashboard)
library(ggplot2)
library(plotly)
library(leaflet)
library(lattice)
library(radarchart)



# ############################################################
#                           GRAPHIQUES
# ############################################################


server <- function(input, output,session) {
  # ------------------------------------------------------------
  #                 Cartographie
  # ------------------------------------------------------------
  
  # #Generation de la carte
   leaf <- reactive({
     #countours regions
     map_regions<-geojsonio::geojson_read("./france-geojson-master/regions/ile-de-france/communes-ile-de-france.geojson", what = "sp")
     leaflet(map_regions) %>%
       addProviderTiles("CartoDB.Positron") %>%
       addLegend(title = 'Légendes', colors= NULL, labels= NULL, opacity = 0.9, position = 'topright') %>%
       # On se place sur l IDF
       setView(lng = 2.333333, lat = 48.866667, zoom = 10)
   })
     
   output$map_france <- renderLeaflet({
     #map_regions<-geojsonio::geojson_read("./france-geojson-master/regions/ile-de-france/region-ile-de-france.geojson", what = "sp")
     return(leaf())
                                   
   })
  # 
}


 


