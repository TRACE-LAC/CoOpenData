source("main_ColOpenData.R")

# Define years and events that you want to download/process in a dataframe
years_to_preprocess <- list("2007", "2008", "2009",
                            "2010", "2011", "2012",
                            "2013", "2014", "2015",
                            "2016", "2017", "2018",
                            "2019", "2020")
events_to_preprocess <- list("DENGUE", "DENGUE GRAVE", "MORTALIDAD POR DENGUE")
save <- TRUE

# Download data from the sivigila server
downloadSivigilaData(years_to_preprocess, events_to_preprocess)

# Preprocess Sivigila data
preprocessData(years_to_preprocess, events_to_preprocess, save)

# Preprocess CENSO data
preprocessDataDemographics(save)
preprocessDataHouseholds(save)