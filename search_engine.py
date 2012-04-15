# multi_lookup will return only urls where the keywords in the query are present
# in the same order as in the query. It's an exact match only.

def multi_lookup(index, query):
  if len(query) == 0: # empty seach query retuns empyt list
    return []

  # currentPos is a list of the urls where you can find the first keyword of
  # the query so you can compare the positions of only those urls in the
  # following keywords
  currentPos = lookup(index, query[0]) 
    
  # check if the next keywords can be found in the same urls of the previous
  # one and if the position is immediatly after
  for keyword in query[1:]:
    nextPos = []
    nextUrlPos = lookup(index, keyword)
    if nextUrlPos: #only runs if lookup finds urls in the index
      for pos in currentPos:
        if [pos[0], pos[1] + 1] in nextUrlPos:
          nextPos.append([ pos[0], pos[1] + 1 ])
      currentPos = nextPos

# return only the urls without the positions
  result = []
  for url in currentPos:
    result.append(url[0])
  return result



# crawl_web will have a list of links to crawl, a list of crawled links, a
# hash graph indicating all the pages a url links to and hash index. It will return
# just the index and the graph

def crawl_web(seed): 
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph


def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def add_page_to_index(index, url, content):
    words = content.split()
    position = 0
    for word in words:
        add_to_index(index, word, url, position)
        position += 1
        
def add_to_index(index, keyword, url, position):
    if keyword in index:
        index[keyword].append([url, position])
    else:
        index[keyword] = [[url,position]]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

# to test the code without actualy crawl the web
cache = {
   'http://www.udacity.com/cs101x/final/multi.html': """<html>
<body>

<a href="http://www.udacity.com/cs101x/final/a.html">A</a><br>
<a href="http://www.udacity.com/cs101x/final/b.html">B</a><br>

</body>
""", 
   'http://www.udacity.com/cs101x/final/b.html': """<html>
<body>

Monty likes the Python programming language
Thomas Jefferson founded the University of Virginia
When Mandela was in London, he visited Nelson's Column.

</body>
</html>
""", 
   'http://www.udacity.com/cs101x/final/a.html': """<html>
<body>

Monty Python is not about a programming language
Udacity was not founded by Thomas Jefferson
Nelson Mandela said "Education is the most powerful weapon which you can
use to change the world."
</body>
</html>
""", 
}

def get_page(url):
    if url in cache:
        return cache[url]
    else:
        print "Page not in cache: " + url
        return None

index, graph = crawl_web('http://www.udacity.com/cs101x/final/multi.html')
