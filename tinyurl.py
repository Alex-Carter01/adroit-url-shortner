import random
import string
import unittest

# this url_map tracks a lookup from short_url extensions to a tuple of a long_url and the count of many times it has been accessed for stat tracking
#url_map<short_url: (long_url, count)>
url_map = {}

# character set allowed in random urls: ASCII letters (lowercase + uppercase) and digits
characters = string.ascii_letters + string.digits

def create_url(long_url, extension=""):
    # if no custom short url is provided, make a random one
    if extension == "":
        
        #generates random short_url extensions until a unique one is found
        extension = ''.join(random.choices(characters, k=8))

        while extension in url_map:
            extension = ''.join(random.choices(characters, k=8))

    # if a custom short url is provided, try to use it, or return an error for not being unique
    else: 
        # note for additional robustness, this could be enhanced to escape special characters or character not valid in a url
        # for example extension "abc?q=x" would be problematic
        if extension in url_map:
            raise ValueError("Custom URL extension already exists.")
    url_map[extension] = (long_url, 0)
    return extension

def delete_short_url(short_url):
    if short_url in url_map:
        del url_map[short_url]
    else:
        raise KeyError("Short URL does not exist.")

def decode_short_url(short_url):
    if short_url in url_map:
        # Increment the count, and return the long URL
        current_tuple = url_map[short_url]
        new_count = current_tuple[1] + 1
        url_map[short_url] = (current_tuple[0], new_count)
        return current_tuple[0]
    raise KeyError("Short URL does not exist.")

def get_stats_short(short_url):
    if short_url in url_map:
        return url_map[short_url]
    else:
        raise KeyError("Short URL does not exist.")

class TestURLShortener(unittest.TestCase):
    def test_create_random_url(self):
        long_url = "https://github.com/Alex-Carter01"
        short_url = create_url(long_url)
        self.assertIn(short_url, url_map)
        self.assertEqual(url_map[short_url], (long_url, 0))

    def test_create_custom_url(self):
        long_url = "https://www.linkedin.com/in/alex-c-963659148/"
        custom_extension = "linkedin"
        short_url = create_url(long_url, custom_extension)
        self.assertIn(short_url, url_map)
        self.assertEqual(url_map[short_url], (long_url, 0))                 

    def test_create_duplicate_custom_url(self):
        long_url = "https://example.com"
        custom_extension = "abc123"
        create_url(long_url, custom_extension)  # First creation
        with self.assertRaises(ValueError):  # Assuming ValueError is raised for duplicates
            create_url(long_url, custom_extension)  # Second attempt

    def test_create_existing_long_url_random(self):
        long_url = "https://example.com"
        create_url(long_url)  # First creation
        short_url = create_url(long_url)  # Second creation
        self.assertNotEqual(short_url, long_url)

    def test_delete_valid_short_url(self):
        long_url = "https://example.com"
        short_url = create_url(long_url)
        delete_short_url(short_url)
        self.assertNotIn(short_url, url_map)

    def test_delete_nonexistent_short_url(self):
        with self.assertRaises(KeyError):
            delete_short_url("nonexistent")

    def test_decode_existing_short_url(self):
        long_url = "https://example.com"
        short_url = create_url(long_url)
        decoded_url = decode_short_url(short_url)
        self.assertEqual(decoded_url, long_url)     

    def test_decode_nonexistent_short_url(self):
        with self.assertRaises(KeyError):
            decode_short_url("nonexistent")

    def test_get_stats_unaccessed_short_url(self):
        long_url = "https://example.com"
        short_url = create_url(long_url)
        stats = get_stats_short(short_url)
        self.assertEqual(stats, (long_url, 0))

    def test_get_stats_accessed_short_url(self):
        long_url = "https://example.com"
        short_url = create_url(long_url)
        for _ in range(4):
            decode_short_url(short_url)
        stats = get_stats_short(short_url)
        self.assertEqual(stats, (long_url, 4))
             
