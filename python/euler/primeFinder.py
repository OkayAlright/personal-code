"""
primeFinder.py
----------------------------------------------------------
  Description:
    A simple prime finder to solver problem 
    7 - "10001st prime": https://projecteuler.net/problem=7

  Use:
    import into a prompt or script and init the object
    and call object.main() to start the program.
----------------------------------------------------------
References: 
    https://docs.python.org/2/
----------------------------------------------------------
  Contact: ldavis@marlboro.edu
           https://github.com/SafeCamp
           https://safecamp.github.io/



Logan Davis | 1/21/16 | Python 2.7
"""
import math
import sets

class PrimeFinder(object):

    def __init__(self):
        self.target = 0
        self.prime_count = 2
        self.lst_of_primes = [2,3]
        
    def test_Prime(self, num_to_test, lst_of_tests):
        """
         A simple, but reasonably fast prime test that returns
         true if the test was positive and false otherwise.

         Arguments = 2:
           - num_to_test: the number to test.
           - lst_of_tests: prime numbers used to test num_to_test.
        """
        for item in lst_of_tests:
            if (num_to_test % item) == 0:
                return False
            elif math.ceil(math.sqrt(num_to_test)) < item:
                return True
            else:
                continue
        return True

    def finder(self):
        """
         This method uses self.target to do one of two things:
              - smaller than self.prime_count:
                      prints the answer.
              - bigger than self.prime_count:
                      calculates to the target from the last prime
                      calculated and then prints the answer.
        """
        if self.target <= self.prime_count:
            answer = self.lst_of_primes[self.target - 1]
            print "The prime number at index {} is {}.".format(self.target,answer)
        else:
            current_num = self.lst_of_primes[-1]
            while(self.target > self.prime_count):
                current_num += 2
                if self.test_Prime(current_num, self.lst_of_primes):
                    self.lst_of_primes.append(current_num)
                    self.prime_count += 1
                else:
                    continue
            self.finder() #self.target has been calculated, recursively call this function again.

    def main(self):
        """
         A wrapper for self.finder. This method sets all the data
         needed for self.finder to calculate some wanted prime index.
         The user is than prompted if they wish to calculate another.
        """
        possible_replies = sets.Set(["y","yes","yeah","sure","uh-huh"])
        self.target = input("Enter the index of the prime number you want (as an integer): ")
        self.finder()
        restart = raw_input("Do you wish to check another (y/n)? ").lower()
        if restart in possible_replies:
            self.main()
        else:
            print "Okay, good-bye!"
            return None
ts = PrimeFinder()
ts.main()
