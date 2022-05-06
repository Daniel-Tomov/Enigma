from enigma.machine import EnigmaMachine
import enigma
import time
import itertools

#ABCDEFGHIJKLMNOPQRSTUVWXYZ - A
#EKMFLGDQVZNTOWYHXUSPAIBRCJ - I
#AJDKSIRUXBLHWTMCQGZNPYFVOE - II
#BDFHJLCPRTXVZNYEIWGAKMUSQO - III
#FVPJIAOYEDRZXWGCTKUQSBNMHL - R
#BDFHJLCPRTXVZNYEIWGAKMUSQO - III
#AJDKSIRUXBLHWTMCQGZNPYFVOE - II
#EKMFLGDQVZNTOWYHXUSPAIBRCJ - I





ciphertext = 'VVIUASDV'
rotor = ['I', 'III', 'V']
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"# input in capital format
reflector = 'C'
UKWC = 'FVPJIAOYEDRZXWGCTKUQSBNMHL' # input in capital format
rotorOne = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ' # input in capital format
rotorTwo = 'AJDKSIRUXBLHWTMCQGZNPYFVOE' # input in capital format
rotorThree = 'BDFHJLCPRTXVZNYEIWGAKMUSQO' # input in capital format
rotorFour = 'ESOVPZJAYQUIRHXLNFTGKDCMWB' # input in capital format
rotorFive = 'VZBRGITYUPSDNHLXAWMJQOFECK' # input in capital format
ring_settings = '7 25 1' # input in # # # format
windowLetters = '1 23 8' # input in # # # capital format
plugboard_settings = 'AC BI SR LM'
new_plugboard_settings = plugboard_settings
letters = ''
newLetters = []

#Extract unused letters

def rotate_rotor(rotor):
  rotor = rotor[1:26] + rotor[0:1]
  print(rotor)
  return rotor

def enigma(ciphertext, plugboard, firstRotor, secondRotor, thirdRotor, windowLetters, ringSettings, reflector):
  lowerCipher = ciphertext.lower()
  lowerplugboard = plugboard.lower()
  lowerReflector = reflector.lower()
  
  indivRingSettings = ringSettings.split(' ')
  shiftedFirstRotor = firstRotor[(int(indivRingSettings[0]) - 1):26] + firstRotor[0:int(indivRingSettings[0]) - 1]
  shiftedSecondRotor = secondRotor[(int(indivRingSettings[1]) - 1):26] + secondRotor[0:int(indivRingSettings[1]) - 1]
  shiftedThirdRotor = thirdRotor[(int(indivRingSettings[2]) - 1):26] + thirdRotor[0:int(indivRingSettings[2]) - 1]
  #print(shiftedFirstRotor)
  #print(shiftedSecondRotor)
  #print(shiftedThirdRotor)

  #shift rotors according to window letters
  indivWindowLetters = windowLetters.split(' ')
  print(indivWindowLetters)
  shiftedFirstRotor = (shiftedFirstRotor[(int(shiftedFirstRotor.find(indivWindowLetters[0]))):26] + shiftedFirstRotor[0:int(shiftedFirstRotor.find(indivWindowLetters[0]))]).lower()
  shiftedSecondRotor = (shiftedSecondRotor[(int(shiftedSecondRotor.find(indivWindowLetters[1]))):26] + shiftedSecondRotor[0:(int(shiftedSecondRotor.find(indivWindowLetters[1])))]).lower()
  shiftedThirdRotor = (shiftedThirdRotor[(int(shiftedThirdRotor.find(indivWindowLetters[2]))):26] + shiftedThirdRotor[0:(int(shiftedThirdRotor.find(indivWindowLetters[2])))]).lower()
  #print(shiftedFirstRotor)
  #print(shiftedSecondRotor)
  #print(shiftedThirdRotor)
  
  #crack each letter

  # plugboard settings
  for i in lowerCipher:
    if i in lowerplugboard:
      if ' ' in lowerplugboard[lowerplugboard.find(i) - 1:lowerplugboard.find(i)]:
        character = lowerplugboard[lowerplugboard.find(i) + 1:lowerplugboard.find(i) + 2]
      elif ' ' in lowerplugboard[lowerplugboard.find(i):lowerplugboard.find(i) + 2]:
        character = lowerplugboard[lowerplugboard.find(i) - 1:lowerplugboard.find(i)]
    #print(character)
    
    # going through rotors
    character = shiftedSecondRotor[shiftedFirstRotor.find(character):shiftedFirstRotor.find(character) + 1]
    character = shiftedThirdRotor[shiftedSecondRotor.find(character):shiftedSecondRotor.find(character) + 1]
    character = lowerReflector[shiftedThirdRotor.find(character):shiftedThirdRotor.find(character) + 1]
    character = shiftedThirdRotor[lowerReflector.find(character):lowerReflector.find(character) + 1]
    character = shiftedSecondRotor[shiftedThirdRotor.find(character):shiftedThirdRotor.find(character) + 1]
    character = shiftedFirstRotor[shiftedFirstRotor.find(character):shiftedFirstRotor.find(character) + 1]
    print(character)
    
  
  text = ''
  return text

enigma('AAAAA', ' AB CD ', rotorOne, rotorTwo, rotorThree, 'A A A', '1 2 1', UKWC)
  
for i in alphabet:
  if i not in plugboard_settings:
    letters = letters + i
print('Using the letters: ' + str(letters) + '\n')
time.sleep(1)

#Get all possible combinations
#print('All possible Combinations: ')
for c in itertools.permutations(letters):
  newLetters.append(''.join(c))
  
print(len(newLetters))

#create new plugboard

for a in newLetters:
  new_plugboard_settings = plugboard_settings
  for i in range(0, len(a)):
    #print(a[0:2] + ' ' + a[2:4])
    new_plugboard_settings = new_plugboard_settings + ' ' + a[i * 2:(i * 2) + 2]
    print(new_plugboard_settings)
    time.sleep(0.1)

    
'''#Remove duplicates
for i in newLetters:
  #print(i[0:1])
  if i[0:1] not in new_plugboard_settings:
    new_plugboard_settings = new_plugboard_settings + ' ' + i
    '''

print("Using the plugboard: ")
print(new_plugboard_settings)
  
try:
  machine = EnigmaMachine.from_key_sheet(rotors=rotor, reflector=reflector, ring_settings=ring_settings, plugboard_settings=new_plugboard_settings)
  machine.set_display('RUH')
  plaintext = machine.process_text(ciphertext)
  print(plaintext)
except enigma.plugboard.PlugboardError:
  print('ERROR: You have input more than 10 plugboard settings')