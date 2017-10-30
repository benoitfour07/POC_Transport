library(shiny)
library(shinydashboard)
library(plotly)
library(radarchart)
library(leaflet)

header <- dashboardHeader(title = "Parking",
                          tags$li(a(href = 'http://www.sia-partners.com/services/data-science',
                                    img(src = 'logo_sia-partners2.png',
                                        title = "Sia Partners", width = '120px', height = '50px'),
                                    style = "padding-top:0px; padding-bottom:0px;"),
                                  class = "dropdown"))

sidebar <- dashboardSidebar(width=260,
  
  sidebarMenu(
    style = "position: fixed; overflow: visible;",
    id="tabs",
    menuItem("Vue carte", tabName = "carte", icon = icon("map")),
    menuItem("Méthodologie", tabName = "methodo", icon = icon("flask")),
    menuItem("Qui sommes-nous ?", tabName = "presentation", icon = icon("diamond")),
    menuItem("Nous contacter", tabName = "contact", icon = icon("envelope"))
    
  )
)

body <- dashboardBody(
  tags$head(
    tags$link(rel = "stylesheet", type = "text/css", href = "custom.css")
  ),
  tabItems(
    # ------------------------------------------------------------
    #                 Onglet Carte
    # ------------------------------------------------------------
    
    tabItem(tabName = "carte",
      leafletOutput("map_france", height = "600px")
        

    ),
    
    # ------------------------------------------------------------
    #                 Onglet methodo
    # ------------------------------------------------------------
    
    tabItem(tabName = "methodo",
            fluidRow(
              column(
                width =1
              ),
              column(
                width = 11,
                h1("Méthodologie", style = "color : #690f3c"), br())
              
            )
            ),
    
    
    # ------------------------------------------------------------
    #                 Onglet qui-sommes nous
    # ------------------------------------------------------------
     
    tabItem(tabName = "presentation",
            fluidRow(
              column(
                width =1
              ),
              column(
                width = 11,
                h1("Sia Partners en quelques mots", style = "color : #690f3c"), br())
              
            ),
            
            fluidRow(
              column(
                width =2
              ),
              column(
                width = 8,
                box(p(strong("Sia Partners est le leader français indépendant des cabinets de conseil en management."),"Fort d'une équipe de consultants de haut niveau,
                     nous accompagnons nos clients dans la conduite de leurs projets de transformation. Avec un portefeuille d'expertises de premier plan, 
                    nous apportons un regard innovant et des résultats concrets. Sia Partners est une partnership mondiale détenue a 100% par ses dirigeants.", 
                      style = "font-size : 12pt; text-align : justify")
                    , header = FALSE, solidHeader = TRUE, width = NULL)),
              column(
                width = 2
              )              
              
            ),
            
            fluidRow(
              column(
                width = 11,
                h1("En quelques chiffres", style = "text-align : right; color : #690f3c"), br()),
              column(
                width =1
              )
            ),
            
            fluidRow(
              column(
                width = 1
                ),
              
              column(
                width = 2,
                img(src = "sia-chiffres.PNG", style = "margin-right : 0pt")
              ),
              
              column(
                width = 3, 
                box(div(h2("Chiffres Clés", style = "margin-top : 0pt"), 
                        hr(style = "margin-top : 0pt; margin-bottom : 1pt; border-color : #690f3c"),
                    "140 M€ de Chiffre d'Affaires", br(),
                    "Créé en 1999", br(),
                    "20 bureaux", br(),
                    "45 Partners"),
                    header = FALSE, solidHeader = TRUE, width = NULL)
              ),
              
              column(
                width = 2,
                img(src= "sia-equipe.PNG", style = "margin-right : 0pt")
              ),
              
              column(
                width = 3,
                box(div(h2("Notre équipe", style = "margin-top : 0pt"), 
                        hr(style = "margin-top : 0pt; margin-bottom : 1pt; border-color : #690f3c"),
                        "Plus de 850 consultants", br(),
                        "Présent dans 15 pays", br(),
                        "Couvre 21 secteurs et services"),
                    header = FALSE, solidHeader = TRUE, width = NULL)
              ),
              
              column(
                width = 1
              )
            ),
            
            fluidRow(
              column(
                width = 1
              ),
              
              column(
                width = 2,
                img(src= "sia-clients.PNG", style = "margin-right : 0pt")
              ),
              
              column(
                width = 3,
                box(div(h2("Nos clients", style = "margin-top : 0pt"), 
                        hr(style = "margin-top : 0pt; margin-bottom : 1pt; border-color : #690f3c"),
                        "Plus de 230 clients", br(),
                        "Plus de 7000 missions depuis sa création", br(),
                        "20% des clients clefs faisant partie des 500 compagnies classées par le magazine Fortune"),
                    header = FALSE, solidHeader = TRUE, width = NULL)
              ),
              
              column(
                width = 2,
                img(src= "sia-services.PNG", style = "margin-right : 0pt")
              ),
              
              column(
                width = 3,
                box(div(h2("Nos services", style = "margin-top : 0pt"), 
                        hr(style = "margin-top : 0pt; margin-bottom : 1pt; border-color : #690f3c"),
                        "15% Stratégie", br(),
                        "70% Projets de transformation", br(),
                        "15% Stratégie IT et digitale"),
                    header = FALSE, solidHeader = TRUE, width = NULL)
              ),
              
              column(
                width = 1
              )   
            ),
            fluidRow(style = "background-color : #f5f5f5",
              column(
                width = 1
              ),
              column(
                width = 5, div(br(),
                              img(src = "data-science.PNG"),
                               h3("UC Data Science", style = "text-align:center"),br()
                               )
              ),
              column(
                width = 1
              )
            ),
            
            fluidRow(
                     column(
                       width = 1
                     ),
                     column(
                       width = 5, div(br(),
                         p("L'unité de Compétences Data Science, développée il y a presque 2 ans chez Sia Partners sur un mode start-up, regroupe des consultants disposant de compétences en matière de modélisation statistique et machine learning.", 
                           style = "text-align : justify"),
                         p("Convaincus qu'un projet de data science repose sur des itérations entre les expertises statistiques et métiers, l'équipe compte aujourd'hui 20 consultants alliant la connaissance des secteurs (énergie, transport, secteur public, banque/assurance, etc..) aux compétences techniques et business.", style ="text-align : justify"),
                         p("Une expertise au service de l'ensemble des secteurs :"),
                         p(strong("Marketing Analytics"), ": 90% des données collectées par les entreprises sont des données relatives aux clients. L'optimisation des actions marketing soulève 4 questions fondamentales : Qui sont mes clients ?
                            Quels sont leurs comportements et opinions ? Sur quels clients dois-je concentrer mes efforts ? Quelle est leur rentabilité future ?", style = "margin-left : 10px"),
                         p(strong("Etude de perception"), ": L'évaluation de la perception client est une méthode d'analyse de la valeur qui permet une meilleure compréhension des relations que vous entretenez avec vos clients.", style = "margin-left : 10px"),
                         p(strong("Detection d'atypisme"), ": avec l'intensification et l'instantanéité des échanges numériques, la détection de dysfonctionnements et de fraudes est devenue une priorité, notamment pour les organismes publics et financiers.", style = "margin-left : 10px"),
                         p(strong("Prevision"), "En permettant d'ajuster les stocks et l'approvisionnement a l'offre et la demande, les techniques de prévision contribuent a une meilleure maitrise des couts dans les maillons de la chaine de valeur des entreprises.", style = "margin-left : 10px"),
                         p(strong("Pricing"), ": Le développement du e-commerce et la pression concurrentielle de plus en plus forte dans certains secteurs, font du pricing et de l'optimisation associée des enjeux clés pour rester compétitif.
                            Les techniques de pricing permettent de répondre aux questions : Quels critères pour fixer le prix? Quel est l'impact du prix?? Quel est le signal prix? Comment optimiser la valeur percue? Quelle stratégie tarifaire adopter?", style = "margin-left : 10px"),
                         style = "padding-left : 30px; padding-right : 30px"),
                       br(),
                       tagList("Découvrez notre showroom :",br(),tags$a("datascience-lab.sia-partners.com", href="http://datascience-lab.sia-partners.com"))
                     ),
                     column(
                       width = 1
                     )
            )
            ),
    
    # ------------------------------------------------------------
    #                 Onglet contact
    # ------------------------------------------------------------
    
    tabItem(tabName = "contact",
            fluidRow(
              img(src = "sia-world.PNG")
            ),
            
            fluidRow(
              column(
                width = 1
              ),
              column(
                width = 11, 
                h1("Contact", style = "text-align : left; color : #690f3c"), br()
              )
            ),
            
            fluidRow(
              column(
                width = 1
              ),
              column(
                width = 5, h2("France", style = "margin-top : 0pt; text-align: left")
              ),
              column(
                width = 5, h2("Nous contacter directement", style = "margin-top: 0pt; text-align:left")
              ),
              column(
                width = 1
              )
            ),
            
            fluidRow(
              column(
                width = 1
              ),
              column(
                width = 2,
                box(p("- Paris", br(),
                "12 Rue Magellan", br(),
                "75008 Paris", br(),
                "+33 1 42 77 76 17", br(),
                "+33 1 42 77 76 16"),
                header = FALSE, solidHeader = TRUE, width = NULL
                )
              ),
              column(
                width = 3,
                box(p("- Lyon", br(), 
                "3 Rue du Président Carnot", br(),
                "69002 Lyon", br(),
                "+33 1 42 77 76 17", br(),
                "+33 1 42 77 76 16"),
                header = FALSE, solidHeader = TRUE, width = NULL
                )
              ),
              column(
                width = 3,
                box(p(strong("Romain LAURANS"), br(), 
                    "Responsable Data Science", br(),
                    "romain.laurans@sia-partners.com"),
                  
                    header = FALSE, solidHeader = TRUE, width = NULL
                )
              )
              ),
            fluidRow(
              column(
                width=9
              ),
              
              column(
                width=3,
                column(
                  width= 3, 
                  a(img(src="picto-web.png"), href = "http://www.sia-partners.com/")
                ),
                column(
                  width = 3,
                  a(img(src="picto-twitter.png"), href = "https://twitter.com/siapartners")  
                ),
                column(
                  width = 3,
                  a(img(src = "picto-linkedin.png"), href = "https://www.linkedin.com/company-beta/22581/")
                ),
                column(
                  width = 3,
                  a(img(src="picto-youtube.png"), href="https://www.youtube.com/user/SiaConseil/featured")  
                )
                
              )
            )
              
    )

    )
)




ui <- dashboardPage(title="Parking",header,sidebar,body)
