library(shiny)
library(shinydashboard)
library(ggplot2)
library(plotly)
library(leaflet)
library(lattice)
library(radarchart)

# ############################################################
#                           DEFINITION CONSTANTES
# ############################################################
input_path <- "C:/Users/psaffers/Documents/POC/Parking/Data/Covoiturage"

# ############################################################
#                           IMPORT
# ############################################################
covoit_table <- as.data.frame(read.table(paste(input_path,"/covoit_20171109.csv",sep=""), header = TRUE, sep = ','))
lat_covoit   <- as.numeric(unlist(covoit_table['lat']))
lng_covoit   <- as.numeric(unlist(covoit_table['lng']))
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
       setView(lng = 2.333333, lat = 48.866667, zoom = 10) %>%
       addMarkers(lng = lng_covoit, lat = lat_covoit)
   })
     
   output$map_france <- renderLeaflet({
     #map_regions<-geojsonio::geojson_read("./france-geojson-master/regions/ile-de-france/region-ile-de-france.geojson", what = "sp")
     return(leaf())
                                   
   })
  # 
}


 


