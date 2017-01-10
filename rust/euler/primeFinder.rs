/*
primefinder.rs 
----------------------------------------------------------
  Description:
    A simple prime finder to solver problem 
    7 - "10001st prime": https://projecteuler.net/problem=7
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



Logan Davis | 1/23/16 | Rust 1.6
 */
use std::io;  //for run-time input

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

fn finder(target: i32) -> i32{
    /*
     Given an index of the prime you wish
     to find, this function will return the 
     value of that prime.

     Arguments = 1:
       - target: the index of the prime you wish to find.
    */
    let mut found: i32 = 1;                     //how many primes we have counted
    let mut current: i32 = 3;                   //the next number to prime test
    let mut lst_of_primes = Vec::new();         //where primes will be stored
    lst_of_primes.push(2);                      //a starting prime for testing others
    while found < target{                       
        if prime_check(current,&lst_of_primes){ //if prime
            &lst_of_primes.push(current);       //catalog
            found += 1;                         //and increase count of knowns 
        }
        if found != target{                     
            current += 2;                        //go to next possible prime
        }
    }
    return current                               //return the last calculated prime
}

fn main(){
    /*
     The accessor function. Prompts the user to 
     enter some integer that is the index of the
     prime they wish to find. It then calls the 
     finder function (if the input is > 1, otherwise
     it just prints the answer as 2) and prints the 
     answer.

     Takes no arguments. 
    */
    println!("What prime do you wish to find?");
    let mut input = String::new();
    io::stdin().read_line(&mut input)
               .expect("Error reading line!");                          //gets input
    let target: i32 = input.trim()
                           .parse()
                           .expect("ERROR! Please enter an integer!");  //casts as int
    //let target: i32 = 10001;
    let mut answer: i32 = 0;
    if target == 1{                                                     //if they enter the
         answer = 2;                                                    //only hard coded prime
    }else{                                                              
         answer = finder(target);                                       //otherwise, find it
    }
    println!("The number you are looking for is {}.", answer);          //print result
}
