import heapq
import os

class codigoHuffman:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codigos = {}
        self.map_reverso = {}

    class NoHeap:
        def __init__(self, char, frequencia):
            self.char = char
            self.frequencia = frequencia
            self.esquerda = None
            self.direita = None

        # comparador de menor que (<)
        def __lt__(self, aux):
            return self.frequencia < aux.frequencia

        # comparador de igual a (==)
        def __eq__(self, aux):
            if aux == None:
                return False
            
            if not isinstance(aux, NoHeap):
                return False
            
            return self.frequencia == aux.frequencia

    # funções para compactacão do arquivo de texto
    def criarDicionarioFrequencia(self, text):
        frequencia = {}
        
        for caractere in text:
            if not caractere in frequencia:
                frequencia[caractere] = 0
            
            frequencia[caractere] += 1
        
        return frequencia

    def criarHeap(self, frequencia):
        for chave in frequencia:
            no = self.NoHeap(chave, frequencia[chave])
            heapq.heappush(self.heap, no)

    def agruparNos(self):
        while len(self.heap) > 1:
            no1 = heapq.heappop(self.heap)
            no2 = heapq.heappop(self.heap)

            agrupado = self.NoHeap(None, no1.frequencia + no2.frequencia)
            agrupado.esquerda = no1
            agrupado.direita = no2

            heapq.heappush(self.heap, agrupado)

    def criarCodigosAux(self, raiz, codigo_atual):
        if raiz == None:
            return

        if raiz.char != None:
            self.codigos[raiz.char] = codigo_atual
            self.map_reverso[codigo_atual] = raiz.char
            
            return

        self.criarCodigosAux(raiz.esquerda, codigo_atual + "0")
        self.criarCodigosAux(raiz.direita, codigo_atual + "1")

    def criarCodigos(self):
        raiz = heapq.heappop(self.heap)
        codigo_atual = ""
        self.criarCodigosAux(raiz, codigo_atual)

    def getTextoCodificado(self, text):
        texto_codificado = ""
        
        for caractere in text:
            texto_codificado += self.codigos[caractere]
            
        return texto_codificado

    def preencherTextoCodificado(self, texto_codificado):
        preenchimento = 8 - len(texto_codificado) % 8
        
        for i in range(preenchimento):
            texto_codificado += "0"

        info_preenchida = "{0:08b}".format(preenchimento)
        texto_codificado = info_preenchida + texto_codificado
        
        return texto_codificado

    def getArrayBites(self, texto_codificado_preenchido):
        if len(texto_codificado_preenchido) % 8 != 0:
            print("Texto codificado não preenchido corretamente!")
            exit(0)

        b = bytearray()
        
        for i in range(0, len(texto_codificado_preenchido), 8):
            byte = texto_codificado_preenchido[i : i + 8]
            b.append(int(byte, 2))
            
        return b

    def compactarTexto(self):
        nome_arquivo, extensao_arquivo = os.path.splitext(self.path)
        output_path = nome_arquivo + ".bin"

        with open(self.path, "r+") as file, open(output_path, "wb") as output:
            text = file.read()
            text = text.rstrip()

            frequencia = self.criarDicionarioFrequencia(text)
            self.criarHeap(frequencia)
            self.agruparNos()
            self.criarCodigos()

            texto_codificado = self.getTextoCodificado(text)
            texto_codificado_preenchido = self.preencherTextoCodificado(texto_codificado)

            b = self.getArrayBites(texto_codificado_preenchido)
            output.write(bytes(b))

        print("Arquivo de texto compactado com sucesso!")
        return output_path
    
    # funções para descompactação do arquivo binário
    def removerPreenchimento(self, texto_codificado_preenchido):
        info_preenchida = texto_codificado_preenchido[:8]
        preenchimento = int(info_preenchida, 2)

        texto_codificado_preenchido = texto_codificado_preenchido[8:]
        texto_codificado = texto_codificado_preenchido[: -1 * preenchimento]

        return texto_codificado

    def decodificarTexto(self, texto_codificado):
        codigo_atual = ""
        texto_decodificado = ""

        for bit in texto_codificado:
            codigo_atual += bit
            if codigo_atual in self.map_reverso:
                caractere = self.map_reverso[codigo_atual]
                texto_decodificado += caractere
                codigo_atual = ""

        return texto_decodificado

    def descompactarTexto(self, input_path):
        nome_arquivo, extensao_arquivo = os.path.splitext(self.path)
        output_path = nome_arquivo + "_descompactado" + ".txt"

        with open(input_path, "rb") as file, open(output_path, "w") as output:
            bit_string = ""

            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, "0")
                bit_string += bits
                byte = file.read(1)

            texto_codificado = self.removerPreenchimento(bit_string)

            descompactado_text = self.decodificarTexto(texto_codificado)

            output.write(descompactado_text)

        print("\nArquivo binário descompactado com sucesso!")
        return output_path

path = "input.txt"

h = codigoHuffman(path)

output_path = h.compactarTexto()
print("Nome do arquivo: " + output_path)

decom_path = h.descompactarTexto(output_path)
print("Nome do arquivo: " + decom_path)