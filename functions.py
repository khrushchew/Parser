def check_hrefs(string):
    if "pix" not in string and "choice" not in string and "brand" not in string and "cabinet" not in string:
        return True
    else:
        return False
