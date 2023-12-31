from PIL import Image
from PIL.ExifTags import TAGS

# Windows Keyword Exif Code: 40094
# Windows Title Exif Code: 40091 / 270
# TAGS.get(int) -> returns the name of the exif code

class ExifEditor:
    '''Class that edits the exif data of an image'''

    def __init__(self, path: str) -> None:
        self.src = path
        self.img = Image.open(path)
        self.img_exif = self.img.getexif()

    @property
    def title(self) -> str:
        '''Returns the image title exif'''
        if self.img_exif.get(270) == None:
            return ""
        return self.img_exif[270].decode("utf-16le")

    def set_title(self, title: str) -> None:
        '''Takes a title and sets it as the image title exif'''
        self.img_exif[270] = title.encode("utf-16le")

    def clear_title(self) -> None:
        '''Clears the image title exif'''
        if self.img_exif.get(270) == None:
            return
        del self.img_exif[270]

    @property
    def keywords(self) -> list:
        '''Returns the image keywords exif'''
        if self.img_exif.get(40094) == None:
            return []
        return [decoded.replace("\x00", "").replace("\ufeff", "") for decoded in self.img_exif[40094].decode("utf-16le").split(";")]

    def set_keywords(self, keywords: list) -> None:
        '''Takes a list of keywords and sets them as the image keyword exif'''
        self.clear_keywords()
        for keyword in keywords:
            self.add_keyword(keyword)

    def clear_keywords(self) -> None:
        '''Clears all keywords from the image keyword exif'''
        if self.img_exif.get(40094) == None:
            return
        del self.img_exif[40094]

    def remove_keyword(self, keyword: str) -> bool:
        '''Takes a keyword and removes it from the image keyword exif'''
        if self.img_exif.get(40094) == None:
            return False
        
        if keyword.__contains__(";"):
            # keyword = keyword.replace(";", "") # I don't think mass removing is a good idea...
            return False
        
        # If the keyword is not in the exif, don't remove it
        if not self.img_exif[40094].__contains__(keyword.encode("utf-16le")):
            return False
        
        # If the keyword is the only keyword, delete the exif
        if len(self.keywords) == 1:
            del self.img_exif[40094]
            return True
        
        # If the keyword is in the exif, remove it
        self.img_exif[40094] = self.img_exif[40094].replace((keyword + ";").encode("utf-16le"), "".encode("utf-16le"))
        return True

    def add_keyword(self, keyword: str) -> None:
        '''Takes a keyword and adds it to the image keyword exif'''
        
        # If the keyword is empty, don't add it
        if keyword == "": 
            return
        
        # Remove whitespaces
        keyword = keyword.strip().rstrip()

        # If the keyword contains a semicolon, split it (Windows doesn't like semicolons)
        if keyword.__contains__(";"):
            self.add_keywords(keyword.split(";"))
            return

        # If there is no keyword exif, create one
        if self.img_exif.get(40094) == None or self.img_exif.get(40094) == "".encode("utf-16le"):
            self.img_exif[40094] = "".encode("utf-16le") + keyword.encode("utf-16le")
            return
        
        # If the keyword is already in the exif, don't add it
        if self.img_exif[40094].__contains__(keyword.encode("utf-16le")):
            return
        
        # If the keyword is not in the exif, add it
        self.img_exif[40094] += ";".encode("utf-16le") + keyword.encode("utf-16le")

    def add_keywords(self, keywords: list) -> None:
        '''Takes a list of keywords and adds them to the image keyword exif'''
        for keyword in keywords:
            self.add_keyword(keyword)

    def get_exif_data(self) -> dict:
        '''Returns the exif data of the image'''
        return {key: value.decode("utf-16le") if type(value) == bytes else value for key, value in self.img_exif.items()}

    def print_exif_data(self) -> None:
        '''Takes an image exif and prints out all the exif data of the image'''
        for img_data in self.img_exif.items():
            if type(img_data[1]) == bytes:
                print(img_data[0], img_data[1].decode("utf-16le"))
            else:
                print(img_data[0], img_data[1])

    def save_image(self) -> None:
        '''Saves the image with the new exif data'''
        self.img.save(self.src, exif=self.img_exif)

    def close_image(self) -> None:
        '''Closes the image'''
        self.img.close()

    def __del__(self) -> None:
        '''Destructor'''
        self.close_image()

    def __repr__(self) -> str:
        '''Returns the image path'''
        return self.src
    
    def __str__(self) -> str:
        '''Returns the image path'''
        return self.src
    
    def __eq__(self, other) -> bool:
        '''Returns True if the image paths are the same'''
        try:
            return self.src == other.src
        except:
            return False