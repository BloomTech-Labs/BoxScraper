import os

from BoxScraper.aws_s3 import S3
from BoxScraper.keywords import get_keywords
from BoxScraper.box_wrapper import BoxWrapper
from BoxScraper.ocr import ocr
from BoxScraper.mongo import Mongo
from BoxScraper.summary import summary
from BoxScraper.thumbnails import get_thumbnail

box = BoxWrapper()
mongo = Mongo()
s3 = S3()


def scrape_box(finished_ids, folder_id="0"):
    folder_info = box.client.folder(folder_id).get()
    print(f"Scanning Folder: {folder_id}, {folder_info['name']}")
    files, folders = box.items_in_folder(folder_id)
    for file in files:
        if file["id"] not in finished_ids:
            finished_ids.add(file["id"])
            scrape_file(file["id"])
    for folder in folders:
        scrape_box(finished_ids, folder["id"])


def scrape_file(file_id):
    info = box.get_file_info(file_id)
    if info["ext"] == "pdf":
        print(f"Scraping File: {info['id']}, {info['name']}")
        print(" -Downloading File")
        pdf_bytes = box.download_file(file_id)
        file_name = f"{file_id}.jpg"
        print(" -Generating Thumbnail")
        file_path = os.path.join("BoxScraper", "thumbs", file_name)
        thumbnail = get_thumbnail(pdf_bytes)
        thumbnail.save(file_path, format="jpeg")
        print(" -Uploading Thumbnail")
        bucket_name = "docdb-thumbnails"
        s3.upload(file_path, bucket_name, file_name)
        print(" -Processing Text")
        ocr_text = ocr(pdf_bytes, dpi=150)
        record = {
            "box_id": info["id"],
            "name": info["name"],
            "path": info["path"],
            "url": info["url"],
            "tags": get_keywords(ocr_text),
            "summary": summary(ocr_text),
            "text": ocr_text,
        }
        print(" -Inserting Data")
        mongo.insert(record)


if __name__ == '__main__':
    print("\nInitializing BoxScraper...", end=" ")
    data = mongo.connect().find({}, {"_id": False, "box_id": True})
    finished_data = {record["box_id"] for record in data}
    print("Ready!\n")
    scrape_box(finished_data, folder_id="0")
