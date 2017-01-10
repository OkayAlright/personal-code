/*
primeSum.rs 
----------------------------------------------------------
  Description:
    A simple prime finder to solver problem 
    10 : https://projecteuler.net/problem=10
  Use:
    compile using Rustc or Cargo, than simply run the 
    compiled file.
----------------------------------------------------------
References: 
    https://doc.rust-lang.org/
    https://learnxinyminutes.com/docs/rust/
----------------------------------------------------------
  Contact: ldavis@marlboro.edu
           https://github.com/SafeCamp
           https://safecamp.github.io/
Logan Davis | 1/28/16 | Rust 1.6
 
*/
use std::io;

fn prime_check(num: i32, lst_of_primes: &[i32]) -> bool{
    /*
     A simple, but reasonably fast prime test that returns
     true if the test was positive and false otherwise.

     Arguments = 2:
       - num: the number to test.
       - lst_of_primes: prime numbers used to test num.
    */
    let num_sqrt: i32 = ((num as f64).sqrt() as i32) + 1; 
    for &item in lst_of_primes.iter(){
        if item > num_sqrt{          //test up to sqrt of num
            return true;
        }else if (num % item) == 0{  //if divisible
            return false;
        }else{               
            continue;                //otherwise, test against the next known prime
        }
    }
    return true;
}

fn sum_primes(ceiling: i32) -> i64{
   /*
   This function returns the sum of all
   primes up to a given number.

   Arguments = 1: 
     - ceiling: The upper limit of the range
                being used for summing primes.
   */
   let mut sum: i64 = 2;
   let mut primes_found: Vec<i32> = vec![2];
   for i in 3..ceiling{
       if prime_check(i, &primes_found){
       	  &primes_found.push(i);
	  sum += i as i64;
       } 
   }
   return sum;
}

fn main(){
   /*
    prompts the user to input a number to denote the 
    range to sum primes under. The resulting sum is 
    printed.
   */
   let mut input = String::new();
   println!("Type the upper bounds you wish to sum primes under:");
   io::stdin().read_line(&mut input)
              .expect("Error reading input!");
   let ceiling: i32 = input.trim()
                           .parse()
                           .expect("Please type an integer!");
   let answer = sum_primes(ceiling);
   println!("The answer is {}.",answer);
}