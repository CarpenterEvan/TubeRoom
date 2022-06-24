import os

sMDT_path = "./Google Drive/Shared drives/sMDT Tube Testing Reports"
TubeTension_path = os.path.join(sMDT_path, "TubeTension/Processed")
def main():
    for file in os.listdir(TubeTension_path):
        file_path = os.path.join(TubeTension_path, file)
        if os.path.isfile(file_path):
            yield file_path

if __name__ == "__main__":
    print(__name__)
