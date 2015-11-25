import math
#import base64
import hashlib
import sys
#import binascii
#from Crypto.Cipher import AES
#from Crypto import Random
import random,string
import myhuffman
import AESCipher
import array

#if os is linux this might be better

def _pad(s,size):
    return s+chr(size-len(s)%size)*(size-len(s)%size)

def _unpadd(s):
    return s[:-ord(s[len(s)-1:])]

def back(secret,n):
    num=len(secret)//n
    lst=[]
    trace=0
    for i in range(num):
        val=0
        for j in range(n):
            val+=int(secret[len(secret)-1-(i*n+j)])*pow(2,j)
            trace+=1
        lst.append(val)
    diff=len(secret)-trace
    val=0
    for i in range(diff):
        val+=int(secret[diff-1-i])*pow(2,i)
    lst.append(val)
    lst.reverse()
    return lst,diff

def to_binary(b_data_l,n,last_n): #b_data는 bytes임
        b_data=""
        for i in range(len(b_data_l)):
            temp="{0:b}".format(b_data_l[len(b_data_l)-1-i])
            if len(b_data_l)-1-i!=0:
                diff=n-len(temp)
                temp='0'*diff+temp
            else:
                diff=last_n-len(temp)
                print("in...:",str(diff))
                temp='0'*diff+temp
            b_data=temp+b_data
        return b_data


class EMD:
    def __init__(self,N,K):
        self.N=N
        self.K=K
        self.ary=2*N+1
        self.L=math.floor(self.K*math.log2(self.ary))
        self.num_lst=[]
#most recent_version
    def to_binary(self,s_data,no_secret=0):
        b_data_l=bytes(s_data,"utf-8")

        #print(b_data_l)
        b_data=""
        for i in range(len(b_data_l)):
            temp="{0:b}".format(b_data_l[i])
            if no_secret==0:
                diff=7-len(temp)
                temp='0'*diff+temp
                #self.num_lst.append(len(temp))
            b_data=b_data+temp
        #print(b_data)
        #print(self.num_lst)
        return b_data

#most recent version
    def to_string(self,s_data):#for secret,먼저 zero padding지우고 그다음 변환
        t_len=len(s_data)

        index=0
        k_len=0
        for i in self.num_lst:
            k_len+=i

        tame=0
        for x in s_data:
            if x=='0':
                if len(s_data)-tame-1<k_len:
                    break;
                tame+=1
            else:
                break
        #s_data=s_data[tame:]

        #t_len=len(s_data)
        #print("length: ",str(t_len))

        b_lst=[]
        print("index range: ",self.num_lst)
        #for i in self.num_lst:
            #val=0
            #for j in range(i):
                #val+=int(s_data[index+j])*pow(2,i-1-j)
                #print(index+j)
            #b_lst.append(val)
            #index=index+i

        b_iter=int(len(s_data)/7)
        for i in range(b_iter):
            val=0
            for j in range(7):
                val+=int(s_data[i*7+j])*pow(2,7-1-j)
            b_lst.append(val)


        b_data=bytes(b_lst) #list이므로
        print(b_data)
    #   try:
            #r_data=b_data.decode()
        #except Exception as e:
        r_data=""
        for x in b_data:
            r_data+=chr(x)
        return r_data
        #sys.exit()

    def to_string_aes(self,data):
        lst,diff=back(data,7)
        print(lst)
        r_data=(bytes(lst)).decode()
        return r_data,diff

    def to_back_aes(r_data):
        temp=bytes(r_data,"utf-8")


    def transform(self,s_data): #s_data는 binary string임
        K_ary_r=[]
        count=1
        temp=0
        idx=0
        n_digit=0
        #form_b="{0:0"+str(len(s_data)*8)+"b}"

        #bitcode=self.to_binary(s_data) #num_lst가 생성*****
        bitcode=s_data #이미 binary string임
        print("transform:",bitcode)
        #bitcode=''.join(["{0:b}".format(x) for x in binascii.a2b_base64(s_data)])
        #bitcode=''.join(["{0:b}".format(x) for x in bytes(s_data)])
        b_size=len(bitcode)

        while count*self.L<=b_size:
            temp=0
            in_L=1
            n_digit=0
            #print(str(idx)+"\n")
            for j in range(self.L):
                temp+=int(bitcode[len(bitcode)-1-idx])*pow(2,j)
                idx=idx+1
            K_ary_r.append([])
            while temp!=0 or in_L:
                in_L=0
                each_d=temp%self.ary
                temp=temp//self.ary
                K_ary_r[count-1].append(each_d)
                n_digit=n_digit+1
            if n_digit<self.K:
                for i in range(self.K-n_digit):
                    K_ary_r[count-1].append(0)
            count=count+1

        n_digit=0
        if idx<b_size:
            #print("additional\n")
            temp=0
            in_L=1
            remain_b=b_size-idx
            for j in range(remain_b):
                temp+=int(bitcode[len(bitcode)-1-idx])*pow(2,j)
                idx=idx+1
            while temp!=0 or in_L:
                in_L=0
                each_d=temp%self.ary
                temp=temp//self.ary
                K_ary_r.append([])
                K_ary_r[count-1].append(each_d)
                n_digit=n_digit+1

            if n_digit<self.K:
                for i in range(self.K-n_digit):
                    K_ary_r[count-1].append(0)

        for i in range(len(K_ary_r)):
            K_ary_r[i].reverse()
        K_ary_r.reverse()
        #print("K_ary_r:")
        #print(K_ary_r)
        return K_ary_r

    #k-ary-r을 01 string으로 back -->이후에 to_string 이루어져야 완벽한 복구
    def back(self,K_ary_r):
        m_data=""
        #k_len=len(K_ary_r) #new
        #trace=0 #new
        for lst in K_ary_r:
            val=0
            #trace+=1 #new
            for i in range(self.K):
                val+=lst[i]*pow(self.ary,self.K-1-i)
            bits_v="{0:b}".format(val)
            b_len=len(bits_v)
            #zero-padding -->맨앞의 경우 to_string시 제거된다.

            #if trace!=0: #new
            for i in range(self.L-b_len):
                bits_v=str(0)+bits_v
            m_data=m_data+bits_v

        return m_data

    def old_embedd(self,data,c_digit,seq):
        d=0
        value=0
        bitcode=''.join(["{0:b}".format(x) for x in data.encode()])

        for i in range(self.N):
            d+=int(bitcode[seq[i]])*pow(2,i)

        d=d%self.ary
        if c_digit!=d:
            s=(c_digit-d)%self.ary
            val=0
            for i in range(len(bitcode)):
                val+=int(bitcode[i])*pow(2,i)
            if s<=self.N:
                value=val+(1<<seq[s])
            else:
                value=val-(1<<seq[s])
        else:
            for i in range(len(bitcode)):
                value+=int(bitcode[i])*pow(2,i)

        r_b="{0:b}".format(value)
        return r_b

    def embedd(self,data,c_digit,seq):#data는 binary string이다.(이미 encrypt에서 to_binary거침)
        d=0
        value=0
        bitcode=data

        for i in range(self.N):
            d+=int(bitcode[len(bitcode)-1-seq[i]])*pow(2,seq[i])
        d=d%self.ary
        bits=""
        if c_digit!=d:
            form="{0:0"+str(self.N)+"b}"
            #bits=form.format(c_digit)
            for i in range(pow(2,self.N)):
                bits=form.format(i)
                val=0
                for j in range(len(bits)):
                    val+=pow(2,seq[j])*int(bits[len(bits)-1-j])
                if val%self.ary==c_digit:
                    break
                else:
                    continue
            b_lst=[]
            for i in range(len(bitcode)):
                b_lst.append(bitcode[i])
            for i in range(len(bits)):
                b_lst[len(b_lst)-1-seq[i]]=bits[len(bits)-1-i]
            bitcode=''.join(b_lst)
        return bitcode

    def old_extract(self,data,seq):
        bitcode=''.join(["{0:b}".format(x) for x in data.encode()])
        value=0
        for i in range(self.N):
            value+=int(bitcode[seq[i]])*(pow(2,i))
        value=value%self.ary
        return value

    def extract(self,data,seq): #data는 binary string이고 한 digit을 return
        value=0
        for i in range(self.N):
            value+=int(data[len(data)-1-seq[i]])*(pow(2,seq[i]))
        value=value%self.ary
        #print(value)
        return value


#RC4 START

class RC4:
    def __init__(self,S_len):
        self.S_len=S_len
        self.S=[]

    def ksa(self,key,seq=[]):
        if seq==[]:
            key_len=len(key)
            for i in range(self.S_len):
                self.S.append(i)
        else:
            key_len=len(key)
            for i in range(self.S_len):
                self.S.append(seq[i])

        j=0
        for i in range(self.S_len):
            j=(j+self.S[i]+ord(key[i%key_len]))%self.S_len
            temp=self.S[i]
            self.S[i]=self.S[j]
            self.S[j]=temp

    def prng(self,rs_len,ary,N,sub,ref_seq=[]): #if sub==1 extra check is needed
        RS=[]
        flag=[]
        count=0
        count_n=0
        i=0; j=0
        chk_lst=[]#flag substitute

        for i in range(rs_len): #ususally rs_len ==self.S_len
            flag.append(0)

        while count<rs_len:
            if count%N==0:
                count_n=0
            again=0
            i=(i+1)%self.S_len
            j=(j+self.S[j])%self.S_len
            temp=self.S[i]
            self.S[i]=self.S[j]
            self.S[j]=temp
            k=self.S[(self.S[i]+self.S[j])%self.S_len]
            if ref_seq==[]:
#                print("in")
                if flag[k]!=0:
                    continue
                if count_n!=0 and sub:
                    for i in range(count_n):
                        if pow(2,RS[count-count_n+i])%ary==pow(2,k)%ary:
                            again=1
                if again!=0:
                    continue
                flag[k]=1
                RS.append(k)
                count=count+1
                count_n=count_n+1
            else:
                if k not in chk_lst:
                   #print(k)
                    chk_lst.append(k)
                    RS.append(k)
                    count=count+1
                else:
                    continue

        return RS

class Cipher:
    def __init__(self,key_1,key_2,emd):
        self.key_1=key_1
        self.key_2=key_2
        self.secret_len=0
        self.s_seq=[]
        self.f_seq=[]
        self.emd=emd
        self.last_n=0

    def set_seq(self,f_seq,start):
        s_seq=[]
        for i in range(self.emd.N):
            s_seq.append(f_seq[start+i])
        return s_seq

    def randomize(self,S_len):
        #S_len=len(PT)*8
        #S_len=len(''.join(["{0:b}".format(x) for x in PT.encode()]))

        #S_len=len(''.join(["{0:b}".format(x) for x in bytes(PT,"utf-8")])) #******
        num_b=math.floor(S_len/self.emd.N)
        #num_b=math.floor(S_len/self.emd.L)
        #result_seq=[]

        rc4_1=RC4(S_len)
        rc4_1.ksa(self.key_1)
        self.f_seq=rc4_1.prng(rc4_1.S_len,self.emd.ary,self.emd.N,1)

        rc4_2=RC4(self.emd.N)
        for i in range(num_b):
            temp_seq=self.set_seq(self.f_seq,i*self.emd.N)
            #print(temp_seq)
            rc4_2.S=[]
            rc4_2.ksa(self.key_2,temp_seq)
            #print(rc4_2.S)
            self.s_seq.append(rc4_2.prng(rc4_2.S_len,self.emd.ary,self.emd.N,0,self.f_seq))


    def encrypt(self,secret): #secret은 binary string임
        #S_len=len(PT)
        #self.randomize(S_len)
        K_ary_r=self.emd.transform(secret)
        n_lst=0
        for i in range(len(K_ary_r)):
            if K_ary_r[i]==[]:
                n_lst=n_lst+1
            else:
                break
        K_ary_r=K_ary_r[n_lst:len(K_ary_r)]
        print(K_ary_r)

#************
        #pt_len=0
        #while pt_len<len(K_ary_r)*self.emd.K*self.emd.N:
            #PT=input("type PT")
            #pt_len=len(PT)*8

        #S_len=len(PT)
        pt_size=len(K_ary_r)*self.emd.K*self.emd.N
        PT=""
        for i in range(pt_size):
            PT+=str(random.getrandbits(1))

        #self.randomize(PT)
        self.randomize(len(PT))

        self.secret_len=len(secret)
        L_num=math.ceil(self.secret_len/self.emd.L)
        index=0

        CT=PT

        #print(CT)

        for i in range(len(K_ary_r)):
            for j in range(self.emd.K):
                CT=self.emd.embedd(CT,K_ary_r[i][j],self.s_seq[index]) #계속 s_seq에서 index error. PT가 너무 짧다..
                index=index+1

        print("1: ",CT)
        r_CT,self.last_n=self.emd.to_string_aes(CT) #이때 r_CT는 binary string이다...
        return r_CT

    def decrypt(self,CT): #CT는 binary string이다.
        kd_list=[]
        index=0
        L_num=math.ceil(self.secret_len/self.emd.L)
        for i in range(L_num):
            kd_list.append([])
            for j in range(self.emd.K):
                kd_list[i].append(self.emd.extract(CT,self.s_seq[index])) #맨앞부터 나옴
                index=index+1

        print(kd_list)
        PT=self.emd.back(kd_list)
        i=0
        while int(PT[i])==0:
            i=i+1
        PT=PT[i:]
        #f_PT=self.emd.to_string(PT)
        #return f_PT
        print("decrypt: ",PT)
        return PT #걍 binary string을 return

    def write_on(self,CT,f_out):
        try:
            fp=open(f_out,"w",encoding="utf-8" )
        except:
            print("pyAES: unable to open output file -", f_out)
            sys.exit()
        fp.write(CT)
        fp.close()

    def read_on(self,f_out):
        try:
            fp=open(f_out,"r",encoding="utf-8" )
        except:
            print("pyAES: unable to open output file -", f_out)
            sys.exit()
        line=fp.readline()
        fp.close()
        return line

    def padd_pt(self,PT): #input for aes must be a multiple of 16 in length
        b_PT=bytes(PT,encoding="utf-8")
        diff=len(b_PT)%16
        diff=16-diff
        PT="1"+PT #구분 위해서 PT앞에 무조건 1을 붙인다...즉 나중에는 첫1을 만날때까지 slice
        for i in range(diff-1):
            PT="0"+PT
        return PT

    def remove_pad_pt(self,p_PT): #remove the padd
        index=0
        for i in range(len(p_PT)):
            index=index+1
        rp_PT=p_PT[index:]
        return rp_PT

    def main(self):
        import myhuffman
        import AESCipher
        import array
        #huffman encoding
        original_file = 'F:\cipher_python\input.txt'
        enc=myhuffman.Encoder(original_file)
        c_str,c_length,root=enc.get_compstr()
        print(c_str)
        #cipher start
        N=int(input("type N: "))
        K=int(input("type K: "))
        emd=EMD(N,K)

        secret_blst=[]
        for x in c_str:
            secret_blst.append(x)

        secret=to_binary(secret_blst,8,8) #secret은 이미 binary string으로 transform

        sec_len=len(secret)
        #pt_size=math.ceil(sec_len/emd.L)*N

        pt_size=(math.ceil(sec_len/emd.L))*(emd.K)*emd.N

        print(str(pt_size)," ",str(emd.L)," ")
        key_1=input("type key_1: ")
        key_2=input("type key_2: ")

        key_1=_pad(key_1,pt_size)
        key_2=_pad(key_2,emd.N)


        #PT=Random.new().read(pt_size)
        #PT=''.join(random.choice(string.ascii_letters) for i in range(math.ceil(pt_size/8)))
        c=Cipher(key_1,key_2,emd)
        print("secret: ",secret)
        CT,last_n=c.encrypt(secret) #CT는 binary string, PT또한 binary string이다.(01010001...)

        key_3=input("type key for aes: ")
        blocksize=input("type blocksize of AES: ")

        aes=AESCipher.AESCipher(key_3,blocksize)
        aes_CT=aes.encrypt(CT)
        aes_PT=aes.decrypt(aes_CT)

        if aes_PT==CT:
            print(aes_PT)
            print("first sucess")

        #aes_PT=to_binary(bytes(aes_PT,"utf-8"),7)
        print(last_n)
        b_data=to_binary(bytes(aes_PT,"utf-8"),7,last_n)
        print("2:",b_data)
        result=c.decrypt(b_data) #binary string을 return 한다
        #result=c.decrypt(CT)

        #print(result)
        if result==secret:
            print(result)
            print("second sucesss")

        #return result

        #huffman uncompress
        c_arr,temp=back(result,8)
        tame=0
        for x in c_arr:
            if x==0:
                tame+=1
            else:
                break
        c_arr=c_arr[tame:]
        c_arr=array.array('B',c_arr)
        print(c_arr)

        dec=myhuffman.Decoder(c_arr,c_length,root)
        uc_str=dec.decode_as()

        #rev=myhuffman.Reverser(enc.code_map)
        #uncp_s=rev.reverse(result)
        #print(uncp_s)

        return uc_str

############

#def preprocess(original_file):
def preprocess(target_secret,key_1,key_2,key_3,N,K,blocksize):
        #huffman encoding
        #original_file = 'H:\cipher_python\input.txt'
        enc=myhuffman.Encoder(target_secret)
        c_str,c_length,root=enc.get_compstr()


        #N=int(input("type N: "))
        #K=int(input("type K: "))
        emd=EMD(N,K)

        secret_blst=[]
        for x in c_str:
            secret_blst.append(x)

        secret=to_binary(secret_blst,8,8) #secret은 이미 binary string으로 transform
        sec_len=len(secret)
        pt_size=(math.ceil(sec_len/emd.L))*(emd.K)*emd.N

        #key_1=input("type key_1: ")
        #key_2=input("type key_2: ")

        key_1=_pad(key_1,pt_size)
        key_2=_pad(key_2,emd.N)
        c=Cipher(key_1,key_2,emd)

        # print("secret: ",secret)
        CT=c.encrypt(secret) #CT는 binary string, PT또한 binary string이다.(01010001...)

        #key_3=input("type key for aes: ")
        #blocksize=input("type blocksize of AES: ")

        aes=AESCipher.AESCipher(key_3,blocksize)
        aes_CT=aes.encrypt(CT)

        #return key_1,key_2,key_3,aes_CT,c_length,root,blocksize,N,K,last_n,c.secret_len
        # [length of dictionary
        # dictionary
        # length whatever
        # whatever
        # aes_CT]
        return aes_CT,emd,c,aes,c_length,root #aes_CT는 byte array이다

#def reverse_preprocess(aes_CT,key_1,key_2,key_3,c_length,root,N,K,blocksize,last_n,secret_len):
def reverse_preprocess(aes_CT,emd,c,aes,c_length,root):

        #aes=AESCipher.AESCipher(key_3,blocksize)
        aes_PT=aes.decrypt(aes_CT)

        #emd=EMD(N,K)
        #c=Cipher(key_1,key_2,emd)
        b_data=to_binary(bytes(aes_PT,"utf-8"),7,c.last_n)

        c.randomize(len(b_data))
        result=c.decrypt(b_data) #binary string을 return 한다

        #huffman uncompress
        c_arr,temp=back(result,8)
        tame=0
        for x in c_arr:
            if x==0:
                tame+=1
            else:
                break
        c_arr=c_arr[tame:]
        c_arr=array.array('B',c_arr)
        dec=myhuffman.Decoder(c_arr,c_length,root)
        uc_str=dec.decode_as()

        return uc_str

def main():
    target_secret=""
    N=int(input("type N: "))
    K=int(input("type K: "))
    key_1=input("type key_1: ")
    key_2=input("type key_2: ")
    key_3=input("type key for aes: ")
    blocksize=input("type blocksize of AES: ")
    aes_CT,emd,c,aes,c_length,root=preprocess(target_secret,key_1,key_2,key_3,N,K,blocksize)
    uc_str=reverse_preprocess(aes_CT,emd,c,aes,c_length,root)
    print(uc_str)
