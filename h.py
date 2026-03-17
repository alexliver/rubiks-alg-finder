import kociemba
import random

#res = kociemba.solve('DRDUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD')
#print(res)

def translate(text):
    dictionary = {
        'W': 'D',
        'G': 'R',
        'R': 'F',
        'B': 'L',
        'O': 'B',
        'Y': 'U',
    }
    res = ''
    for c in text:
        res += dictionary[c]
    return res

class Cube:
    def __init__(self, centers, corners, edges):
        self.centers = centers
        self.corners = corners
        self.edges = edges

    def print(self):
        #UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
        inds = [0,2,1,5,4,3]
        result = ''
        for ind in inds:
            result += self.print_face(ind)
        return result

    def put_edge(self, sticker1, sticker2, color1, color2):
        self.edges[sticker1[0]][sticker1[1]] = color1
        self.edges[sticker2[0]][sticker2[1]] = color2

    def put_corner(self, sticker1, sticker2, sticker3, color1, color2, color3):
        self.corners[sticker1[0]][sticker1[1]] = color1
        self.corners[sticker2[0]][sticker2[1]] = color2
        self.corners[sticker3[0]][sticker3[1]] = color3
    
    def print_face(self, ind):
        result = ''
        result += self.corners[ind][0]
        result += self.edges[ind][0]
        result += self.corners[ind][1]
        result += self.edges[ind][3]
        result += self.centers[ind]
        result += self.edges[ind][1]
        result += self.corners[ind][3]
        result += self.edges[ind][2]
        result += self.corners[ind][2]
        return result

def put_cross(cube):
    cube.put_edge([1,2], [5, 0], 'R', 'W')
    cube.put_edge([2,2], [5, 1], 'G', 'W')
    cube.put_edge([3,2], [5, 2], 'O', 'W')
    cube.put_edge([4,2], [5, 3], 'B', 'W')

def put_edges_f2l(cube):
    edges = ['RB', 'BO', 'OG', 'GR']
    slots = [
        [[1,1], [2,3]], 
        [[2,1], [3,3]], 
        [[3,1], [4,3]], 
        [[4,1], [1,3]], 
    ]
    put_edges(cube, edges, slots)

def put_edges_top(cube):
    edges = ['RY', 'BY', 'OY', 'GY']
    slots = [
        [[1,0], [0,2]], 
        [[2,0], [0,1]], 
        [[3,0], [0,0]], 
        [[4,0], [0,3]], 
    ]
    put_edges(cube, edges, slots)

def put_edges(cube, edges, slots):
    seq = get_random_seq()
    for ind, i in enumerate(seq):
        e = edges[i]
        if random.random() < 0.5:
            e = e[::-1]
        cube.put_edge(slots[ind][0], slots[ind][1], e[0], e[1])

def put_corners_f2l(cube):
    edges = ['RGW', 'GOW', 'OBW', 'BRW']
    slots = [
        [[1,2], [2,3], [5, 1]], 
        [[2,2], [3,3], [5, 2]], 
        [[3,2], [4,3], [5, 3]], 
        [[4,2], [1,3], [5, 0]], 
    ]
    put_corners(cube, edges, slots)

def put_corners_top(cube):
    edges = ['RGY', 'GOY', 'OBY', 'BRY']
    slots = [
        [[1,1], [2,0], [0, 2]], 
        [[2,1], [3,0], [0, 1]], 
        [[3,1], [4,0], [0, 0]], 
        [[4,1], [1,0], [0, 3]], 
    ]
    put_corners(cube, edges, slots)

def put_corners(cube, edges, slots):
    seq = get_random_seq()
    for ind, i in enumerate(seq):
        e = edges[i]
        if random.random() < 1/3:
            e = [e[1], e[2], e[0]]
        elif random.random() < 2/3:
            e = [e[2], e[0], e[1]]
        cube.put_corner(slots[ind][0], slots[ind][1], slots[ind][2], e[0], e[1], e[2])

def get_random_seq():
    seq = [0,1,2,3]
    random.shuffle(seq)
    return seq

def reverse_sol(res):
    l = res.split(' ')
    result = ''
    for item in l[::-1]:
        reversed1 = None
        if item.endswith('2'):
            reversed1 = item
        elif item.endswith('\''):
            reversed1 = item[0]
        else:
            reversed1 = item + "'"
        result += reversed1 + ' '
    return result

def main():
    edges = [
        list('NNNN'),
        list('NNNN'),
        list('NNNN'),
        list('NNNN'),
        list('NNNN'),
        list('NNNN'),
    ]
    corners = [
        list('NNNN'),
        list('NNNN'),
        list('NNNN'),
        list('NNNN'),
        list('NNNN'),
        list('NNNN'),
    ]
    cube = Cube('YRGOBW', corners, edges)
    put_cross(cube)
    put_edges_f2l(cube)
    put_corners_f2l(cube)

    while True:
        put_edges_top(cube)
        put_corners_top(cube)

        text = cube.print()
        n = 3
        result = "\n".join([text[i:i+n] for i in range(0, len(text), n)])

        text = translate(text)
        try:
            res = kociemba.solve(text)
            #print(result)
            #print(text)
            print(res)
            #print(reverse_sol(res))
            break
        except:
            continue
    #cube = Cube('YRGOBW',['BORB', 'YGRR', 'YYGG', 'GYOO', 'ORBB', 'WWWW'], ['BRGO', 'YRRR', 'YGGG', 'YOOO', 'YBBB', 'WWWW'])
    #text = cube.print()
    #res = kociemba.solve(translate(text))
    #print(res)

if __name__ == '__main__':
    for i in range(1):
        main()
