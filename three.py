import logging
import sys
import copy
import arrow
logger = logging.getLogger(__name__)

T = "R U R' U' R' F R2 U' R' U' R U R' F'"
def get_face_move(dir1):
    if dir1 == 'R':
        return 'ijkl'
    if dir1 == 'L':
        return 'qrst'
    if dir1 == 'U':
        return 'abcd'
    if dir1 == 'F':
        return 'efgh'
    if dir1 == 'B':
        return 'mnop'
    if dir1 == 'D':
        return 'uvwx'
    if dir1 == 'M':
        return ''
    if dir1 == 'E':
        return ''
    if dir1 == 'S':
        return ''

def get_side_move(dir1):
    if dir1 == 'R':
        return [ "bc",  "pm","vw", "fg" ]
    if dir1 == 'L':
        return ['ad', 'eh', 'ux', 'on']
    if dir1 == 'U':
        return [ "qr", "mn", "ij",  "ef"]
    if dir1 == 'F':
        return [ "cd", "li", "uv", "rs"]
    if dir1 == 'B':
        return ['ab', 'tq', 'wx', 'jk']
    if dir1 == 'D':
        result = ['hg', 'lk', 'po', 'ts']
        #result.reverse()
        return result
    if dir1 == 'M':
        return []
    if dir1 == 'E':
        return []
    if dir1 == 'S':
        return []

def get_side_move_edges(dir1):
    if dir1 == 'R':
        return [ "b",  "p","v", "f" ]
    if dir1 == 'L':
        return ['d', 'h', 'x', 'n']
    if dir1 == 'U':
        return [ "q", "m", "i",  "e"]
    if dir1 == 'F':
        return [ "c", "l", "u", "r"]
    if dir1 == 'M':
        result = [ "ca", "mo", "wu", "ge"]
        result.reverse()
        return result
    if dir1 == 'E':
        result = [ "hf", "lj", "pn", "tr"]
        result.reverse()
        return result
    if dir1 == 'S':
        result = [ "bd", "ki", "xv", "qs"]
        #result.reverse()
        return result
    if dir1 == 'B':
        return ['a', 't', 'w', 'j']
    if dir1 == 'D':
        result = ['g', 'k', 'o', 's']
        #result.reverse()
        return result

def face_move(cube_arr, poses, prime):
    side_move(cube_arr, poses, prime)

def get_ind_from_pos(pos):
    return ord(pos) - ord('a')

def side_move(cube_arr, poses_list, prime):
    if not poses_list:
        return
    inds_list = []
    for poses in poses_list:
        inds = []
        for pos in poses:
            inds.append(get_ind_from_pos(pos))
        inds_list.append(inds)
    #if len(poses_list[0][0]) == 1:
    #print(inds_list)
    if not prime:
        inds_list.reverse()
    temp0 = get_pieces(cube_arr, inds_list[0])
    for i in range(len(poses_list) - 1):
        set_pieces(cube_arr, inds_list[i], get_pieces(cube_arr, inds_list[i+1]))
    set_pieces(cube_arr, inds_list[-1], temp0)

def set_pieces(cube_arr, inds, pieces):
    for i in range(len(inds)):
        cube_arr[inds[i]] = pieces[i]

def get_pieces(cube_arr, inds):
    result = []
    for ind in inds:
        result.append(cube_arr[ind])
    return result

def center_move(centers, prime, inds):
    if prime:
        inds.reverse()
    temp = centers[inds[0]]
    for i in range(len(inds) - 1):
        centers[inds[i]] = centers[inds[i+1]]
    centers[inds[-1]] = temp

class Cube():
    def __init__(self, corners, edges, centers):
        self.corners = list(corners)
        self.edges = list(edges)
        self.centers = list(centers)

    def move_adr(self, dir1, adr):
        if adr == '2':
            self.mover(dir1, True)
            self.mover(dir1, True)
        else:
            self.mover(dir1, adr == "'")

    def mover(self, dir1, prime):
        if dir1 == 'l':
            self.move('L', prime)
            self.move('M', prime)
        elif dir1 == 'r':
            self.move('R', prime)
            self.move('M', not prime)
        elif dir1 == 'f':
            self.move('F', prime)
            self.move('S', prime)
        elif dir1 == 'y':
            self.move('U', prime)
            self.move('E', prime)
            self.move('D', not prime)
        elif dir1 == 'x':
            self.move('R', prime)
            self.move('M', not prime)
            self.move('L', not prime)
        elif dir1 == 'z':
            self.move('F', prime)
            self.move('S', prime)
            self.move('B', not prime)
        else:
            self.move(dir1, prime)

    def move(self, dir1, prime):
        face_move(self.corners, get_face_move(dir1), prime)
        face_move(self.edges, get_face_move(dir1), prime)
        side_move(self.corners, get_side_move(dir1), prime)
        side_move(self.edges, get_side_move_edges(dir1), prime)
        if dir1 == 'M':
            inds = [0, 1, 5, 3]
            inds.reverse()
            center_move(self.centers, prime, inds)
        if dir1 == 'E':
            center_move(self.centers, prime, [1,2,3,4])
        if dir1 == 'S':
            inds = [0,2,5,4]
            inds.reverse()
            center_move(self.centers, prime, inds)

    def move_seq(self, seq):
        prev_move = None
        prev_adr = ''
        def execute():
            nonlocal prev_move
            nonlocal prev_adr
            if prev_move is None:
                return 
            #logger.info('{0}{1}'.format(prev_move, prev_adr))
            self.move_adr(prev_move, prev_adr)
            #self.print()
            prev_move = None
            prev_adr = ''
        for c in seq:
            if c == ' ':
                continue
            if c in "'2":
                if prev_adr == '':
                    prev_adr = c
            else:
                execute()
                prev_move = c
        execute()

    def print(self):
        for i in range(6):
            self.print_face(i)

    def print_face(self, i):
        start_ind = i * 4
        logger.info('{0}{1}{2}'.format(\
            self.corners[start_ind], self.edges[start_ind], self.corners[start_ind+1]))
        logger.info('{0}{1}{2}'.format(\
            self.edges[start_ind+3], self.centers[i], self.edges[start_ind+1]))
        logger.info('{0}{1}{2}'.format(\
            self.corners[start_ind+3], self.edges[start_ind+2], self.corners[start_ind+2]))
        logger.info('')

    def __eq__(self, other):
        if self.corners != other.corners:
            return False
        if self.edges != other.edges:
            return False
        if self.centers != other.centers:
            return False
        return True

    def copy(self):
        return Cube(self.corners, self.edges, self.centers)

    def set_edge(self, ind1, ind2, color):
        ind = ind1 * 4 + ind2
        self.edges[ind] = color

    def set_corner(self, ind1, ind2, color):
        ind = ind1 * 4 + ind2
        self.corners[ind] = color

    def get_face_ind(self, color):
        for i, center_color in enumerate(self.centers):
            if color == center_color:
                return i

    def get_face(self, color):
        i = self.get_face_ind(color)
        return self.get_face_from_ind(i)

    def get_face_from_ind(self, ind):
        i = ind
        return self.corners[i*4:(i+1)*4], self.edges[i*4:(i+1)*4]

class Cube2(Cube):
    def __init__(self, corners):
        super().__init__(corners, ['n']*24, ['n'] * 6)

class Cube223(Cube):
    def __init__(self, corners, edges):
        mid_edges = ''
        for ind  in range(4):
            mid_edges += 'n'
            mid_edges += edges[2*ind + 1]
            mid_edges += 'n'
            mid_edges += edges[2*ind ]
        super().__init__(corners, 'nnnn'+mid_edges + 'nnnn', ['n'] * 6)

def print_in_chunks(input_string, chunk_size):
    for i in range(0, len(input_string), chunk_size):
        logger.info(input_string[i:i + chunk_size])

def get_default_cube2():
    corners = 'yyyyrrrrggggoooobbbbwwww'
    return Cube2(corners)

def get_default_cube223():
    corners = 'yyyyrrrrggggoooobbbbwwww'
    edges = 'rrggoobb'
    return Cube223(corners, edges)

def get_default_cube():
    edges = 'yyyyrrrrggggoooobbbbwwww'
    corners = 'yyyyrrrrggggoooobbbbwwww'
    centers = 'yrgobw'
    return Cube(corners, edges, centers)

def solve_rec(init_cube, is_solved_func, allowed_moves, current_moves, perms, max_moves):
    perms += 1
    if len(current_moves) > max_moves:
        return perms
    #if perms % 100 == 0:
        #print('perms {0}'.format(perms))
    #if init_cube == target_cube:
    if is_solved_func(init_cube):
        logger.info(''.join(current_moves))
        return perms
    adrs = ['', "'", '2']
    for m in allowed_moves:
        if not can_move(current_moves, m):
            continue
        for adr in adrs:
            #if m in [ 'R', 'F', 'B', 'x', 'z', 'L']:
                #if adr != '2':
                    #continue
            new_cube = init_cube.copy()
            new_cube.move_adr(m, adr)
            new_moves = list(current_moves)
            new_moves.append('{0}{1}'.format(m, adr))
            perms = solve_rec(new_cube, is_solved_func, allowed_moves, new_moves, perms, max_moves)
    return perms

def can_move(current_moves, move):
    if len(current_moves) == 0:
        return True
    if move.lower() == current_moves[-1][0].lower():
        return False
    return True

def get_isetup():
    with open("setup.txt", "r") as file:
        lines = file.readlines()  # Reads all lines into a list
        return lines[0], lines[1].strip()

def get_algs2():
    algs = get_algs()
    result = []
    prefixes = ['', "U", "U2", "U'"]
    for alg in algs:
        for prefix in prefixes:
            result.append(prefix + alg)
    return result

def get_algs():
    with open("l.txt", "r") as file:
        lines = file.readlines()  # Reads all lines into a list
        return [line.strip() for line in lines]  # Removes newline characters

def is_face_same_rotate(l1, l2):
    for i in range(len(l1)):
        found = False
        for j in range(len(l1)):
            if l1[j] != l2[(j+i)%len(l1)]:
                found = True
        if not found:
            return True
    return False

def get_setup_cube(setups, isetup):
    cube = get_default_cube()
    cube.move_seq(setups)
    #cube.print()
    cube.move_seq(isetup)
    return cube

def is_same_colors(colors,color) :
    for c in colors:
        if c != color:
            return False
    return True

def is_solved_face(cube, face):
    face_corners, face_edges = cube.get_face(face)
    if not (is_same_colors(face_corners,face) and is_same_colors(face_edges,face)):
        return False
    return True

def is_f2l_solved_face(cube, face):
    face_corners, face_edges = cube.get_face(face)
    for start in range(4):
        found = False
        for i in range(2):
            ind = (i+2+start) % 4
            if face_corners[ind] != face:
                found=True
        for i in range(3):
            ind = (i+1+start) % 4
            if face_edges[ind] != face:
                found=True
        if not found:
            return True
    return False

def is_solved_cpll(cube):
    face_ind = cube.get_face_ind('y')
    solved_faces = ['y', 'w']
    for face in solved_faces:
        if not is_solved_face(cube, face):
            return False
    f2l_solved_faces = ['r', 'g', 'o', 'b']
    for face in f2l_solved_faces:
        if not is_f2l_solved_face(cube, face):
            return False
    face_corners, face_edges = cube.get_face('y')
    if not (is_same_colors(face_corners, 'y') and is_same_colors(face_edges, 'y')):
        return False
    face_ind_moves = "UFRBLD"
    #logger.info('face_ind {0}'.format(face_ind))
    corner_perms = get_side_move(face_ind_moves[face_ind])
    #logger.info('corner_perms {0}'.format(corner_perms))
    for corners in corner_perms:
        color1 =  cube.corners[get_ind_from_pos(corners[0])]
        color2 =  cube.corners[get_ind_from_pos(corners[1])]
        #logger.info('corners {0} color1 {1} color 2 {2}'.format(corners, color1, color2))
        if color1 != color2:
            return False
    return True

def doll2():
    setups = ['', T, T+"U'", T + "U", T + "U2", T+"U2" + T]
    #setups = ['', T, T+"U2" + T]
    isetup, check_corners  = get_isetup()
    algs = get_algs()
    dist_dict = []
    for i in range(len(setups)):
        dist_dict .append([])
    for alg in algs:
        found = False
        for i in range(len(setups)):
            cube = get_setup_cube(setups[i], isetup)
            #if i == 1:
                #cube.print()
            cube.move_seq(alg)
            #if i == 1:
                #cube.print()
            #exit()
            if is_solved_cpll(cube):
                dist_dict[i].append(alg)
                found = True
            #exit()
        if not found:
            logger.info('not found {0}'.format(alg))
    for i in range(len(setups)):
        cube = get_setup_cube(setups[i], isetup)
        logger.info(i)
        cube.print_face(cube.get_face_ind('y'))
        logger.info(print_check_corners(cube, check_corners))
        for alg in dist_dict[i]:
            logger.info(alg)
            
def print_check_corners(cube, check_corners):
    result = ''
    for c in check_corners:
        ind = get_ind_from_pos(c)
        #logger.info(ind)
        result += cube.corners[ind]
    return result

def doll():
    algs = get_algs()
    dist_dict = []
    for alg in algs:
        cube = get_default_cube()
        cube.move_seq(alg)
        #cube.print()
        corners, _ = cube.get_face('y')
        #logger.info(corners)
        found = False
        for item in dist_dict:
            if is_face_same_rotate(item[0], corners):
                item[1].append(alg)
                found = True
        if not found:
            dist_dict.append((corners, [alg]))
    for item in dist_dict:
        logger.info(item[0])
        for alg in item[1]:
            logger.info(alg)

def scramble2(cube, moves):
    cube.move_seq('x2y')
    cube.move_seq(moves)

def main(allowed_moves='RUF'):
    #test()
    #return doll2()
    '''
    cube = get_default_cube()
    cube.move_adr('B', '')
    cube.print()
    cube.move_adr('B', "'")
    cube.print()
    #cube.move_adr('R', "'")
    #cube.print()
    #cube.move_adr('U', "'")
    #cube.print()
    return
    #'''
    ''' vhls 1
    #init_cube = Cube(''.join(['nnrn', 'nwnr', 'gngn', 'nnoo', 'nnbb', 'wnww']),
                     #''.join(['nryy', 'nnrr', 'gggy', 'yooo', 'nbbb', 'wwww']),
                     #'yrgobw')
    #init_cube = Cube(''.join(['nnrn', 'nwnr', 'gngn', 'nnoo', 'nnbb', 'wnww']),
                     #''.join(['nryn', 'nyrr', 'gggn', 'yooo', 'ybbb', 'wwww']),
                     #'yrgobw')
    init_cube = Cube(''.join(['nnrn', 'nwnr', 'gngn', 'nnoo', 'nnbb', 'wnww']),
                     ''.join(['yryn', 'nnrr', 'gggy', 'nooo', 'ybbb', 'wwww']),
                     'yrgobw')
    #init_cube.move_seq("y'")
    target_cube = Cube(''.join(['nnnn', 'nnrr', 'nngg', 'nnoo', 'nnbb', 'wwww']),
                       ''.join(['yyyy', 'nrrr', 'nggg', 'nooo', 'nbbb', 'wwww']),
                       'yrgobw')
    #target_cube.move_seq("y'")
    #target_cube.move_seq("U'E'D")
    #init_cube.move_seq("U2 F R' F' R2 U2 R'")
    #init_cube.move_seq("U2 R' F R F' R U2 R'")
    #'''
    ''' vhls 1 dot
    init_cube = Cube(''.join(['nnrn', 'nwnr', 'gngn', 'nnoo', 'nnbb', 'wnww']),
                     ''.join(['nrnn', 'ynrr', 'gggy', 'yooo', 'ybbb', 'wwww']),
                     'yrgobw')
    #init_cube.move_seq("y'")
    target_cube = Cube(''.join(['nnnn', 'nnrr', 'nngg', 'nnoo', 'nnbb', 'wwww']),
                       ''.join(['yyyy', 'nrrr', 'nggg', 'nooo', 'nbbb', 'wwww']),
                       'yrgobw')
    #target_cube.move_seq("y'")
    #target_cube.move_seq("U'E'D")
    #init_cube.move_seq("U2 R' F R F' R U2 R'")
    #init_cube.move_seq("URUR2FRF'U2R'FRF'")
    #'''
    ''' intuitive
    init_cube = Cube(''.join(['nngn', 'nrnr', 'wngn', 'nnoo', 'nnbb', 'wnww']),
                     ''.join(['nngn', 'rnrr', 'nggn', 'nooo', 'nbbb', 'wwww']),
                     'yrgobw')
    target_cube = Cube(''.join(['nnnn', 'nnrr', 'nngg', 'nnoo', 'nnbb', 'wwww']),
                       ''.join(['nnnn', 'nrrr', 'nggg', 'nooo', 'nbbb', 'wwww']),
                       'yrgobw')
    #init_cube.move_seq("U' F' U F")
    #'''
    ''' vhls 2 right
    #init_cube = Cube(''.join(['nngn', 'nrnr', 'wngn', 'nnoo', 'nnbb', 'wnww']),
                     #''.join(['rynn', 'yyrr', 'nggn', 'gooo', 'ybbb', 'wwww']),
                     #'yrgobw')
    #init_cube = Cube(''.join(['nngn', 'nrnr', 'wngn', 'nnoo', 'nnbb', 'wnww']),
                     #''.join(['ryyn', 'nnrr', 'nggy', 'gooo', 'ybbb', 'wwww']),
                     #'yrgobw')
    #init_cube = Cube(''.join(['nngn', 'nrnr', 'wngn', 'nnoo', 'nnbb', 'wnww']),
                     #''.join(['rnyy', 'nnrr', 'yggy', 'gooo', 'nbbb', 'wwww']),
                     #'yrgobw')
    init_cube = Cube(''.join(['nngn', 'nrnr', 'wngn', 'nnoo', 'nnbb', 'wnww']),
                     ''.join(['rnyn', 'nyrr', 'yggn', 'gooo', 'ybbb', 'wwww']),
                     'yrgobw')
    #init_cube.move_seq("y'")
    target_cube = Cube(''.join(['nnnn', 'nnrr', 'nngg', 'nnoo', 'nnbb', 'wwww']),
                       ''.join(['yyyy', 'nrrr', 'nggg', 'nooo', 'nbbb', 'wwww']),
                       'yrgobw')
    #target_cube.move_seq("y'")
    #init_cube.move_seq("R U2 R' F' L' U' L F")
    #'''
    ''' vhls 2 middle
    init_cube = Cube(''.join(['nngn', 'nrnr', 'wngn', 'nnoo', 'nnbb', 'wnww']),
                     ''.join(['rnyn', 'nyrr', 'yggn', 'gooo', 'ybbb', 'wwww']),
                     'yrgobw')
    init_cube.move_seq("y'")
    target_cube = Cube(''.join(['nnnn', 'nnrr', 'nngg', 'nnoo', 'nnbb', 'wwww']),
                       ''.join(['yyyy', 'nrrr', 'nggg', 'nooo', 'nbbb', 'wwww']),
                       'yrgobw')
    target_cube.move_seq("y'")
    #init_cube.move_seq("R U2 R' F' L' U' L F")
    #'''
    ''' vhls 2 left
    init_cube = Cube(''.join(['nngn', 'nrnr', 'wngn', 'nnoo', 'nnbb', 'wnww']),
                     ''.join(['rnny', 'yyrr', 'yggn', 'gooo', 'nbbb', 'wwww']),
                     'yrgobw')
    #init_cube.move_seq("y'")
    target_cube = Cube(''.join(['nnnn', 'nnrr', 'nngg', 'nnoo', 'nnbb', 'wwww']),
                       ''.join(['yyyy', 'nrrr', 'nggg', 'nooo', 'nbbb', 'wwww']),
                       'yrgobw')
    #target_cube.move_seq("y'")
    #init_cube.move_seq("R U2 R' F' L' U' L F")
    #'''
    ''' vhls 2 dot
    init_cube = Cube(''.join(['nngn', 'nrnr', 'wngn', 'nnoo', 'nnbb', 'wnww']),
                     ''.join(['rnnn', 'ynrr', 'yggy', 'gooo', 'ybbb', 'wwww']),
                     'yrgobw')
    #init_cube.move_seq("y'")
    target_cube = Cube(''.join(['nnnn', 'nnrr', 'nngg', 'nnoo', 'nnbb', 'wwww']),
                       ''.join(['yyyy', 'nrrr', 'nggg', 'nooo', 'nbbb', 'wwww']),
                       'yrgobw')
    #target_cube.move_seq("y'")
    #init_cube.move_seq("R'D'rUr'DR2UR'")
    #'''
    #''' vhls lf 1
    #init_cube = Cube(''.join(['nnnr', 'wnrn', 'nngg', 'nnoo', 'nbnb', 'nwww']),
                     #''.join(['ynnr', 'yrry', 'yggg', 'nooo', 'bnbb', 'wwww']),
                     #'yrgobw')
    #init_cube = Cube(''.join(['nnnr', 'wnrn', 'nngg', 'nnoo', 'nbnb', 'nwww']),
                     #''.join(['nyyr', 'nrrn', 'nggg', 'yooo', 'bybb', 'wwww']),
                     #'yrgobw')
    #init_cube = Cube(''.join(['nnnr', 'wnrn', 'nngg', 'nnoo', 'nbnb', 'nwww']),
                     #''.join(['ynyr', 'nrrn', 'yggg', 'nooo', 'bybb', 'wwww']),
                     #'yrgobw')
    #init_cube = Cube(''.join(['nnnr', 'wnrn', 'nngg', 'nnoo', 'nbnb', 'nwww']),
                     #''.join(['nynr', 'yrry', 'nggg', 'yooo', 'bnbb', 'wwww']),
                     #'yrgobw')
    #init_cube = Cube(''.join(['nnnr', 'wnrn', 'nngg', 'nnoo', 'nbnb', 'nwww']),
                     #''.join(['yynr', 'yrrn', 'nggg', 'nooo', 'bybb', 'wwww']),
                     #'yrgobw')
    #init_cube = Cube(''.join(['nnnr', 'wnrn', 'nngg', 'nnoo', 'nbnb', 'nwww']),
                     #''.join(['nnyr', 'nrry', 'yggg', 'yooo', 'bnbb', 'wwww']),
                     #'yrgobw')
    #init_cube = Cube(''.join(['nnnr', 'wnrn', 'nngg', 'nnoo', 'nbnb', 'nwww']),
                     #''.join(['nnnr', 'yrrn', 'yggg', 'yooo', 'bybb', 'wwww']),
                     #'yrgobw')
    #init_cube.move_seq("y'")
    #target_cube = Cube(''.join(['nnnn', 'nnrr', 'nngg', 'nnoo', 'nnbb', 'wwww']),
                       #''.join(['yyyy', 'nrrr', 'nggg', 'nooo', 'nbbb', 'wwww']),
                       #'yrgobw')
    #target_cube.move_seq("y'")
    #init_cube.move_seq('y2')
    #target_cube.move_seq('y2')
    #init_cube.print()
    #init_cube.move_seq("y'FR'F2U'FURy")
    #init_cube.move_seq("y2 LUF'U'L2ULFy2")
    #init_cube.move_seq("U'FU2F'L'UL")
    #init_cube.move_seq("U2LF'L'FL'U2L")
    #init_cube.move_seq("U'L'U'LU2LF'L'F")
    #init_cube.move_seq("U2F'LFL2U2L")
    #init_cube.move_seq("U2LF'L'FU2LF'L'F")
    #init_cube.move_seq("U2Rf'U'fU2Rf'U'f")
    #init_cube.move_seq("y'")
    #'''
    ''' vhls lf2 
    #init_cube = Cube(''.join(['nnnb', 'rnrn', 'nngg', 'nnoo', 'nwnb', 'nwww']),
                     #''.join(['rnyy', 'nrrn', 'yggg', 'booo', 'nybb', 'wwww']),
                     #'yrgobw')
    #init_cube = Cube(''.join(['nnnb', 'rnrn', 'nngg', 'nnoo', 'nwnb', 'nwww']),
                     #''.join(['rynn', 'yrry', 'nggg', 'booo', 'ynbb', 'wwww']),
                     #'yrgobw')
    #init_cube = Cube(''.join(['nnnb', 'rnrn', 'nngg', 'nnoo', 'nwnb', 'nwww']),
                     #''.join(['rnny', 'yrry', 'yggg', 'booo', 'nnbb', 'wwww']),
                     #'yrgobw')
    init_cube = Cube(''.join(['nnnb', 'rnrn', 'nngg', 'nnoo', 'nwnb', 'nwww']),
                     ''.join(['ryyn', 'nrrn', 'nggg', 'booo', 'yybb', 'wwww']),
                     'yrgobw')
    #init_cube = Cube(''.join(['nnnb', 'rnrn', 'nngg', 'nnoo', 'nwnb', 'nwww']),
                     #''.join(['ryny', 'yrrn', 'nggg', 'booo', 'nybb', 'wwww']),
                     #'yrgobw')
    #init_cube = Cube(''.join(['nnnb', 'rnrn', 'nngg', 'nnoo', 'nwnb', 'nwww']),
                     #''.join(['rnyn', 'nrry', 'yggg', 'booo', 'ynbb', 'wwww']),
                     #'yrgobw')
    #init_cube = Cube(''.join(['nnnb', 'rnrn', 'nngg', 'nnoo', 'nwnb', 'nwww']),
                     #''.join(['rnnn', 'yrrn', 'yggg', 'booo', 'yybb', 'wwww']),
                     #'yrgobw')
    target_cube = Cube(''.join(['nnnn', 'nnrr', 'nngg', 'nnoo', 'nnbb', 'wwww']),
                       ''.join(['yyyy', 'nrrr', 'nggg', 'nooo', 'nbbb', 'wwww']),
                       'yrgobw')
    #init_cube.move_seq('y2')
    #target_cube.move_seq('y2')
    init_cube.print()
    #init_cube.move_seq("UFU2F'LF'L'F")
    #init_cube.move_seq("L'U'f'L'fUL")
    #init_cube.move_seq("L'ULF2l'U'lF'")
    #init_cube.move_seq("UFU2F'U'L'UL")
    #init_cube.move_seq("L'ULU2LF'L'F")
    #init_cube.move_seq("U'F'U'L'UL2FL'")
    #init_cube.move_seq("LDl'U'lD'L2U'L")
    #'''
    ''' exf2l rl lr 
    init_cube = Cube(''.join(['nnnn', 'nnrn', 'nngg', 'nnoo', 'nnnb', 'nwww']),
                     ''.join(['nnnn', 'nnrg', 'nggn', 'nooo', 'nrbb', 'wwww']),
                     'yrgobw')
    #init_cube = Cube(''.join(['nnnn', 'nnrn', 'nngg', 'nnoo', 'nnnb', 'nwww']),
                     #''.join(['nnnn', 'nnrr', 'nggn', 'nooo', 'ngbb', 'wwww']),
                     #'yrgobw')
    init_cube = Cube(''.join(['nnnn', 'nngn', 'nngw', 'nnoo', 'nnnb', 'nrww']),
                     ''.join(['nnnn', 'nnrg', 'nggn', 'nooo', 'nrbb', 'wwww']),
                     'yrgobw')
    init_cube = Cube(''.join(['nnnn', 'nngn', 'nngw', 'nnoo', 'nnnb', 'nrww']),
                     ''.join(['nnnn', 'nnrr', 'nggn', 'nooo', 'ngbb', 'wwww']),
                     'yrgobw')
    init_cube = Cube(''.join(['nnnn', 'nnng', 'nngn', 'nnoo', 'nnrb', 'wnww']),
                     ''.join(['nnnn', 'ngrn', 'nggr', 'nooo', 'nnbb', 'wwww']),
                     'yrgobw')
    init_cube = Cube(''.join(['nnnn', 'nnnr', 'nngn', 'nnoo', 'nnwb', 'gnww']),
                     ''.join(['nnnn', 'nrrn', 'nggg', 'nooo', 'nnbb', 'wwww']),
                     'yrgobw')
    init_cube = Cube(''.join(['nnnn', 'nnnw', 'nngn', 'nnoo', 'nngb', 'rnww']),
                     ''.join(['nnnn', 'nrrn', 'nggg', 'nooo', 'nnbb', 'wwww']),
                     'yrgobw')
    target_cube = Cube(''.join(['nnnn', 'nnnn', 'nngn', 'nnoo', 'nnnb', 'nnww']),
                       ''.join(['nnnn', 'nnrn', 'nggn', 'nooo', 'nnbb', 'wwww']),
                       'yrgobw')
    #'''
    init_cube = Cube(''.join(['nnnn', 'nngb', 'nnro', 'nnng', 'nnon', 'wwwn']),
                     ''.join(['nnnn', 'nnbb', 'nrrn', 'nggg', 'nooo', 'wwww']),
                     'ybrgow')
    init_cube = Cube(''.join(['nnnn', 'nnob', 'nnrw', 'nnng', 'nnon', 'wgwn']),
                     ''.join(['nnnn', 'nnbb', 'nrrn', 'nggg', 'nooo', 'wwww']),
                     'ybrgow')
    init_cube = Cube(''.join(['nnnn', 'nnwb', 'nnrg', 'nnng', 'nnon', 'wown']),
                     ''.join(['nnnn', 'nnbb', 'nrrn', 'nggg', 'nooo', 'wwww']),
                     'ybrgow')
    target_cube = Cube(''.join(['nnnn', 'nnnb', 'nnrn', 'nnng', 'nnon', 'wnwn']),
                       ''.join(['nnnn', 'nnbb', 'nrrn', 'nngg', 'noon', 'wwww']),
                       'ybrgow')
    ''' 2x2
    #init_cube = Cube2(''.join(['nnnn', 'nnbg', 'nngr', 'nnoo', 'nnrb', 'wwww']))
    init_cube = Cube2(''.join(['nnnn', 'nngr', 'nnro', 'nnog', 'nnbb', 'wwww']))
    #init_cube = Cube2(''.join(['nnnn', 'nngr', 'nnro', 'nnog', 'nnbb', 'wwww']))
    #init_cube = Cube2(''.join(['nnnn', 'nnrw', 'nngg', 'nnoo', 'nnrb', 'bwww']))
    #init_cube = Cube2(''.join(['nnnn', 'nnww', 'nngr', 'nnoo', 'nnrb', 'bgww']))
    #init_cube = Cube2(''.join(['nnnn', 'nnww', 'nngr', 'nnoo', 'nnrb', 'bgww']))
    #init_cube = get_default_cube2()
    y = "R U' R' U' R U R' F' R U R' U' R' F R"
    #init_cube.move_seq("F' R' {0} R F".format(y))
    #init_cube.move_seq("R' {0} R".format(y))
    init_cube.move_seq("y")
                     
    target_cube = Cube2(''.join(['nnnn', 'nnrr', 'nngg', 'nnoo', 'nnbb', 'wwww']))
    target_cube.move_seq("y")
    #target_cube = get_default_cube2()
    #init_cube.move_seq("L2 U' L2 U L2")
    #'''
    #'''
    
    #init_cube = get_default_cube2()
    #init_cube = get_default_cube223()
    #init_cube = Cube223(corners='yyyyrrrrggggoooobbbbwwww', edges = 'gbrgoobr')
    #init_cube = Cube223(corners='yyyyrrrrggggoooobbbbwwww', edges = 'roggrobb')
    #init_cube = Cube223(corners='yyyyrrrrggggoooobbbbwwww', edges = 'rbrgoobg')
    #init_cube = Cube223(corners='yyyyrrrrggggoooobbbbwwww', edges = 'grbgoobr')
    #init_cube.move_seq(T+ "U2" + T)
    #init_cube.move_seq("R2U2R2U2R2U2")
    #target_cube = get_default_cube223()
    #scramble2(init_cube, 'RUFRUDFUFRUD')
    #INFO:re_embeddings.three:R2U2RU'L
    #INFO:re_embeddings.three:R2U2LF'R
    #scramble2(init_cube, "RUFR'UDFUF'RUD")
    #INFO:re_embeddings.three:UR'FL2U2L'
    #INFO:re_embeddings.three:ULF2R2U'F
    #scramble2(init_cube, "RUFRU'DFU'FR'UD")
    #Generate a list of descriptive keywords (comma-separated) for a property image. Respond ONLY in English.INFO:re_embeddings.three:UR'FL2U2L'
    #INFO:re_embeddings.three:ULF2R2U'F
    #init_cube = Cube(''.join(['rrrr', 'rrbb', 'rrbb', 'rrbb', 'rrbb', 'bbbb']),
                       #''.join(['yryr', 'yrby', 'rrbr', 'yybr', 'ryby', 'bbbb']),
                       #'ryyyyb')
    #init_cube = Cube(''.join(['rrrr', 'rrbb', 'rrbb', 'rrbb', 'rrbb', 'bbbb']),
                       #''.join(['ryyr', 'yrby', 'yrbr', 'rybr', 'ryby', 'bbbb']),
                       #'ryyyyb')
    #init_cube = Cube(''.join(['rrrr', 'rrbb', 'rrbb', 'rrbb', 'rrbb', 'bbbb']),
                       #''.join(['ryyr', 'yrby', 'yybr', 'rrby', 'rybr', 'bbbb']),
                       #'ryyyyb')
    #init_cube = Cube(''.join(['rrrr', 'rrbb', 'rrbb', 'rrbb', 'rrbb', 'bbbb']),
                       #''.join(['yryr', 'yrby', 'rybr', 'yrby', 'rybr', 'bbbb']),
                       #'ryyyyb')
    #init_cube = Cube(''.join(['rrrr', 'rrbb', 'rrbb', 'rrbb', 'rrbb', 'bbbb']),
                       #''.join(['yyyr', 'yrbr', 'yrbr', 'yybr', 'rrby', 'bbbb']),
                       #'ryyyyb')
    #init_cube = Cube(''.join(['rrrr', 'rrbb', 'rrbb', 'rrbb', 'rrbb', 'bbbb']),
                       #''.join(['yyyy', 'yrbr', 'yrbr', 'yrbr', 'yrbr', 'bbbb']),
                       #'ryyyyb')
    #init_cube = Cube(''.join(['rrbr', 'rbrb', 'brbr', 'rrbb', 'rrbb', 'brbb']),
                       #''.join(['rrrr', 'ryby', 'ryby', 'ryby', 'ryby', 'bbbb']),
                       #'ryyyyb')
    #init_cube = Cube(''.join(['rrrr', 'rrbb', 'rrbb', 'rrbb', 'rrbb', 'bbbb']),
                       #''.join(['ryrr', 'rrby', 'yybr', 'ryby', 'ryby', 'bbbb']),
                       #'ryyyyb')
    #init_cube = Cube(''.join(['rrbr', 'rbrb', 'brbr', 'rrbb', 'rrbb', 'brbb']),
                       #''.join(['rryr', 'yrby', 'rybr', 'ryby', 'ryby', 'bbbb']),
                       #'ryyyyb')
    #init_cube.move_seq("y2")
    #target_cube = Cube(''.join(['rrrr', 'rrbb', 'rrbb', 'rrbb', 'rrbb', 'bbbb']),
                       #''.join(['rrrr', 'ryby', 'ryby', 'ryby', 'ryby', 'bbbb']),
                       #'ryyyyb')
    #init_cube.print()
    #'''
    '''
    T = "R U R' U' R' F R2 U' R' U' R U R' F'"
    setups = ['', T, T+"U'", T + "U", T + "U2", T+"U2" + T]
    isetup, check_corners  = get_isetup()
    init_cube = get_setup_cube(setups[1], isetup)

    init_cube.print()
    #'''
    '''
    init_cube = Cube(''.join(['yynn', 'yyrr', 'nngg', 'nnoo', 'nnbb', 'wwww']),
                       ''.join(['ynyy', 'ygrr', 'nggr', 'nooo', 'nbbb', 'wwww']),
                       'yrgobw')
    #init_cube.move_seq("y2")
    target_cube = Cube(''.join(['yyyy', 'nnrr', 'nngg', 'nnoo', 'nnbb', 'wwww']),
                       ''.join(['yyyy', 'nrrr', 'nggg', 'nooo', 'nbbb', 'wwww']),
                       'yrgobw')
    init_cube.print()
    #'''
    #void
    '''
    init_cube = Cube(''.join(['yyyy', 'oooo', 'bbbb', 'rrrr', 'gggg', 'wwww']),
                       ''.join(['yyyy', 'booo', 'obbb', 'rrrr', 'gggg', 'wwww']),
                       'nnnnnn')
    #'''
    '''
    init_cube = Cube(''.join(['yyyy', 'oooo', 'bbbb', 'rrrr', 'gggg', 'wwww']),
                       ''.join(['yyyy', 'gooo', 'obbb', 'rrrr', 'bggg', 'wwww']),
                       'nnnnnn')
    #'''
    '''
    init_cube = Cube(''.join(['yyyy', 'oooo', 'bbbb', 'rrrr', 'gggg', 'wwww']),
                       ''.join(['yyyy', 'gooo', 'rbbb', 'orrr', 'bggg', 'wwww']),
                       'nnnnnn')
    init_cube.move_seq("U2")
    #'''
    '''
    init_cube = Cube(''.join(['yyyy', 'oooo', 'bbbb', 'rrrr', 'gggg', 'wwww']),
                       ''.join(['yyyy', 'rooo', 'bbbb', 'orrr', 'gggg', 'wwww']),
                       'nnnnnn')
    #'''
    '''
    init_cube = Cube(''.join(['yyyy', 'oooo', 'bbbb', 'rrrr', 'gggg', 'wwww']),
                       ''.join(['yyyy', 'booo', 'rbbb', 'grrr', 'oggg', 'wwww']),
                       'nnnnnn')
    #'''
    '''
    init_cube = Cube(''.join(['yyyy', 'oooo', 'bbbb', 'rrrr', 'gggg', 'wwww']),
                       ''.join(['yyyy', 'gooo', 'obbb', 'brrr', 'rggg', 'wwww']),
                       'nnnnnn')
    target_cube = Cube(''.join(['yyyy', 'oooo', 'bbbb', 'rrrr', 'gggg', 'wwww']),
                       ''.join(['yyyy', 'oooo', 'bbbb', 'rrrr', 'gggg', 'wwww']),
                       'nnnnnn')
    #'''

    init_cube.print()
    target_cube.print()
    logger.info(init_cube == target_cube)
    #return
    #'''
    '''
    init_cube = Cube(''.join(['ybry', 'rwrr', 'gygy', 'ogoo', 'obbb', 'wgww']),
                     ''.join(['yryy', 'ryrr', 'gggo', 'gooo', 'bbbb', 'wwww']),
                     'yrgobw')
    target_cube = get_default_cube()
    '''
    #solve_rec(init_cube, get_is_solved_func(target_cube),allowed_moves, [], 0, 7)
    #solve_rec(init_cube, get_is_f2l_paired_func(target_cube, 'r', 'g'),allowed_moves, [], 0, 7)
    solve_rec(init_cube, get_is_f2l_paired_func(target_cube, 'o', 'g'),allowed_moves, [], 0, 7)
    #solve_rec(init_cube, is_solved_cpll,allowed_moves, [], 0, 10)
    #solve_rec(init_cube, is_solved_fl,allowed_moves, [], 0, 6)

def get_is_f2l_paired_func(target_cube, color1, color2):
    def func(init_cube):
        #R1
        new_target = target_cube.copy()
        new_target.set_corner(0,2, color1)
        new_target.set_corner(1,1, 'w')
        new_target.set_corner(2,0, color2)
        new_target.set_edge(0,1, color1)
        new_target.set_edge(2,0, color2)
        if init_cube == new_target:
            logger.info('R1')
            return True
        new_target = target_cube.copy()
        new_target.set_corner(0,2, color2)
        new_target.set_corner(1,1, 'w')
        new_target.set_corner(2,0, color1)
        new_target.set_edge(0,1, color2)
        new_target.set_edge(2,0, color1)
        if init_cube == new_target:
            logger.info('R1')
            return True
        #L1
        new_target = target_cube.copy()
        new_target.set_corner(0,3, color1)
        new_target.set_corner(1,0, 'w')
        new_target.set_corner(4,1, color2)
        new_target.set_edge(0,3, color1)
        new_target.set_edge(4,0, color2)
        if init_cube == new_target:
            logger.info('L1')
            return True
        new_target = target_cube.copy()
        new_target.set_corner(0,3, color2)
        new_target.set_corner(1,0, 'w')
        new_target.set_corner(4,1, color1)
        new_target.set_edge(0,3, color2)
        new_target.set_edge(4,0, color1)
        if init_cube == new_target:
            logger.info('L1')
            return True
        #R2
        new_target = target_cube.copy()
        new_target.set_corner(0,2, color1)
        new_target.set_corner(1,1, color2)
        new_target.set_corner(2,0, 'w')
        new_target.set_edge(0,0, color2)
        new_target.set_edge(3,0, color1)
        if init_cube == new_target:
            logger.info('R2')
            return True
        new_target = target_cube.copy()
        new_target.set_corner(0,2, color2)
        new_target.set_corner(1,1,color1)
        new_target.set_corner(2,0, 'w')
        new_target.set_edge(0,0, color1)
        new_target.set_edge(3,0, color2)
        if init_cube == new_target:
            logger.info('R2')
            return True
        #L2
        new_target = target_cube.copy()
        new_target.set_corner(0,3, color1)
        new_target.set_corner(1,0,color2)
        new_target.set_corner(4,1, 'w')
        new_target.set_edge(0,0, color2)
        new_target.set_edge(3,0, color1)
        if init_cube == new_target:
            logger.info('L2')
            return True
        new_target = target_cube.copy()
        new_target.set_corner(0,3, color2)
        new_target.set_corner(1,0,color1)
        new_target.set_corner(4,1, 'w')
        new_target.set_edge(0,0, color1)
        new_target.set_edge(3,0, color2)
        if init_cube == new_target:
            logger.info('L2')
            return True
        return False
    return func

def is_solved_fl(cube):
    corners, _ = cube.get_face_from_ind(5)
    for c in corners:
        if c != 'w':
            return False
    for i in range(1, 5):
        corners, _ = cube.get_face_from_ind(i)
        if corners[2] != corners[3]:
            return False  
    return True  
    
def get_is_solved_func(target_cube):
    def func(init_cube):
        return init_cube == target_cube
    return func

logging.basicConfig(filename='o3.txt',
                        filemode='a',
                        level=logging.INFO)



def fast_deepcopy(obj):
    if isinstance(obj, dict):
        return {k: fast_deepcopy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        if len(obj) == 0:
            return []
        if not isinstance(obj[0], dict) and not isinstance(obj[0], list):
            return obj[:]
        return [fast_deepcopy(x) for x in obj]
    else:
        return obj

def test():
    d = dict()
    for i in range(1000):
        d[i] = [0]*1000
    start = arrow.get()
    for i in range(100):
        #d = copy.deepcopy(d)
        d = fast_deepcopy(d)
        d[i][0] += 1
    print(arrow.get() - start)
    exit()

if __name__ == '__main__':
    main( sys.argv[1])
