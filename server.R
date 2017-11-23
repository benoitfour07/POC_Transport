library(shiny)
library(shinydashboard)
library(ggplot2)
library(plotly)
library(leaflet)
library(lattice)
library(radarchart)
library(dplyr)
library(data.table)
# ############################################################
#                           SOURCES
# ############################################################
source("Rfunc/content_css.R")
source("Rfunc/import_fread.R")
# ############################################################
#                           DEFINITION CONSTANTES
# ############################################################
input_path <- "C:/Users/psaffers/Documents/POC/Parking/Data/"
icon_path  <- "C:/Users/psaffers/Documents/POC/Parking/Graph/Icons"
#Creation des icons
source("Rfunc/create_icon.R")
#Corps HTML exemple pour pop-up
html_content <- paste(css_content,
                      '<body>',
                      '<b><font color = "#610B4B" size = "4">','Nom du parking',"</font></b>","</br>",
                      '</br>',
                       '<b><font size="2" face="calibri" color = "#6E6E6E">',"Evolution de l'occupation du parking","</font></b>","</br>",
                       '<i><font size="2">',"Graphique ici","</font></i>","</br>","</br>","</br>",
                       '<div class="corps"> ',
                          '<div class="colonnes">',
                            '<div class="colgauche">',
                                '<font size="2" face="calibri" color = "#6E6E6E"><b> Données Météorologiques </b></font></br></br></br></br>',
                            '</div>',
                            '<div class="colgauche">',
                                '<font size="2" face="calibri" color = "#6E6E6E"><b> Evénements a proximité </b></font></br></br></br></br>',
                            '</div>',
                          '</div>',
                      '</div>',
                      '</body>'
)

# ############################################################
#                           IMPORT
# ############################################################
#Import des data de covoiturage
covoit_table <- import_fich(paste(input_path,"Covoiturage/covoit_20171120.csv",sep=""))
lat_covoit   <- as.numeric(unlist(covoit_table['lat']))
lng_covoit   <- as.numeric(unlist(covoit_table['lng']))

#Import des data de patrimoine
patrim_table <- import_fich(paste(input_path,"Patrimoine/referentiel-parkings.csv",sep=""))
patrim_table$icon <- factor(ifelse(patrim_table$Flag_Data==1,
                            "icon_park_1",
                            "icon_park_2"),
                            c("icon_park_1","icon_park_2")
)
lat_patrim   <- as.numeric(unlist(patrim_table['lat']))
lng_patrim   <- as.numeric(unlist(patrim_table['lng']))
siz_patrim   <- length(lat_patrim)
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
       setView(lng = 2.344894, lat = 48.853873, zoom = 12) %>%
       addMarkers(lng = lng_covoit, lat = lat_covoit, icon=icon_car) %>%
       addMarkers(lng = lng_patrim, lat = lat_patrim, icon=parkIcons[unlist(patrim_table['icon'])],
                  popup = rep(html_content,siz_patrim),
                  popupOptions = popupOptions(maxWidth=1000,minWidth=500))
   })
     
   output$map_france <- renderLeaflet({
     #map_regions<-geojsonio::geojson_read("./france-geojson-master/regions/ile-de-france/region-ile-de-france.geojson", what = "sp")
     return(leaf())
                                   
   })
  # 
}


 


