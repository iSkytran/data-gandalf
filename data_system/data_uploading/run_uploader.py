from json_to_db_uploader import JsonToDbUploader

INPUT_FOLDER = "metadata/"

INPUT_PATHS = ["academics", "finance", "health", "housing", "sports"]

for path in INPUT_PATHS:
    uploader = JsonToDbUploader(file_input_path=str(INPUT_FOLDER + path))

    uploader.prepare_upload()
    uploader.upload()