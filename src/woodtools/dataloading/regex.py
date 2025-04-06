import re

def match_acer_file(filename, subid: str):
    # Pattern matches "acer_links" at the beginning followed by any characters,
    # then a number at the end
    pattern = r'^acer_' + str(subid) + r'.*?(\d+)$'
    
    match = re.match(pattern, filename)
    if match:
        # Extract the number and convert to integer
        number = int(match.group(1))
        return True, number
    else:
        return False, None
    
def match_reko_file(filename, suffix: str = ''):
    # Pattern matches "reko" at the beginning followed by any characters,
    # then a number at the end
    pattern = r'^reko' + str(suffix) + r'.*?(\d+)$'
    
    match = re.match(pattern, filename)
    if match:
        # Extract the number and convert to integer
        number = int(match.group(1))
        return True, number
    else:
        return False, None
    
    
def match_reslice_file(filename, suffix: str = ''):
    # Pattern matches "reko" at the beginning followed by any characters,
    # then a number at the end
    pattern = r'^Reslice of Reslice' + str(suffix) + r'.*?(\d+)$'
    
    match = re.match(pattern, filename)
    if match:
        # Extract the number and convert to integer
        number = int(match.group(1))
        return True, number
    else:
        return False, None