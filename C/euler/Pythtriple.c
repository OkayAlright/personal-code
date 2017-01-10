/*
Pythtriple.c 
----------------------------------------------------------
  Description:
    Finds pythagorean triplets to solve Project Euler 9 
    "Special Pythagorean triplet": 
     https://projecteuler.net/problem=9
  Use:
    compile using GCC:
      $ gcc Pythtriple.c -o pythtriple -lm
----------------------------------------------------------
References: 
    http://users.ece.utexas.edu/~adnan/c-refcard.pdf
----------------------------------------------------------
  Contact: ldavis@marlboro.edu
           https://github.com/SafeCamp
           https://safecamp.github.io/



Logan Davis | 1/19/16 | GCC 5.2.1
 */
#include <stdio.h>
#include <math.h>
#define TARGET_SUM 1000

int main(){
  /*
   The accessor function. Running this will find a
   Pythagorean triplet that sums to the number
   defined in TARGET SUM.
   */
  int a,b;
  double _a, _b, c;
  printf("Trying to find a pythagerorean triple that sums to %d.\n", TARGET_SUM);
  for(a = 1; a < TARGET_SUM/2; a++){
    for( b = a + 1; b < TARGET_SUM/2; b++){
      _a = (double) a;
      _b = (double) b;
      c = sqrt((_a * _a) + (_b * _b));
      if((a + b + c == TARGET_SUM)){
	printf("FOUND TARGET SUM:\n a = %d \n b = %d \n c = %d\n",a,b,(int) c);
	return 0;
      }
    }
  }
  printf("Oh no! A triplet was not found!\n"); 
  return 0;
}
