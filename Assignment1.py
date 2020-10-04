# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 12:43:47 2020

@author: ishitaverma
"""
#importing libraries
import sys #for exit function
#importing AES libraries
from cryptography.hazmat.primitives.ciphers import Cipher , algorithms, modes
from cryptography.hazmat.backends import default_backend
#for interacting with operating system
import os 
#to compute gcd
import math
#for generating random number 
import random
from sympy.ntheory.modular import crt

#defining the menu
def main():
        menu()

def menu():
    print("Please choose from the following Menu:")
    #time.sleep(3)
    print()
    
    choice = input("""
    A-Primality Test using Miller-Rabin
    B-Chinese Reminder Theorem
    C-Symmetric Encryption
    D-Exit
    
    Enter your choice: """)

    if choice == "A" or choice =="a":
       millerrabin()
    elif choice == "B" or choice =="b":
       chinesereminder()
    elif choice=="C" or choice=="c":
       symencryption()
    elif choice=="D" or choice=="d":
        sys.exit
    else:
        print("Please enter the valid choice")
        menu()

#reference for miller-rabin logic as per notes shared in class and https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/?ref=lbp
def millerrabin(): 
    #acceptng input from user
    n = int(input('Please enter a number='))
    #initializing k
    k = 0 
    #initializing q
    q = 0 
    if n > 10000:
        #checking for valid number
        print('Please enter a number less than 10000')
    else:
        #return false if n is even
        if n % 2 ==0 :
            print('Number is even. Try with different number')
        elif n == 0:
            print('Please enter number other than 0') 
        elif n == 2:
            print('Entered number is prime')
        else:
            new_n = n-1 #calculating n-1
            while (new_n!=1):
                if (new_n % 2 !=0):
                    print('Value of k = ',k,'\nValue of q =',q)
                    break
                k = k+1 #increement k
                new_n = int(new_n/2)
                q = new_n 
        #selecting a random number      
        a=random.randint(2,(n-2))
    
        print('Initial Value of a:',a)
        a = a**q #calculating the power of a
        prime=0
        if a % n == 1:
            print('Given number is prime')
        elif a % n != 1:
            j=0
            for j in range(k):
                q1 = pow(2,j)
                q2 = q1*q
                
                new_a = pow(a,q2)
                print('Iteration of j:',j,' Value of a:',new_a)
                #print('Iteration j:',j,'new_a:',new_a)
                if new_a % n == (n-1) % n: #calculating a mod n 
                    prime=1
                    break
        if prime == 1:
            print('Number is prime')
        else:
            print('Number is not prime')   
        #return
        print("Enter 'Y' to go back to menu and 'E' to exit")
        user_input= input("Enter your choice as 'Y' or 'E': ")
        if user_input == "Y":
                 menu()
        elif user_input == "E":
                 exit()
    
#Reference for crt function and chinese theorem logic https://www.geeksforgeeks.org/python-sympy-crt-method/ 
def chinesereminder():
    #accepting positive integer a,b,c and r,s,t from user
    print("Enter the values for  divisors A,B,C and remainders R,S,T:-")
    a=input('A:')
    b=input('B:')
    c=input('C:')
    r=input('R:')
    s=input('S:')
    t=input('T:')
    
    a=int(a)
    b=int(b)
    c=int(c)
    r=int(r)
    s=int(s)
    t=int(t)
    
    if r > 0 and s > 0 and t > 0 and a > 0 and b > 0 and c > 0:
        #checking for pairwaise relatively prime integers
        if math.gcd(r, s) ==1 and math.gcd(s, t) == 1 and math.gcd(r,t) == 1:
            x = [r,s,t]
            y = [a,b,c] 
            final_value = crt(x,y) #crt
            print("Result of the Chinese Remainder Theorem = {} ".format(final_value[0])) 
        else:
            print("Something went wrong. Please enter the input again")
    #return
    print("Enter 'Y' to go back to menu and 'E' to exit")
    user_input= input("Enter your choice as 'Y' or 'E': ")
    if user_input == "Y":
                     menu()
    elif user_input == "E":
                     exit()

    
def symencryption():
    print("You have chosen Symmetric Encryption")
    print("Plase choose the type of encryption: ")
    user_input = input("Type 'AES' or '3DES' to proceed: \n ")
    if user_input == "AES":
        AES()
    elif user_input == "3DES":
        triple_DES()
    else :
        print("Please enter the correct choice")

#reference used:https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/
#reference used: https://medium.com/quick-code/aes-implementation-in-python-
#refernce used: https://cryptography.io/en/latest/hazmat/backends/interfaces/        
#defining the AES function and generating the key for encryption/decryption
#AES is one of the symmetric blockciphers in which a block of 128 (16*8) bits is encrypted 
def AES():
     block_size = 16 #AES uses fixed block sizes 
     #padding for encryption to ensure plain text is multiple of 16
     pad = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)
     unpad = lambda s : s[:-ord(s[len(s)-1:])]  #to unpad after decryption
     plain_text = str(input("Enter the plaintext to be encrypted: \n"))
     plain_text = pad((plain_text)) #padding plaintext
     #bytes conversion as input to encryption process must be binary data
     plain_text2 = bytes(plain_text, 'utf-8')
     backend = default_backend() #backend interfaces support symmetric encryption
     key = os.urandom(32) #32 bytes key 
     iv = os.urandom(16) # intializing vector with length=16 used with secret key
     #utilizing CBC
     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend = backend) 
     encryptor = cipher.encryptor()
     ct = encryptor.update(plain_text2) + encryptor.finalize()
     print("Key: \n" + str(key)) #derived key
     print("Text after encryption: \n"+ str(ct)) #encrypted text after key
     decryptor = cipher.decryptor() 
     decrypt = decryptor.update(ct) + decryptor.finalize()
     decrypt = unpad(decrypt) #unpadding after decryption
     print("Plain text after decryption: \n"+ str(decrypt)) #decrypted text
     print("Do you want to proceed with encryption?")
     user_input= input("Enter your choice as 'Yes' or 'No': ")
     if user_input == "Yes":
         symencryption()
     elif user_input == "No":
         exit()

#In 3DES it comprises of 3 single DES ciphers; Encryption-Decryption-Encryption
#Step-1: Plaintext is encrypted with DES with Key-1
#Step-2: Encrypted text in Step-1 is decrypted withsingle DES Key-2
#Step-3: The output of Step-2 is encrypted with Key-3 and the ciphertext is obtained
#Reference:https://legrandin.github.io/pycryptodome/Doc/3.4.6/Crypto.Cipher.DES3-module.html
def triple_DES(): 
    block_size = 16 #fixed block size of 16 bytes
    #padding
    pad = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)
    unpad = lambda s : s[:-ord(s[len(s)-1:])] #unpad after decryption
    plain_text = str(input("Enter the plaintext to be encrypted: \n"))
    plain_text = pad((plain_text)) #padding the text
    #bytes conversion as input to encryption process must be binary data
    plain_text2 = bytes(plain_text, 'utf-8')
    backend = default_backend() #backend interfaces support symmetric encryption
    key = os.urandom(24)  #24 bytes key
    iv = os.urandom(8) #TDES vector initializtion length=8 used along with secret key
    #utilizing Cipher Feedback(CFB)
    cipher = Cipher(algorithms.TripleDES(key), modes.CFB(iv), backend = backend)
    encryptor = cipher.encryptor()
    ct = encryptor.update(plain_text2) + encryptor.finalize()
    decryptor = cipher.decryptor()
    decrypt = decryptor.update(ct) + decryptor.finalize()
    decrypt = unpad(decrypt) #unpad the text after decryption
    print("Key: \n" + str(key)) #drived key
    print("Text after Encryption: \n"+ str(ct)) #encrypted text
    print("Text after Decryption \n"+ str(decrypt)) #decrypted text
    print("Do you want to proceed with encryption?")
    user_input= input("Enter your choice as 'Yes' or 'No': ")
    if user_input == "Yes":
        symencryption()
    elif user_input == "No":
         exit()

def exit():
    print("See you!")   
    
main()

