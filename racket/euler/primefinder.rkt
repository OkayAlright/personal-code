#lang racket
#|
primefinder.rkt 
----------------------------------------------------------
  Description:
    A simple prime finder to solver problem 
    7 - "10001st prime": https://projecteuler.net/problem=7
  Use:
    import or run a promt with these definitions and call
    (main).
----------------------------------------------------------
References: 
    https://docs.racket-lang.org/
    https://learnxinyminutes.com/docs/racket/
----------------------------------------------------------
  Contact: ldavis@marlboro.edu
           https://github.com/SafeCamp
           https://safecamp.github.io/



Logan Davis | 1/23/16 | DrRacket:6.2/Lang:racket
|#

(define prime?
  #|
    A simple, but reasonably fast prime test that returns
    true if the test was positive and false otherwise.

    Arguments = 2:
      - num: the number to test.
      - lst-of-tests: prime numbers used to test num_to_test.
  |#
  (lambda (num lst-of-primes)
    (cond [(null? lst-of-primes) #t]
          [(< (+ (sqrt num) 1) (first lst-of-primes)) #t]
          [(= (remainder num (first lst-of-primes)) 0) #f]
          [else (prime? num (rest lst-of-primes))])))

(define finder
  #|
   Finds what prime number corresponders to
   a given index. This function is 0 indexing,
   E.G. passing '0' to the index arg will result
   in '2' being returned.

   Arguments = 3:
      current-num: The number to be tested.
      index: The desired index of prime to be found.
      lst-of-primes: prime numbers found.
  |#
  (lambda (current-num index lst-of-primes)
    (cond [(= index 0) (last lst-of-primes)]
          [(prime? current-num lst-of-primes)
           (finder (+ current-num 2)
                   (- index 1)
                   (append lst-of-primes
                           (list current-num)))]
          [else (finder (+ current-num 2) index lst-of-primes)])))

(define main
  #|
   Prompts the user to enter a the index of the prime
   they wish to know and then calulates it using (finder).
  |#
  (lambda ()
    (print "Please enter the desired index of the number you wish to find:")
    (define target (read-line))
    (define answer (finder 3 (- (string->number target) 1) '(2)))
    answer))

