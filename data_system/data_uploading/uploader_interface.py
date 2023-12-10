import os

class MetadataUploader:
    """
    Acts as an abstract class with some common state. Subclasses should override prepare_upload, 
    upload, and report_issues. 

    Attributes
    --------------

    """
    def __init__(self):
        self.problem_files = []

    def prepare_upload(self, topics):
        pass

    def upload(self):
        pass

    def report_issues(self):
        pass
