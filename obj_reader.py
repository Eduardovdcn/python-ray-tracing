from point import Ponto
from vector import Vetor
from color_map import Colormap
import os

class Face:
    def __init__(self):
        self.vertice_indices = [0, 0, 0]
        self.normal_indices = [0, 0, 0]
        self.ka = Vetor(0, 0, 0)
        self.kd = Vetor(0, 0, 0)
        self.ks = Vetor(0, 0, 0)
        self.ke = Vetor(0, 0, 0)
        self.ns = 0
        self.ni = 0
        self.d = 0

class ObjReader:
    '''
        Classe leitora de arquivos .obj. Onde o arquivo contém os vários pontos, normais e faces do objeto. No projeto 
        trabalhamos com faces triangulares, ou seja, uma face consiste em 3 pontos. 

        No arquivo .obj, temos:
            - v = pontos
            - vn = normais
            - vt = texturas
            - f = faces

        Nessa classe podem ser obtidas as seguintes informações:
            - Pontos
            - Normais
            - Lista de faces com seus respectivos pontos
            - Informações de cor, brilho, opacidade, etc.

        Obs: -  Para fins de abstração, as normais de cada ponto são ignoradas e assumimos apenas uma normal para cada face. 
            -  As texturas também são ignoradas.

        Caso sintam necessidade, podem editar a classe para obter mais informações.
    '''

    def __init__(self, file_path):
        self.file_path = file_path
        self.vertices = []
        self.normals = []
        self.faces = []
        self.faces_points = []
        self.cur_material = None
        self.colormap = None
        self.read_file(file_path)

    def read_file(self, file_path):
        base_dir = os.path.dirname(file_path)
        with open(file_path, 'r') as file:
            for line in file:

                if line.startswith('mtllib '):
                    file_name = line.split()[1]
                    mtl_path = os.path.join(base_dir, file_name)
                    self.colormap = Colormap(mtl_path)

                elif line.startswith('usemtl '):
                    material_name = line.split()[1]
                    self.cur_material = self.colormap.get_material(material_name)

                elif line.startswith('v '):
                    self.vertices.append(Ponto(*map(float, line[2:].split())))

                elif line.startswith('vn '):
                    pass

                elif line.startswith('f '):
                    face = Face()
                    face.vertice_indices = list(map(lambda x: int(x.split('/')[0]) - 1, line[2:].split()))
                    face.normal_indices = list(map(lambda x: int(x.split('/')[2]) - 1, line[2:].split()))
                    face.ka = self.cur_material.ka
                    face.kd = self.cur_material.kd
                    face.ks = self.cur_material.ks
                    face.ke = self.cur_material.ke
                    face.ns = self.cur_material.ns
                    face.ni = self.cur_material.ni
                    face.d = self.cur_material.d
                    self.faces.append(face)

            for face in self.faces:
                face_points = []
                for vertice_index in face.vertice_indices:
                    face_points.append(self.vertices[vertice_index])
                self.faces_points.append(face_points)

    def get_faces_points(self):
        ''' 
            Retorna uma lista com as coordenadas dos pontos das faces.
        '''
        return self.faces_points

    def get_faces(self):
        ''' 
            Retorna uma lista com as faces do objeto. Cada face contém:
                - Índices dos pontos
                - Índices das normais
                - Cores (ka, kd, ks, ke)
                - Brilho (ns)
                - Índice de refração (ni)
                - Opacidade (d)
        '''
        return self.faces

    def get_kd(self):
        '''
            Retorna a cor difusa do objeto.
        '''
        
        return self.cur_material.kd
    
    def get_ka(self):
        '''
            Retorna a cor ambiente do objeto.
        '''
        return self.cur_material.ka
    
    def get_ks(self):
        '''
            Retorna o coeficiente especular do objeto.
        '''

        return self.cur_material.ks
    
    def get_ke(self):
        '''
            Retorna a cor emissiva do objeto.
        '''
        return self.cur_material.ke
    
    def get_ns(self):
        '''
            Retorna o brilho do objeto.
        '''
        return self.cur_material.ns
    
    def get_ni(self):
        '''
            Retorna o índice de refração do objeto.
        '''
        return self.cur_material.ni
    
    def get_d(self):
        '''
            Retorna a opacidade do objeto.
        '''
        return self.cur_material.d

    def get_vertices(self):
        '''
            Retorna a lista de vértices do objeto.
        '''
        return self.vertices

    def print_faces_points(self):
        for(enum, face) in enumerate(self.faces_points):
            print(f"Face {enum}:")
            for point in face:
                print(point)
            print()

    def print_faces(self):
        for (enum, face) in enumerate(self.faces):
            print(f"Face {enum}:")
            print(f"Vertices: {face.vertice_indices}")
            print(f"Normals: {face.normal_indices}")
            print(f"Ka: {face.ka}")
            print(f"Kd: {face.kd}")
            print(f"Ks: {face.ks}")
            print(f"Ke: {face.ke}")
            print(f"Ns: {face.ns}")
            print(f"Ni: {face.ni}")
            print(f"d: {face.d}")
            print()
