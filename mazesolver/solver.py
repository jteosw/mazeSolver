import Image
import Tkinter, ImageTk
from heapq import *

global srcX
global srcY
global destX
global destY


####### INITIAL VALUES ############################

srcfilename = 'img.jpg'
destfilename = 'Heh.jpg'
srcX = 420
srcY = 875
destX = 1582
destY = 861
debugColor = (255, 0, 0)
routeColor = (255, 255, 255)
debug = True
allowance = 5   #path-width / 2

####################################################


## Heuristic for faster searching
## Default on 5 * manhatten-distance
def heuristic(a, b):
    return 5 * (abs(a[0] - b[0]) + abs(a[1] + b[1]))

## Function to determine if a pixel passes
## Change the Wall definition to whatever color constraint
def consider(n, square):
    x = n[0]
    y = n[1]
    if x < srcX or x > destX:
        return False
# Check that there are no walls within 5 pixels
    for xx in square:
        for yy in square:
            ########## WALL DEFINITION ###############
            if pix[x+xx,y+yy][2] > 100:
                return False
    return True


root = Tkinter.Tk()
square = (-allowance, -allowance / 2,  0, allowance / 2, allowance)
im = Image.open(srcfilename);
resize = im.resize((im.size[0] / 2, im.size[1] / 2), Image.NEAREST)
tkimage = ImageTk.PhotoImage(resize)
label = Tkinter.Label(root, image=tkimage)
label.pack()
root.update()
pix = im.load()
src = (srcX, srcY)
dest = (destX, destY)
pq = []
pq2 = []
heappush(pq, (heuristic(dest, src), (0, src)))
heappush(pq2,(heuristic(src,dest), (0, dest)))
visited = set()
visited.add(src)
visited2 = set()
visited2.add(dest)
trace = dict()
count = 0
if (not consider(dest, square)):
    print "Dest does not pass condition"
    print "Choose another dest"
    exit(1)
flag = True
while (flag):
    if len(pq) == 0 or len(pq2) == 0:
        resize = im.resize((im.size[0] / 2, im.size[1] / 2), Image.NEAREST)
        tkimage = (ImageTk.PhotoImage(resize))
        label.configure(image=tkimage)
        label.image = tkimage
        root.update_idletasks()
        break
    count += 1
    if debug and count % 500 == 0:
        resize = im.resize((im.size[0] / 2, im.size[1] / 2), Image.NEAREST)
        tkimage = (ImageTk.PhotoImage(resize))
        label.configure(image=tkimage)
        label.image = tkimage
        root.update_idletasks()

    curr = heappop(pq)[1]
    dist = curr[0]
    node = curr[1]
    curr2 = heappop(pq2)[1]
    dist2 = curr2[0]
    node2 = curr2[1]
    if debug:
        pix[node] = debugColor
        pix[node2] = debugColor
    x = node[0]
    y = node[1]
    x2 = node2[0]
    y2 = node2[1]
#Boundary Condition
    for (dx,dy) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        xx = x + dx
        yy = y + dy
        if (consider((xx,yy), square)  and (xx,yy) not in visited):
            heappush(pq, (dist + heuristic((xx,yy), dest) + 1, (dist + 1, (xx, yy))))
            visited.add((xx,yy))
            if (xx,yy) in visited2:
                flag = False
                break
        xx = x2 + dx
        yy = y2 + dy
        if (consider((xx,yy), square) and (xx,yy) not in visited2):
            heappush(pq2, (dist2 + heuristic((xx,yy), src) + 1, (dist2 + 1, (xx, yy))))
            visited2.add((xx,yy))
            if (xx,yy) in visited:
                flag = False
                print (xx,yy)
                break


resize = im.resize((im.size[0] / 2, im.size[1] / 2), Image.NEAREST)
tkimage = (ImageTk.PhotoImage(resize))
label.configure(image=tkimage)
label.image = tkimage
root.update_idletasks()
allNodes = visited.union(visited2)
visited = set()
flag = True
pq = []
heappush(pq, (heuristic(src, dest), (0, src)))
while flag:
    curr = heappop(pq)[1]
    dist = curr[0]
    orig = curr[1]
    x = orig[0]
    y = orig[1]
    for (dx,dy) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        xx = x + dx
        yy = y + dy
        node = (xx, yy)

        if (node in allNodes and node not in visited):
            heappush(pq, (dist + heuristic(node,  dest) + 1, (dist + 1, node)))
            trace[node] = orig
            visited.add(node)
            if (xx,yy) == dest:
                flag = False
                break

curr = dest
while (curr != src):
    pix[curr] = routeColor
    curr = trace[curr]

resize = im.resize((im.size[0] / 2, im.size[1] / 2), Image.NEAREST)
tkimage = (ImageTk.PhotoImage(resize))
label.configure(image=tkimage)
label.image = tkimage
root.update_idletasks()
im.save(destfilename)
root.destroy()
