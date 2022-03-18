import time, sys, random
sys.path.append('../lib/')
from smart_buffer import smart_buffer

class checker:
    def __init__(self, length_of_byte_array):
        
        self.inst = smart_buffer("buf")

        # creating a bytearray with inputted length to use as comparison
        self.var = bytearray(length_of_byte_array)

        # setting that bytearray to have random values
        self.var = self.set_rand_in_bytearray()

        # running the testing on smart_buffer
        self.testing_methods()


    # checks if the value is correct and stops the program when it is not
    def check(self, msg, answer, correct_answer):
        if answer != correct_answer:
            print(msg, end=' ')
            print("\nfailed\n\nInputted->", answer, "\nActual--->", correct_answer)
            print("Comparison array:", self.var)
            print("Instance array:", self.inst.get(0, len(self.inst))) # I trust the get method
            print("\nComparison array has length:", len(self.var))
            print("Instance array has length:", len(self.inst))
            exit(1)


    def set_rand_in_bytearray(self):
        for i in range(len(self.var)):
            self.var[i] = random.randint(0, 15)
        return self.var


    # lets the user keep up
    def wait(self):
        input("press enter to continue:")


    # goes through many different combinations of the arrays to make sure that everything works as expected
    def iterate(self, instance, original):
        for i in range(len(instance)):
            self.check("element " + str(i) + ":", instance.get(i, 1), original[i:i+1])

    '''

    Main testing method

    '''
    def testing_methods(self):
        # informs the user of the size of array being tested
        print("\n\nTesting an array with length:", len(self.var), "\n")
        
        # if the length of the variable is so that it will end up in the large buffer
        if len(self.var) > 252:
            print("In Large Buffer")
        else:
            print("In Small Buffer")

        #self.wait()

        # remembering the original bytearray
        orig_var = self.var
        
        # write method
        self.inst.write(self.var)
       
        # the len method
        print("\nchecking length")
        self.check("len:", len(self.inst), len(self.var))
        print("- passed")

        print("\nchecking write")
        # checks every element to make sure it is the same
        self.iterate(self.inst, self.var)
        print("- passed")

        # append method
        self.inst.append(b'\x08')
        # appending to the bytearray too
        self.var+=bytearray(b'\x08')
        
        # checks every element to make sure it is the same
        print("\nchecking append")
        self.iterate(self.inst, self.var)
        print("- passed")


        print("\nchecking get")
        # iterates many times and generates a random start index and a random length to use as inputts into get function
        for i in range(1000):
            start = random.randint(0, len(self.inst) - 1) # random start index
            length = random.randint(1, len(self.inst) - start) # random length
            # checking the get method against python's method for getting elements from a bytearray
            self.check("elements [" + str(start) + ":" + str(start+length) + "]:", self.inst.get(start, length),  self.var[start:start+length])

        print("- passed")


        # pop method
        print("\nchecking pop")
        
        # checks the pop method by randomly generating a start index and a length to remove and repeating this until the smart_buffer has no length
        # then reseting the smart buffer and repeating
        for i in range(100):
            self.var = orig_var # reseting the bytearray to was it first was
            self.inst.write(self.var) # setting the smart buffer "equal" to it
            while len(self.inst): # while the smart buffer has a length
                start = random.randint(0, len(self.inst) - 1) # random start index
                length = random.randint(1, len(self.inst) - start) # random length
                # using the pop method to remove elements from the smart_buffer
                self.inst.pop(start, length)
                # doing the same for the python data type
                self.var = self.var[:start] + self.var[start+length:]
                # chekcing to make sure they have the same contents
                self.iterate(self.inst, self.var)
        
        print("- passed")

        print("\nchecking clear")

        # reseting the variable
        self.var = orig_var
        self.inst.write(self.var)

        # clear method
        self.inst.clear()

        self.check("len:", len(self.inst), 0)
        print("- passed")

        print("\nchecking write_to_target")
        # opening the target file for writing bytes
        f = open("target.txt", 'wb')
        # setting the smart_buffer to the bytearray
        self.var = orig_var
        self.inst.write(self.var)

        # using the method to write to the file
        self.inst.write_to_target(f)
        f.close()
        
        # opening the target file for reading bytes
        f = open("target.txt", 'rb')
        # getting its contents to compare to later
        compare = f.read()
        f.close()
        # remember what the original byte array was
        self.var = orig_var

        # checking what the code wrote to the file versus what it should have wrote to the file
        self.check("Contents:", compare, self.var)
        print("- passed")

        print("\nchecking read_from_target")
        # opening the target file for reading bytes
        f = open("target.txt", 'rb')
        # getting its contents to compare to later
        compare = f.read()
        f.close()
        # opening the target file for reading bytes
        f = open("target.txt", 'rb')
        # using the smart_buffer method to read from the file
        self.inst.read_from_target(f)
        f.close()
        # checking that what was read is the same as what should have been read
        self.check("Contents:", compare, self.var)
        print("- passed")



for i in range(10):
    for i in range(1, 325):
        checker(i)
print("\n\npassed all\n\n")