"""
 LZW.py

    An implementation of LZW for the Final

|Logan Davis|5/1/15|Python 2.7|Terminal Emacs|
"""
# SOUrCES CONSULTED:
#     https://cs.marlboro.edu/courses/spring2015/algorithms/notes/Apr_30.attachments/lzw_10.py
#          used when trying to figure out how to handle the special case.
#
class LZW(object):
    """
    An API to handle the compression and decompression 
    of files using the Lepel-Ziv_welch algorithm. This is
    a memory heavy implemetation and therefore displays
    O(n) growth.
    _____________________________________________________
    >> lzw = LZW()  # creates the object instance named 'lzw'
    >> print lzw.bit_trunc
    16
    """
	
    def __init__(self, data = [], codes = [], binary = [], bit_size = 16):
        """
	The initializing values of the instance:
		data/char_stream = the file being, uncompressed
		codes/code_stream = the compressed codes for the file
		binary/binary_stream = the binary for the compressed codes
		code_book = the hash table holding character-to-code data
  		code_ref = a hashtable holding code-to-character information
		bit_size = the amount of entries that can be made into code_book  
        """
        self.char_stream = data
        self.code_stream = codes
        self.binary_stream = binary
        self.code_book = self._initCodeBook()
        self.code_ref = self._initCodeRefs()
        self.bit_size = 2**bit_size
        self.bit_trunc = bit_size

    def reset(self):
	"""
	Resets all values to their default values. 
	Call this inbetween compressions of different
	files.
	"""
        self.char_stream = ""
        self.code_stream = []
        self.binary_stream = []
        self.code_book = self._initCodeBook()
        self.code_ref = self._initCodeRefs()

    def __str__(self):
        print "Codebook/Coderefs/Binary:"
        for i in xrange(len(self.code_book)-1):
            print "| {} | {} | {} |".format(self.code_book[self.code_ref[i]],self.code_ref[i],bin(self.code_ref[i]))

    def _initCodeBook(self):
	"""
	Generates the initail code book
	(characters-to-code) to use.
	Based off the ASCII table.
        """
        code_book = {}
        for i in xrange(256):
            code_book[chr(i)] = i
        return code_book
        
    def _initCodeRefs(self):
	"""
	Generates the initial 
	code-to-charcter values
	for decompression. Based
	off the ASCII table.
	"""
        code_ref = {}
        for i in xrange(256):
            code_ref[i] = chr(i)
        return code_ref

    def compress(self):
	"""
	The compression method. It enacts, in place, on whatever is
	being held in self.char_stream. The results are written to 
	self.code_stream.
	____________________________________________________________
	>> lzw.char_stream = "TOBEORNOTTOBEORTOBEORNOT"
	>> lzw.compress()
	>> print lzw.code_stream
	[84, 79, 66, 69, 79, 82, 78, 79, 84, 256, 258, 260, 265, 259, 261, 263]
	"""
        off_set = 0
        while off_set < len(self.char_stream):
            pattern = self.char_stream[off_set]
            while pattern in self.code_book:
                off_set += 1
                try:
                    pattern += self.char_stream[off_set]
                except IndexError:
                    break
            if off_set < len(self.char_stream):
                if len(self.code_book) <= self.bit_size:
                    self.code_book[pattern] = len(self.code_book)
                self.code_stream.append(self.code_book[pattern[:-1]])
            else:
                self.code_stream.append(self.code_book[pattern])

    def decompress(self):
	"""
	Handles decompression of whatever value is stored in
	self.code_stream. This hapopens in-place.
	____________________________________________________
	>> lzw.code_stream = [84, 79, 66, 69, 79, 82, 78, 79, 84, 256, 258,
			      260, 265, 259, 261, 263]
	>> lzw.decompress()
	>> print lzw.char_stream
        'TOBEORNOTTOBEORTOBEORNOT'
	""" 
	self.code_stream
        self.char_stream = ""
        for index in xrange(len(self.code_stream)):
            pattern = self.code_ref[self.code_stream[index]]
            self.char_stream += pattern
            try:
                if self.code_stream[index+1] in self.code_ref:
                    pattern_extension = (self.code_ref[self.code_stream[index+1]])[0]
                else:
                    pattern_extension = pattern[0]
                self.code_ref[len(self.code_ref)] = pattern + pattern_extension
            except IndexError:
                continue

    def bin_conversion(self):
	"""
	Converts all values in self.code_stream in
	their binary representations. Call this 
	before calling self.write_bin()
	"""
        for code in self.code_stream:
            byte = bin(code)[2:]
            for place in xrange(self.bit_trunc - len(byte)):
                byte = '0' + byte
            self.binary_stream.append(byte)

    def load_bin(self, filename):
	"""
	Loads binary files for decompression and 
	converts them into base-10 codes.
	"""
        self.binary_stream = []
        binary_file = open(filename,'r')
        binary_string = binary_file.read()[0:-1]
        for index in xrange(self.bit_trunc,len(binary_string)+1,self.bit_trunc):
            self.binary_stream.append(binary_string[index-self.bit_trunc:index])
        binary_file.close()
	self.code_stream = []
	for code in self.binary_stream:
	    self.code_stream.append(int(code, 2))
	

    def write_bin(self, filename):	
	"""
	Writes a compressed version of the original file 
	under the name passed into the arguement 'filename'
	"""
        binary_file = open(filename,'w')
        for code in self.binary_stream:
            binary_file.write(code)
        binary_file.close()
    
    def load_text(self, filename):
	"""
	Loads text to be compressed.
	"""
        text_file = open(filename,'r')
        self.char_stream = text_file.read()
        text_file.close()
        
    def write_text(self, filename):
	"""
	Writes the uncompressed data out of the program.
	"""
        text_file = open(filename,'w')
        print self.char_stream
        text_file.write(self.char_stream)
        text_file.close()
