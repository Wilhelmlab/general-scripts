#' Import a citation dataset generated from Web of Science's Citation Report and make a heatmap of the publications or citations for a timeline marked by each year
#' Requires citation dataset be reduced to four columns: Year, Value, Citations, Publications (.csv)
#' Requires tidyverse
#'
#' @param file1 input file in quotes
#' @param cites specifies you will plot citations, by default it will plot publications 
#' 
#' @return Returns a ggplot value that can be visualized and saved
#'
#' @example
#' PubCites_heatmap("webofscience_citationreport_Date.csv")
#'
#' @export

PubCites_heatmap <- function(file1, cites){
  Rawfile <- read.csv(file1,
                      na.strings = c("","NA"))
  
  if(missing(cites)){graph<-ggplot(Rawfile, aes(x=Year, y=Value, color=Publications))  +
    geom_line(size=20) +
    scale_color_gradient(low="greenyellow", high="darkgreen")}
  
  else{graph<-ggplot(Rawfile, aes(x=Year, y=Value, color=Citations)) +
      geom_line(size=20) +
      scale_color_gradient(low="khaki1", high="darkorange")}
  
  return(graph)
}


      
  
  