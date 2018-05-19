#Set our working directory.
dir="/Users/elinlarsen/GoogleDrive/PhD_elin/Projets/WordSegComprehension/wordsegcomp/R_pipeline/"
setwd(dir)

#render your website.
rmarkdown::render_site()

# actually remove the files
#rmarkdown::clean_site()