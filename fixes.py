import pywikibot
from pywikibot import pagegenerators
import mwparserfromhell
import re

def search_in(page):
    x = re.search(search, page.text)
    if x is not None:
        section = x.group(1)
        object = x.group(2)
        id = x.group(3)
        return re.sub(search, "{{Images from Auckland Museum|section=" + section + "|object=" + object + "|id=" + id + "}}", page.text)
    else:
        return None

search = r"\[(?:https?:\/\/api\.aucklandmuseum\.com\/id\/)([^\/]+)\/([^\/]+)\/(\d+) Object record\]\<br\>"
site = pywikibot.Site('commons','commons')

def main():
    cat = pywikibot.Category(site, "Category:Images from Auckland Museum")
    for page in pagegenerators.CategorizedPageGenerator(cat):
        wikicode = mwparserfromhell.parse(page.text)
        for template in wikicode.filter_templates():
            if template.name == "Images from Auckland Museum":
                print("Already done")
                continue
        search_result = search_in(page)
        if search_result:
            page.text = search_result
            page.save(summary=u"Adding [[Template:Images from Auckland Museum]] and updating [[Template:Photograph]] source ([[Commons:Bots/Requests/TheSandBot 4|BRFA]])", minor=True, botflag=True, force=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
