from itertools import permutations, product

rotors = [
  "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
  "AJDKSIRUXBLHWTMCQGZNPYFVOE",
  "BDFHJLCPRTXVZNYEIWGAKMUSQO",
  "ESOVPZJAYQUIRHXLNFTGKDCMWB",
  "VZBRGITYUPSDNHLXAWMJQOFECK"
]
rotor_notches = ["Q", "E", "V", "J", "Z"]
reflector = {"A":"Y","Y":"A","B":"R","R":"B","C":"U","U":"C","D":"H","H":"D","E":"Q","Q":"E","F":"S","S":"F","G":"L","L":"G","I":"P","P":"I","J":"X","X":"J","K":"N","N":"K","M":"O","O":"M","T":"Z","Z":"T","V":"W","W":"V"}
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

rotors_in_use = [rotors[0], rotors[1], rotors[2]]

class Enigma:
  def __init__(self, rotors_in_use, ring_position, plugboard):
    self.rotors_in_use = rotors_in_use
    self.ring_position = ring_position
    self.pb_connections = plugboard.upper().split(" ")
    self.pb_dict = {}
    for pair in self.pb_connections:
      if len(pair)==2:
        self.pb_dict[pair[0]] = pair[1]
        self.pb_dict[pair[1]] = pair[0]

  def get_rotor(self, index):
    return rotors[index]

  def get_rotor_notch(self, index):
    return rotor_notches[index]

  def rotate(self, index):
    self.ring_position[index] = alphabet[
      (alphabet.index(self.ring_position[index])+1) % 26
    ]

  def rotate_and_check_next_rotate(self, index):
    flag = False
    if self.ring_position[index] == self.get_rotor_notch(index):
      flag = True
    self.rotate(index)
    return flag

  def rotor_encrypt(self, encryptedLetter, index, offset):
    pos = alphabet.index(encryptedLetter)
    char = self.get_rotor(index)[(pos+offset)%26]
    pos = alphabet.index(char)
    return alphabet[(pos-offset+26)%26]

  def rotor_encrypt_reflect(self, encryptedLetter, index, offset):
    pos = alphabet.index(encryptedLetter)
    char = alphabet[(pos+offset)%26]
    pos = self.get_rotor(index).index(char)
    return alphabet[(pos-offset+26)%26]

  def encode(self, plaintext):
    ciphertext = ""
    plaintext = plaintext.upper()
    for char in plaintext:
      encryptedLetter = char

      if char in alphabet:
        # rotate rotors
        if self.rotate_and_check_next_rotate(2): # check if need to rotate the second rotor
          if self.rotate_and_check_next_rotate(1):
            self.rotate_and_check_next_rotate(0)
        elif self.ring_position[1] == self.get_rotor_notch(1): # check double step sequence
          self.rotate(1)
          self.rotate(0)
          
        if char in self.pb_dict.keys():
          if self.pb_dict[char]!="":
            encryptedLetter = self.pb_dict[char]

        # encrypt
        offset = []
        for i in range(3):
          offset.append(alphabet.index(self.ring_position[i]))
    
        for i in range(3):
          encryptedLetter = self.rotor_encrypt(encryptedLetter, 2-i, offset[2-i])

        if encryptedLetter in reflector.keys():
          if reflector[encryptedLetter] != "" :
            encryptedLetter = reflector[encryptedLetter]
        
        for i in range(3):
          encryptedLetter = self.rotor_encrypt_reflect(encryptedLetter, i, offset[i])

        if encryptedLetter in self.pb_dict.keys():
          if self.pb_dict[encryptedLetter]!="":
            encryptedLetter = self.pb_dict[encryptedLetter]
        
      ciphertext = ciphertext + encryptedLetter
    return ciphertext

# def rejewski_analyse(ciphertext):
#     rotor_list = list(permutations([0, 1, 2], 3))
#     start_positions = list(product(alphabet, alphabet, alphabet))
    
#     for rotor_combination in rotor_list:
#       for start_position in start_positions:
#         decoded = encode()

if __name__ == "__main__":
  plaintext = input("enter text to code: ")
  rotors_in_use = [0, 1, 2]
  ring_position = ["H","D","X"]
  plugboard = ""
  enigma = Enigma(rotors_in_use, ring_position, plugboard)
  ciphertext = enigma.encode(plaintext)
  print(ciphertext)
  # rejewski_analyse("abcdf")