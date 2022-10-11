##
##  This script is the main script for the EpiCo package.
##  It is used to run the EpiCo algorithm on a given dataset.
##  This is the R translation of the python code in EpiCo_python
##

library(reticulate) # for Python interoperability

# Load Python shell
use_python("/Users/samueltorres/opt/anaconda3/bin/python") # path to Python environment

# Point to controller
source_python("controller.py")


downloadSivigilaData <- function(years_to_download, events_to_download) {
    download_Data <- download_sivigila_data(years_to_download, events_to_download)
    return(download_Data)
}


preprocessData <- function(years_to_preprocess, events_to_preprocess, save) {
    if (save) {
    if (length(years_to_preprocess) == 1) {
        years_save <- years_to_preprocess[[1]]
    } else {
        years_save <- paste(years_to_preprocess[[1]], 
                years_to_preprocess[[length(years_to_preprocess)]],
                sep = "-")
    }
}
    preprocess_data <- preprocess_sivigila_data(years_to_preprocess,
                                                events_to_preprocess,
                                                years_save,
                                                save)
    return(preprocess_data)
}


preprocessDataDemographics <- function(save) {
    preprocess_data_demographics <- preprocess_cesus_demographic(save)
    return(preprocess_data_demographics)
}

preprocessDataHouseholds <- function(save) {
    preprocess_data_households <- preprocess_cesus_household(save)
    return(preprocess_data_households)
}


preprocessDataHouseholds(save = TRUE)