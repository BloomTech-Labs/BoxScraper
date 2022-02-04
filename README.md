# Onetime Setup
1. Install Docker Desktop

# Run the BoxScraper
- Run Docker Desktop 
- Refresh the Box Developer Token (every 60 minutes)
   - https://app.box.com/developers/console/app/1646792/configuration
- From the Terminal on Linux, WSL, Gitbash or Unix (macOS)
```shell
./run.sh
```
- For Windows run the following instead
```shell
docker build . -t box_scraper
docker run -it box_scraper
```
