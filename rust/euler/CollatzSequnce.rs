/*
CollatzSequence.rs 
----------------------------------------------------------
  Description:
    A simple program to solve project Euler 14
    https://projecteuler.net/problem=14
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
Logan Davis | 1/29/16 | Rust 1.6
 */
use std::io;

fn collatz_step(num: i64, index: i64) -> i64 {
    /*
    recursively tests a given number and 
    returns the length of it's collatz sequence.

    Arguments = 2:
       - num: the number to test 
       - index: the amount of steps take through
         a sequence.
    */
    let mut len: i64 = 0;
    if num == 1{
       len = index;
    }else if num % 2 == 0{          //even
       len = collatz_step(num/2, index + 1);
    }else{                          //odd
       len = collatz_step((3 * num) + 1, index + 1);
    }
    return len;
}

fn find_longest_collatz_seq(ceiling: i64) -> i64 {
    /*
    tests every number from 0 to 'ceiling'
    and returns the number that resulted in
    the longest sequence.
   
    Arguments = 1:
       - ceiling: the upper bound to test 
         Collatz sequences up to.
    */ 
    let mut champion: i64 = 0; //longest seq seen
    let mut champion_seq_len: i64 = 0; 
    let mut test_seq_len: i64 = 0;
    for i in 1..ceiling{
    	test_seq_len = collatz_step(i, 1);
	if test_seq_len > champion_seq_len{
	   champion = i;
	   champion_seq_len = test_seq_len;
	}
    }
    return champion;
}

fn main(){
   /*
   Prompts user for some input
   to use as an upper bounds in
   testing for collatz sequences.
   */
   let mut input = String::new();
   println!("Please enter the upper bound you wish to test to:");
   io::stdin().read_line(&mut input)
              .expect("Error reading input!");
   let ceiling: i64 = input.trim()
                           .parse()
                           .expect("ERROR! Please enter an integer!");
   let answer: i64  = find_longest_collatz_seq(ceiling);
   println!("The answer is {}.", answer);
}