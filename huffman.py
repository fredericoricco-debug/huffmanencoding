from heapq import *
from bitarray import *
import json

#returns info json_file data as dict.
def get_json_1():
    with open("info.json", "r") as json_file: #Opens json file w/ read.
        data = json.load(json_file)           #Creates internal list with json data.
        return data

#returns encoding json_file data as dict.
def get_json_2():
    with open("encoding.json", "r") as json_file: #Opens json file w/ read.
        data = json.load(json_file)           #Creates internal list with json data.
        return data

#gets option.
def get_option():
    test = input("""Choose between:\n1.Compression\n2.Decompression
3.Create Custom Encoding\n4.Apply Custom Encoding
0.Exit\n""")
    #validity check
    try:
        return int(test)
    except:
        print("You did not enter an integer.")
        get_option()

#clears the screen.
def clear():
    print("\n" * 25);

#gets text data to compress.
def get_text():
    test = input("Please enter the path of your .txt file (input 'sample' for sample test).\n\n")
    if test == 'sample':
        return "Our rangers of the null postings are leaping up, high atop this fluff."
    else:
        #validity check
        try:
            with open(test, "r") as file:
                return file.read()
        except:
            clear()
            print("\nPlease enter a correct file path or 'sample'.\n")
            get_text()

#gets binary data to decompress
def get_file():
    test = input("Please enter the path of your .bin file.\n\n")
    #validity check
    try:
        temp_text = bitarray() #Creates bitmap "data structure" to store bits.
        data = get_json_1()
        list = data[test]
        with open(test, 'rb') as r:
            temp_text.fromfile(r)
        return temp_text, list
    except:
        clear()
        print("\nPlease enter a correct file path.\n")
        get_file()

#gets text data to compress.
def save_file(temp_binary):
    clear()
    filename = input("Please enter a name for your compressed file.\n\n")
    forbidden = ["#","%","&","{","}","\\","<",">","*","?","/"," ","$","!","'","\"",":","@","+","`","|", "=", "."]
    error = False
    for i in forbidden:
        for a in filename:
            if i == a:
                error = True
    if error == True:
        return "You entered a character that can't be a file name, try again."
    else:
        filename += ".bin"
        path = "/Users/admin/OneDrive - University of Exeter/CS/Data Structures and Algorithms/CA/compressed/" + filename
        try:
            with open(path, 'wb') as file:
                temp_binary.tofile(file)
            return path, filename
        except:
            clear()
            print("\nFile could not be saved, try naming it again.\n")
            save_file(temp_binary)

#creates a frequency dictionary.
def create_frequency(text):
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency

#creates a sorted heap tree and dictionary.
def create_huffman_tree(frequency):
    heap = []
    #Iterate through frequency dictionary
    #and format into list as so:
    #[frequency,[char, "blank space for binary code"]].
    for char, freq in frequency.items():
         heap.append([freq, [char, ""]])
    #Turns list to heap data structure.
    heapify(heap)
    #Until last node is reached:
    while len(heap) > 1:
        x = heappop(heap) #least frequent node x
        y = heappop(heap) #least frequent node y
        for char in x[1:]:
            char[1] = '0' + char[1] #adds a 0 for the 'right' node
        for char in y[1:]:
            char[1] = '1' + char[1] #adds a 1 for the 'left' node
        frequency_x = x[0] #frequency of child x
        frequency_y = y[0] #frequency of child y
        z = frequency_x + frequency_y #z node
        child_nodes = x[1:] + y[1:] #left and right nodes
        final = [z] + child_nodes
        heappush(heap, final) #pushes final onto heap
    #Creates a formatted list.
    list = x[1:] + y[1:]
    return list

def finalize_tree(list):
    dict = {}
    for a in list:
        dict[a[0]] = bitarray(str(a[1]))
    return dict

#compresses text.
def compress(dict, text):
    temp_text = bitarray() #Creates bitmap "data structure" to store bits.
    temp_text.encode(dict, text) #Encodes text with dict as map.
    padding = 8 - (len(temp_text) % 8) #Calculates padding for decompression.
    return temp_text, padding

#compresses a file.
def option_compress():
    clear()
    #Get text.
    text = get_text()
    clear()
    #Get frequency.
    frequency = create_frequency(text)
    #Turn frequency into a list of bitarrays.
    list = create_huffman_tree(frequency)
    #Creates a formatted dictionary with char and binary code for char.
    dict = finalize_tree(list)
    #Encode text
    temp_binary, padding = compress(dict, text)
    #Save file
    pathname, filename = save_file(temp_binary)
    #Save compression dictionary
    data = get_json_1()
    with open("info.json", 'w+') as json_file:  #Opens file w/ write, clearing file.
        data[pathname] = [list, padding]  #Changes one value in internal list.
        json.dump(data, json_file)  #Dumps old and new data to json.
    clear()
    print("Binary code: " + str(temp_binary) + "\n")
    print("Compressed and saved successfully as: " + filename + ". At: " + pathname + "\n")

#decompresses a file.
def option_decompress():
    clear()
    print("You can only decompress files that you've compressed using this program.\n")
    input("Press any key to continue...")
    temp_text, list = get_file()
    huffman = finalize_tree(list[0])
    padding = list[1]
    temp_text = temp_text[:-padding]
    temp_text = temp_text.decode(huffman)
    temp_text = ''.join(temp_text)
    clear()
    print(temp_text)

#create a huffman tree.
def arbitrary_huffman():
    clear()
    input("Use this to create an encoding that can applied to any text, as long as it shares the same characters.\nPress any key to continue...")
    clear()
    #Get text.
    text = get_text()
    clear()
    #Get frequency.
    frequency = create_frequency(text)
    #Turn frequency into a list of bitarrays.
    list = create_huffman_tree(frequency)
    #Creates a formatted dictionary with char and binary code for char.
    dict = finalize_tree(list)
    #Save compression dictionary
    data = get_json_2()
    with open("encoding.json", 'w+') as json_file:  #Opens file w/ write, clearing file.
        data["encoding"] = list  #Changes one value in internal list.
        json.dump(data, json_file)  #Dumps old and new data to json.
    clear()
    print("Created encoding. Use option 4 to compress a file using this encoding.")

#applies the encoding to a text file.
def apply_huffman():
    clear()
    #Get text.
    text = get_text()
    clear()
    #Get encoding from encoding.json file.
    data = get_json_2()
    list = data["encoding"]
    dict = finalize_tree(list)
    #Encode text
    try:
        temp_binary, padding = compress(dict, text)
    except:
        clear()
        input("The text file you tried to encode cannot be encoded with this \"tree\"\nRemeber the files must share the same charaters.")
        menu()
    #Save file
    pathname, filename = save_file(temp_binary)
    #Save compression dictionary
    data = get_json_1()
    with open("info.json", 'w+') as json_file:  #Opens file w/ write, clearing file.
        data[pathname] = [list, padding]  #Changes one value in internal list.
        json.dump(data, json_file)  #Dumps old and new data to json.
    clear()
    print("Binary code: " + str(temp_binary) + "\n")
    print("Compressed and saved successfully as: " + filename + ". At: " + pathname + "\n")

#displays menu, recursive.
def menu():
    clear()
    option = get_option()
    if option == int(1):
        option_compress()
        input("Press any key to continue...")
        menu()
    elif option == int(2):
        option_decompress()
        input("Press any key to continue...")
        menu()
    elif option == int(3):
        arbitrary_huffman()
        input("Press any key to continue...")
        menu()
    elif option == int(4):
        apply_huffman()
        input("Press any key to continue...")
        menu()
    elif option == int(0):
        clear()
        print("Thank you for using this program!")
        quit()
    else:
        print("Please enter a correct number.")
        input("Press any key to continue...")
        menu()

#Start of program.
clear()
print("\nWelcome to The Huffman Compression & Decompression Program!\nby Frederico Richardson\n")
input("Press any key to continue...")
menu()
