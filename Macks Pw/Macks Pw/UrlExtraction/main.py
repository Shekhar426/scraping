import xml.etree.ElementTree as ET


def extract_links_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define the namespace
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    # Find all 'loc' tags within the specified namespace
    loc_elements = root.findall('.//ns:loc', namespace)

    # Extract the text content from each 'loc' element
    links = [loc.text for loc in loc_elements]

    return links

# Provide the path to your XML file
file_path = 'data.xml'
links = extract_links_from_xml(file_path)

for link in links:
    with open('links.txt', 'a') as f:
        f.write(link + '\n')
