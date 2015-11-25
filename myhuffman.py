import os
import marshal
import pickle
import array
import operator

class HuffmanNode(object):
    recurPrint = False
    def __init__(self, ch=None, fq=None, lnode=None, rnode=None, parent=None):
        self.L = lnode
        self.R = rnode
        self.p = parent
        self.c = ch
        self.fq = fq
        
    def __repr__(self):
        if HuffmanNode.recurPrint:
            lnode = self.L if self.L else '#'  
            rnode = self.R if self.R else '#'        
            return ''.join( ('(%s:%d)'%(self.c, self.fq), str(lnode), str(rnode) ) )
        else:
            return '(%s:%d)'%(self.c, self.fq)
    
    def __cmp__(self, other):
        if not isinstance(other, HuffmanNode):
            return super(HuffmanNode, self).__cmp__(other)
        return cmp(self.fq, other.fq)

def _pop_first_two_nodes(nodes):
    if len(nodes)>1:
        first=nodes.pop(0)
        second=nodes.pop(0)
        return first, second
    else:
        #print "[popFirstTwoNodes] nodes's length <= 1"
        return nodes[0], None
        
def _build_tree(nodes):    
    nodes.sort(key=operator.attrgetter('fq'))
    while(True):
        first, second = _pop_first_two_nodes(nodes)
        if not second:
            return first
        parent = HuffmanNode(lnode=first, rnode=second, fq=first.fq+second.fq)
        first.p = parent
        second.p = parent
        nodes.insert(0, parent)
        nodes.sort(key=operator.attrgetter('fq'))

def _gen_huffman_code(node, dict_codes, buffer_stack=[]):
    if not node.L and not node.R:
        dict_codes[node.c] = ''.join(buffer_stack)
        return
    buffer_stack.append('0')
    _gen_huffman_code(node.L, dict_codes, buffer_stack)
    buffer_stack.pop()
    
    buffer_stack.append('1')
    _gen_huffman_code(node.R, dict_codes, buffer_stack)
    buffer_stack.pop()

def _cal_freq(long_str):
    from collections import defaultdict
    d = defaultdict(int)
    for c in long_str:
        d[c] += 1
    return d

MAX_BITS = 8

class Encoder(object):
    def __init__(self, filename_or_long_str=None):
        if filename_or_long_str:
            if os.path.exists(filename_or_long_str):
                self.encode(filename_or_long_str)
            else:
                print('[Encoder] take \'%s\' as a string to be encoded.'% filename_or_long_str)
                self.long_str = filename_or_long_str

    def __get_long_str(self):
        return self._long_str
    def __set_long_str(self, s):
        self._long_str = s
        if s:
            self.root = self._get_tree_root()
            self.code_map = self._get_code_map()
            self.array_codes, self.code_length = self._encode()
            #self.array_codes, self.compress_str = self._convert()
    long_str = property(__get_long_str, __set_long_str)
    
    def _get_tree_root(self):
        d = _cal_freq(self.long_str)
        return _build_tree([HuffmanNode(ch=ch, fq=int(fq)) for ch, fq in d.items()])

    def _get_code_map(self):
        a_dict={}
        _gen_huffman_code(self.root, a_dict)
        return a_dict
        
    def _encode(self):
        array_codes = array.array('B')
        code_length = 0
        buff, length = 0, 0
        for ch in self.long_str: #long_str는 bytes이다
            code = self.code_map[ch]   #map     
            for bit in list(code):
                if bit=='1':
                    buff = (buff << 1) | 0x01 #즉 마지막에 1추가 10<<1|1 -->101
                else: # bit == '0'
                    buff = (buff << 1) #즉 마지막에 0추가 10<<1 -->100
                length += 1 #한 bit가 추가되었으므로
                if length == MAX_BITS: #8bit가 되면 arraycode에 추가
                    array_codes.extend([buff])
                    buff, length = 0, 0 #최기화

            code_length += len(code) #즉 code의 총 길이...

        #즉 array_code가 compress된 결과이다.
        if length != 0: #즉 나머지 있는 경우 즉 8로 나뭐지지 않는 경우를 array_code에 마저 붙임
            array_codes.extend([buff << (MAX_BITS-length)])
            
        return array_codes, code_length

    def _convert(self):
        compress_lst=[]
        for ch in self.long_str:
            val=0
            index=0
            code=self.code_map[ch]
            for i in list(code):
                val+=int(i)*pow(2,len(code)-1-index)
                index+=1
            compress_lst.append(val)
        compress_byte=bytes(compress_lst)
        compress_str=compress_byte.decode()
        return self.code_map,compress_str

    def encode(self, filename):
        fp = open(filename, 'rb')
        self.long_str = fp.read() #_set_long_str이 불러지고, 이를 통해 _convert가 불러진다. 그 결과 compress_str,array_codes가 set
        fp.close()
    


    #def write(self, filename):
        #if self._long_str:
            #fcompressed = open(filename, 'wb')
            #marshal.dump(
                #(pickle.dumps(self.root), self.code_length, self.array_codes),
                #fcompressed)
            #fcompressed.close()
        #else:
            #print("You haven't set 'long_str' attribute.")
    def write(self,filename=None):
        if self._long_str:
            #fcompressed=open(filename, 'w')
            #fcompressed.write(self.compress_str)
            #fcompressed.close()
            return self.com
        else:
            print("no trarget to compress")

    def get_compstr(self):
        return self.array_codes,self.code_length,self.root


class Decoder(object):
    def __init__(self,array_codes,code_length,root):
        self.array_codes=array_codes
        self.code_length=code_length
        self.root=root

    def _decode(self):
        string_buf = []
        total_length = 0    
        node = self.root
        for code in self.array_codes: #compress된 str를 하나씩 가져온다
            buf_length = 0
            while (buf_length < MAX_BITS and total_length != self.code_length):
                buf_length += 1
                total_length += 1            
                if code >> (MAX_BITS - buf_length) & 1:
                    node = node.R
                    if node.c:
                        string_buf.append(node.c)
                        node = self.root
                else:
                    node = node.L
                    if node.c:
                        string_buf.append(node.c)
                        node = self.root
        #print(string_buf)
        #string_buf는 bytes임
        ###decode 하는 방향으로
        ##일단 결과 값은 맞게 나온다...
        #return ''.join(string_buf)        
        return string_buf
    
    def read(self, filename):
        fp = open(filename, 'rb')
        unpickled_root,length,array_codes = marshal.load(fp)        
        self.root = pickle.loads(unpickled_root)
        self.code_length = length        
        self.array_codes = array.array('B', array_codes)
        fp.close()

    def decode_as(self):
        decoded = (bytes(self._decode())).decode()
        return decoded
    
