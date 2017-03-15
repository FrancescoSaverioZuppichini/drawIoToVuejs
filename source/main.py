import xmltodict
from bs4 import BeautifulSoup
import os
import sys
import re

class Node:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.components = []
        self.parent = None
        self.dependencies = []
        self.basePath = ""
        self.componentsBasePath = "./"

    def __str__(self):
        return self.value

    def render(self):
        return "to be override"


class VueNode(Node):
    def render(self):
        importString = ""
        componentsString = ""
        componentEl = ""

        for component in self.dependencies:
            # importPath = os.path.normpath(self.componentsBasePath + "/" + component.value)
            importPath = self.componentsBasePath+ os.path.normpath(findFileFromNode(self,"",component))
            # print(component.basePath)
            importString += "import %s from '%s/%s.vue'\n" % (
                component, importPath,component.value)
            componentsString += "%s," % (component)
            componentEl += "<%s/>"%("-".join(re.findall('[A-Z][a-z]*',component.value)))
            # print(componentsString)
        template = "<template><div>%s%s</div></template>\n<script>%sexport default { name: '%s', components: { %s }, }</script>\n<style></style>" % (self.value,componentEl, importString, self.value, componentsString)
        soup = BeautifulSoup(template, 'html.parser')

        return soup.prettify()

    def create(self):
        if not os.path.exists(self.basePath + '/' + self.componentsBasePath):
            os.makedirs(self.basePath + '/' + self.componentsBasePath)

        template = self.render()

        if not os.path.exists(self.basePath):
            os.makedirs(self.basePath)

        open("{}.vue".format(self.basePath + '/' + self.value), 'w').write(template)

        print("Created %s" % (self.value + '.vue'))

        for component in self.components:
            component.create()


def findFileFromNode(start,path,toFind):
    Q = []
    return findFileFromNodeInner(start,path,toFind,False,Q)

def findFileFromNodeInner(start,path,toFind,wentDown,Q):
    # check if visited
    if start in Q:
        return False
    # check is we reach the top
    if not start:
        return False
    if start.id == toFind.id:
        return path
    # append current node to visited
    Q.append(start)
    if wentDown:
        return searchInChildren(start, path, toFind, Q)
    return searchInChildren(start,path,toFind,Q) or searchInParent(start,path,toFind,Q)

def searchInParent(start,path,toFind,Q):
    return findFileFromNodeInner(start.parent, "../" + path, toFind, False,Q)

def searchInChildren(start,path,toFind,Q):
    for component in start.components:
        realPath = findFileFromNodeInner(component, path + '/' + component.value, toFind,True,Q)
        if realPath != False:
              return realPath
    return False

def createAllPathes(root,basePath):
    root.basePath = basePath
    for component in root.components:
            if component == root:
                print("circular dependency detected. Removing %s from %s" %(component,root))
                root.components.remove(component)
                continue
            else:
                newPath = os.path.join(basePath, root.componentsBasePath, component.value)
                createAllPathes(component,newPath)

def createAll(root,destinationPath):
    createAllPathes(root,destinationPath)
    root.create()

def usage():
    print("usage: python3 main.py [xmlFile] [destinationPath]")


def parse(xmlFileName):
    cache = {}
    graph = []
    with open(xmlFileName) as fd:
        doc = xmltodict.parse(fd.read())
        for cell in (doc['mxGraphModel']['root']['mxCell']):
            if not cell.get('@edge'):
                # node
                if cell.get('@value'):
                    id = cell.get("@id")
                    # remove html junk in the title
                    value = BeautifulSoup(cell.get("@value"), "lxml").text
                    # make first letter uppercase
                    value = value[0].upper() + value[1:]
                    node = VueNode(id, value)
                    cache[node.id] = node
                    graph.append(node)

        for cell in (doc['mxGraphModel']['root']['mxCell']):
            if cell.get('@edge'):
                # try to get the Node from the edge
                try:
                    source = cache[cell.get('@source')]
                    target = cache[cell.get('@target')]
                    if (cell.get('@value') == "Use"):
                        if target not in source.dependencies:
                            source.dependencies.append(target)
                    else:
                        if source not in target.components:
                            target.components.append(source)
                            source.parent = target
                except:
                    # sometimes there is some problem with the UML,
                    # we just don't care
                    pass

        del cache
        return graph


def main():
    xmlFileName = sys.argv[1]
    destinationPath = sys.argv[2]
    # xmlFileName = "./test.xml"
    #
    # destinationPath = "../"
    try:
        graph = parse(xmlFileName)
        graph[0].componentsBasePath = "./components"
        createAll(graph[0],destinationPath)
        print('done.')

    except Exception as e:
        print(e)
        usage()


main()
