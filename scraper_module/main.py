from scraper_module.scraper  import crawl, save_results_to_json

base_url = "https://theinventorymaster.com"
max_pages = 100

# Run scraper
scraped_data = crawl(base_url,max_pages)

# Save to file
save_results_to_json(scraped_data, "inventory_data.json")

# Print a preview
for page in scraped_data[:3]:
    print(page["url"], page["title"])
