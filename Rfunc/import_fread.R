#Fonction qui permet d'importer une table avec fread et un répertoire
import_fich <- function(path_){
  table <- as.data.frame(fread(path_,
                               encoding = 'UTF-8'))
  return(table)
}