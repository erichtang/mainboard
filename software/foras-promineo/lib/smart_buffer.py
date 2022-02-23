"""

Author: Marek Brodke

Last Edit 12/10/2021

"""


class smart_buffer:
    def __init__(self, file_name):
        '''
        Initializes the class, the lone argument is the file that you want to use as the big/overflow buffer. 

        :param file_name: string, name of the file that you want to use as the big/overflow buffer
        
        '''
        # name of the file that will be used as the big but slower buffer
        self._buffer_file = file_name

        # secondary big buffer file, for use in operations on the main big buffer
        self._secondary_buffer_file = file_name + "__s"

        # variable that holds memory to be used as the small but faster buffer
        self.SEND_BUFF = bytearray(253)

        # setting a variable that indicates the maximum amount of bytes that can be stored in the small buffer
        self._max_len_small_buf = len(self.SEND_BUFF) - 1 # one less to retain a default value at the end of
                                                          # the small buffer so it can be reset to that value 

        # setting the small buffer to the memory allocated by the previously defined variable
        self._small_buff = memoryview(self.SEND_BUFF) # exposes python's buffer protocol
        
        # remembers the how many of the slots in the small buffer are being used to store a byte
        self._cur_size = 0

        # if data overflowed from the small buffer and is currently stored in the big buffer
        self._in_big_buf = False

        # some error messages
        self._index_error = "ERROR IN BUFFER: Invalid Index "
        self._index_type_error = "ERROR IN BUFFER: Index must be integer type"
        self._invalid_type  = "ERROR IN BUFFER: Invalid type to input into buffer"


    def read_from_target(self, target, append=False, start_condition=None, stop_condition=bytearray(1)):
        '''
        this function reads data from the target in the buffer, if start condition is provided the first bytes read from the
        target must be it otherwise this funciton will exit with False, this function returns a boolean that indicates if it
        succeeded, True it did, False if not

        :param target: an object with a method named "read" that is where you want to read data from, the read method
                        must return a byte

        :param append: a boolean that indicates if you want the read data to be appended to the buffer (True) or if you want to
                        overwrite the buffer with the read data (False)

        :param start_condition: a bytes or bytearray value that is what the "read" method from the target, must return first in order to continue

        :param stop_condition: a bytes or bytearray value that when read using the "read" method from the target stops the reading of data, this
                                has a default value of \x00 because that indicates the end of a file and it made sense to me to set it as that

        :return: a boolean that indicates if this code succeeded, False if it did not succeed and True if it did

        '''
        # if you do not want it to append to the buffer, clears it
        if not append: self.clear()
        
        # if a start condition was provided
        if start_condition is not None:
            
            return_val = b""

            # makes sure that the correct number of bytes are read, for this algorithm to work
            while len(return_val) < len(start_condition):
                data = target.read(1) # reading from the port
                if data is None:
                    return False# if port timeout, bad, returns nothing
                return_val += data
            
            # if the first thing read was not the start condition then return nothing
            if return_val != start_condition: return False
            print("return val=", return_val)
        if not isinstance(stop_condition, bytearray): stop_condition = bytearray(stop_condition)

        # holds data read from the port to compare against to see if the stop condition was returned
        stor_data = bytearray(len(stop_condition))

        # indicates whether or not the stop condition was met
        stop_condition_met = False

        fs = open(self._secondary_buffer_file, 'wb')
        #print("start data")
        while True:
            data = target.read(1) # reading a byte from the target
            # if no data was returned, bad, exits loop
            if data is None: break

            print(data)

            # converting to integer so it can be added to byte array
            data = int.from_bytes(data, 'big')

            # setting read data to the last index
            stor_data = stor_data[1:]
            stor_data.append(data)
            
            # if the last len(stop_condition) bytes are equal to the stop condition, stop condition is not recorded in memory
            if stor_data == stop_condition:
                # setting that the condition was met
                stop_condition_met = True
                # exit
                break
            
            # counting the change in size of the buffer
            self._cur_size+=1
            # writing the value in bytes to the buffer
            fs.write(data.to_bytes(1, 'big'))

        fs.close()
        #print("end data")
        # if the stop condition was encountered and the read loop was exited due to that
        if stop_condition_met:
            # if the buffer can fit in the smaller faster buffer
            if self._cur_size <= self._max_len_small_buf:
                # promoting it to the smaller buffer
                with open(self._secondary_buffer_file, 'rb') as fs:
                    for i in range(self._cur_size): self._small_buff[i] = int.from_bytes(fs.read(1), 'big')

            else: # if the buffer can not fit in the smaller buffer
                # if you do not want to append the data to the buffer
                if not append:
                    # swapping what file the data is in, faster than transfering data back to the main buffer file
                    self._buffer_file, self._secondary_buffer_file = self._secondary_buffer_file, self._buffer_file

                else: # if you want the data to be appended
                    # opening the file where the buffer data currently is
                    f = open(self._buffer_file, 'ab')
                    # opening the file where the data read was sent
                    fs = open(self._secondary_buffer_file, 'rb')

                    # addding the read data to the current buffer data
                    for i in range(self._cur_size): f.write(fs.read(1))
                    
                    # saves changes
                    fs.close()
                    f.close()

        else: # if the stop condition was not met
            # erases the secondary buffer so that there is no chance that this data will survive and cause problems later
            fs = open(self._secondary_buffer_file, 'wb')
            fs.close()

        # telling the user if stop condition was met, like an exit code, True is good, False is bad
        return stop_condition_met


    def write_to_target(self, target, clear_after_write=True):
        '''
        Writes the contents of this buffer to the inputted target

        :param target: an object with a method called "write", that represents where you want data to end up

        :param clear_after_write: if you want the buffer to be cleared after writing, True if yes and False if no, default value is yes (True)

        :return: None
        '''
        # if data is in the big buffer
        if self._in_big_buf:
            # open for reading bytes
            with open(self._buffer_file, 'rb') as f:
                # writing the data from the buffer to the target
                for i in range(self._cur_size): target.write(f.read(1))
           
        else: # if the small buffer is being used
            # writing the data from the buffer to the target in bytes form
            for i in range(self._cur_size): target.write(self._small_buff[i].to_bytes(1, 'big'))

        # if buffer should be cleared after writing, doing that
        if clear_after_write: self.clear()


    def write(self, value):
        '''
        Writes the inputted bytes or bytearray to buffer, chooses which one (small one or big one) based on conditions, so the user does
        not have to

        :param value: bytes or bytearray object to write to the buffer

        :return: None
        '''

        # if the inputted value is not a bytearray, converting it to one
        if isinstance(value, bytes): value = bytearray(value)

        # checks to make sure it is the right type, if not raises an exception
        if not isinstance(value, bytearray): raise TypeError(self._invalid_type)

        # setting the size of the buffer to the length of the inputted value
        self._cur_size = len(value)
        
        # if the inputted data is too large to add to the small buffer
        if self._cur_size > self._max_len_small_buf:
            # setting a flag that indicates that data is in the large buffer
            self._in_big_buf = True

            # opening the big buffer file and writing the data to that file
            f = open(self._buffer_file, 'wb') # open file for writing bytes
            # adding the inputted value to the big buffer
            for i in range(self._cur_size): f.write(value[i].to_bytes(1, 'big'))
            f.close() # saves the changes

        else:
            # overwriting the data in the small buffer with the new data
            for i in range(self._cur_size): self._small_buff[i] = value[i]


    def append(self, value):
        '''
        adds the inputted bytes to the end of the buffer

        :param value: bytes or bytearray object to add to the end of the buffer

        :return: None

        '''
        # if the inputted value is a bytearray, converting it to one
        if isinstance(value, bytes): value = bytearray(value)

        # checks to make sure it is the right type, if not raises an exception
        if not isinstance(value, bytearray): raise TypeError(self._invalid_type)


        # if already writing to the big buffer
        if self._in_big_buf:
            f = open(self._buffer_file, 'ab') # opening file for appending bytes

            # adding the inputted value to the big buffer
            for i in range(len(value)): f.write(value[i].to_bytes(1, 'big'))

            f.close()

        # if data is not already in big buffer
        else:
            if self._cur_size + len(value) > self._max_len_small_buf: # if adding the data would over flow the small buffer
                f = open(self._buffer_file, 'wb') # opening file for appending bytes

                # setting a flag that indicates that data is in the large buffer
                self._in_big_buf = True

                # adding the data from the small buffer to the bigger buffer
                for i in range(self._cur_size): f.write(self._small_buff[i].to_bytes(1, 'big'))

                # adding the inputted value to the big buffer
                for i in range(len(value)): f.write(value[i].to_bytes(1, 'big'))

                f.close()

            else: # not too big for the small buffer
                # goes through the inputted value and adds it to the small buffer
                for i in range(len(value)): self._small_buff[self._cur_size+i] = value[i]

        # records the change in size of the buffer
        self._cur_size+=len(value)


    def clear(self):
        '''
        clears the buffer by reseting the values that determine how data is handled, do this will cause data in the
        buffer to be over written and the rest of the data in the buffer will be essentially forgot by this class
        
        :return: None
        
        '''
        self._in_big_buf = False
        self._cur_size = 0


    def get(self, start, length=1):
        '''
        Returns the bytes number of the number of bytes specified in length from the buffer from and including the start index

        :param start: an index that represents the start of the data that you want to read from the buffer
        :param length: an int that represents the number of bytes that you want to read from the buffer

        :return: bytearray object that represents the data in the buffer from the start index with a length=length
        '''
        # checks indexing types, raises an exception if invalid
        if not isinstance(start, int) or not isinstance(length, int): raise IndexError(self._index_type_error)

        # makes sure the inputs are valid
        if start < 0 or length < 1 or start + length > self._cur_size:
            print("in get")
            raise IndexError(self._index_error)

        # if in the big buffer
        if self._in_big_buf:
            # initializes to bytearray object for memory saving
            to_return = bytearray()
            
            # open for reading bytes
            f = open(self._buffer_file, 'rb')

            for i in range(0, start+length):
                # reading a byte from the beginning of file but rememebers where the last read was, that is why the for loop starts at 0
                val = f.read(1)

                # if it is greater that the start index adding it to the list (also will be less than stop due to the for loop)
                if i >= start:
                    # convert to int so that it is compatible with byte array
                    to_return.append(int.from_bytes(val, 'big'))

            f.close() # close the file

            return bytes(to_return)
           
        else: # if the small buffer is being used
            # returning a "length" number of bytes starting at the "start" index
            return bytes(self._small_buff[start:start + length])
        

    def pop(self, start, length=1):
        '''
        Removes the a number of bytes equal to length in the buffer from and including the start index, remove
        the index in the range [start, start+index)

        :param start: an index that represents the start of the data that you want to remove from the buffer
        :param length: an int that represents the number of bytes you want to remove

        :return: None
        '''

        # checks indexing types, raises an exception if invalid
        if not isinstance(start, int) or not isinstance(length, int):
            print("in pop")
            raise IndexError(self._index_type_error)

        # makes sure the inputs are valid, raises an exception if invalid
        if start < 0 or length < 1 or start + length > self._cur_size:
            print("in pop")
            raise IndexError(self._index_error)

        if self._in_big_buf:
            # what is about to happen is that any data indexs that are not in the range [start, start+index)
            # are copied to the secondary buffer, then the secondary buffer is as the primary buffer, which is essentially poping
            # the data from the buffer. Could erase former buffer if storage is a problem, but should not be
            # opening files accordingly
            f = open(self._buffer_file, 'rb')
            fs = open(self._secondary_buffer_file, 'wb') # erases file
            for i in range(self._cur_size):
                var = f.read(1) # reads a byte from the file, must do this so we can move through the stream!!
                # reading a byte from the file if it is a valid index, adding it to the secondary file
                if i < start or i >= start + length: fs.write(var)

            # closes the files
            f.close()
            fs.close()

            # recording the change in size
            self._cur_size = self._cur_size - length

            # if the number of bytes that remain can fit in the small buffer
            if self._cur_size <= self._max_len_small_buf: # promotes the data into the small buffer
                f = open(self._secondary_buffer_file, 'rb')
                # reads a byte from the file then assigns it to a slot in the small buffer
                for i in range(self._cur_size): self._small_buff[i] = int.from_bytes(f.read(1), 'big')
                f.close()

                # data is no longer in the big buffer so remembering that
                self._in_big_buf = False

            else:
                # swapping what file the data is in, faster than transfering data back to main buffer file
                self._buffer_file, self._secondary_buffer_file = self._secondary_buffer_file, self._buffer_file

        else:
            # essentially shifts all values that were at larger indexes down erasing what needs to be erased
            #print("cur size:", self._cur_size)
            #print("start:", start)
            #print("length:", length)
            for i in range(self._cur_size-(start + length)): self._small_buff[start + i] = self._small_buff[start + length + i]

            self._cur_size-=length # subtracting the number that were removed from the number that remembers the size of the buffer


    def __len__(self):
        '''
        This is an overload of the python len() function, so you can use that function on an instance of this class
        just like you would on a string

        :return: Returns an int that represents how many bytes are in the buffer
        '''
        return self._cur_size
